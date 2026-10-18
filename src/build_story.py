"""把被服厂主张集转成前端可加载的 story.js，并校验引文可对照。

用法：
    python src/build_story.py

检查：
- 每条 claim 的 quote 必须能在存档原文中逐字定位（去空白后比对）
- 章节号连续、claim id 唯一
- 任一条不通过则非零退出，不写产物
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "curated" / "story_claims.json"
ARCH = ROOT / "data" / "probe_archive" / "story_beifuchang__wlt-hlj.html"
OUT = ROOT / "web" / "story.js"


def plain_text(html: str) -> str:
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = re.sub(r"&[^;]{1,8};", " ", t)
    return t


def norm(s: str) -> str:
    return re.sub(r"\s+", "", str(s or ""))


def main() -> int:
    if not SRC.exists():
        print(f"缺少主张集：{SRC}")
        return 2
    story = json.loads(SRC.read_text(encoding="utf-8"))
    chapters = story.get("chapters") or []

    problems: list[str] = []
    seen_ids: set[str] = set()
    for i, ch in enumerate(chapters, start=1):
        if ch.get("no") != i:
            problems.append(f"章节号不连续：第 {i} 个章节 no={ch.get('no')}")
        for c in ch.get("claims") or []:
            cid = c.get("id") or ""
            if not cid:
                problems.append(f"第 {i} 章有 claim 缺 id")
            elif cid in seen_ids:
                problems.append(f"claim id 重复：{cid}")
            seen_ids.add(cid)
            if not (c.get("quote") or "").strip():
                problems.append(f"{cid} 缺 quote")

    # 引文可对照：必须能在存档原文里逐字找到
    if ARCH.exists():
        tnorm = norm(plain_text(ARCH.read_bytes().decode("utf-8", errors="replace")))
        for ch in chapters:
            for c in ch.get("claims") or []:
                q = norm(c.get("quote"))
                if q and q not in tnorm:
                    problems.append(f"{c.get('id')} 的引文无法在存档原文中定位：{c['quote'][:36]}…")
    else:
        problems.append(f"缺少存档原文：{ARCH}（引文无法校验）")

    if problems:
        print(f"校验未通过（{len(problems)} 项）：")
        for p in problems:
            print("  !", p)
        return 1

    claims = sum(len(ch.get("claims") or []) for ch in chapters)
    payload = {
        "_note": "由 src/build_story.py 从 story_claims.json 生成，勿手工编辑。",
        "source": story.get("source"),
        "chapters": chapters,
        "stats": {"chapters": len(chapters), "claims": claims},
    }
    OUT.write_text(
        "window.__MIYING_STORY__ = "
        + json.dumps(payload, ensure_ascii=False, indent=1)
        + ";\n",
        encoding="utf-8",
    )
    print(f"{len(chapters)} 章 / {claims} 条主张，引文全部可对照 → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
