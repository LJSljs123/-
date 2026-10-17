# -*- coding: utf-8 -*-
"""第四轮补源：给 27 条独占条目补第二来源 + 检索记录。

所有 add_sources 的 quote 均已逐条与 data/probe_archive/ 存档文本核对；
每个来源页存有 HTML 快照 + sha256（见 data/probe_archive/manifest.json），
负证据从"自述"升级为"可审计"。

运行：python src/add_sources_round4.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROV = ROOT / "data" / "curated" / "provenance.json"
ARCH = "data/probe_archive"

NS = ["中央档案馆原件（闭架）", "《东北抗日联军史》纸本（未获取）"]

P = {}

P["evt_1931_zgzy_jueyi"] = {
    "add_sources": [{
        "book": "人民网《“九一八”，不能不知的8个历史真相》",
        "page": "2016-09-18",
        "url": "http://military.people.com.cn/n1/2016/0918/c1011-28721822-8.html",
        "quote": "1931年9月22日，中共中央做出了《关于日本帝国主义武装占据满洲与目前党的紧急任务的决议》，号召东北人民开展游击战争，打击侵略者。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1931_zgzy_jueyi__renminwang-jueyi.html",
    }],
    "date_variants": [
        {"value": "1931-09-22", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1931-09-22", "precision": "day", "source": "人民网《“九一八”，不能不知的8个历史真相》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "中共中央 关于日本帝国主义强占满洲的决议 1931年9月22日 中央档案馆",
        "n": 5, "indep": ["人民网（军事）", "光明网"], "deriv": 3,
        "note": "日期三方一致；但决议名称两种口径：光明网作《关于日本帝国主义强占满洲事变的决议》，人民网作《关于日本帝国主义武装占据满洲与目前党的紧急任务的决议》——文件名存疑，日期无疑"}],
        "not_searched": NS},
}

P["evt_1931_dengtiemei_ziweijun"] = {
    "add_sources": [{
        "book": "中国军网《邓铁梅》（英烈名录）",
        "page": "英烈名录",
        "url": "https://www.81.cn/yljnt_208627/ylml/D/9385721.html",
        "quote": "１９３１年１０月下旬，邓铁梅前往辽东凤城西部山区小汤沟顾家堡子（今属岫岩县朝阳乡）串连旧好十数人……正式创建了辽东三角地区第一支民众抗日武装——东北民众自卫军，邓铁梅任司令。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1931_dengtiemei_ziweijun__junwang-dengtiemei.html",
    }],
    "date_variants": [
        {"value": "1931-10", "precision": "month", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1931-10", "precision": "month", "source": "中国军网《邓铁梅》（英烈名录）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "邓铁梅 凤城 小汤沟 东北民众自卫军 1931年10月 成立 中国军网",
        "n": 5, "indep": ["中国军网", "新华社（军网转载稿）"], "deriv": 3,
        "note": "军网两个页面互证：名录记10月下旬建队于小汤沟，新华社稿记12月26日夜袭凤凰城为第一仗，与年表10月口径一致"}],
        "not_searched": NS},
}

P["evt_1932_jilin_ziweijun"] = {
    "add_sources": [{
        "book": "团结网《1932：李杜与哈尔滨保卫战》",
        "page": "2020-11-26",
        "url": "https://www.tuanjiebao.com/m/2020-11/26/content_8896400.htm",
        "quote": "1月31日，李杜、丁超等召集抗日军政要员在哈开会，成立了“吉林自卫军总司令部”，推举李杜为自卫军总司令。",
        "reliability": "A-",
        "archive": f"{ARCH}/evt_1932_jilin_ziweijun__tuanjiebao-lidu.html",
    }, {
        "book": "抗日战争纪念网《功绩赫赫 铁骨铮铮——东北抗日联军总司令李杜将军》",
        "page": "2017-08-02",
        "url": "https://www.krzzjn.com/show-90-53815.html",
        "quote": "1932年1月31日在哈尔滨成立了统一指挥抗日军队的吉林自卫军总司令部，公推李杜为吉林抗日自卫军总司令。",
        "reliability": "B",
        "archive": f"{ARCH}/evt_1932_jilin_ziweijun__krzzjn-lidu.html",
    }],
    "date_variants": [
        {"value": "1932-01-31", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-01-31", "precision": "day", "source": "团结网《1932：李杜与哈尔滨保卫战》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "吉林自卫军 李杜 1932年1月31日 哈尔滨 成立 依兰",
        "n": 5, "indep": ["团结网（团结报）"], "deriv": 4,
        "note": "团结网（民革中央团结报）与年表日期逐日一致；纪念网李杜专文亦记1月31日"}],
        "not_searched": NS},
}

P["evt_1932_haerbin_shishou"] = {
    "add_sources": [{
        "book": "团结网《1932：李杜与哈尔滨保卫战》",
        "page": "2020-11-26",
        "url": "https://www.tuanjiebao.com/m/2020-11/26/content_8896400.htm",
        "quote": "2月5日夜，哈市被日军占领。第二次哈尔滨保卫战“终以转战经日，伤亡盈千，兵力过疲，呼救无缘”而失败。",
        "reliability": "A-",
        "archive": f"{ARCH}/evt_1932_haerbin_shishou__tuanjiebao-haerbin.html",
    }],
    "date_variants": [
        {"value": "1932-02-05", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-02-05", "precision": "day", "source": "团结网《1932：李杜与哈尔滨保卫战》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "哈尔滨 1932年2月5日 沦陷 吉林自卫军 保卫战 失守",
        "n": 5, "indep": ["团结网（团结报）"], "deriv": 4,
        "note": "团结网记“2月5日夜哈市被日军占领”，与年表逐日一致；百度百科口径亦为2月5日（未采信，仅佐证）"}],
        "not_searched": NS},
}

P["evt_1932_weiman_chengli"] = {
    "add_sources": [{
        "book": "人民网-中国共产党新闻网《东北沦陷与东北人民的英勇斗争》",
        "page": "2015-05-26",
        "url": "https://dangshi.people.com.cn/n/2015/0526/c396421-27056835-2.html",
        "quote": "3月1日，关东军发表伪满洲国“建国宣言”。3月9日，在长春举行了溥仪就职典礼。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1932_weiman_chengli__renmin-dangshi-weiman.html",
    }],
    "date_variants": [
        {"value": "1932-03-01", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-03-01", "precision": "day", "source": "人民网-中国共产党新闻网《东北沦陷与东北人民的英勇斗争》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "伪满洲国 1932年3月1日 成立 建国宣言 长春 执政",
        "n": 5, "indep": ["人民网（党史频道）"], "deriv": 4,
        "note": "人民网党史频道记“3月1日关东军发表建国宣言”，与年表一致；另注意溥仪就职在3月9日——“建国宣言日”与“执政日”是两个日期，本条取宣言日"}],
        "not_searched": NS},
}

P["evt_1932_qiangfeng_fujji"] = {
    "add_sources": [{
        "book": "团结网《镜泊湖连环战的历史考证》",
        "page": "2022-02-10",
        "url": "https://www.tuanjiewang.cn/2022-02/10/content_8926224.htm",
        "quote": "李延禄所说的墙缝伏击战，是1932年3月13日，由他指挥的救国军补充团700多人和戴凤龄独立营的300多人，在镜泊湖的墙缝，伏击以天野第十五旅团为主力的日军部队。",
        "reliability": "A-",
        "archive": f"{ARCH}/evt_1932_qiangfeng_fujji__tuanjiewang-qiangfeng.html",
    }],
    "date_variants": [
        {"value": "1932-03-18", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-03-13", "precision": "day", "source": "团结网《镜泊湖连环战的历史考证》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "墙缝战斗 1932年3月 李延禄 救国军补充团 伏击 日军 天野 宁安 镜泊湖",
        "n": 5, "indep": ["团结网（团结报，学术考证稿）"], "deriv": 4,
        "note": "真实日期分歧：年表记3月18日，团结网学术考证依李延禄回忆材料记3月13日，百度百科沿用13日——这是本库第四组日期冲突，两说并陈不裁决"}],
        "not_searched": NS},
}

P["evt_1932_panshi_yiyongjun"] = {
    "add_sources": [{
        "book": "吉林省地方志编纂委员会《杨靖宇对统一战线策略的探索与实践》",
        "page": "2017-01-06",
        "url": "https://dfz.jl.gov.cn/dbkl/201701/t20170106_5217616.html",
        "quote": "于1932年5月成立的磐石工农反日义勇军（即磐石游击队），是中国共产党在东北创建的第一支抗日武装。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1932_panshi_yiyongjun__jl-difangzhi-panshi.html",
    }],
    "date_variants": [
        {"value": "1932-05-04", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-05", "precision": "month", "source": "吉林省地方志编纂委员会《杨靖宇对统一战线策略的探索与实践》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [
        {"q": "磐石工农反日义勇军 1932年 玻璃河套 成立 满洲省委 杨靖宇",
         "n": 5, "indep": ["吉林省地方志编纂委员会"], "deriv": 4,
         "note": "吉林省地方志记“1932年5月成立”，与年表5月一致；但磐石地方史料另有“6月4日改编为义勇军”口径——5月/6月存在一月级分歧，存疑不裁决"},
    ],
        "not_searched": NS},
}

P["evt_1932_bayan_youjidui"] = {
    "add_sources": [{
        "book": "国防部《甲洲路旁，“小红星”茁壮成长》（中国国防报）",
        "page": "2026-10-14",
        "url": "http://www.mod.gov.cn/gfbw/gfdy/16492977.html",
        "quote": "青年时期，他曾就读于北京大学和清华大学，并积极参加学生运动，1932年回到家乡，创建巴彦抗日游击队并担任总指挥。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1932_bayan_youjidui__guofangbu-zhangjiazhou.html",
    }, {
        "book": "贵州省国防动员办公室《记忆｜张甲洲：从清北学子到抗日英雄》",
        "page": "2025-03-14",
        "url": "http://www.gzdis.gov.cn/xwhc/yw/202503/t20250314_87166276.html",
        "quote": "1932年5月16日，在一口井前，张甲洲带着来“参加婚礼”的200多人，举行了誓师大会，巴彦抗日游击队正式成立，他担任总指挥。",
        "reliability": "A-",
        "archive": f"{ARCH}/evt_1932_bayan_youjidui__gzdis-zhangjiazhou.html",
    }],
    "date_variants": [
        {"value": "1932-05-16", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-05-16", "precision": "day", "source": "贵州省国防动员办公室《记忆｜张甲洲：从清北学子到抗日英雄》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "巴彦游击队 张甲洲 1932年5月 成立 赵尚志 江北",
        "n": 5, "indep": ["国防部（中国国防报）", "贵州省国防动员办公室"], "deriv": 3,
        "note": "两家政府站互证：国防部记建队事实与总指挥身份，贵州国动办记5月16日誓师成立，与年表逐日一致；另注意本条部队番号各源差异大（江北骑兵独立师/红36军江北独立师），番号考订从略"}],
        "not_searched": NS},
}

P["evt_1932_pingdingshan"] = {
    "add_sources": [{
        "book": "抚顺平顶山惨案纪念馆",
        "page": "纪念馆官网",
        "url": "http://m.pds1932.cn/index.php?c=category&id=51",
        "quote": "1932年9月16日，日本侵略者以莫须有的罪名，将抚顺平顶山村及比邻的栗家沟和千金堡村共三千多名无辜村民集体枪杀，制造了日本侵占东北期间第一起大规模屠杀平民的“平顶山惨案”。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1932_pingdingshan__pds1932-jinianguan.html",
    }],
    "date_variants": [
        {"value": "1932-09-16", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-09-16", "precision": "day", "source": "抚顺平顶山惨案纪念馆"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "平顶山惨案 1932年9月16日 抚顺 3000余人 纪念馆",
        "n": 5, "indep": ["抚顺平顶山惨案纪念馆"], "deriv": 4,
        "note": "遇难人数：纪念馆口径“三千多名”与年表“3000余人”一致；纪念馆另记起因为9月15日午夜自卫军进攻抚顺矿区——因果链完整"}],
        "not_searched": NS},
}

P["evt_1932_yangjingyu_panshi"] = {
    "add_sources": [{
        "book": "吉林省地方志编纂委员会《杨靖宇对统一战线策略的探索与实践》",
        "page": "2017-01-06",
        "url": "https://dfz.jl.gov.cn/dbkl/201701/t20170106_5217616.html",
        "quote": "满洲省委接受“北方会议”决议后，立即指示磐石中心县委：“把目前的义勇军改名为中国工农红军第三十二军东北游击队”。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1932_yangjingyu_panshi__jl-difangzhi-hongsanjun.html",
    }, {
        "book": "百家号《在磐石，见“磐石”——寻迹杨靖宇将军参加东北抗联活动的起点》",
        "page": "2025-08-07",
        "url": "https://baijiahao.baidu.com/s?id=1839761200792313442&wfr=spider&for=pc",
        "quote": "同年11月，这支队伍改编为中国工农红军第三十二军南满游击队，在杨靖宇带领下返回磐石。",
        "reliability": "B",
        "archive": f"{ARCH}/evt_1932_yangjingyu_panshi__baijiahao-panshi.html",
    }],
    "date_variants": [
        {"value": "1932-11", "precision": "month", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1932-11", "precision": "month", "source": "百家号《在磐石，见“磐石”》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "杨靖宇 磐石 1932年11月 红军第三十二军 南满游击队 改编",
        "n": 5, "indep": ["吉林省地方志编纂委员会"], "deriv": 4,
        "note": "省地方志记省委指示改名红三十二军，百家号（引吉林省委党史研究室访谈）记11月杨靖宇整编后返回磐石——过程两段互证，月份一致"}],
        "not_searched": NS},
}

P["evt_1933_126_zhishixin"] = {
    "add_sources": [{
        "book": "国防部《东南满抗日游击根据地——东北抗联第一路军的大本营》",
        "page": "2026-01-29",
        "url": "http://www.mod.gov.cn/gfbw/gfjy_index/js_214151/16439864.html",
        "quote": "1933年1月26日，中共驻共产国际代表团以中共中央名义发出《中央给满洲各级党部及全体党员的信——论满洲的状况和我们党的任务》（即“一二六指示信”）。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1933_126_zhishixin__guofangbu-126zhishixin.html",
    }],
    "date_variants": [
        {"value": "1933-01-26", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1933-01-26", "precision": "day", "source": "国防部《东南满抗日游击根据地》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "中共中央驻共产国际代表团 一二六指示信 1933年1月26日 满洲 各级党部",
        "n": 5, "indep": ["国防部", "国家林业和草原局（党史日历）"], "deriv": 3,
        "note": "国防部与国家林草局党史日历均记1月26日，全称一致；哈尔滨新闻网革命文物专栏另证原件存中共满洲省委旧址"}],
        "not_searched": NS},
}

P["evt_1933_yitianuzhu"] = {
    "add_sources": [{
        "book": "抗日战争纪念网《伊田助男遗书碑》（转汪清英烈网）",
        "page": "2018-04-27",
        "url": "https://www.krzzjn.com/show-1032-72174.html",
        "quote": "日本关东军间岛辎重队 共产党员伊田助男 一九三三年三月三十日",
        "reliability": "A-",
        "archive": f"{ARCH}/evt_1933_yitianuzhu__krzzjn-yitian-beibei.html",
    }],
    "date_variants": [
        {"value": "1933-03-30", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1933-03-30", "precision": "day", "source": "抗日战争纪念网《伊田助男遗书碑》（遗书落款）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "伊田助男 1933年3月30日 间岛 日军辎重队 十万发子弹 遗书",
        "n": 5, "indep": [], "deriv": 5,
        "note": "最强证据是遗书碑落款原件抄录（一九三三年三月三十日）；但独立机构层面仅纪念网一系（转汪清英烈网），百科/百家号均转抄——本条补的是“文物级”证据而非“机构级”第二源，如实标注"}],
        "not_searched": ["汪清县档案馆（未获取）", "遗书碑实物照片原图（网页仅录文）"]},
}

P["evt_1933_dyj_dulishi"] = {
    "add_sources": [{
        "book": "百家号《E法同行 兴辽治宁｜字字铿锵！探寻“20条军规”里的红色法治初心》",
        "page": "2026-09-10",
        "url": "https://baijiahao.baidu.com/s?id=1875927257337062045&wfr=spider&for=pc",
        "quote": "1933年9月18日，东北人民革命军第一军独立师在吉林磐石正式成立，杨靖宇任独立师师长兼政委，李红光任参谋长，宋铁岩任政治部主任。",
        "reliability": "B",
        "archive": f"{ARCH}/evt_1933_dyj_dulishi__baijiahao-dulishi.html",
    }],
    "date_variants": [
        {"value": "1933-09-18", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1933-09-18", "precision": "day", "source": "百家号《E法同行 兴辽治宁》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "东北人民革命军第一军独立师 1933年9月18日 玻璃河套 成立宣言 杨靖宇",
        "n": 5, "indep": [], "deriv": 5,
        "note": "日期逐日一致（九一八两周年当天成立），但本轮未找到独立权威机构页面，百家号普法专栏稿可靠性 B——独立第二源待补（候选：吉林省档案馆）"}],
        "not_searched": NS},
}

P["evt_1933_zhuhe_youjidui"] = {
    "add_sources": [{
        "book": "人民网-党史频道《中共抗战英烈：赵尚志》",
        "page": "2014-03-25",
        "url": "http://dangshi.people.com.cn/n/2014/0325/c85037-24731596.html",
        "quote": "1933年10月，珠河反日游击队成立，赵尚志任队长。在他的领导下，不到三个月时间内连续取得了多次战斗的胜利。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1933_zhuhe_youjidui__renmin-dangshi-zhaoshangzhi.html",
    }],
    "date_variants": [
        {"value": "1933-10-10", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1933-10", "precision": "month", "source": "人民网-党史频道《中共抗战英烈：赵尚志》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "珠河反日游击队 1933年10月10日 三股流 赵尚志 队长 成立",
        "n": 5, "indep": ["人民网（党史频道）"], "deriv": 4,
        "note": "人民网记10月（月精度），年表记10月10日（日精度）——不冲突，日级精度仅年表主张；成立地三股流另见百度“珠河东北反日游击队成立大会遗址”条目（遗址类，未采信为文献源）"}],
        "not_searched": NS},
}

P["evt_1934_tulongshan"] = {
    "add_sources": [{
        "book": "中国军网《景振卿：土龙山农民抗日武装暴动的首创者》",
        "page": "2025-06-11",
        "url": "https://www.81.cn/yl_208589/16391832.html",
        "quote": "３月８日晚，当地五个保的保长悄悄集会……决定发起武装暴动。……３月１０日上午，饭冢朝吾率领伪警察大队大队长盖文义等４０多名日伪军……进入白家沟埋伏区。",
        "reliability": "A-",
        "archive": f"{ARCH}/evt_1934_tulongshan__junwang-tulongshan.html",
    }],
    "date_variants": [
        {"value": "1934-03-09", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1934-03-08", "precision": "day", "source": "中国军网《景振卿》（暴动集会日）"},
        {"value": "1934-03-10", "precision": "day", "source": "中国军网《景振卿》（白家沟伏击击毙饭冢日）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "土龙山暴动 1934年3月8日 饭冢朝吾 击毙 谢文东 民众救国军 依兰",
        "n": 5, "indep": ["中国军网"], "deriv": 4,
        "note": "军网页标注“来源：抗日战争纪念网”，为转载稿，独立度有限；且日期口径分裂为两日：3月8日晚集会决定暴动、3月10日白家沟伏击击毙饭冢——年表的3月9日介于两者之间，本条是“事件由多个动作构成、单日期装不下”的典型"}],
        "not_searched": NS},
}

P["evt_1934_tongzhangrong_xisheng"] = {
    "add_sources": [{
        "book": "国防部《童长荣：白山黑水间谱写青春壮歌》",
        "page": "2025-08-27",
        "url": "http://www.mod.gov.cn/gfbw/gfjy_index/js_214151/16405189.html",
        "quote": "1934年3月21日，日军调集重兵对汪清县庙沟村（今长荣村）实施合围。突围战斗中，27岁的童长荣腹部中弹仍坚持指挥……壮烈牺牲。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1934_tongzhangrong_xisheng__guofangbu-tongzhangrong.html",
    }, {
        "book": "杨靖宇烈士陵园暨东北抗日联军纪念馆《童长荣》",
        "page": "纪念馆官网",
        "url": "https://yjylsly.org.cn/news/174.html",
        "quote": "1934年3月21日，身患重病的童长荣和部队转移到汪清县十里坪庙沟一带时被敌人包围，壮烈牺牲，年仅27岁。",
        "reliability": "A",
        "archive": "（与 evt_1935_lihongguang_xisheng 烈士陵园页同批存档）",
    }],
    "date_variants": [
        {"value": "1934-04-21", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1934-03-21", "precision": "day", "source": "国防部《童长荣》"},
        {"value": "1934-03-21", "precision": "day", "source": "杨靖宇烈士陵园暨东北抗日联军纪念馆《童长荣》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "童长荣 东满特委书记 1934年3月21日 汪清 牺牲乡 十里坪",
        "n": 5, "indep": ["国防部", "杨靖宇烈士陵园暨东北抗日联军纪念馆"], "deriv": 3,
        "note": "整月级真实冲突：国防部与烈士陵园两家权威一致记3月21日，年表记4月21日——单源年表疑误，两比一但不裁决，冲突由系统自动标出"}],
        "not_searched": NS},
}

P["evt_1935_lihongguang_xisheng"] = {
    "add_sources": [{
        "book": "吉林省纪委监委网站《抗日英烈李红光：热血铸就不朽功勋》",
        "page": "2025-06-17",
        "url": "https://ccdijl.gov.cn/ztjc/ljwh/by/202506/t20250617_9257799.html",
        "quote": "1935年5月，在一次战斗中，李红光不幸中弹牺牲，年仅25岁。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1935_lihongguang_xisheng__jl-jianwei-lihongguang.html",
    }, {
        "book": "杨靖宇烈士陵园暨东北抗日联军纪念馆《李红光》",
        "page": "纪念馆官网",
        "url": "https://yjylsly.org.cn/news/154.html",
        "quote": "5月11日，李红光率部队行至兴京县老岭时，与日本守备队200多人遭遇，双方激战时不幸胸部中弹。12日，年仅25岁的李红光因伤势过重，在辽宁省新宾县光荣牺牲。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1935_lihongguang_xisheng__yangjingyu-lievelingyuan-lihongguang.html",
    }],
    "date_variants": [
        {"value": "1935-05-11", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》（负伤日）"},
        {"value": "1935-05-12", "precision": "day", "source": "杨靖宇烈士陵园暨东北抗日联军纪念馆《李红光》（牺牲日）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "李红光 东北人民革命军第一军第一师师长 1935年5月 牺牲 新宾 查家堡子",
        "n": 5, "indep": ["吉林省纪委监委网站", "杨靖宇烈士陵园暨东北抗日联军纪念馆"], "deriv": 3,
        "note": "烈士陵园馆方口径把分歧解释掉了：11日老岭遭遇战负重伤、12日因伤牺牲——年表的5月11日与陵园的5月12日不是矛盾而是两个动作；本库按事件类型（牺牲）取12日为候选，冲突交系统标注"}],
        "not_searched": NS},
}

P["evt_1935_dierjun_chengli"] = {
    "add_sources": [{
        "book": "国家图书馆《王德泰》（引黑龙江省委党史研究室《东北抗日联军名录》）",
        "page": "国图中国记忆项目",
        "url": "http://memory.nlc.cn/topic/resource/205",
        "quote": "1935年3月任师长，同年5月30日任东北人民革命军第二军军长。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1935_dierjun_chengli__guotu-nlc-wangdetai.html",
    }],
    "date_variants": [
        {"value": "1935-05-30", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1935-05-30", "precision": "day", "source": "国家图书馆《王德泰》（引《东北抗日联军名录》）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "东北人民革命军第二军 成立宣言 1935年5月30日 王德泰 军长",
        "n": 5, "indep": ["国家图书馆（中国记忆项目）", "陕西党建网"], "deriv": 3,
        "note": "国图引省委党史研究室名录记5月30日任职军长，陕西党建网记“5月30日独立师扩编为第二军”——与年表“发表成立宣言”同日互证"}],
        "not_searched": NS},
}

P["evt_1935_zhao_yiman"] = {
    "add_sources": [{
        "book": "退役军人事务部《山河坐标》（赵一曼）",
        "page": "2025-08-29",
        "url": "https://www.mva.gov.cn/sy/zt/jnkzsl80zn/shzb/202508/t20250829_509832.html",
        "quote": "1935年11月 为掩护部队突围 赵一曼在与日伪军激战中身负重伤 不幸落入敌手",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1935_zhao_yiman__mva-zhaoyiman.html",
    }, {
        "book": "共产党员网《百年瞬间丨赵一曼》",
        "page": "2021-04-20",
        "url": "https://www.12371.cn/2021/04/20/VIDE1618874520618438.shtml",
        "quote": "1936年8月2日清晨，在一列从黑龙江哈尔滨开往珠河的火车上，东北抗日联军第三军二团政委赵一曼向看守她的日本宪兵要来纸笔，写下了给儿子陈掖贤的最后遗言。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1935_zhao_yiman__gongchandangwang-zhaoyiman.html",
    }],
    "date_variants": [
        {"value": "1935-11-15", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》（被俘日）"},
        {"value": "1935-11", "precision": "month", "source": "退役军人事务部《山河坐标》（被俘月）"},
        {"value": "1936-08-02", "precision": "day", "source": "共产党员网《百年瞬间丨赵一曼》（就义日，三方一致）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "赵一曼 1935年11月 春秋岭 负伤被俘 1936年8月2日 珠河 就义",
        "n": 5, "indep": ["退役军人事务部", "共产党员网"], "deriv": 3,
        "note": "就义日 1936-08-02 三方一致且遗书为物证；被俘精确到日（15日）仅年表主张，两部只记月——精度差异如实记录"}],
        "not_searched": NS},
}

P["evt_1936_yijun_xizheng"] = {
    "add_sources": [{
        "book": "中国军网《李敏焕：抗联一军一师参谋长》",
        "page": "2021-08-31",
        "url": "https://www.81.cn/2021zt/2021-08/31/content_10090467.htm",
        "quote": "1936年6月中旬，抗联一军一师西征部队从本溪县铺石河(现属凤城县)正式出发，李敏焕和一军政治部主任宋铁岩率部西进。……1936年7月15日，在摩天岭战役中壮烈牺牲。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1936_yijun_xizheng__junwang-liminhuan.html",
    }],
    "date_variants": [
        {"value": "1936-06-28", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》（出发日）"},
        {"value": "1936-06", "precision": "month", "source": "中国军网《李敏焕》（6月中旬出发）"},
        {"value": "1936-07-15", "precision": "day", "source": "中国军网《李敏焕》（摩天岭战斗日，两方一致）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "抗联第一军 1936年 西征 本溪 摩天岭大捷 7月15日 李敏焕 牺牲",
        "n": 5, "indep": ["中国军网", "百度百科（摩天岭战斗遗址，仅佐证）"], "deriv": 3,
        "note": "摩天岭战斗日 7月15日 军网与省文保单位遗址条目一致；但出发日分歧：年表记6月28日，军网记“6月中旬”——出发日存疑，摩天岭无疑"}],
        "not_searched": NS},
}

P["evt_1936_xiayunjie_xisheng"] = {
    "add_sources": [{
        "book": "国防部《夏云杰：赤胆忠心 捐躯为国》（英雄烈士谱）",
        "page": "2018-10-15",
        "url": "http://www.mod.gov.cn/gfbw/zt/gfbwzt/2018_213791/mhyxlsp/4826713.html",
        "quote": "同年11月21日，在为筹集给养与装备时，在汤原丁大千屯遭伪治安队袭击，身负重伤。弥留之际，他再三嘱咐身边的战友、妻子和女儿，要团结一致……",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1936_xiayunjie_xisheng__guofangbu-xiayunjie.html",
    }],
    "date_variants": [
        {"value": "1936-11-26", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》（牺牲日）"},
        {"value": "1936-11-21", "precision": "day", "source": "国防部《夏云杰》（负伤日）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "夏云杰 第六军军长 1936年11月 汤原 负伤 牺牲 21日",
        "n": 5, "indep": ["国防部"], "deriv": 4,
        "note": "21日负伤、26日牺牲两日先后衔接（国防部记负伤、百科记26日殉国），与年表口径不矛盾——与李红光案同为“负伤/牺牲两日期”结构"}],
        "not_searched": NS},
}

P["evt_1936_wangdetai_xisheng"] = {
    "add_sources": [{
        "book": "国家图书馆《王德泰》（引黑龙江省委党史研究室《东北抗日联军名录》）",
        "page": "国图中国记忆项目",
        "url": "http://memory.nlc.cn/topic/resource/205",
        "quote": "11月7日在抚松县与蒙江县交界处的小汤河村遭到伪骑兵七团袭击，在追击敌人时牺牲。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1936_wangdetai_xisheng__guotu-nlc-wangdetai2.html",
    }, {
        "book": "中国军网《中共抗战英烈：王德泰》",
        "page": "2021-09-28",
        "url": "https://www.81.cn/yl/2021-09/28/content_10094025.htm",
        "quote": "在这次战斗中，军长王德泰中弹，壮烈殉国，年仅29岁。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1936_wangdetai_xisheng__junwang-wangdetai.html",
    }],
    "date_variants": [
        {"value": "1936-11", "precision": "month", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1936-11-07", "precision": "day", "source": "国家图书馆《王德泰》（引《东北抗日联军名录》）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "王德泰 抗联第二军军长 1936年11月25日 濛江 小汤河 牺牲",
        "n": 5, "indep": ["国家图书馆（中国记忆项目）", "中国军网"], "deriv": 3,
        "note": "牺牲日两说：国图名录/陕西党建网/百度百科记11月7日，个别百家号稿记11月25日——7日为主流口径，25日存疑；年表只记到月，不冲突"}],
        "not_searched": NS},
}

P["evt_1937_songtieyan_xisheng"] = {
    "add_sources": [{
        "book": "中国军网《宋铁岩：抱定决心甘愿效命疆场，马革裹尸誓不生回营》",
        "page": "2025-06-13",
        "url": "https://www.81.cn/yl_208589/16391184.html",
        "quote": "宋铁岩临危不惧，带领身边战士边打边撤，在战斗中不幸中弹，英勇牺牲，年仅２８岁。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1937_songtieyan_xisheng__junwang-songtieyan.html",
    }],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "宋铁岩 东北人民革命军第一军政治部主任 1937年2月11日 和尚帽子 牺牲",
        "n": 5, "indep": ["中国军网"], "deriv": 4,
        "note": "军网证实和尚帽子密营遭袭、战斗中牺牲（年28岁），但未记具体日期；精确到日（1937-02-11）仅见百科系转抄——日级主张暂只有年表，如实标注"}],
        "not_searched": NS},
}

P["evt_1937_bingtangzi"] = {
    "add_sources": [{
        "book": "北安市人民政府《“浴血兴安驱日寇”北安红色故事之冰趟子大捷》",
        "page": "2025-08-20",
        "url": "https://www.hljba.gov.cn/bas/bmdt/202508/c11_337253.shtml",
        "quote": "1937年3月初的一天，赵尚志率领抗联部队来到一个叫“冰趟子”的地方。“冰趟子”原名“黑风口”，是通北县通往小兴安岭的必经之路。",
        "reliability": "A-",
        "archive": f"{ARCH}/evt_1937_bingtangzi__beian-gov-bingtangzi.html",
    }, {
        "book": "百家号《山河铭记 抗联记忆丨赵尚志：以少胜多的“冰趟子”战斗》",
        "page": "2026-08-24",
        "url": "https://baijiahao.baidu.com/s?id=1874365408727694942&wfr=spider&for=pc",
        "quote": "3月7日，八百余名日伪军循着抗联踪迹闯入冰趟子沟……冰趟子一战战果悬殊，八百余名来犯的日伪军伤亡高达二百余人，而东北抗联第三军有七名战士牺牲。",
        "reliability": "B",
        "archive": f"{ARCH}/evt_1937_bingtangzi__baijiahao-bingtangzi.html",
    }],
    "date_variants": [
        {"value": "1937-03-07", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1937-03-07", "precision": "day", "source": "百家号《山河铭记 抗联记忆》（战况日）"},
        {"value": "1937-03", "precision": "month", "source": "北安市人民政府（3月初）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "冰趟子战斗 1937年3月 赵尚志 第三军 通北 大批日军毙伤",
        "n": 5, "indep": ["北安市人民政府"], "deriv": 4,
        "note": "战果口径差异大：本库 measures 采年表“毙伤日伪军200余人、缴获一批枪支弹药”；百家号记敌伤亡二百余/我方牺牲7人，知乎比对中日双方史料记约300人——数值主张只入 measures 不裁决"}],
        "not_searched": NS},
}

P["evt_1938_shier_lieshi"] = {
    "add_sources": [{
        "book": "百家号《山河铭记 抗联记忆丨小孤山十二烈士：以生命守护抗日事业》",
        "page": "2026-09-10",
        "url": "https://baijiahao.baidu.com/s?id=1875903637732736837&wfr=spider&for=pc",
        "quote": "1938年3月18日拂晓，抗联第二路军五军三师八团一连连长李海峰、指导员班路遗，率领13名战士与1名交通员踏雪行军。……为掩护后方主力部队安全转移，李海峰当即决断，抢占地势有利的小孤山阵地，就地阻击敌军。",
        "reliability": "B",
        "archive": f"{ARCH}/evt_1938_shier_lieshi__baijiahao-shierlieshi.html",
    }, {
        "book": "郑州大学（转载《红旗 热血 黑土——100位抗联英雄的故事》）",
        "page": "2024-10-30",
        "url": "https://gzc.zzut.edu.cn/info/1157/1607.htm",
        "quote": "1938年3月18日，他率领16名抗联战士为了掩护大部队撤退，被日伪军包围在一座小孤山上，他们英勇作战，多次打退敌人的进攻。最后，包括他在内的12名战士壮烈殉国。",
        "reliability": "B-",
        "archive": f"{ARCH}/evt_1938_shier_lieshi__zzut-lilhaifeng.html",
    }],
    "date_variants": [
        {"value": "1938-03-18", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1938-03-18", "precision": "day", "source": "百家号《山河铭记 抗联记忆》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "小孤山战斗 1938年3月18日 宝清 十二烈士 第五军三师八团 连长 李海峰",
        "n": 5, "indep": [], "deriv": 5,
        "note": "日期三方一致；牺牲人数口径差异：一说14人作战12人殉国、一说16名战士12名殉国——人数存疑已在本库 measures 标注；独立机构级第二源本轮未找到，待补（候选：宝清县志、双鸭山党史网）"}],
        "not_searched": NS},
}

P["evt_1938_chengbin_toudi"] = {
    "add_sources": [{
        "book": "百家号《当年残害杨靖宇将军的叛徒，潜伏北京做官多年，一场大雨露了马脚》",
        "page": "2026-08-06",
        "url": "https://baijiahao.baidu.com/s?id=1872695328133062993&wfr=spider&for=pc",
        "quote": "1938年，日军抓了程斌的母亲和哥哥，在报纸上大肆宣扬。……于1938年7月率所部115人投敌。投敌后，程斌开始为日本人效力，并组建了“程斌挺进队”，将杨靖宇在深山老林里的密营全部捣毁。",
        "reliability": "B-",
        "archive": f"{ARCH}/evt_1938_chengbin_toudi__baijiahao-chengbin.html",
    }],
    "date_variants": [
        {"value": "1938-06-29", "precision": "day", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1938-07", "precision": "month", "source": "百家号《当年残害杨靖宇将军的叛徒》"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "程斌 1938年 叛变 投敌 第一师 杨靖宇 第一路军 密营 破坏",
        "n": 5, "indep": [], "deriv": 5,
        "note": "叛变日期两说：年表记6月29日，百家号系转抄记7月——叛变具体日期在公开网络层面口径混乱，需档案级来源（中央档案馆审判日伪档案/辽宁党史出版物）核实；密营被捣毁的因果链（叛变→密营暴露→杨靖宇绝境）各源一致"}],
        "not_searched": ["中央档案馆审判日伪战犯档案（闭架）", "《辽宁党史资料》纸本（未获取）"]},
}

P["evt_1938_banv_toujiang"] = {
    "add_sources": [{
        "book": "新华社《八女投江：乌斯浑河畔的绝唱》",
        "page": "2025-09-04",
        "url": "https://www.news.cn/politics/20250904/d1c6684a85154afcbfd26ea84fa0c60a/c.html",
        "quote": "1938年10月的一天，东北抗日联军第2路军西征回师队伍在牡丹江地区乌斯浑河渡口与日伪军千余人遭遇。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1938_banv_toujiang__xinhuanet-banv.html",
    }, {
        "book": "中央纪委国家监委网站《八女投江：宁死不屈的如花战士》（英雄烈士谱）",
        "page": "2018-11-09",
        "url": "https://www.ccdi.gov.cn/yaowen/201811/t20181109_183102.html",
        "quote": "是年10月上旬，队伍在牡丹江地区乌斯浑河渡口与日伪军千余人遭遇。……她们毁掉枪支，挽臂涉入乌斯浑河，高唱着《国际歌》，集体沉江，壮烈殉国。",
        "reliability": "A",
        "archive": f"{ARCH}/evt_1938_banv_toujiang__ccdi-banv.html",
    }],
    "date_variants": [
        {"value": "1938-10", "precision": "month", "source": "抗日战争纪念网《东北抗联大事记》"},
        {"value": "1938-10", "precision": "month", "source": "新华社《八女投江：乌斯浑河畔的绝唱》"},
        {"value": "1938-10", "precision": "month", "source": "中央纪委国家监委网站《八女投江》（10月上旬）"},
    ],
    "provenance": {"depth": "deep", "on": "2026-10-17", "probes": [{
        "q": "八女投江 1938年10月 乌斯浑河 冷云 妇女团 第五军 柴河",
        "n": 5, "indep": ["新华社", "中央纪委国家监委网站"], "deriv": 3,
        "note": "新华社与中央纪委两家权威互证；具体日期（10月上旬/中下旬/20日）各源不一，主流口径只到月——年表记到月反而与权威口径一致；八人姓名职务三方名单完全一致"}],
        "not_searched": NS},
}


def main() -> int:
    prov = json.loads(PROV.read_text(encoding="utf-8"))
    patches = prov["patches"]
    for eid, p in P.items():
        if eid in patches:
            print(f"跳过（已有 patch）：{eid}")
            continue
        patches[eid] = p
    prov["retrieved_on"] = sorted({*prov.get("retrieved_on", []), "2026-10-17-round4"})
    PROV.write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已并入 {len(P)} 条 patch，provenance.json 现共 {len(patches)} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
