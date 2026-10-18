"""把检索对位结果合并进事件库。

用法：
    python src/merge_provenance.py

输入：
    data/curated/events.json      事件库
    data/curated/provenance.json  人工检索后录入的对位记录

做的事：
    1. add_sources   —— 把检索到的来源记录补进 sources（按 book 去重）
    2. date_variants —— 记录每个来源各自主张的日期（一致也记，用于来源间对照）
    3. provenance    —— 写入检索记录（负证据）
    4. 没有对位记录的条目，写入 depth=none，如实标注"尚未逐条检索"

为什么要单独一步：检索结果属于数据，不该硬编码在代码里。脚本可重跑，
provenance.json 可复核，事件库可回滚。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / "data" / "curated" / "events.json"
PROV = ROOT / "data" / "curated" / "provenance.json"


def load(p: Path) -> dict:
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    db = load(EVENTS)
    patches = load(PROV)["patches"]
    events = db["events"]
    by_id = {e["id"]: e for e in events}

    missing = [k for k in patches if k not in by_id]
    if missing:
        print(f"provenance.json 里有 {len(missing)} 条对不上事件 id：")
        for m in missing:
            print("  ", m)
        return 1

    added_src = 0
    added_var = 0
    for eid, patch in patches.items():
        ev = by_id[eid]

        # 1) 补来源，按 book 去重（同一本书不因检索两次而入两遍）
        have = {s.get("book") for s in ev.get("sources", [])}
        for s in patch.get("add_sources", []):
            if s["book"] in have:
                continue
            ev.setdefault("sources", []).append(s)
            have.add(s["book"])
            added_src += 1

        # 2) 日期主张（来源级）
        if patch.get("date_variants"):
            ev["date_variants"] = patch["date_variants"]
            added_var += 1

        # 3) 检索记录
        if patch.get("provenance"):
            ev["provenance"] = patch["provenance"]

    # 4) 未对位的条目如实标注
    untouched = 0
    for ev in events:
        if "provenance" not in ev:
            ev["provenance"] = {
                "depth": "none",
                "on": "2026-10-17",
                "probes": [],
                "not_searched": ["本条尚未逐条检索 —— 不冒充已检索"],
            }
            untouched += 1

    with EVENTS.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    total_src = sum(len(e.get("sources", [])) for e in events)
    multi = sum(1 for e in events if len(e.get("sources", [])) > 1)
    # 统计的是最终分布，不是本次新增量——否则重跑一次就显示「未查 0 条」，
    # 把没查过的说成查过了。
    deep = sum(1 for e in events if e["provenance"]["depth"] == "deep")
    shallow = sum(1 for e in events if e["provenance"]["depth"] == "shallow")
    none_ = sum(1 for e in events if e["provenance"]["depth"] == "none")

    print(f"合并完成：{len(events)} 条事件")
    print(f"  新增来源 {added_src} 条，来源总数 {total_src}")
    print(f"  多源结论 {multi} 条（原 2 条）")
    print(f"  日期主张 {added_var} 条事件")
    print(f"  检索深度：deep {deep} / shallow {shallow} / none {none_}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
