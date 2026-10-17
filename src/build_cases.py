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
    decompose  拆解   把命题拆成原子断言，逐项标注确定性
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
OUT = ROOT / "data" / "curated" / "cases.json"

# 时点模糊的语汇。原文出现这些词，说明命题本身没落在具体某一天。
VAGUE_TIME = ["鼎盛", "前后", "左右", "之际", "期间", "时期", "初期", "末期", "年初", "年底"]
# 数值为约数的语汇。原文出现这些词，数字就不能当精确值用。
# 注意不含「多」：它会误命中「一年多」这类非数值用法。
APPROX = ["约", "余", "近", "逾", "一说", "估计"]

RELIABILITY_CN = {"A": "一手档案", "B": "学术著作/权威报道", "C": "回忆录/展陈说明"}


def hits(text: str, words: list[str]) -> list[str]:
    return [w for w in words if w in (text or "")]


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


def build_decompose(ev: dict, claim_value, claim_unit: str) -> dict:
    """把命题拆成原子断言，逐项判定确定性。"""
    d = ev.get("date") or {}
    p = ev.get("place") or {}
    quote_all = " ".join(s.get("quote", "") for s in ev.get("sources", []))

    prec_cn = {"day": "日", "month": "月", "year": "年"}.get(d.get("precision"), "年")
    time_state = {"day": "确定", "month": "较粗", "year": "模糊"}.get(d.get("precision"), "模糊")
    if hits(quote_all, VAGUE_TIME):
        time_state = "模糊"

    place_text, place_state = place_label(p)

    approx = hits(quote_all, APPROX)
    value_state = "约数" if approx else "确定"

    assertions = [
        {"k": "主体", "v": "、".join(ev.get("units") or []) or "（原文未点名）", "state": "确定"},
        {"k": "时点", "v": f"{date_label(d)}（仅到{prec_cn}）", "state": time_state},
        {"k": "地点", "v": place_text, "state": place_state},
        {"k": "数值", "v": f"{fmt(claim_value)} {claim_unit}", "state": value_state},
    ]

    lines = [
        f"命题拆成 {len(assertions)} 个原子断言。任何一个不成立，命题就不能成立。",
    ]
    vt = hits(quote_all, VAGUE_TIME)
    if time_state == "模糊":
        tag = "".join(f"「{w}」" for w in vt) if vt else f"仅到{prec_cn}"
        lines.append(f"时点{tag}，没有落到具体年月——"
                     f"这会是后面所有分歧的源头，因为不同来源可能各自指向不同年份。")
    if approx:
        lines.append(f"原文出现「{'」「'.join(approx)}」，说明这个数字本身是约数。"
                     f"把它当成精确值来比较，方法上就已经失真。")

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

    # R1 时点无定义
    vt = hits(quote_all, VAGUE_TIME)
    if vt:
        ch.append({
            "code": "R1", "name": "时点无统一定义", "severity": "high",
            "text": f"两条原文都用「{vt[0]}」指代时间，但没有一条给出起止年月。"
                    f"「鼎盛」在史学上没有公认区间，不同来源可能各自指向不同年份——"
                    f"这是分歧的根，不是数字本身。",
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
        caveat = "（这个百分比本身建立在约数换算上，只能看量级，见 R6）" if hits(quote_all, APPROX) else ""
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
    ap = hits(quote_all, APPROX)
    if ap:
        ch.append({
            "code": "R6", "name": "约数被当作精确值", "severity": "medium",
            "text": f"原文用的是「{'」「'.join(ap[:3])}」。把「三万余」换算成 30,000 再算百分比差异，"
                    f"方法上就已经失真——约数只能比量级，不能比个位。",
        })

    # R7 自认分歧
    if "一说" in quote_all:
        ch.append({
            "code": "R7", "name": "史料自认存在异说", "severity": "high",
            "text": "有一条原文自己就写着「一说」。这不是我们比对出来的分歧，"
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
    quote_all = " ".join(s.get("quote", "") for s in ev.get("sources", []))

    # 从原文里抠出各方一致的硬事实（如「11个军」）
    consensus = []
    for pat, label in ((r"(\d+)\s*个军", "编成 {n} 个军"), (r"(\d+)\s*个路军", "编成 {n} 个路军")):
        m = re.search(pat, quote_all)
        if m:
            consensus.append(label.format(n=m.group(1)))

    missing = []
    if not any(s.get("reliability") == "A" for s in ev.get("sources", [])):
        missing.append("抗联各军兵力统计的原始报表或档案（现库内 0 条 A 级来源）")
    if hits(quote_all, VAGUE_TIME):
        missing.append("「鼎盛时期」的起止年月，需权威辞书或军史给出界定")
    if hits(quote_all, APPROX):
        missing.append("精确到百位的统计口径说明（现有原文全为约数）")

    if len(vals) >= 2:
        if consensus:
            sure = f"可以确定的是：{'、'.join(consensus)}——这一点各条原文一致。"
        else:
            sure = ("可以确定的是：各来源对「此时处于规模高点」这一定性并无分歧，"
                    "分歧只在具体数字。")
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
    """定谳案：多源在某一层级上一致。

    这类案子存在的意义是证明系统不是个只会说「不知道」的怀疑论者——
    该定的定，但要说清楚**定到哪一层**。
    三条来源都说 1942 年，年份可以定；月日说法不一，月日就不定。
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
        "reliability": s.get("reliability"),
        "reliability_cn": RELIABILITY_CN.get(s.get("reliability"), "未标"),
        "value": None, "unit": None,
        "is_primary": s.get("reliability") == "A",
    } for s in ev.get("sources", [])]

    # 月日层面：优先用来源级日期主张（date_variants）。
    # 从 quote 里正则抠时间不可靠——纪念网同一条里既有「7月22日编成」
    # 又有「8月1日成立」，正则取第一个就会把建军日当成成立日。
    variants = ev.get("date_variants") or []
    if variants:
        exprs = [{"short": short_src(v.get("source")),
                  "expr": md_label(v.get("value", ""), v.get("precision"))}
                 for v in variants]
        day_vals = sorted({v["value"] for v in variants if v.get("precision") == "day"})
        if len(day_vals) == 1:
            distinct = {md_label(day_vals[0], "day")}
        elif len(day_vals) > 1:
            distinct = {md_label(v, "day") for v in day_vals}
        else:
            distinct = sorted({md_label(v.get("value", ""), "month") for v in variants})
    else:
        exprs = []
        for s in ev.get("sources", []):
            q = s.get("quote", "")
            found = re.findall(r"\d{1,2}月\d{1,2}日|\d{1,2}月|(?:春|夏|秋|冬)季?|年初|年底", q)
            exprs.append({"short": short_src(s.get("book")),
                          "expr": found[0] if found else "未载具体时间"})
        distinct = {e["expr"] for e in exprs}
    assertions = [
        {"k": "主体", "v": subject, "state": "确定"},
        {"k": "时点", "v": f"{year}年（{len(srcs)} 条来源均记此年）", "state": "确定"},
        {"k": "月日", "v": "／".join(sorted(distinct)), "state": "较粗" if len(distinct) > 1 else "确定"},
        {"k": "地点", "v": place_text, "state": place_state},
    ]

    ch = []
    # 分歧分两种，不能混：精度不同是「记得粗」，日值不同是「记得不一样」。
    if len(distinct) > 1:
        if variants and len(day_vals) > 1:
            ch.append({
                "code": "R9", "name": "日期记载不一致", "severity": "medium",
                "text": f"{len(day_vals)} 条来源都精确到日，却给出不同的日子："
                        + "、".join(f"「{e['expr']}」({e['short']})" for e in exprs)
                        + "。这不是精度问题，是记载本身对不上——系统只定到月，日子留作悬案。",
            })
        else:
            ch.append({
                "code": "R8", "name": "时间精度不一致", "severity": "medium",
                "text": f"{len(srcs)} 条来源对年份没有分歧，但月日停在不同的精度上："
                        + "、".join(f"「{e['expr']}」({e['short']})" for e in exprs)
                        + "。这不是矛盾，是粗细不同——粗的让位于细的，但细的一方仍需第二家佐证。",
            })
    if not any(s.get("reliability") == "A" for s in srcs):
        ch.append({
            "code": "R3", "name": "库内无一手档案", "severity": "medium",
            "text": f"{len(srcs)} 条来源均为转述，无一出自原始档案。"
                    "所以能定的是「这几家都这样写」，不是「档案原件如此」。",
        })

    if variants and len(day_vals) == 1:
        status_cn, missing = "可以定谳", []
    elif len(distinct) > 1:
        status_cn = "可以定谳 · 限于月"
        missing = ["日层面的分歧需原始档案或命令原件才能消除"]
    elif d.get("precision") == "day":
        status_cn, missing = "可以定谳", []
    else:
        status_cn = f"可以定谳 · 限于{prec_cn}"
        missing = []

    register = {
        "kind": "register", "agent": "存疑",
        "case_no": case_no,
        "status": "settled",
        "status_cn": status_cn,
        "missing": missing,
        "conservative": f"{len(srcs)} 条独立来源对「{year}年」没有分歧，这一点可以定谳。"
                        + ("月日层面各方精度不一或日子对不上，系统不在该层面下结论——"
                           "定谳是有范围的，超出范围的部分仍是悬案。"
                           if len(distinct) > 1 else ""),
        "high_count": 0,
    }

    return {
        "id": f"case_{case_no.lower().replace('-', '_')}",
        "case_no": case_no,
        "kind": "settled",
        "title": f"{subject}{act}于何时",
        "claim_text": f"{subject}于{year}年{act}",
        "event_id": ev["id"],
        "predicate": f"{act}时间", "unit": None, "values": [],
        "summary": ev.get("summary"),
        "steps": [
            {"kind": "decompose", "agent": "拆解",
             "lines": [f"命题拆成 {len(assertions)} 个原子断言。"
                       f"本次有 {len(srcs)} 条独立来源可比对。"],
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
                     if not e.get("measures") and len(e.get("sources") or []) >= 2]
    # 定谳案不是全量罗列：多源一致是正常条目，不构成案子。
    # 只挑来源最多的几个，用来示范「多源如何收敛到同一天」。
    # 来源数相同则优先有日期主张的（能展示粗精度让位于细精度）。
    settled_cands.sort(key=lambda e: (-len(e.get("sources") or []),
                                      -len(e.get("date_variants") or [])))
    for e in settled_cands[:4]:
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

        decompose = build_decompose(e, vals[0], unit)
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
            "steps": [decompose, retrieve, examine, register],
        })

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

    # 排序即叙事：先证明系统会定谳，再展示它敢悬案，最后划清「库内不足」的界线
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
