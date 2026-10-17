# -*- coding: utf-8 -*-
"""在 probe_archive 文本中核对候选引文，打印命中上下文。"""
from pathlib import Path
import re, sys

ARCH = Path(__file__).resolve().parent.parent / "data" / "probe_archive"

CHECKS = [
    # (文件slug, 关键词正则)
    ("evt_1931_zgzy_jueyi__renminwang-jueyi", r"9月22日"),
    ("evt_1931_dengtiemei_ziweijun__junwang-dengtiemei", r"10月下旬"),
    ("evt_1932_jilin_ziweijun__tuanjiebao-lidu", r"1月31日|自卫军总司令部"),
    ("evt_1932_jilin_ziweijun__krzzjn-lidu", r"1月31日"),
    ("evt_1932_haerbin_shishou__tuanjiebao-haerbin", r"2月5日|哈尔滨(沦陷|失守)"),
    ("evt_1932_weiman_chengli__renmin-dangshi-weiman", r"3月1日|建国宣言|伪满洲国"),
    ("evt_1932_qiangfeng_fujji__tuanjiewang-qiangfeng", r"3月13日"),
    ("evt_1932_panshi_yiyongjun__jl-difangzhi-panshi", r"1932年5月|磐石工农反日义勇军"),
    ("evt_1932_bayan_youjidui__guofangbu-zhangjiazhou", r"巴彦|张甲洲"),
    ("evt_1932_bayan_youjidui__gzdis-zhangjiazhou", r"5月16日"),
    ("evt_1932_pingdingshan__pds1932-jinianguan", r"9月16日"),
    ("evt_1932_yangjingyu_panshi__baijiahao-panshi", r"11月"),
    ("evt_1932_yangjingyu_panshi__jl-difangzhi-hongsanjun", r"第三十二军|三十二军"),
    ("evt_1933_126_zhishixin__guofangbu-126zhishixin", r"1月26日"),
    ("evt_1933_yitianuzhu__krzzjn-yitian-beibei", r"伊田助男|三月三十"),
    ("evt_1933_dyj_dulishi__baijiahao-dulishi", r"9月18日"),
    ("evt_1933_zhuhe_youjidui__renmin-dangshi-zhaoshangzhi", r"1933年10月"),
    ("evt_1933_zhuhe_youjidui__hljshs-hlf-lin", r"10月10日"),
    ("evt_1934_tulongshan__junwang-tulongshan", r"3月8日|暴动"),
    ("evt_1934_tongzhangrong_xisheng__guofangbu-tongzhangrong", r"3月21日"),
    ("evt_1935_lihongguang_xisheng__jl-jianwei-lihongguang", r"1935年5月"),
    ("evt_1935_lihongguang_xisheng__yangjingyu-lievelingyuan-lihongguang", r"牺牲|5月"),
    ("evt_1935_dierjun_chengli__guotu-nlc-wangdetai", r"5月30日"),
    ("evt_1935_zhao_yiman__mva-zhaoyiman", r"1935年11月"),
    ("evt_1935_zhao_yiman__gongchandangwang-zhaoyiman", r"8月2日"),
    ("evt_1936_yijun_xizheng__junwang-liminhuan", r"7月15日|西征"),
    ("evt_1936_xiayunjie_xisheng__guofangbu-xiayunjie", r"11月21日"),
    ("evt_1936_wangdetai_xisheng__guotu-nlc-wangdetai2", r"11月7日"),
    ("evt_1936_wangdetai_xisheng__junwang-wangdetai", r"壮烈殉国|中弹"),
    ("evt_1937_songtieyan_xisheng__junwang-songtieyan", r"1937年|牺牲"),
    ("evt_1937_bingtangzi__beian-gov-bingtangzi", r"冰趟子"),
    ("evt_1937_bingtangzi__baijiahao-bingtangzi", r"3月7日|二百余"),
    ("evt_1938_shier_lieshi__baijiahao-shierlieshi", r"3月18日"),
    ("evt_1938_shier_lieshi__zzut-lilhaifeng", r"3月18日"),
    ("evt_1938_chengbin_toudi__baijiahao-chengbin", r"1938年6月29日|7月|115人"),
    ("evt_1938_banv_toujiang__cctv-banvtoujiang", r"1938年10月|乌斯浑河"),
]

for slug, pat in CHECKS:
    p = ARCH / f"{slug}.txt"
    if not p.exists():
        print(f"[缺] {slug}")
        continue
    t = p.read_text(encoding="utf-8").replace("\n", "")
    ms = list(re.finditer(pat, t))
    print(f"[{'OK ' if ms else 'NO '}] {slug} ({len(t)}字)")
    for m in ms[:2]:
        s = max(0, m.start() - 30)
        print(f"      …{t[s:m.end()+60]}…")
