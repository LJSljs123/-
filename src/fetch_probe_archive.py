# -*- coding: utf-8 -*-
"""probe_archive: 抓取来源原始页面并归档（HTML + 纯文本 + manifest）。

每条事件选定 1-2 个权威来源页，curl 下载后：
  - <event_id>__<slug>.html   原始 HTML（所见即所存）
  - <event_id>__<slug>.txt    去标签纯文本（供引文核对）
  - manifest.json             url / 抓取时间 / sha256 / 页面标题

可重跑：同名文件覆盖，manifest 重建。哈希可证明存档自抓取时刻未被改动。
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCH = ROOT / "data" / "probe_archive"

# (event_id, slug, url)
TARGETS = [
    ("evt_1931_zgzy_jueyi",      "renminwang-jueyi",        "http://military.people.com.cn/n1/2016/0918/c1011-28721822-8.html"),
    ("evt_1931_dengtiemei_ziweijun", "junwang-dengtiemei",  "https://www.81.cn/yljnt_208627/ylml/D/9385721.html"),
    ("evt_1932_jilin_ziweijun",  "tuanjiebao-lidu",         "https://www.tuanjiebao.com/m/2020-11/26/content_8896400.htm"),
    ("evt_1932_jilin_ziweijun",  "krzzjn-lidu",             "https://www.krzzjn.com/show-90-53815.html"),
    ("evt_1932_haerbin_shishou", "tuanjiebao-haerbin",      "https://www.tuanjiebao.com/m/2020-11/26/content_8896400.htm"),
    ("evt_1932_weiman_chengli",  "renmin-dangshi-weiman",   "https://dangshi.people.com.cn/n/2015/0526/c396421-27056835-2.html"),
    ("evt_1932_qiangfeng_fujji", "tuanjiewang-qiangfeng",   "https://www.tuanjiewang.cn/2022-02/10/content_8926224.htm"),
    ("evt_1932_panshi_yiyongjun","jl-difangzhi-panshi",     "https://dfz.jl.gov.cn/dbkl/201701/t20170106_5217616.html"),
    ("evt_1932_bayan_youjidui",  "guofangbu-zhangjiazhou",  "http://www.mod.gov.cn/gfbw/gfdy/16492977.html"),
    ("evt_1932_bayan_youjidui",  "gzdis-zhangjiazhou",      "http://www.gzdis.gov.cn/xwhc/yw/202503/t20250314_87166276.html"),
    ("evt_1932_pingdingshan",    "pds1932-jinianguan",      "http://m.pds1932.cn/index.php?c=category&id=51"),
    ("evt_1932_yangjingyu_panshi","baijiahao-panshi",       "https://baijiahao.baidu.com/s?id=1839761200792313442&wfr=spider&for=pc"),
    ("evt_1932_yangjingyu_panshi","jl-difangzhi-hongsanjun","https://dfz.jl.gov.cn/dbkl/201701/t20170106_5217616.html"),
    ("evt_1933_126_zhishixin",   "guofangbu-126zhishixin",  "http://www.mod.gov.cn/gfbw/gfjy_index/js_214151/16439864.html"),
    ("evt_1933_yitianuzhu",      "baike-yitianuzhu",        "https://baike.baidu.com/item/%E4%BC%8A%E7%94%B0%E5%8A%A9%E7%94%B7/8259999"),
    ("evt_1933_yitianuzhu",      "krzzjn-yitian-beibei",    "https://www.krzzjn.com/show-1032-72174.html"),
    ("evt_1933_dyj_dulishi",     "baijiahao-dulishi",       "https://baijiahao.baidu.com/s?id=1875927257337062045&wfr=spider&for=pc"),
    ("evt_1933_zhuhe_youjidui",  "renmin-dangshi-zhaoshangzhi","http://dangshi.people.com.cn/n/2014/0325/c85037-24731596.html"),
    ("evt_1933_zhuhe_youjidui",  "hljshs-hlf-lin",          "https://www.hljshswhyjh.com/nd.jsp?id=98"),
    ("evt_1934_tulongshan",      "junwang-tulongshan",      "https://www.81.cn/yl_208589/16391832.html"),
    ("evt_1934_tongzhangrong_xisheng","guofangbu-tongzhangrong","http://www.mod.gov.cn/gfbw/gfjy_index/js_214151/16405189.html"),
    ("evt_1935_lihongguang_xisheng","jl-jianwei-lihongguang","https://ccdijl.gov.cn/ztjc/ljwh/by/202506/t20250617_9257799.html"),
    ("evt_1935_lihongguang_xisheng","yangjingyu-lievelingyuan-lihongguang","https://yjylsly.org.cn/news/154.html"),
    ("evt_1935_dierjun_chengli", "guotu-nlc-wangdetai",      "http://memory.nlc.cn/topic/resource/205"),
    ("evt_1935_dierjun_chengli", "sx-dj-wangdetai",          "https://www.sx-dj.gov.cn/dylt/dscq/2067067527396417537.html"),
    ("evt_1935_zhao_yiman",      "mva-zhaoyiman",            "https://www.mva.gov.cn/sy/zt/jnkzsl80zn/shzb/202508/t20250829_509832.html"),
    ("evt_1935_zhao_yiman",      "gongchandangwang-zhaoyiman","https://www.12371.cn/2021/04/20/VIDE1618874520618438.shtml"),
    ("evt_1936_yijun_xizheng",   "junwang-liminhuan",        "https://www.81.cn/2021zt/2021-08/31/content_10090467.htm"),
    ("evt_1936_xiayunjie_xisheng","guofangbu-xiayunjie",      "http://www.mod.gov.cn/gfbw/zt/gfbwzt/2018_213791/mhyxlsp/4826713.html"),
    ("evt_1936_wangdetai_xisheng","guotu-nlc-wangdetai2",     "http://memory.nlc.cn/topic/resource/205"),
    ("evt_1936_wangdetai_xisheng","junwang-wangdetai",        "https://www.81.cn/yl/2021-09/28/content_10094025.htm"),
    ("evt_1937_songtieyan_xisheng","junwang-songtieyan",      "https://www.81.cn/yl_208589/16391184.html"),
    ("evt_1937_bingtangzi",      "beian-gov-bingtangzi",     "https://www.hljba.gov.cn/bas/bmdt/202508/c11_337253.shtml"),
    ("evt_1937_bingtangzi",      "baijiahao-bingtangzi",     "https://baijiahao.baidu.com/s?id=1874365408727694942&wfr=spider&for=pc"),
    ("evt_1938_shier_lieshi",    "baijiahao-shierlieshi",    "https://baijiahao.baidu.com/s?id=1875903637732736837&wfr=spider&for=pc"),
    ("evt_1938_shier_lieshi",    "zzut-lilhaifeng",          "https://gzc.zzut.edu.cn/info/1157/1607.htm"),
    ("evt_1938_chengbin_toudi",  "baike-chengbin",           "https://baike.baidu.com/item/%E7%A8%8B%E6%96%8C/7206798"),
    ("evt_1938_chengbin_toudi",  "baijiahao-chengbin",       "https://baijiahao.baidu.com/s?id=1872695328133062993&wfr=spider&for=pc"),
    ("evt_1938_banv_toujiang",   "cctv-banvtoujiang",        "https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=16609844486641375624"),
    ("evt_1938_banv_toujiang",   "baike-lengyun",            "https://baike.baidu.com/item/%E5%86%B7%E4%BA%91/1706195"),
]


def fetch(url: str) -> bytes:
    r = subprocess.run(
        ["curl.exe", "-sS", "-L", "-m", "60", "-A",
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
         url],
        capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(r.stderr.decode("utf-8", "replace")[:120])
    return r.stdout


TAG = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
TAG2 = re.compile(r"<[^>]+>")


def to_text(b: bytes) -> str:
    for enc in ("utf-8", "gb18030"):
        try:
            raw = b.decode(enc)
            if "charset" in raw[:2000].lower() and enc == "utf-8":
                m = re.search(r'charset=["\']?([\w-]+)', raw[:2000], re.I)
                if m and m.group(1).lower() in ("gbk", "gb2312", "gb18030"):
                    raw = b.decode("gb18030", "replace")
            break
        except UnicodeDecodeError:
            raw = b.decode("gb18030", "replace")
    t = TAG.sub(" ", raw)
    t = TAG2.sub("\n", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
          .replace("&#160;", " ").replace("&ldquo;", "\u201c").replace("&rdquo;", "\u201d"))
    lines = [re.sub(r"[ \t\u3000]+", " ", l).strip() for l in t.split("\n")]
    return "\n".join(l for l in lines if l)


def title_of(text: str) -> str:
    m = re.search(r"(.{4,60})", text[:3000].split("\n", 1)[0] if text else "")
    return (m.group(1).strip() if m else "")[:60]


def main() -> int:
    ARCH.mkdir(parents=True, exist_ok=True)
    manifest = {}
    ok = fail = 0
    for eid, slug, url in TARGETS:
        fname = f"{eid}__{slug}"
        try:
            b = fetch(url)
            if len(b) < 800:
                raise RuntimeError(f"too small: {len(b)}B")
            text = to_text(b)
            if len(text.strip()) < 100:
                raise RuntimeError(f"page body is not readable: {len(text.strip())} chars")
            html_p = ARCH / f"{fname}.html"
            html_p.write_bytes(b)
            (ARCH / f"{fname}.txt").write_text(text, encoding="utf-8")
            manifest[fname] = {
                "event": eid, "url": url,
                "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
                "sha256": hashlib.sha256(b).hexdigest(),
                "bytes": len(b),
                "title": title_of(text),
                "capture_status": "readable_snapshot",
            }
            ok += 1
            print(f"OK  {fname}  {len(b)}B")
        except Exception as e:
            fail += 1
            print(f"FAIL {fname}: {e}")
    (ARCH / "manifest.json").write_text(
        json.dumps({"_note": "仅 capture_status=readable_snapshot 的记录视为可用快照；其他记录保留失败元数据。", **manifest},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{ok} ok / {fail} fail -> {ARCH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
