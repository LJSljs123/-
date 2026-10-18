# -*- coding: utf-8 -*-
"""核对所有引用的本地快照、哈希和引文，并执行少量代表性关键词检查。"""
from pathlib import Path
import hashlib
import json
import re
import unicodedata
from fetch_probe_archive import to_text

ARCH = Path(__file__).resolve().parent.parent / "data" / "probe_archive"

CHECKS = [
    # (文件slug, 关键词正则)：全量引文核查之外的稳定抽查项。
    ("evt_1931_zgzy_jueyi__renminwang-jueyi", r"9月22日"),
    ("evt_1931_dengtiemei_ziweijun__junwang-dengtiemei", r"10月下旬"),
    ("evt_1932_jilin_ziweijun__tuanjiebao-lidu", r"1月31日|自卫军总司令部"),
    ("evt_1933_zhuhe_youjidui__renmin-dangshi-zhaoshangzhi", r"1933\s*年\s*10\s*月"),
    ("evt_1934_tongzhangrong_xisheng__guofangbu-tongzhangrong", r"1934年3月21日"),
    ("evt_1937_bingtangzi__beian-gov-bingtangzi", r"小兴安岭的一个重要通道"),
    ("evt_1938_banv_toujiang__xinhuanet-banv", r"1938年10月"),
]

ROOT = ARCH.parent.parent
EVENTS = ROOT / "data" / "curated" / "events.json"
MANIFEST = ARCH / "manifest.json"


def normalized(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    return "".join(c for c in text if not c.isspace() and not unicodedata.category(c).startswith("P"))


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    raw = json.loads(EVENTS.read_text(encoding="utf-8"))
    events = raw.get("events", []) if isinstance(raw, dict) else raw
    errors = []
    checked = 0

    for event in events:
        for index, source in enumerate(event.get("sources") or []):
            archive = source.get("archive")
            if not archive:
                continue
            if not isinstance(archive, str) or not archive.endswith(".html"):
                errors.append(f"{event['id']} source[{index}]: archive 必须指向本地 HTML 快照")
                continue

            html = (ROOT / archive).resolve()
            archive_root = ARCH.resolve()
            if html == archive_root or archive_root not in html.parents:
                errors.append(f"{event['id']} source[{index}]: archive path escapes the local snapshot directory")
                continue
            slug = html.stem
            text_path = ARCH / f"{slug}.txt"
            record = manifest.get(slug)
            if not html.is_file() or not text_path.is_file() or not record:
                errors.append(f"{event['id']} source[{index}]: 本地快照、文本或 manifest 记录缺失（{slug}）")
                continue

            if record.get("event") != event["id"] or (
                source.get("url") and record.get("url") != source["url"]
            ):
                errors.append(f"{slug}: event 或 URL 与 manifest 不符")
                continue

            content = html.read_bytes()
            digest = hashlib.sha256(content).hexdigest()
            if digest != record.get("sha256") or len(content) != record.get("bytes"):
                errors.append(f"{slug}: SHA256 或字节数与 manifest 不符")
                continue

            body = text_path.read_text(encoding="utf-8").strip()
            derived = to_text(content).strip()
            if record.get("capture_status") != "readable_snapshot" or len(body) < 100:
                errors.append(f"{slug}: 存档正文不可读或未标记为可用快照")
                continue
            if body != derived:
                errors.append(f"{slug}: extracted text does not match the hashed HTML snapshot")
                continue

            haystack = normalized(derived)
            quote = source.get("quote") or ""
            segments = [normalized(part) for part in re.split(r"(?:…+|\.{2,}|．{2,})", quote)]
            segments = [part for part in segments if len(part) >= 12]
            if not segments or not all(part in haystack for part in segments):
                errors.append(f"{event['id']} source[{index}]: 引文片段未在本地文本中命中（{slug}）")
                continue
            checked += 1

    print(f"引文存档核查：{checked} 条通过，{len(errors)} 条失败")
    for error in errors:
        print(f"[FAIL] {error}")

    spot_failures = 0
    for slug, pattern in CHECKS:
        path = ARCH / f"{slug}.txt"
        if not path.is_file():
            print(f"[缺] {slug}")
            spot_failures += 1
            continue
        text = unicodedata.normalize("NFKC", path.read_text(encoding="utf-8"))
        found = re.search(pattern, text)
        print(f"[{'OK ' if found else 'NO '}] {slug}")
        if not found:
            spot_failures += 1

    print(f"代表性关键词核查：{len(CHECKS) - spot_failures}/{len(CHECKS)} 通过")
    return 1 if errors or spot_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
