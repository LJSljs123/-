"""把事件库与冲突报告打包成前端可直接读取的 data.js。

用法：
    python src/conflicts.py data/demo/_demo_synthetic.json -o data/demo/conflicts.json
    python src/build_web.py data/demo/_demo_synthetic.json data/demo/conflicts.json

产出：web/data.js，内容为 window.__MIYING__ = {...}
用 <script src="data.js"> 引入，file:// 协议下也能加载（不受 fetch 的 CORS 限制）。
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def year_of(e: dict) -> int:
    try:
        return int(str(e["date"]["start"])[:4])
    except (KeyError, ValueError, TypeError):
        return 0


def site_to_event(s: dict) -> dict:
    """把国务院名录中的遗址条目转成前端可用的实体。"""
    return {
        "id": s["id"],
        "layer": "site",
        "event_type": "遗址",
        "category": s.get("category", ""),
        "summary": s["name"],
        "date": {"start": None, "end": None, "precision": "year"},
        "place": {
            "name": s.get("address", ""),
            "modern": s.get("address", ""),
            "lat": s.get("lat"),
            "lng": s.get("lng"),
            "precision": s.get("precision", "county"),
        },
        "region": s.get("region", ""),
        "batch": s.get("batch"),
        "published": s.get("published", ""),
        "units": [],
        "persons": [],
        "sources": [
            {
                "book": f"国务院《关于公布第{s.get('batch')}批国家级抗战纪念设施、遗址名录的通知》",
                "page": f"{s.get('published')}年",
                "quote": f"{s['name']}　位于{s.get('address', '')}",
                "reliability": "A",
            }
        ],
        "confidence": 1.0,
        "conflict_group": None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("events", type=Path)
    ap.add_argument("conflicts", type=Path)
    ap.add_argument("--sites", type=Path, default=ROOT / "data" / "curated" / "sites.json")
    ap.add_argument("-o", "--out", type=Path, default=ROOT / "web" / "data.js")
    args = ap.parse_args()

    raw = json.loads(args.events.read_text(encoding="utf-8"))
    events = raw.get("events", []) if isinstance(raw, dict) else raw
    report = json.loads(args.conflicts.read_text(encoding="utf-8"))

    conf = report.get("confidence", {})
    for e in events:
        e["confidence"] = conf.get(e["id"], e.get("confidence", 0))
        e["layer"] = "event"

    sites = []
    if args.sites and args.sites.exists():
        sdata = json.loads(args.sites.read_text(encoding="utf-8"))
        sites = [site_to_event(s) for s in sdata.get("sites", [])]

    years = [y for y in (year_of(e) for e in events) if y]
    named = sum(1 for e in events if e.get("persons"))
    conflict_ids = {i for r in report.get("conflicts", []) for i in r["members"]}

    by_year = Counter(year_of(e) for e in events)
    by_type = Counter(e.get("event_type", "其他") for e in events)

    payload = {
        "events": events + sites,
        "conflicts": report.get("conflicts", []),
        "meta": {
            "total": len(events),
            "sites": len(sites),
            "named": named,
            "unnamed": len(events) - named,
            "conflict_groups": len(report.get("conflicts", [])),
            "conflict_events": len(conflict_ids),
            "year_min": min(years) if years else 1931,
            "year_max": max(years) if years else 1945,
            "by_year": dict(sorted(by_year.items())),
            "by_type": dict(by_type.most_common()),
            "problems": len(report.get("problems", [])),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    js = "window.__MIYING__ = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n"
    args.out.write_text(js, encoding="utf-8")

    m = payload["meta"]
    print(f"已写出 {args.out}")
    print(f"事件 {m['total']} 条，有名 {m['named']}，无名 {m['unnamed']}，"
          f"冲突组 {m['conflict_groups']}，校验问题 {m['problems']}")
    print(f"年份跨度 {m['year_min']}–{m['year_max']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
