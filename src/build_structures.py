"""把事件库转成「承重结构」——来源与结论的支撑关系图。

用法：
    python src/build_structures.py

产出：
    data/curated/structures.json
    web/structures.js

要回答的问题不是「抗联发生了什么」，而是：
    **我们关于抗联的知识，是靠几根柱子在撑？**

每个结论（一条事件）由若干来源支撑。当一个来源同时支撑大量结论时，
它就是整个知识体系的单点故障——抽掉它，几十条结论同时失去依据。

这不是可视化技巧，是可计算的脆弱性。
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / "data" / "curated" / "events.json"
OUT = ROOT / "data" / "curated" / "structures.json"

RELIABILITY_WEIGHT = {"A": 1.0, "B": 0.7, "C": 0.45}
RELIABILITY_CN = {"A": "一手档案", "B": "学术著作/权威报道", "C": "回忆录/展陈/待核转述"}


# 长机构名的固定短写。图上柱宽有限，全称放不下；
# 但缩写不能自己造词，必须是这个机构通行的简称，否则读图的人对不上。
SHORT_OVERRIDE = {
    "侵华日军南京大屠杀遇难同胞纪念馆": "南京大屠杀馆",
    "抗日战争纪念网": "抗战纪念网",
    "国家图书馆": "国图",
    "赵尚志纪念馆": "赵尚志馆",
    "莆田市博物馆": "莆田博物馆",
    "辽宁日报": "辽宁日报",
}


def short_src(s: str) -> str:
    s = str(s or "")
    head = s.split("《")[0].split("（")[0].strip()
    if head in SHORT_OVERRIDE:
        return SHORT_OVERRIDE[head]
    return head or s[:18]


def _prov_summary(prov: dict) -> dict:
    """把检索记录压成前端够用的摘要。

    前端要回答的问题只有一个：这条结论，到底查没查过。
    查过就说清查了几组词、检索记录如何标注来源关系；没查就直说没查。
    """
    probes = prov.get("probes") or []
    return {
        "depth": prov.get("depth") or "none",
        "probes": len(probes),
        "queries": [p.get("q") for p in probes if p.get("q")],
        "indep": sum(len(p.get("indep") or []) for p in probes),
        "deriv": sum(int(p.get("deriv") or 0) for p in probes),
        "not_searched": prov.get("not_searched") or [],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", type=Path, default=OUT)
    ap.add_argument("--web", type=Path, default=ROOT / "web" / "structures.js")
    args = ap.parse_args()

    raw = json.loads(EVENTS.read_text(encoding="utf-8"))
    events = raw.get("events", []) if isinstance(raw, dict) else raw

    # 来源归并：同一本书视为同一根柱子。
    # 以「出版社/机构名」为键——同一本书在录入时可能带不同的括注（如「（引孔令波…）」），
    # 按全串归并会把一本书拆成两根柱子，直接毁掉承重分析。
    src_index: dict[str, dict] = {}
    for e in events:
        for s in e.get("sources", []):
            book = s.get("book") or "（未署来源）"
            key = short_src(book)
            node = src_index.setdefault(key, {
                "id": f"src_{len(src_index) + 1}",
                "full": book,
                "short": key,
                "reliability": s.get("reliability"),
                "reliability_cn": RELIABILITY_CN.get(s.get("reliability"), "未标"),
                "page": s.get("page"),
                "supports": [],
                "weight": RELIABILITY_WEIGHT.get(s.get("reliability"), 0.4),
            })
            # 保留信息量更大的书名写法
            if len(book) > len(node["full"]):
                node["full"] = book
            if e["id"] not in node["supports"]:
                node["supports"].append(e["id"])

    conclusions = []
    for e in events:
        keys: list[str] = []
        for s in e.get("sources", []):
            k = short_src(s.get("book"))
            if k and k not in keys:
                keys.append(k)
        d = e.get("date") or {}
        p = e.get("place") or {}
        conclusions.append({
            "id": e["id"],
            "claim": e.get("summary") or e["id"],
            "year": int(str(d.get("start"))[:4] or 0),
            "precision": d.get("precision"),
            "place": p.get("modern") or p.get("name") or "",
            "event_type": e.get("event_type"),
            "persons": e.get("persons") or [],
            "supports": keys,
            "load": round(sum(src_index[k]["weight"] for k in keys), 2),
            "conflict_group": e.get("conflict_group"),
            "measures": e.get("measures") or [],
            # 检索记录摘要：前端据此告诉观众「这条到底查没查过」
            "prov": _prov_summary(e.get("provenance") or {}),
            "sources": [
                {"book": s.get("book"), "short": short_src(s.get("book")),
                 "page": s.get("page"), "quote": s.get("quote"),
                 "url": s.get("url"), "archive": s.get("archive"),
                 "archive_note": s.get("archive_note"),
                 "reliability": s.get("reliability")}
                for s in e.get("sources", [])
            ],
        })

    # 关键性：一个来源独占支撑了多少结论（抽掉它，这些结论立刻失去全部依据）
    for node in src_index.values():
        node["count"] = len(node["supports"])
        node["exclusive"] = 0
    by_event = {c["id"]: c for c in conclusions}
    for node in src_index.values():
        for eid in node["supports"]:
            if len(by_event[eid]["supports"]) == 1:
                node["exclusive"] += 1

    total = len(conclusions)
    for node in src_index.values():
        node["share"] = round(node["count"] / total, 3) if total else 0
        # 独占率：只靠它一家的结论占比。抽掉它，这些结论彻底归零。
        node["exclusive_share"] = round(node["exclusive"] / total, 3) if total else 0
        # 单点故障判在"独占"上，不是"支撑"上。
        # 一个来源可以支撑 100% 的结论却一条都不独占 —— 抽掉它什么也不塌，
        # 那不是单点故障，那是冗余。用支撑占比判会把冗余误报成脆弱。
        node["single_point"] = node["exclusive_share"] >= 0.5

    sources = sorted(src_index.values(), key=lambda x: -x["count"])

    # 每个来源被移除后，仍有多少结论保有支撑
    resilience = []
    for node in sources:
        remain = sum(1 for c in conclusions
                     if any(k != node["short"] for k in c["supports"]))
        resilience.append({
            "source": node["short"], "full": node["full"],
            "removed": node["count"],
            "surviving": remain,
            "collapse_rate": round(1 - remain / total, 3) if total else 0,
        })

    single = sum(1 for c in conclusions if len(c["supports"]) == 1)
    no_primary = sum(1 for c in conclusions
                     if all(s["reliability"] != "A" for s in c["sources"]))

    by_year = defaultdict(lambda: {"n": 0, "load": 0.0})
    for c in conclusions:
        if c["year"]:
            by_year[c["year"]]["n"] += 1
            by_year[c["year"]]["load"] += c["load"]
    year_series = [
        {"year": y, "n": v["n"],
         "avg_load": round(v["load"] / v["n"], 2) if v["n"] else 0}
        for y, v in sorted(by_year.items())
    ]

    # 数值裁决链（curated/verdicts.json）注入 2D
    verdicts = {}
    vp = ROOT / "data" / "curated" / "verdicts.json"
    if vp.exists():
        verdicts = json.loads(vp.read_text(encoding="utf-8")).get("verdicts", {})

    payload = {
        "_note": "由 src/build_structures.py 从 events.json 生成。支撑关系取自 sources.book。",
        "sources": sources,
        "conclusions": conclusions,
        "resilience": resilience,
        "year_series": year_series,
        "verdicts": verdicts,
        "stats": {
            "conclusions": total,
            "sources": len(sources),
            "multi_support": sum(1 for c in conclusions if len(c["supports"]) > 1),
            "single_support": single,
            "single_support_rate": round(single / total, 3) if total else 0,
            "no_primary_source": no_primary,
            "top_source_share": sources[0]["share"] if sources else 0,
            "top_exclusive_share": sources[0]["exclusive_share"] if sources else 0,
            "critical_sources": sum(1 for s in sources if s["single_point"]),
            "deep_searched": sum(1 for e in events
                                 if (e.get("provenance") or {}).get("depth") == "deep"),
            "shallow_searched": sum(1 for e in events
                                    if (e.get("provenance") or {}).get("depth") == "shallow"),
            "unsearched": sum(1 for e in events
                              if (e.get("provenance") or {}).get("depth") in (None, "none")),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    if args.web:
        args.web.parent.mkdir(parents=True, exist_ok=True)
        args.web.write_text(
            "window.__MIYING_STRUCT__ = "
            + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n",
            encoding="utf-8",
        )

    st = payload["stats"]
    print(f"结论 {st['conclusions']} 条 · 来源 {st['sources']} 个")
    print(f"多来源机构支撑 {st['multi_support']} 条")
    print(f"单一支撑 {st['single_support']} 条（{st['single_support_rate']:.0%}）")
    print(f"无一手档案的结论 {st['no_primary_source']} 条")
    print(f"最大来源：支撑面 {st['top_source_share']:.0%} · 独占面 {st['top_exclusive_share']:.0%}")
    print(f"检索深度：deep {st['deep_searched']} / shallow {st['shallow_searched']} / "
          f"未检索 {st['unsearched']}")
    print("\n来源承重排行：")
    for s in sources:
        flag = "  ← 单点故障" if s["single_point"] else ""
        print(f"  {s['short']:<26} 支撑 {s['count']:>2} 条  独占 {s['exclusive']:>2} 条"
              f"  支撑面 {s['share']:.0%}  独占面 {s['exclusive_share']:.0%}{flag}")
    print("\n移除后崩塌率：")
    for r in resilience:
        print(f"  去掉 {r['source']:<26} → 崩塌 {r['collapse_rate']:.0%}"
              f"（{r['removed']} 条失去依据，剩 {r['surviving']} 条）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
