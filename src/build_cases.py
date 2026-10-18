"""从事件库生成「灯下案」——把一条史实的推理过程展开成可回放的轨迹。

用法：
    python src/build_cases.py
    python src/build_cases.py -o data/curated/cases.json

设计原则：
- 不生成任何史实。所有引文都从 events.json 的 sources.quote 里逐字取出。
- 对勘结论由规则判定（时点是否模糊、是否同源、有无一手档案、数值离散度），
  不由模型自由发挥。
- 「存疑」是正常产出：解决不了的分歧登记为悬案，并写明缺什么材料才能定谳。
- 输出的是**推理轨迹**，前端按段落逐条回放，不是一段静态报告。

一个案子的四段：
    decompose  拆解   把命题拆成原子断言，分别标注来源提及、记录精度与数值分歧
    retrieve   辑录   库内找到哪些记载，各自说了什么
    examine    对勘   这些记载撑不撑得住命题
    register   存疑   登记悬案，给出证据支持的最保守结论
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / "data" / "curated" / "events.json"
CONF = ROOT / "data" / "curated" / "conflicts.json"
VERDICTS_PATH = ROOT / "data" / "curated" / "verdicts.json"
OUT = ROOT / "data" / "curated" / "cases.json"

# 时点模糊的语汇。原文出现这些词，说明命题本身没落在具体某一天。
VAGUE_TIME = ["鼎盛", "全盛", "前后", "之际", "期间", "时期", "初期", "末期", "年初", "年底"]
# 数量引文中的概数语汇；「一说」标记异说，不等于数字本身是约数。
# 注意不含「多」：它会误命中「一年多」这类非数值用法。
APPROX = ["约", "余", "近", "逾", "估计", "左右"]
AMBIGUOUS_QUANTITY = ["之多"]

RELIABILITY_CN = {"A": "一手档案", "B": "学术著作/权威报道", "C": "回忆录/展陈/待核转述"}


def hits(text: str, words: list[str]) -> list[str]:
    return [w for w in words if w in (text or "")]


def time_markers(text: str) -> list[str]:
    markers = hits(text, VAGUE_TIME)
    if re.search(r"\d+(?:年|年代|月|日)左右", text or ""):
        markers.append("左右")
    return markers


def numeric_approx_claims(ev: dict, measures: list[dict]) -> list[dict]:
    """只用该数量主张对应来源的引文判定概数，不把异说词传给另一来源。"""
    claims = []
    sources = {s.get("book"): s.get("quote", "") for s in ev.get("sources", [])}
    for measure in measures:
        quote = sources.get(measure.get("source"), "")
        markers = hits(quote, APPROX)
        if markers:
            claims.append({**measure, "markers": markers})
    return claims


def describe_numeric_claims(claims: list[dict]) -> str:
    return "；".join(
        f"{short_src(m.get('source'))}的 {fmt(m.get('value'))} {m.get('unit', '')}（「{'」「'.join(m['markers'])}」）"
        for m in claims
    )


def fmt(n) -> str:
    return f"{n:,}" if isinstance(n, (int, float)) else str(n)


def date_label(d: dict) -> str:
    """1936-01-01 + precision=year 显示成「1936年」，不暴露补位的 01。"""
    s = str(d.get("start") or "")
    p = d.get("precision")
    if p == "year":
        return s[:4] + "年"
    if p == "month":
        return f"{s[:4]}年{int(s[5:7])}月"
    return s[:10]


def md_label(iso: str, prec: str | None) -> str:
    """「1942-08-01」+day →「8月1日」；+month →「8月」。"""
    parts = (str(iso or "").split("-") + ["1", "1"])[:3]
    try:
        m, d = int(parts[1]), int(parts[2])
    except (ValueError, IndexError):
        return str(iso)
    return f"{m}月{d}日" if prec == "day" else f"{m}月"


def short_src(s: str) -> str:
    """「国家图书馆《抗联简史》（引…）」→「国家图书馆」"""
    s = str(s or "")
    head = s.split("《")[0].split("（")[0].strip()
    return head or s[:16]


# ---------------------------------------------------------------- 日期支持关系
# P0-02：不能用「来源条数」代替「逐条比对」，也不能把一家到日、几家到月
# 判成「来源记载相合」。四态：未载 / 范围相容 / 明确相合 / 互斥，
# 另加一态「另一动作」——编成与成立是不同动作，不可直接判矛盾。

SEASON_MONTHS = {"春": (3, 4, 5), "夏": (6, 7, 8),
                 "秋": (9, 10, 11), "冬": (12, 1, 2)}
FORM_ACTION_WORDS = ("编为", "编成", "改编", "合编", "整编")
FOUND_ACTION_WORDS = ("成立", "建立", "组建")
# 考订型引文：引文里出现的是「被考订的错误值」，不能当成该来源的主张
CORRECTION_WORDS = ("笔误", "应为", "实为", "显然", "误记", "疑为", "当为", "系误", "有误")
# 起始年表述：「自 1931 年起……发表」说的是起点，不是该文件的发表年
RANGE_PREFIX = re.compile(r"自\s*\d{4}\s*年起")


def parse_time_claim(text: str) -> dict | None:
    """从引文解析时间表达，返回最细精度的 {precision,y,m,d,season,expr}。

    只取第一处时间表达：同一条引文里可能同时写「7月22日编成」与「8月1日成立」，
    取第一个会把建军日当成成立日——调用方需先用 action_kind 排除动作不符的来源。
    """
    t = str(text or "")
    m = re.search(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", t)
    if m:
        mm, dd = int(m.group(2)), int(m.group(3))
        return {"precision": "day", "y": int(m.group(1)), "m": mm, "d": dd,
                "expr": f"{mm}月{dd}日"}
    m = re.search(r"(\d{4})\s*年\s*(\d{1,2})\s*月", t)
    if m:
        mm = int(m.group(2))
        return {"precision": "month", "y": int(m.group(1)), "m": mm, "d": None,
                "expr": f"{mm}月"}
    m = re.search(r"(\d{4})\s*年\s*(春|夏|秋|冬)", t)
    if m:
        return {"precision": "season", "y": int(m.group(1)), "m": None, "d": None,
                "season": m.group(2), "expr": f"{m.group(2)}季"}
    m = re.search(r"(\d{1,2})\s*月\s*(\d{1,2})\s*日", t)
    if m:
        mm, dd = int(m.group(1)), int(m.group(2))
        return {"precision": "day", "y": None, "m": mm, "d": dd,
                "expr": f"{mm}月{dd}日"}
    m = re.search(r"(\d{1,2})\s*月", t)
    if m:
        mm = int(m.group(1))
        return {"precision": "month", "y": None, "m": mm, "d": None,
                "expr": f"{mm}月"}
    m = re.search(r"(\d{4})\s*年", t)
    if m:
        return {"precision": "year", "y": int(m.group(1)), "m": None, "d": None,
                "expr": f"{m.group(1)}年"}
    return None


def action_kind(text: str) -> str | None:
    """粗分动作类别：编成 / 成立。两者是不同动作，不可直接判成日期矛盾。"""
    t = str(text or "")
    if any(w in t for w in FORM_ACTION_WORDS):
        return "编成"
    if any(w in t for w in FOUND_ACTION_WORDS):
        return "成立"
    return None


def date_support(ev: dict) -> dict:
    """逐来源 × 逐精度计算日期支持关系。

    返回 {"claim": {...}, "rows": [...], "counts": {...},
          "year_counts": {...}, "state": str}
    rows 每项：{short, expr, precision, state}，state ∈
    未载 / 明确相合 / 范围相容 / 范围不符 / 互斥 / 另一动作
    """
    d = ev.get("date") or {}
    start = str(d.get("start") or "")
    prec = d.get("precision") or "year"
    try:
        cy = int(start[:4])
        cm = int(start[5:7]) if len(start) >= 7 else None
        cd = int(start[8:10]) if len(start) >= 10 else None
    except ValueError:
        cy, cm, cd = None, None, None

    claim_act = action_kind(ev.get("summary") or "")
    rows = []
    year_exact = year_off = year_none = 0

    for s in ev.get("sources", []):
        quote = s.get("quote") or ""
        tc = parse_time_claim(quote)
        short = short_src(s.get("book"))
        if tc is None:
            year_none += 1
            rows.append({"short": short, "expr": "未载具体时间",
                         "precision": "none", "state": "未载"})
            continue
        # 考订说明 / 起始年表述：引文里的年份不是该来源对「本条主张」的记载
        if any(w in quote for w in CORRECTION_WORDS):
            rows.append({"short": short, "expr": tc["expr"],
                         "precision": tc["precision"], "state": "考订说明"})
            continue
        if RANGE_PREFIX.search(quote):
            rows.append({"short": short, "expr": tc["expr"],
                         "precision": tc["precision"], "state": "起始年表述"})
            continue
        # 年份先单独记账：即便月日互斥，年份是否明载也要分开说
        if tc["y"] is None:
            year_none += 1
        elif cy and tc["y"] != cy:
            year_off += 1
        else:
            year_exact += 1
        # 动作不符：先判，避免把「编成」的日期当成「成立」的日期比对
        src_act = action_kind(quote)
        if claim_act and src_act and src_act != claim_act:
            rows.append({"short": short, "expr": tc["expr"],
                         "precision": tc["precision"], "state": "另一动作"})
            continue
        if tc["y"] and cy and tc["y"] != cy:
            rows.append({"short": short, "expr": tc["expr"],
                         "precision": tc["precision"], "state": "互斥"})
            continue
        if tc["precision"] == "year":
            rows.append({"short": short, "expr": tc["expr"],
                         "precision": "year", "state": "范围相容"})
            continue
        if tc["precision"] == "season":
            months = SEASON_MONTHS.get(tc["season"], ())
            ok = cm is not None and cm in months
            rows.append({"short": short, "expr": tc["expr"], "precision": "season",
                         "state": "范围相容" if ok else "范围不符"})
            continue
        if tc["precision"] == "month":
            same = cm is not None and tc["m"] == cm
            rows.append({"short": short, "expr": tc["expr"], "precision": "month",
                         "state": "明确相合" if same else "互斥"})
            continue
        # 到日：主张到日则须月日全同；主张只到月，则同月即支持（更细的来源支持更粗的主张）
        if prec == "day":
            same = (cm == tc["m"] and cd == tc["d"])
        else:
            same = (cm is not None and tc["m"] == cm)
        rows.append({"short": short, "expr": tc["expr"], "precision": "day",
                     "state": "明确相合" if same else "互斥"})

    counts = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1

    # 汇总状态：只认「明确相合」为支持；其余逐类陈述，绝不合并成「相合」
    exact = counts.get("明确相合", 0)
    compat = counts.get("范围相容", 0)
    total = len(rows)
    if counts.get("互斥"):
        state = f"{counts['互斥']} 家记载与主张不符"
    elif exact and (exact + compat) == total:
        state = f"{exact} 家明确相合" + (f"（{compat} 家更粗但相容）" if compat else "")
    elif exact:
        state = (f"仅 {exact} 家明确相合；"
                 + "、".join(f"{counts[k]} 家{k}" for k in
                            ("范围相容", "范围不符", "另一动作", "考订说明",
                             "起始年表述", "未载") if counts.get(k)))
    elif compat:
        state = f"无明确到该精度的记载；{compat} 家范围相容"
    else:
        state = "无来源支持该精度"

    return {"claim": {"y": cy, "m": cm, "d": cd, "precision": prec},
            "rows": rows, "counts": counts,
            "year_counts": {"exact": year_exact, "off": year_off, "none": year_none},
            "state": state}




def place_label(p: dict) -> tuple[str, str]:
    """返回 (显示文本, 确定性)。原文没写地点时不能标成「省级精度」。"""
    pprec_cn = {"site": "遗址", "town": "乡镇", "county": "县", "province": "省"}.get(
        p.get("precision"), "未知")
    name = p.get("modern") or p.get("name") or ""
    if not name:
        return "原文未载地点", "缺失"
    state = {"site": "确定", "town": "确定", "county": "较粗",
             "province": "模糊"}.get(p.get("precision"), "缺失")
    return f"{name}（{pprec_cn}级精度）", state


def court_no(i: int) -> str:
    return f"KL-{i:03d}"


def build_decompose(ev: dict, claim_value, claim_unit: str, claim_measures: list[dict]) -> dict:
    """把命题拆成原子断言，展示来源提及、记录精度和库内数值分歧。"""
    d = ev.get("date") or {}
    p = ev.get("place") or {}
    quote_all = " ".join(s.get("quote", "") for s in ev.get("sources", []))

    prec_cn = {"day": "日", "month": "月", "year": "年"}.get(d.get("precision"), "年")
    time_state = {"day": "记录精确到日", "month": "记录精确到月", "year": "记录仅到年"}.get(
        d.get("precision"), "时点待核")
    vt = sorted({marker for s in ev.get("sources", []) for marker in time_markers(s.get("quote", ""))})
    if vt:
        time_state = "原文时点表述较宽"

    place_text, place_state = place_label(p)
    place_state_label = "未载地点" if place_state == "缺失" else {
        "site": "遗址级位置", "town": "乡镇级范围", "county": "县级范围",
        "province": "省级范围",
    }.get(p.get("precision"), "位置精度待核")

    approx_claims = numeric_approx_claims(ev, claim_measures)
    approx = sorted({marker for claim in approx_claims for marker in claim["markers"]})
    value_state = "存在分歧且为约数" if approx else "存在分歧"
    subjects = list(ev.get("units") or []) + list(ev.get("persons") or [])
    subject_value = "、".join(ev.get("units") or ev.get("persons") or []) or "（原文未点名）"
    subject_state = ("来源引文提及" if subjects and all(s and s in quote_all for s in subjects)
                     else "主体需逐项核查" if subjects else "原文未点名")

    assertions = [
        {"k": "主体", "v": subject_value, "state": subject_state},
        {"k": "时点", "v": f"{date_label(d)}（仅到{prec_cn}）", "state": time_state},
        {"k": "地点", "v": place_text, "state": place_state_label},
        {"k": "数值", "v": f"{fmt(claim_value)} {claim_unit}", "state": value_state},
    ]

    lines = [
        f"命题拆成 {len(assertions)} 个原子断言。任何一个不成立，命题就不能成立。",
    ]
    vt = time_markers(quote_all)
    if time_state in {"记录仅到年", "时点待核", "原文时点表述较宽"}:
        tag = "".join(f"「{w}」" for w in vt) if vt else f"仅到{prec_cn}"
        lines.append(f"时点{tag}未落到统一年月；这可能影响不同来源所指时间的可比性，需先查明。")
    if approx_claims:
        lines.append(f"对应数量引文含概数表达：{describe_numeric_claims(approx_claims)}。"
                     "本项只作量级比较，不按精确值解释。")
    ambiguous_claims = []
    source_quotes = {s.get("book"): s.get("quote", "") for s in ev.get("sources", [])}
    for measure in claim_measures:
        markers = hits(source_quotes.get(measure.get("source"), ""), AMBIGUOUS_QUANTITY)
        if markers:
            ambiguous_claims.append({**measure, "markers": markers})
    if ambiguous_claims:
        lines.append(f"对应引文另有数量措辞：{describe_numeric_claims(ambiguous_claims)}；"
                     "本规则保留原文，不自动将其判作约数，统计口径仍需核查。")
    lines.append("本案数值已出现互异主张；拆解展示的是库内记录精度，不将主张写成已证实事实。")

    return {"kind": "decompose", "agent": "拆解", "lines": lines, "assertions": assertions}


def build_retrieve(ev: dict, all_sources: list[dict]) -> dict:
    """辑录：列出本条事件的每条来源，以及跨条目的旁证。"""
    ev_sources = []
    for s in ev.get("sources", []):
        m = next((x for x in ev.get("measures") or []
                  if x.get("source") == s.get("book")), None)
        ev_sources.append({
            "book": s.get("book"),
            "short": short_src(s.get("book")),
            "page": s.get("page"),
            "quote": s.get("quote"),
            "url": s.get("url"),
            "archive": s.get("archive"),
            "archive_note": s.get("archive_note"),
            "reliability": s.get("reliability"),
            "reliability_cn": RELIABILITY_CN.get(s.get("reliability"), "未标"),
            "value": m.get("value") if m else None,
            "unit": m.get("unit") if m else None,
            "is_primary": s.get("reliability") == "A",
        })

    # 跨条目旁证：别的记载里也提到同一主体的数字。
    # 只认主体全称——「东北抗日」这种前缀会同时命中联军和义勇军，是两支不同的队伍。
    subject = (ev.get("units") or [""])[0]
    side = []
    seen = {s.get("book") for s in ev.get("sources", [])}
    if subject:
        for other in all_sources:
            if other["book"] in seen:
                continue
            q = other.get("quote", "")
            if subject in q and hits(q, ["万人", "余人", "人数", "兵力"]):
                side.append({
                    "book": other["book"],
                    "short": short_src(other["book"]),
                    "quote": q,
                    "year": other.get("year"),
                    "event": other.get("event_summary"),
                })

    n_val = sum(1 for s in ev_sources if s["value"] is not None)
    lines = [f"库内共 {len(ev_sources)} 条记载，其中 {n_val} 条给出具体数字。"
             f"以下原文逐字照录，未作改写。"]
    if side:
        lines.append(f"另有 {len(side)} 条旁证不在本条事件下，但提到了同一主体的人数——"
                     f"它们决定了「鼎盛」这个时点到底指哪一年。")

    return {"kind": "retrieve", "agent": "辑录", "lines": lines,
            "evidence": ev_sources, "side": side}


def build_examine(ev: dict, sources: list[dict], measures: list[dict]) -> dict:
    """对勘：规则驱动，只挑毛病，不下结论。"""
    ch: list[dict] = []
    quote_all = " ".join(s.get("quote", "") for s in sources)
    approx_claims = numeric_approx_claims(ev, measures)

    # R1 时点无定义；逐条来源呈现原文用词，避免把异词并成同一表述。
    vague_sources = []
    for source in sources:
        markers = time_markers(source.get("quote", ""))
        if markers:
            vague_sources.append(f"{short_src(source.get('book'))}（「{'」「'.join(markers)}」）")
    if vague_sources:
        ch.append({
            "code": "R1", "name": "时点无统一定义", "severity": "high",
            "text": f"参与对勘的 {len(sources)} 条来源中，有 {len(vague_sources)} 条引文含未定义的时点措辞："
                    f"{'；'.join(vague_sources)}。当前数据未给这些词统一界定起止年月，"
                    "不能据此认定各数字指向同一时段。",
        })

    # R2 同源风险
    cited = [s for s in sources if "引" in (s.get("book") or "")]
    if cited:
        ch.append({
            "code": "R2", "name": "转引而非独立记载", "severity": "high",
            "text": f"「{short_src(cited[0]['book'])}」注明是转引（{cited[0]['book'].split('（')[-1].rstrip('）')}）。"
                    f"转引不构成独立互证——两条记载看起来是两票，实际可能只有一票。",
        })

    # R3 无一手档案
    if not any(s.get("reliability") == "A" for s in sources):
        ch.append({
            "code": "R3", "name": "库内无一手档案", "severity": "high",
            "text": "参与比对的所有记载均为 B/C 级（转述、报道、展陈），没有一条出自原始档案。"
                    "这意味着无论数字多接近，都只能证明「有人这样写过」，"
                    "不能证明「当时确实如此」。",
        })

    # R4 数值离散
    vals = [m["value"] for m in measures if isinstance(m.get("value"), (int, float))]
    if len(set(vals)) >= 2:
        lo, hi = min(vals), max(vals)
        ratio = (hi - lo) / max(hi, 1)
        caveat = (f"（参与比较的数量引文含概数表达：{describe_numeric_claims(approx_claims)}；"
                  "百分比只作量级参考，见 R6）" if approx_claims else "")
        ch.append({
            "code": "R4", "name": "数值离散超出容差", "severity": "high" if ratio >= 0.25 else "medium",
            "text": f"最高 {fmt(hi)}，最低 {fmt(lo)}，机械相除差 {ratio:.0%}{caveat}。"
                    f"这个量级不是四舍五入能解释的，是两个口径。",
        })

    # R5 孤证
    if len(sources) == 1:
        ch.append({
            "code": "R5", "name": "孤证", "severity": "high",
            "text": "只有一条记载支持。孤证不立——无法排除抄录错误或记忆偏差。",
        })

    # R6 约数当精确值
    if approx_claims:
        ch.append({
            "code": "R6", "name": "约数被当作精确值", "severity": "medium",
            "text": f"参与本案比较的数量引文含概数表达：{describe_numeric_claims(approx_claims)}。"
                    "将其转换成整数单点参与计算只能作量级参考，不能视作精确值。",
        })

    # R7 自认分歧
    if "一说" in quote_all:
        ch.append({
            "code": "R7", "name": "史料自认存在异说", "severity": "high",
            "text": "至少一条原文自己写着「一说」。这不是我们比对出来的分歧，"
                    "是史料本身承认了它——这类分歧通常比外部比对更值得记。",
        })

    if not ch:
        ch.append({"code": "R0", "name": "未发现结构性缺陷", "severity": "low",
                   "text": "本轮规则未在这组记载中发现时点、同源、孤证或口径问题。"
                           "但这不等于命题成立，只说明现有材料没有暴露矛盾。"})

    return {"kind": "examine", "agent": "对勘", "lines": [], "challenges": ch}


def build_register(ev: dict, ch: list[dict], measures: list[dict],
                   case_no: str) -> dict:
    """存疑：登记悬案，给出证据支持的最保守结论。"""
    vals = sorted({m["value"] for m in measures if isinstance(m.get("value"), (int, float))})
    # 只在每条来源都明确给出同一数值时，才把它记作来源共识。
    consensus = []
    source_quotes = [s.get("quote", "") for s in ev.get("sources", []) if s.get("quote")]
    for pat, label in ((r"(\d+)\s*个军", "编成 {n} 个军"), (r"(\d+)\s*个路军", "编成 {n} 个路军")):
        mentions = [re.search(pat, quote) for quote in source_quotes]
        values = [m.group(1) for m in mentions if m]
        if len(source_quotes) >= 2 and len(values) == len(source_quotes) and len(set(values)) == 1:
            consensus.append(label.format(n=values[0]))

    missing = []
    if not any(s.get("reliability") == "A" for s in ev.get("sources", [])):
        missing.append("抗联各军兵力统计的原始报表或档案（现库内 0 条 A 级来源）")
    if any(time_markers(s.get("quote", "")) for s in ev.get("sources", [])):
        missing.append("模糊时点措辞的时间范围，需由可引用的权威史料界定")
    approx_claims = numeric_approx_claims(ev, measures)
    if approx_claims:
        missing.append(f"需核对概数表达对应的统计口径：{describe_numeric_claims(approx_claims)}")

    if len(vals) >= 2:
        if consensus:
            sure = f"可以确定的是：{'、'.join(consensus)}——这一点各条原文一致。"
        else:
            sure = "可以确认的是：库内存在互异的数量主张；现有引文不足以证明它们采用相同的统计口径和时点。"
        conservative = (
            f"{sure}"
            f"数值上只能给出区间：{fmt(vals[0])} 至 {fmt(vals[-1])} "
            f"{measures[0].get('unit', '')}。"
            f"在此区间内取任何单一数字，都是超出材料的判断。"
        )
        status = "unresolved"
        status_cn = "悬案 · 无法定谳"
    else:
        conservative = "现有材料不足以支撑任何数值结论。"
        status = "insufficient"
        status_cn = "证据不足"

    return {
        "kind": "register", "agent": "存疑",
        "case_no": case_no, "status": status, "status_cn": status_cn,
        "missing": missing, "conservative": conservative,
        "high_count": sum(1 for c in ch if c["severity"] == "high"),
    }


def build_date_case(ev: dict, dv: list[dict], case_no: str) -> dict:
    """日期悬案：同一事件的日期主张出现高严重度分歧（整月级）。

    与数值悬案对称：数值案证明「系统对数字不敢下结论」，
    本案证明「系统对日期也不敢下结论——即使分歧一方是权威机构」。
    处置不是和稀泥：给出机构权重对比与最保守表述，定谳留给档案级证据。
    """
    d = ev.get("date") or {}
    year = str(d.get("start"))[:4]
    # 主语复用定谳案的抽取逻辑
    subject = ("、".join(ev.get("persons") or [])
               or "、".join(ev.get("units") or [])
               or "该事件")
    if subject == "该事件":
        m_v = re.search(r"(成立|爆发|失守|殉国|牺牲)", ev.get("summary") or "")
        if m_v:
            subject = (ev.get("summary") or "")[:m_v.start()].split("的")[-1].strip("，。、； ") or "该事件"
    et = ev.get("event_type", "事件")
    act = {"牺牲": "牺牲", "战斗": "作战"}.get(et, "发生")

    a, b = dv[0]["a"], dv[0]["b"]
    ga, gb = a["source"].split("《")[0], b["source"].split("《")[0]

    # P0-03：月精度不能伪装成「6 月 1 日」。原文只写「6月」，补位的 01 不是史料。
    def claim_label(c: dict) -> str:
        v = str(c.get("value") or "")
        if c.get("precision") == "day":
            return v + "（日精度）"
        if c.get("precision") == "month":
            try:
                return f"{v[:4]}年{int(v[5:7])}月（月精度，原文未到日）"
            except ValueError:
                return v + "（月精度）"
        return v[:4] + "年（年精度）"

    # 只有双方都到日，天数差才有意义；否则只能说精度不同
    both_day = (a.get("precision") == "day" and b.get("precision") == "day")
    if both_day:
        gap_text = f"{dv[0]['gap_days']} 天（整月级）" if dv[0]["gap_days"] >= 15 else f"{dv[0]['gap_days']} 天"
        gap_value = f"{dv[0]['gap_days']} 天"
    else:
        gap_text = "精度不同（一方到月、一方到日），不计算天数差——先对齐精度，再谈差多少"
        gap_value = "不可比（精度不同）"

    # 拆解：把「X 于何时」拆成双方各自的主张
    decompose = {
        "kind": "decompose", "agent": "拆解",
        "lines": [f"「{subject}{act}于何时」拆成两条互斥的日期主张：",
                  f"主张甲：{a['source']} 记 {claim_label(a)}；",
                  f"主张乙：{b['source']} 记 {claim_label(b)}。",
                  gap_text + "。"],
        "assertions": [
            {"k": "事件本体", "v": ev.get("summary", ""), "state": "确定"},
            {"k": "主张甲", "v": f"{claim_label(a)}（{ga}）", "state": "存疑"},
            {"k": "主张乙", "v": f"{claim_label(b)}（{gb}）", "state": "存疑"},
            {"k": "分歧量级", "v": gap_value, "state": "确定" if both_day else "较粗"},
        ],
    }

    # 辑录：双方引文逐字照录
    quotes_by_src = {}
    for s in ev.get("sources", []):
        quotes_by_src.setdefault(s.get("book", ""), s.get("quote", ""))
    def evd(claim):
        bk = claim["source"]
        meta = next((s for s in ev.get("sources", []) if s.get("book") == bk), {})
        return {"book": bk, "short": short_src(bk), "page": meta.get("page") or "",
                "quote": quotes_by_src.get(bk) or "引文未在事件层定位——该来源只以日期主张入链，需回补原文",
                "url": meta.get("url"), "archive": meta.get("archive"),
                "reliability": meta.get("reliability") or "B",
                "value": claim["value"], "unit": "date", "is_primary": False}
    retrieve = {
        "kind": "retrieve", "agent": "辑录",
        "lines": ["库内对同一条事实给出了两条日期主张。以下原文逐字照录，未作改写。"],
        "evidence": [evd(a), evd(b)],
        "side": [],
    }

    # 对勘：整月级分歧 + 机构权重
    ch = [{
        "code": "R9", "name": "整月级日期分歧",
        "severity": "high",
        "text": f"{ga} 记 {a['value']}，{gb} 记 {b['value']}，相差 {dv[0]['gap_days']} 天，"
                "超出精度误差能解释的范围——这是实质性分歧，不是「一个记约数一个记精确数」。",
    }]
    w_a = ("国防部" in ga or "纪念馆" in ga or "军网" in ga or "新华社" in ga
           or "纪委监委" in ga or "退役军人" in ga or "党史" in ga)
    w_b = ("国防部" in gb or "纪念馆" in gb or "军网" in gb or "新华社" in gb
           or "纪委监委" in gb or "退役军人" in gb or "党史" in gb)
    if w_a != w_b:
        ch.append({
            "code": "R10", "name": "机构权重不对称",
            "severity": "medium",
            "text": ("分歧一方为国防部门/官方纪念机构，另一方为媒体年表——"
                     "但这不构成裁决：年表同样有档案出处，且单方权威转述也可能沿用一处笔误。"
                     "权重只改变候选倾向，不替代证据。"),
        })
    examine = {"kind": "examine", "agent": "对勘", "lines": [], "challenges": ch}

    # 存疑：登记悬案，最保守表述 + 裁决路径
    register = {
        "kind": "register", "agent": "存疑",
        "case_no": case_no, "status": "unresolved", "status_cn": "悬案 · 整月分歧",
        "missing": ["事件所在省档案馆革命历史档案（闭架）",
                    "当事人回忆录纸本或烈士传记的档案级引文"],
        "conservative": (
            f"两说并陈：{a['value']}（{ga}）与 {b['value']}（{gb}）。"
            f"本库按「不动原记载、不加权下结论」处置——"
            f"机构权重倾向{'主张甲' if w_a and not w_b else ('主张乙' if w_b and not w_a else '双方')}，"
            f"但倾向不是定谳。任何一侧改字都会在系统里留下痕迹："
            f"这不是没能得出结论，而是**证据还没到能得出结论的程度**。"),
        "high_count": 1,
    }

    return {
        "id": f"case_{case_no.lower().replace('-', '_')}",
        "case_no": case_no,
        "kind": "dispute",
        "title": f"{subject}{act}于何时（整月分歧）",
        "claim_text": f"{subject}{act}日期：{a['value']}（{ga}）vs {b['value']}（{gb}）",
        "event_id": ev["id"],
        "predicate": "date.start",
        "unit": "date",
        "values": sorted({a["value"], b["value"]}),
        "summary": ev.get("summary"),
        "steps": [decompose, retrieve, examine, register],
    }


def build_single_case(ev: dict, case_no: str) -> dict:
    """孤证案：库内只有一条记载。

    这类案子存在的意义是划清一条界线——
    「史实存疑」说的是历史本身不确定，
    「库内证据不足」说的是我们还没收集够。
    把两者混为一谈，是数字人文项目最常见的自欺。
    """
    d = ev.get("date") or {}
    p = ev.get("place") or {}
    persons = "、".join(ev.get("persons") or [])
    prec_cn = {"day": "日", "month": "月", "year": "年"}.get(d.get("precision"), "年")
    place_text, place_state = place_label(p)
    time_state = {"day": "确定", "month": "较粗", "year": "模糊"}.get(d.get("precision"), "模糊")

    assertions = [
        {"k": "主体", "v": persons or "、".join(ev.get("units") or []) or "（原文未点名）", "state": "确定"},
        {"k": "时点", "v": f"{date_label(d)}（仅到{prec_cn}）", "state": time_state},
        {"k": "地点", "v": place_text, "state": place_state},
    ]

    srcs = [{
        "book": s.get("book"), "short": short_src(s.get("book")),
        "page": s.get("page"), "quote": s.get("quote"),
        "url": s.get("url"), "archive": s.get("archive"),
        "archive_note": s.get("archive_note"),
        "reliability": s.get("reliability"),
        "reliability_cn": RELIABILITY_CN.get(s.get("reliability"), "未标"),
        "value": None, "unit": None,
        "is_primary": s.get("reliability") == "A",
    } for s in ev.get("sources", [])]

    ch = [{
        "code": "R5", "name": "孤证", "severity": "medium",
        "text": "库内只有一条记载，无法做独立互证。但请注意：这不等于史实存疑，"
                "只说明本库还没收录第二个来源。这两件事必须分开说。",
    }]
    if not any(s.get("reliability") == "A" for s in ev.get("sources", [])):
        ch.append({
            "code": "R3", "name": "库内无一手档案", "severity": "medium",
            "text": "唯一来源属转述性质。它能证明「有人这样写过」，"
                    "不足以单独支撑一条定谳结论。",
        })

    time_desc = {"确定": "时点精确到日", "较粗": "时点只到月",
                 "模糊": "时点只到年"}.get(time_state, "时点不明")
    place_desc = {"确定": "地点精确到点", "较粗": "地点只到县",
                  "模糊": "地点只到省", "缺失": "原文未载地点"}.get(place_state, "地点不明")
    register = {
        "kind": "register", "agent": "存疑",
        "case_no": case_no, "status": "insufficient", "status_cn": "库内证据不足",
        "missing": [f"需补第二条独立来源（须不同于「{srcs[0]['short']}」）"],
        "conservative": f"本条记载{time_desc}、{place_desc}，但库内无第二条独立记载可比对。"
                        "系统登记为「证据不足」，而不是「存疑」——"
                        "前者说的是本库，后者说的是历史。",
        "high_count": sum(1 for c in ch if c["severity"] == "high"),
    }

    return {
        "id": f"case_{case_no.lower().replace('-', '_')}",
        "case_no": case_no,
        "kind": "single",
        "title": f"{persons or '该事件'}：孤证怎么处置",
        "claim_text": ev.get("summary"),
        "event_id": ev["id"],
        "predicate": None, "unit": None, "values": [],
        "summary": ev.get("summary"),
        "steps": [
            {"kind": "decompose", "agent": "拆解",
             "lines": [f"命题拆成 {len(assertions)} 个原子断言。"
                       f"库内只有 1 条来源可供比对。"],
             "assertions": assertions},
            {"kind": "retrieve", "agent": "辑录",
             "lines": ["库内共 1 条记载。原文逐字照录，未作改写。"],
             "evidence": srcs, "side": []},
            {"kind": "examine", "agent": "对勘", "lines": [], "challenges": ch},
            register,
        ],
    }


def build_settled_case(ev: dict, case_no: str) -> dict:
    """多来源同年记载案：有一手来源才可定谳。

    这类案子展示来源记录在时间精度上的收敛；是否定谳取决于是否有一手来源。
    若多条转述都记为 1942 年，只能说明当前库内记载相合，不能据此认定历史原件如此。
    """
    d = ev.get("date") or {}
    p = ev.get("place") or {}
    year = str(d.get("start"))[:4]
    place_text, place_state = place_label(p)
    prec_cn = {"day": "日", "month": "月", "year": "年"}.get(d.get("precision"), "年")

    # 主体与动作按事件性质取，不能一律写「成立」——
    # 赵尚志牺牲案的 units 是「第二路军」（他的职务），拿它当主体会得出
    # 「第二路军成立于哪一年」，把殉国案写成建军案。
    et = ev.get("event_type")
    subject = ("、".join(ev.get("persons") or [])
               or "、".join(ev.get("units") or [])
               or "该事件")
    # 仍无主语的：从摘要里截取主语——取谓语（成立/爆发/失守…）之前的片段，
    # 再取最后一个「的」之后的尾段，避免整句入题。
    if subject == "该事件":
        m_v = re.search(r"(成立|爆发|失守|投降|殉国|会师|牺牲)", ev.get("summary") or "")
        if m_v:
            frag = (ev.get("summary") or "")[:m_v.start()]
            subject = frag.split("的")[-1].strip("，。、； ") or "该事件"
    # 文书/宣言类事件没有人物与部队，主体从摘要里的书名号提取——
    # 否则会写成「该事件成立于何时」，案名不知所云。
    m_doc = re.search(r"《([^》]+)》", ev.get("summary") or "")
    if m_doc:
        subject = f"《{m_doc.group(1)}》"
        act = "发表"
    else:
        act = {"牺牲": "牺牲", "战斗": "作战", "被捕": "被捕",
               "会议": "开会", "转移": "转移", "密营建立": "建立密营"}.get(et, "成立")

    srcs = [{
        "book": s.get("book"), "short": short_src(s.get("book")),
        "page": s.get("page"), "quote": s.get("quote"),
        "url": s.get("url"), "archive": s.get("archive"),
        "archive_note": s.get("archive_note"),
        "reliability": s.get("reliability"),
        "reliability_cn": RELIABILITY_CN.get(s.get("reliability"), "未标"),
        "value": None, "unit": None,
        "is_primary": s.get("reliability") == "A",
    } for s in ev.get("sources", [])]
    has_primary = any(s.get("reliability") == "A" for s in srcs)

    # P0-02：逐来源 × 逐精度算支持关系，不用来源条数代替逐条比对。
    # 「一家到日、几家到月」不是「来源记载相合」——只有明确到该精度才叫支持；
    # 到月/到季的来源只能算「范围相容」，动作不同的（编成 vs 成立）算「另一动作」。
    ds = date_support(ev)
    cnt = ds["counts"]
    yc = ds["year_counts"]
    md_prec = d.get("precision") or "year"
    if md_prec == "day":
        md_value = f"{ds['claim']['m']}月{ds['claim']['d']}日"
    elif md_prec == "month":
        md_value = f"{ds['claim']['m']}月"
    else:
        md_value = "原文仅到年"
    year_state = (f"{yc['exact']}/{len(srcs)} 家明载该年"
                  + (f"，{yc['none']} 家未载年份" if yc["none"] else "")
                  + (f"，{yc['off']} 家记他年" if yc["off"] else ""))
    assertions = [
        {"k": "主体", "v": subject, "state": "确定" if has_primary else "来源记载相合"},
        {"k": "时点", "v": f"{year}年（{year_state}）",
         "state": "确定" if has_primary else "来源记载相合"},
        {"k": "月日", "v": f"{md_value}（本库主张精度：{prec_cn}）", "state": ds["state"]},
        {"k": "地点", "v": place_text,
         "state": place_state if has_primary or place_state != "确定" else "来源记载"},
    ]

    ch = []
    if cnt.get("互斥"):
        bad = [r for r in ds["rows"] if r["state"] == "互斥"]
        ch.append({
            "code": "R9", "name": "日期记载不一致", "severity": "medium",
            "text": f"{len(bad)} 家来源给出与主张不符的时间："
                    + "、".join(f"「{r['expr']}」({r['short']})" for r in bad)
                    + "。这不是精度问题，是记载本身对不上——系统不替它们折中。",
        })
    if cnt.get("范围不符"):
        bad = [r for r in ds["rows"] if r["state"] == "范围不符"]
        ch.append({
            "code": "R10", "name": "精度范围不相容", "severity": "medium",
            "text": "、".join(f"「{r['expr']}」({r['short']})" for r in bad)
                    + f" 的时段不含主张的{md_value}。季节/区间是粗精度，但粗精度也可能与细主张冲突。",
        })
    if cnt.get("另一动作"):
        bad = [r for r in ds["rows"] if r["state"] == "另一动作"]
        ch.append({
            "code": "R11", "name": "动作不同，不作日期比对", "severity": "low",
            "text": "、".join(f"「{r['expr']}」({r['short']})" for r in bad)
                    + " 记的是「编成/改编」，与本条主张的「成立」不是同一动作，"
                      "既不计入支持，也不判为矛盾——需要档案确认两者是否为同一事件。",
        })
    if cnt.get("明确相合", 0) == 1 and cnt.get("范围相容"):
        only = [r for r in ds["rows"] if r["state"] == "明确相合"][0]
        ch.append({
            "code": "R12", "name": "仅一家明确到该精度", "severity": "medium",
            "text": f"只有「{only['short']}」明确记到 {md_value}；其余来源更粗（相容但不支持该精度）。"
                    "所以这是「一家明确 + 数家相容」，不是「来源记载相合」。",
        })
    if not has_primary:
        ch.append({
            "code": "R3", "name": "库内无一手档案", "severity": "medium",
            "text": f"{len(srcs)} 条来源记录均未标为一手档案。"
                    "所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。",
        })

    if not has_primary:
        status = "consistent"
        # 状态文案必须反映逐条比对结果：1 家明确 ≠ 记载相合
        if cnt.get("互斥") or cnt.get("范围不符"):
            status_cn = "库内年份相合 · 月日有分歧 · 未达定谳"
        elif cnt.get("明确相合", 0) >= 2:
            status_cn = f"库内 {cnt['明确相合']} 家记载相合 · 未达定谳"
        elif cnt.get("明确相合", 0) == 1:
            status_cn = "仅 1 家明确到该精度 · 未达定谳"
        else:
            status_cn = "库内年份记载相合 · 未达定谳"
        missing = ["需可核验的一手档案或命令原件，才能支持历史层面的定谳"]
        if cnt.get("互斥") or cnt.get("范围不符") or cnt.get("明确相合", 0) < 2:
            missing.insert(0, "月日主张缺少第二家明确记载，需原始档案或命令原件才能补足")
    elif cnt.get("互斥"):
        status, status_cn = "settled", "可以定谳 · 限于月"
        missing = ["日层面的分歧需原始档案或命令原件才能消除"]
    elif md_prec == "day" and cnt.get("明确相合", 0) >= 2:
        status, status_cn, missing = "settled", "可以定谳", []
    else:
        status = "settled"
        status_cn = f"可以定谳 · 限于{prec_cn}"
        missing = []

    conservative = (f"库内 {len(srcs)} 条来源记录中，{yc['exact']} 家明载「{year}年」"
                    + (f"、{yc['none']} 家未载年份" if yc["none"] else "")
                    + "；来源机构数不等于独立史源数。")
    if has_primary:
        conservative += "该结论仅在页面标明的时间精度范围内成立。"
    else:
        conservative += "这只能说明当前库内记载口径相合，不能据此定谳。"

    register = {
        "kind": "register", "agent": "存疑",
        "case_no": case_no,
        "status": status,
        "status_cn": status_cn,
        "missing": missing,
        "conservative": conservative,
        "high_count": 0,
    }

    return {
        "id": f"case_{case_no.lower().replace('-', '_')}",
        "case_no": case_no,
        "kind": status,
        "title": f"{subject}{act}于何时",
        "claim_text": f"{subject}于{year}年{act}",
        "event_id": ev["id"],
        "predicate": f"{act}时间", "unit": None, "values": [],
        "summary": ev.get("summary"),
        "steps": [
            {"kind": "decompose", "agent": "拆解",
             "lines": [f"命题拆成 {len(assertions)} 个原子断言。"
                       f"本次有 {len(srcs)} 条来源记录可比对；来源机构数不等于独立史源数。"],
             "assertions": assertions},
            {"kind": "retrieve", "agent": "辑录",
             "lines": [f"库内共 {len(srcs)} 条记载，均指向同一事件。原文逐字照录。"],
             "evidence": srcs, "side": []},
            {"kind": "examine", "agent": "对勘", "lines": [], "challenges": ch},
            register,
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", type=Path, default=OUT)
    ap.add_argument("--web", type=Path, default=ROOT / "web" / "cases.js",
                    help="同时输出前端可用的 cases.js（script 注入，file:// 可加载）")
    args = ap.parse_args()

    raw = json.loads(EVENTS.read_text(encoding="utf-8"))
    events = raw.get("events", []) if isinstance(raw, dict) else raw

    # 消费冲突报告：高严重度日期分歧的事件不做定谳案，单独立日期悬案
    conf = json.loads(CONF.read_text(encoding="utf-8")) if CONF.exists() else {}
    # 数值裁决链：三视图必须同源——卷宗也读同一份 verdicts
    verdicts = {}
    if VERDICTS_PATH.exists():
        verdicts = json.loads(VERDICTS_PATH.read_text(encoding="utf-8")).get("verdicts", {})
    high_date = {}   # event_id -> [date_variant 冲突条目]
    for dv in conf.get("date_variants", []):
        if dv.get("severity") == "high":
            high_date.setdefault(dv["event_id"], []).append(dv)
    for g in conf.get("conflicts", []):
        high_date.setdefault("_groups", []).extend(g.get("members", []))

    # 全库来源索引，供「辑录」做跨条目旁证检索
    all_sources = []
    for e in events:
        for s in e.get("sources", []):
            all_sources.append({
                "book": s.get("book"),
                "quote": s.get("quote"),
                "year": str((e.get("date") or {}).get("start"))[:4],
                "event_summary": e.get("summary"),
            })

    settled: list[dict] = []
    dispute: list[dict] = []
    single: list[dict] = []

    settled_cands = [e for e in events
                     if not e.get("measures") and len(e.get("sources") or []) >= 2
                     and e["id"] not in high_date]
    # 同年记载案不是全量罗列：只挑来源记录较多的几个，展示记录口径如何收敛。
    # 来源数相同则优先有日期主张的（能展示粗精度让位于细精度）。
    settled_cands.sort(key=lambda e: (-len(e.get("sources") or []),
                                      -len(e.get("date_variants") or [])))
    for e in settled_cands[:8]:
        settled.append(build_settled_case(e, "KL-000"))

    # 数值冲突案：同一数量项出现 ≥2 个不同取值，才立 case
    for e in events:
        ms = e.get("measures") or []
        if not ms:
            continue
        by_name: dict[str, list] = {}
        for m in ms:
            by_name.setdefault(m.get("name"), []).append(m)
        # 只在同一数量项出现 ≥2 个不同取值时立 case
        if not any(len({m["value"] for m in v}) >= 2 for v in by_name.values()):
            continue

        name, group = next((k, v) for k, v in by_name.items()
                           if len({m["value"] for m in v}) >= 2)
        vals = sorted({m["value"] for m in group})
        unit = group[0].get("unit", "")

        claim_measures = [m for m in group if m.get("value") == vals[0]]
        decompose = build_decompose(e, vals[0], unit, claim_measures)
        retrieve = build_retrieve(e, all_sources)
        examine = build_examine(e, e.get("sources", []), group)
        register = build_register(e, examine["challenges"], group, "KL-000")

        dispute.append({
            "id": "case_kl_000",
            "case_no": "KL-000",
            "kind": "dispute",
            "title": f"{'、'.join(e.get('units') or []) or '该主体'}{name}究竟是多少",
            "claim_text": f"{'、'.join(e.get('units') or []) or '该主体'}"
                          f"在{date_label(e.get('date') or {})}{name}为 {fmt(vals[0])} {unit}"
                          f"（库内最低的一种说法）",
            "event_id": e["id"],
            "predicate": name,
            "unit": unit,
            "values": vals,
            "summary": e.get("summary"),
            "verdict": verdicts.get(e.get("conflict_group") or ""),
            "steps": [decompose, retrieve, examine, register],
        })

    # 日期悬案：高严重度日期分歧单独立案（与数值悬案对称）
    for e in events:
        if e["id"] in high_date:
            dispute.append(build_date_case(e, high_date[e["id"]], "KL-000"))

    # 孤证案：挑两条标志性的牺牲事件，示范「史实存疑」与「库内证据不足」的界线。
    # 按人物在全库出现的频次排序——反复出现的人物才承载得起一个示范案。
    freq: dict[str, int] = {}
    for e in events:
        for p in e.get("persons") or []:
            freq[p] = freq.get(p, 0) + 1

    cands = [e for e in events
             if not e.get("measures")
             and len(e.get("sources") or []) == 1
             and e.get("event_type") == "牺牲"
             and e.get("persons")]
    cands.sort(key=lambda e: -max(freq.get(p, 0) for p in e["persons"]))
    for e in cands[:2]:
        single.append(build_single_case(e, "KL-000"))

    # 排序即叙事：先展示库内记载相合或有档案支撑的案例，再展示悬案与证据不足
    cases = settled + dispute + single
    for i, c in enumerate(cases, 1):
        no = court_no(i)
        c["case_no"] = no
        c["id"] = f"case_{no.lower().replace('-', '_')}"
        c["steps"][-1]["case_no"] = no

    payload = {
        "_note": "由 src/build_cases.py 从 events.json 生成。所有引文取自 sources.quote，未经改写。",
        "cases": cases,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    if args.web:
        args.web.parent.mkdir(parents=True, exist_ok=True)
        args.web.write_text(
            "window.__MIYING_CASES__ = "
            + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n",
            encoding="utf-8",
        )

    print(f"生成 {len(cases)} 个灯下案 → {args.out}")
    if args.web:
        print(f"前端数据 → {args.web}")
    for c in cases:
        reg = c["steps"][-1]
        print(f"  {c['case_no']} {c['title']}  "
              f"（{reg['status_cn']}，{reg['high_count']} 项高严重度对勘）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
