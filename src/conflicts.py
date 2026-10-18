"""史料事件库校验 + 多源冲突检测。

用法：
    python src/conflicts.py data/curated/events.json -o data/curated/conflicts.json

只依赖标准库。输出：
    1) 校验报告（缺字段 / 枚举越界 / 无来源 / 数值主张不完整）
    2) 冲突报告
    3) 每个事件的置信度（按来源等级加权，冲突扣分）

冲突有两种形态，必须分开处理：

    between —— 同一事实被拆成两条事件记录，彼此字段不一致。
               适用于日期、地点、伤亡这类"整条记载"层面的分歧。

    within  —— 一条事件内部，不同来源对同一个数量项给出不同数值。
               这是史料分歧最常见的形态（同一个"鼎盛时期兵力"，
               人民日报说 3 万余，国图简史说四万五千余）。
               不能靠伪造第二条事件来比对，所以数量项必须绑定到来源上。

数量项（measures）因此是"来源级"的：每条数值都记着自己出自哪本书。
脱离出处的数字不入库 —— 与"无来源不入库"同一条底线。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

REQUIRED = ["id", "date", "place", "event_type", "summary", "sources", "confidence"]
EVENT_TYPES = {"战斗", "转移", "密营建立", "被捕", "牺牲", "会议", "群众工作", "其他"}
PRECISIONS = {"day", "month", "year"}
PLACE_PRECISIONS = {"site", "town", "county", "province"}
PROV_DEPTHS = {"deep", "shallow", "none"}
RELIABILITY_WEIGHT = {"A": 1.0, "B": 0.7, "C": 0.45}

# 数量项相对差的分级阈值
MEASURE_HIGH = 0.25
MEASURE_MID = 0.10


def validate(events: list[dict]) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for i, e in enumerate(events):
        tag = e.get("id", f"#{i}")
        if tag in seen:
            problems.append(f"{tag}: id 重复")
        seen.add(tag)

        for k in REQUIRED:
            if k not in e:
                problems.append(f"{tag}: 缺必填字段 {k}")

        d = e.get("date", {})
        if d.get("precision") not in PRECISIONS:
            problems.append(f"{tag}: date.precision 非法（{d.get('precision')}）")
        if not d.get("start"):
            problems.append(f"{tag}: date.start 缺失")

        p = e.get("place", {})
        if p.get("precision") not in PLACE_PRECISIONS:
            problems.append(f"{tag}: place.precision 非法（{p.get('precision')}）")
        if p.get("precision") == "site" and (p.get("lat") is None or p.get("lng") is None):
            problems.append(f"{tag}: place.precision=site 但缺坐标")
        if p.get("precision") == "county" and (p.get("lat") is None or p.get("lng") is None):
            problems.append(f"{tag}: place.precision=county 应填县质心坐标")

        if e.get("event_type") not in EVENT_TYPES:
            problems.append(f"{tag}: event_type 非法（{e.get('event_type')}）")

        srcs = e.get("sources") or []
        if not srcs:
            problems.append(f"{tag}: 无来源，禁止入库")
        for j, s in enumerate(srcs):
            if not s.get("book") or not s.get("quote"):
                problems.append(f"{tag}: sources[{j}] 缺 book 或 quote")
            if s.get("reliability") not in RELIABILITY_WEIGHT:
                problems.append(f"{tag}: sources[{j}] reliability 非法（{s.get('reliability')}）")

        books = {s.get("book") for s in srcs}
        for j, m in enumerate(e.get("measures") or []):
            if not m.get("name"):
                problems.append(f"{tag}: measures[{j}] 缺 name")
            if not isinstance(m.get("value"), (int, float)):
                problems.append(f"{tag}: measures[{j}] value 非数字（{m.get('value')}）")
            if not m.get("unit"):
                problems.append(f"{tag}: measures[{j}] 缺 unit")
            if not m.get("source"):
                problems.append(f"{tag}: measures[{j}] 缺 source —— 数值必须绑定来源")
            elif m.get("source") not in books:
                problems.append(
                    f"{tag}: measures[{j}] 的 source 不在 sources 中（{m.get('source')}）"
                )

        problems.extend(check_provenance(tag, e, books))
    return problems


def check_provenance(tag: str, e: dict, books: set) -> list[str]:
    """校验检索记录（负证据）。

    这里只做结构校验与两条一致性检查，后者才是关键：

    1. 不许重复计票——已入库的来源，不能在检索记录里再算作"独立命中"。
    2. 不许检索到了却装没看见——若某轮检索命中了独立记载，而事件仍只有
       一条来源，就说明要么该补 source，要么得写明为何那条不算支撑。
       "没找到"可以，但"找到了不用"必须给理由。
    """
    out: list[str] = []
    prov = e.get("provenance")
    if prov is None:
        return out

    depth = prov.get("depth")
    if depth not in PROV_DEPTHS:
        out.append(f"{tag}: provenance.depth 非法（{depth}）")

    probes = prov.get("probes") or []
    if depth in ("deep", "shallow") and not probes:
        out.append(f"{tag}: provenance.depth={depth} 却没有任何检索记录")

    srcs = e.get("sources") or []
    for k, pr in enumerate(probes):
        if not pr.get("q"):
            out.append(f"{tag}: provenance.probes[{k}] 缺检索词 q")
        if not isinstance(pr.get("n"), int):
            out.append(f"{tag}: provenance.probes[{k}] 的 n 必须是整数")
        indep = pr.get("indep") or []
        for name in indep:
            if name in books:
                out.append(
                    f"{tag}: 检索记录把已入库来源「{name}」又算作独立命中，重复计票"
                )
        if indep and len(srcs) == 1 and not pr.get("note"):
            out.append(
                f"{tag}: 检索到独立记载「{indep[0]}」但未入库，且未写明理由"
                f" —— 要么补 source，要么在 note 里说明为何不算支撑"
            )
    return out


def parse_date(s: str) -> date | None:
    try:
        y, m, d = (s.split("-") + ["1", "1"])[:3]
        return date(int(y), int(m), int(d))
    except (ValueError, AttributeError):
        return None


def month_gap(a: dict, b: dict) -> int | None:
    da, db = parse_date(a.get("start", "")), parse_date(b.get("start", ""))
    if not da or not db:
        return None
    return abs((da.year - db.year) * 12 + (da.month - db.month))


def diff_pair(a: dict, b: dict) -> list[dict]:
    """返回两条事件记录之间的字段级差异。"""
    out: list[dict] = []

    gap = month_gap(a.get("date", {}), b.get("date", {}))
    if gap is not None and gap > 0:
        out.append({
            "field": "date.start",
            "kind": "field",
            "a": a["date"]["start"],
            "b": b["date"]["start"],
            "delta_months": gap,
            "severity": "high" if gap >= 6 else "low",
        })

    pa, pb = a.get("place", {}).get("modern"), b.get("place", {}).get("modern")
    if pa and pb and pa != pb:
        out.append({"field": "place.modern", "kind": "field", "a": pa, "b": pb,
                    "severity": "high"})

    ca = (a.get("casualties") or {}).get("our")
    cb = (b.get("casualties") or {}).get("our")
    if ca is not None and cb is not None and ca != cb:
        base = max(ca, cb, 1)
        ratio = abs(ca - cb) / base
        out.append({
            "field": "casualties.our",
            "kind": "field",
            "a": ca,
            "b": cb,
            "ratio": round(ratio, 2),
            "severity": "high" if ratio >= 0.5 else "low",
        })
    return out


def measure_diffs(events: list[dict]) -> list[dict]:
    """同一组事件里，同名数量项的取值分歧。

    先按「数值」归并来源，再对不同数值两两出报告。
    这样两个来源都说 50 万时只算一个取值，不会报成两处分歧。
    """
    pool: dict[str, dict[float, dict]] = defaultdict(lambda: defaultdict(
        lambda: {"unit": "", "srcs": [], "pages": [], "eids": set()}
    ))
    for e in events:
        for m in e.get("measures") or []:
            name = (m.get("name") or "").strip()
            v = m.get("value")
            if not name or not isinstance(v, (int, float)):
                continue
            slot = pool[name][v]
            slot["unit"] = slot["unit"] or (m.get("unit") or "")
            src = m.get("source") or ""
            if src and src not in slot["srcs"]:
                slot["srcs"].append(src)
            pg = m.get("page")
            if pg and pg not in slot["pages"]:
                slot["pages"].append(pg)
            slot["eids"].add(e["id"])

    diffs: list[dict] = []
    for name, by_val in pool.items():
        vals = list(by_val.keys())
        if len(vals) < 2:
            continue
        for va, vb in combinations(vals, 2):
            sa, sb = by_val[va], by_val[vb]
            base = max(abs(va), abs(vb), 1)
            ratio = abs(va - vb) / base
            if ratio >= MEASURE_HIGH:
                sev = "high"
            elif ratio >= MEASURE_MID:
                sev = "medium"
            else:
                sev = "low"
            ids = sa["eids"] | sb["eids"]
            diffs.append({
                "field": name,
                "kind": "measure",
                "a": va,
                "b": vb,
                "unit": sa["unit"] or sb["unit"],
                "a_src": "、".join(sa["srcs"]),
                "b_src": "、".join(sb["srcs"]),
                "a_page": "、".join(sa["pages"]) or None,
                "b_page": "、".join(sb["pages"]) or None,
                "a_id": sorted(sa["eids"])[0],
                "b_id": sorted(sb["eids"])[0],
                "same_event": len(ids) == 1,
                "ratio": round(ratio, 2),
                "severity": sev,
            })
    return diffs


def date_variant_diffs(events: list[dict]) -> list[dict]:
    """同一事件内，不同来源对日期的不同主张。

    史料里"日期打架"很少表现为两条事件记录，多数是同一条记载被几家
    写出不同的日子。所以日期也必须做成来源级主张（date_variants），
    与 measures 同构。

    精度不同的两方要分开判：一方只到月、另一方到日，而日落在那个月里，
    这是精度差异不是矛盾 —— 硬判成冲突，等于把"记得细"当成"记得不一样"。
    """
    out: list[dict] = []
    for e in events:
        vs = e.get("date_variants") or []
        if len(vs) < 2:
            continue
        for a, b in combinations(vs, 2):
            da, db = parse_date(a.get("value", "")), parse_date(b.get("value", ""))
            if not da or not db:
                continue
            days = abs((da - db).days)
            pa, pb = a.get("precision"), b.get("precision")

            if days == 0:
                kind = "same"
            elif pa == pb:
                kind = "conflict"
            else:
                # 粗的一方是否覆盖细的一方（同年同月即视为覆盖）
                coarse, fine = (a, b) if pa == "month" else (b, a)
                dc, df = parse_date(coarse["value"]), parse_date(fine["value"])
                kind = "precision" if (dc.year, dc.month) == (df.year, df.month) else "conflict"

            if kind == "same":
                continue
            if days > 30:
                sev = "high"
            elif days > 3:
                sev = "mid"
            else:
                sev = "low"
            if kind == "precision":
                sev = "low"

            out.append({
                "event_id": e["id"],
                "field": "date.start",
                "kind": kind,
                "gap_days": days,
                "a": a,
                "b": b,
                "severity": sev,
            })
    out.sort(key=lambda d: (-d["gap_days"], d["event_id"]))
    return out


def detect_conflicts(events: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for e in events:
        g = e.get("conflict_group")
        if g:
            groups[g].append(e)

    reports: list[dict] = []
    for gid, members in groups.items():
        bucket: dict[tuple[str, str, str], list[dict]] = {}

        for a, b in combinations(members, 2):
            diffs = diff_pair(a, b)
            if diffs:
                bucket[(a["id"], b["id"], "between")] = diffs

        for d in measure_diffs(members):
            key = (d["a_id"], d["b_id"], "within" if d["same_event"] else "between")
            bucket.setdefault(key, []).append(d)

        if not bucket:
            continue

        pairs = [
            {"a": k[0], "b": k[1], "scope": k[2], "diffs": v}
            for k, v in bucket.items()
        ]
        reports.append({
            "conflict_group": gid,
            "members": [m["id"] for m in members],
            "pairs": pairs,
            "high_severity": sum(
                1 for p in pairs for d in p["diffs"] if d["severity"] == "high"
            ),
            "field_count": len({d["field"] for p in pairs for d in p["diffs"]}),
        })

    reports.sort(key=lambda r: (-r["high_severity"], -r["field_count"], r["conflict_group"]))
    return reports


def score_confidence(events: list[dict], conflicts: list[dict]) -> dict[str, float]:
    """启发式分值 = 最高来源等级权重 + 来源机构数加成 − 冲突惩罚。

    分值不是概率；机构不同也不代表史源彼此独立，来源谱系需单独审查。

    注意：同一事件内部的冲突，p["a"] 与 p["b"] 是同一个 id，
    扣分只能记一次，否则一条分歧会被算成两处。
    """
    penalized: dict[str, int] = defaultdict(int)
    for rep in conflicts:
        for p in rep["pairs"]:
            high = sum(1 for d in p["diffs"] if d["severity"] == "high")
            if high:
                for eid in {p["a"], p["b"]}:
                    penalized[eid] += high

    scores: dict[str, float] = {}
    for e in events:
        weights = [RELIABILITY_WEIGHT.get(s.get("reliability"), 0.4) for s in e.get("sources", [])]
        if not weights:
            scores[e["id"]] = 0.0
            continue
        base = max(weights)
        orgs = {short_src(s.get("book")) for s in e.get("sources", []) if s.get("book")}
        bonus = 0.08 * min(max(len(orgs) - 1, 0), 3)  # 不同来源机构加分，最多 +0.24
        score = min(1.0, base + bonus) - 0.12 * penalized.get(e["id"], 0)
        scores[e["id"]] = round(max(0.05, score), 2)
    return scores


def short_src(s: str) -> str:
    """把「国家图书馆《抗联简史》（引…）」缩成「国家图书馆」，便于终端阅读。"""
    s = str(s or "")
    head = s.split("《")[0].split("（")[0].strip()
    return head or s[:18]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=None)
    args = ap.parse_args()

    if not args.path.exists():
        print(f"找不到 {args.path}", file=sys.stderr)
        return 1

    events = json.loads(args.path.read_text(encoding="utf-8"))
    if isinstance(events, dict):
        events = events.get("events", [])

    problems = validate(events)
    print(f"事件数：{len(events)}")
    print(f"校验问题：{len(problems)}")
    for p in problems[:20]:
        print("  !", p)
    if len(problems) > 20:
        print(f"  ... 另有 {len(problems) - 20} 条")

    conflicts = detect_conflicts(events)
    scores = score_confidence(events, conflicts)

    measures = sum(len(e.get("measures") or []) for e in events)
    print(f"\n数值主张：{measures} 条")
    print(f"冲突组：{len(conflicts)}")
    for rep in conflicts:
        scope = "事件内" if all(p["scope"] == "within" for p in rep["pairs"]) else "事件间"
        print(f"  [{rep['conflict_group']}] {scope} · {rep['field_count']} 个字段 · "
              f"{rep['high_severity']} 处高严重度差异")
        for p in rep["pairs"]:
            for d in p["diffs"]:
                if d["kind"] == "measure":
                    print(f"     {d['field']}: {d['a']:,}{d['unit']}（{short_src(d['a_src'])}）"
                          f" vs {d['b']:,}{d['unit']}（{short_src(d['b_src'])}）"
                          f" 差 {d['ratio']:.0%} [{d['severity']}]")
                else:
                    print(f"     {p['a']} vs {p['b']} | {d['field']}: "
                          f"{d['a']} / {d['b']} ({d['severity']})")

    low = sorted(scores.items(), key=lambda x: x[1])[:5]
    print("\n置信度最低的 5 条：", low)

    dv = date_variant_diffs(events)
    print(f"\n日期主张分歧：{len(dv)} 处")
    for d in dv:
        if d["kind"] == "precision":
            print(f"  {d['event_id']} [精度差异] "
                  f"{d['a']['value']}（{d['a']['precision']}，{d['a']['source']}） vs "
                  f"{d['b']['value']}（{d['b']['precision']}，{d['b']['source']}）"
                  f" —— 一方只到月，另一方到日，日落在同月内，非矛盾")
        else:
            print(f"  {d['event_id']} [日期冲突·{d['severity']}] 差 {d['gap_days']} 天："
                  f"{d['a']['value']}（{d['a']['source']}） vs "
                  f"{d['b']['value']}（{d['b']['source']}）")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(
                {
                    "problems": problems,
                    "conflicts": conflicts,
                    "date_variants": dv,
                    "confidence": scores,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"\n已写出 {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
