window.__MIYING_CASES__ = {
 "_note": "由 src/build_cases.py 从 events.json 生成。所有引文取自 sources.quote，未经改写。",
 "cases": [
  {
   "id": "case_kl_001",
   "case_no": "KL-001",
   "kind": "consistent",
   "title": "东北抗日联军教导旅成立于何时",
   "claim_text": "东北抗日联军教导旅于1942年成立",
   "event_id": "evt_1942_jiaodaolv_chengli",
   "predicate": "成立时间",
   "unit": null,
   "values": [],
   "summary": "东北抗日联军教导旅在北野营正式成立。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 5 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "东北抗日联军教导旅",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1942年（5 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "8月1日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "俄罗斯哈巴罗夫斯克（县级精度）",
       "state": "较粗"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 5 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "page": "2025-09-18",
       "quote": "8月：东北抗日联军教导旅在北野营正式成立。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "彭施鲁《东北抗日联军和苏联远东军关系回顾》（载《中共党史资料》）",
       "short": "彭施鲁",
       "page": "2014-09-11",
       "quote": "到了1942年的8月1日，东北抗日联军教导旅正式成立。设旅、营、连三级，军政主官都由抗联人员担任，另由苏联军官担任副职，以协助进行军事训练。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "国家图书馆《抗联简史》",
       "short": "国家图书馆",
       "page": "抗战胜利80周年专题",
       "quote": "1942年秋，南北野营合编为国际旅（番号为苏联远东方面军步兵第八十八旅，又称东北抗联教导旅）。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "抗日战争纪念网《东北抗联大事记》",
       "short": "抗日战争纪念网",
       "page": "1942年7—8月",
       "quote": "7月22日　东北抗日联军南北两野营及在东北活动的抗联人员统一编为东北抗联教导旅(亦称八十八独立步兵旅)。周保中任旅长，张寿钱任政治副旅长。",
       "url": "https://www.krzzjn.com/show-3159-162423.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "中国军网《不熄的火种——东北抗联教导旅组建始末》",
       "short": "中国军网",
       "page": "2020-08-18",
       "quote": "他们就是由退入苏联境内的东北抗日联军余部改编而成的教导旅，又称中国特别旅。",
       "url": "https://www.81.cn/wh_208594/9884382.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "5 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-001",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 5 条来源记录均记载「1942年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_002",
   "case_no": "KL-002",
   "kind": "consistent",
   "title": "《告满洲各地义勇军书》发表于何时",
   "claim_text": "《告满洲各地义勇军书》于1932年发表",
   "event_id": "evt_1932_mgzsw_gaoshu",
   "predicate": "发表时间",
   "unit": null,
   "values": [],
   "summary": "中共满洲省委发表《告满洲各地义勇军书》。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 4 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "《告满洲各地义勇军书》",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1932年（4 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "3月31日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "原文未载地点",
       "state": "缺失"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 4 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "page": "2025-09-18",
       "quote": "3月31日：中共满洲省委发表《告满洲各地义勇军书》。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "黑龙江省文化和旅游厅《文物会说话——守护龙江文脉》",
       "short": "黑龙江省文化和旅游厅",
       "page": "2025-08-30",
       "quote": "1932年3月31日，中共满洲省委印发《告满洲各地义勇军书》，鼓舞义勇军团结劳苦群众，坚决与日本侵略者战斗。在党的号召下，义勇军迅速壮大，半年多就发展到30多万人，遍布东北93个市县。",
       "url": "https://wlt.hlj.gov.cn/wlt/c116709/202508/c00_31869288.shtml",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "东北烈士纪念馆馆藏说明（东北抗联博物馆）",
       "short": "东北烈士纪念馆馆藏说明",
       "page": "藏品条目",
       "quote": "《告满洲各地义勇军书》为黄褐色薄纸，1页……刻印时间在标题下面，写的是“1931年3月31日”。因行文内写的是1931年九一八事变后日本帝国主义已侵占东北三省，故以上时间显然是笔误，应为“1932年3月31日”。",
       "url": "https://www.jn1948.cn/news/641.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "黑龙江省档案馆《义勇军进行曲的奏响》专题",
       "short": "黑龙江省档案馆",
       "page": "2025-09-20",
       "quote": "自1931年起中共满洲省委发表《告满洲各地义勇军书》《为反对日本帝国主义进攻热河华北举行援助义勇军运动周的决议》……",
       "url": "http://hljsdag.org.cn/index.php?m=home&c=View&a=index&aid=271783",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "4 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-002",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 4 条来源记录均记载「1932年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_003",
   "case_no": "KL-003",
   "kind": "consistent",
   "title": "赵尚志牺牲于何时",
   "claim_text": "赵尚志于1942年牺牲",
   "event_id": "evt_1942_zhaoshangzhi_xisheng",
   "predicate": "牺牲时间",
   "unit": null,
   "values": [],
   "summary": "东北抗联第二路军副总指挥赵尚志身负重伤牺牲。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 4 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "赵尚志",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1942年（4 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "2月12日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "黑龙江省萝北县（县级精度）",
       "state": "较粗"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 4 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "page": "2025-09-18",
       "quote": "2月12日：东北抗联第二路军副总指挥赵尚志身负重伤牺牲。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "抗日战争纪念网《东北抗联大事记》",
       "short": "抗日战争纪念网",
       "page": "1942年2月",
       "quote": "2月12日　赵尚志率小部队在袭击鹤立县梧桐河伪警察分驻所时，遭混入队内的特务分子枪击，重伤被俘后，英勇牺牲。",
       "url": "https://www.krzzjn.com/show-3159-162423.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "赵尚志纪念馆《大事年表》",
       "short": "赵尚志纪念馆",
       "page": "馆方年表",
       "quote": "1942年2月12日　在去袭击鹤立县梧桐河金矿伪警察分驻所途中，被混入队内的敌特打伤、被俘，八个小时后英勇牺牲。",
       "url": "https://www.zszjng.cn/about/19.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "侵华日军南京大屠杀遇难同胞纪念馆《抗日将领赵尚志生命的最后时刻》",
       "short": "侵华日军南京大屠杀遇难同胞纪念馆",
       "page": "2022-03-25",
       "quote": "1942年2月12日凌晨，在东北的凛冽寒风中，一支不足10人的抗日小分队正在密林中穿行。",
       "url": "http://www.19371213.cn/information/news/hotnews/202203/t20220325_3327047.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "4 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-003",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 4 条来源记录均记载「1942年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_004",
   "case_no": "KL-004",
   "kind": "consistent",
   "title": "《为反对日本强盗围剿东北义勇军告东北民众书》发表于何时",
   "claim_text": "《为反对日本强盗围剿东北义勇军告东北民众书》于1933年发表",
   "event_id": "evt_1933_mgzsw_gaominzhong",
   "predicate": "发表时间",
   "unit": null,
   "values": [],
   "summary": "中共满洲省委发表《为反对日本强盗围剿东北义勇军告东北民众书》。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 3 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "《为反对日本强盗围剿东北义勇军告东北民众书》",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1933年（3 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "7月11日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "原文未载地点",
       "state": "缺失"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 3 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "page": "2025-09-18",
       "quote": "7月：中共满洲省委发表《为反对日本强盗围剿东北义勇军告东北民众书》，号召东北抗日武装坚持抗战。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "中央档案馆《东北人民抗击日本帝国主义侵略档案文献网上展览》",
       "short": "中央档案馆",
       "page": "2020-08-27（微信发布）",
       "quote": "1933年7月11日，中共满洲省委发表《为反对日本强盗围剿东北义勇军告东北民众书》。(中央档案馆提供)",
       "url": "https://mp.weixin.qq.com/s?__biz=MzAxNDIxMDE2NQ==&mid=2651204718&idx=1&sn=815c0af9710eb182005e5794b4db1d52&chksm=80644974b713c062d0000adfbd71432ca9687b45dee5f64cb1acf2d146ab64e6a6501ac02812&scene=27",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "抗日战争纪念网《东北抗日联军1933年大事记》",
       "short": "抗日战争纪念网",
       "page": "2017-08-05",
       "quote": "11日 中共满洲省委发表《为反对日本强盗“围剿”东北义勇军告东北民众书》。",
       "url": "https://www.krzzjn.com/show-90-54080.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "3 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-004",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 3 条来源记录均记载「1933年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_005",
   "case_no": "KL-005",
   "kind": "consistent",
   "title": "《东北抗日联军统一军队建制宣言》发表于何时",
   "claim_text": "《东北抗日联军统一军队建制宣言》于1936年发表",
   "event_id": "evt_1936_tongyi_jianzhi",
   "predicate": "发表时间",
   "unit": null,
   "values": [],
   "summary": "《东北抗日联军统一军队建制宣言》发表。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 3 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "《东北抗日联军统一军队建制宣言》",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1936年（3 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "2月20日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "原文未载地点",
       "state": "缺失"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 3 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "page": "2025-09-18",
       "quote": "2月20日：《东北抗日联军统一军队建制宣言》发表。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "抗日战争纪念网《东北抗联大事记》",
       "short": "抗日战争纪念网",
       "page": "1936年2月",
       "quote": "20日 《东北抗日联军统一军队建制宣言》发表。",
       "url": "https://www.krzzjn.com/show-3159-162417.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "本溪县人民政府“铭记历史 缅怀先烈”专栏",
       "short": "本溪县人民政府“铭记历史 缅怀先烈”专栏",
       "page": "2025-07-31",
       "quote": "1936年2月20日，中国共产党领导的东北人民革命军共同发表《东北抗日联军统一军队建制宣言》，宣布东北人民革命军“一律改组军队建制为东北抗日联军”。",
       "url": "http://www.bxszx.gov.cn/wysc/content_648725",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "3 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-005",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 3 条来源记录均记载「1936年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_006",
   "case_no": "KL-006",
   "kind": "consistent",
   "title": "赵尚志作战于何时",
   "claim_text": "赵尚志于1937年作战",
   "event_id": "evt_1937_bingtangzi",
   "predicate": "作战时间",
   "unit": null,
   "values": [],
   "summary": "赵尚志率第三军西征部队在通北冰趟子设伏，重创日伪军。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 3 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "赵尚志",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1937年（3 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "3月7日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "原文未载地点",
       "state": "缺失"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 3 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "抗日战争纪念网《东北抗联大事记》",
       "short": "抗日战争纪念网",
       "page": "1937年3月",
       "quote": "7日 赵尚志率第三军西征部队在通北冰趟子设伏重创敌军。",
       "url": "https://www.krzzjn.com/show-3159-162418.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "北安市人民政府《“浴血兴安驱日寇”北安红色故事之冰趟子大捷》",
       "short": "北安市人民政府",
       "page": "2025-08-20",
       "quote": "1937年3月初的一天，赵尚志率领抗联部队来到一个叫“冰趟子”的地方。“冰趟子”原名“黑风口”，是通北县通往小兴安岭的一个重要通道。",
       "url": "https://www.hljba.gov.cn/bas/bmdt/202508/c11_337253.shtml",
       "archive": "data/probe_archive/evt_1937_bingtangzi__beian-gov-bingtangzi.html",
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "百家号《山河铭记 抗联记忆丨赵尚志：以少胜多的“冰趟子”战斗》",
       "short": "百家号",
       "page": "2026-08-24",
       "quote": "3月7日，八百余名日伪军循着抗联踪迹闯入冰趟子沟……冰趟子一战战果悬殊，八百余名来犯的日伪军伤亡高达二百余人，而东北抗联第三军有七名战士牺牲。",
       "url": "https://baijiahao.baidu.com/s?id=1874365408727694942&wfr=spider&for=pc",
       "archive": "data/probe_archive/evt_1937_bingtangzi__baijiahao-bingtangzi.html",
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "3 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-006",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 3 条来源记录均记载「1937年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_007",
   "case_no": "KL-007",
   "kind": "consistent",
   "title": "吉林自卫军成立于何时",
   "claim_text": "吉林自卫军于1932年成立",
   "event_id": "evt_1932_jilin_ziweijun",
   "predicate": "成立时间",
   "unit": null,
   "values": [],
   "summary": "以李杜为总司令的吉林自卫军成立，成为吉林抗日武装的主力。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 3 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "吉林自卫军",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1932年（3 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "1月31日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "原文未载地点",
       "state": "缺失"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 3 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "抗日战争纪念网《东北抗联大事记》",
       "short": "抗日战争纪念网",
       "page": "1932年1月",
       "quote": "31日 以李杜为总司令的吉林自卫军成立。",
       "url": "https://www.krzzjn.com/show-3159-162413.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "团结网《1932：李杜与哈尔滨保卫战》",
       "short": "团结网",
       "page": "2020-11-26",
       "quote": "1月31日，李杜、丁超等召集抗日军政要员在哈开会，成立了“吉林自卫军总司令部”，推举李杜为自卫军总司令。",
       "url": "https://www.tuanjiebao.com/m/2020-11/26/content_8896400.htm",
       "archive": "data/probe_archive/evt_1932_jilin_ziweijun__tuanjiebao-lidu.html",
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "抗日战争纪念网《功绩赫赫 铁骨铮铮——东北抗日联军总司令李杜将军》",
       "short": "抗日战争纪念网",
       "page": "2017-08-02",
       "quote": "1932年1月31日在哈尔滨成立了统一指挥抗日军队的吉林自卫军总司令部，公推李杜为吉林抗日自卫军总司令。",
       "url": "https://www.krzzjn.com/show-90-53815.html",
       "archive": "data/probe_archive/evt_1932_jilin_ziweijun__krzzjn-lidu.html",
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "3 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-007",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 3 条来源记录均记载「1932年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_008",
   "case_no": "KL-008",
   "kind": "consistent",
   "title": "巴彦游击队（东北工农义勇军江北骑兵独立师）正式成立于何时",
   "claim_text": "巴彦游击队（东北工农义勇军江北骑兵独立师）正式于1932年成立",
   "event_id": "evt_1932_bayan_youjidui",
   "predicate": "成立时间",
   "unit": null,
   "values": [],
   "summary": "巴彦游击队（东北工农义勇军江北骑兵独立师）正式成立，张甲洲任总指挥；赵尚志后到该部工作。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。本次有 3 条来源记录可比对；来源机构数不等于独立史源数。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "巴彦游击队（东北工农义勇军江北骑兵独立师）正式",
       "state": "来源记载相合"
      },
      {
       "k": "时点",
       "v": "1932年（3 条来源均记此年）",
       "state": "来源记载相合"
      },
      {
       "k": "月日",
       "v": "5月16日",
       "state": "来源记载相合"
      },
      {
       "k": "地点",
       "v": "原文未载地点",
       "state": "缺失"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 3 条记载，均指向同一事件。原文逐字照录。"
     ],
     "evidence": [
      {
       "book": "抗日战争纪念网《东北抗联大事记》",
       "short": "抗日战争纪念网",
       "page": "1932年5月",
       "quote": "16日 东北工农义勇军江北骑兵独立师 (巴彦游击队)正式成立，张甲洲任总指挥。",
       "url": "https://www.krzzjn.com/show-3159-162413.html",
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "国防部《甲洲路旁，“小红星”茁壮成长》（中国国防报）",
       "short": "国防部",
       "page": "2026-10-14",
       "quote": "青年时期，他曾就读于北京大学和清华大学，并积极参加学生运动，1932年回到家乡，创建巴彦抗日游击队并担任总指挥。",
       "url": "http://www.mod.gov.cn/gfbw/gfdy/16492977.html",
       "archive": "data/probe_archive/evt_1932_bayan_youjidui__guofangbu-zhangjiazhou.html",
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      },
      {
       "book": "贵州省国防动员办公室《记忆｜张甲洲：从清北学子到抗日英雄》",
       "short": "贵州省国防动员办公室",
       "page": "2025-03-14",
       "quote": "1932年5月16日，在一口井前，张甲洲带着来“参加婚礼”的200多人，举行了誓师大会，巴彦抗日游击队正式成立，他担任总指挥。",
       "url": "http://www.gzdis.gov.cn/xwhc/yw/202503/t20250314_87166276.html",
       "archive": "data/probe_archive/evt_1932_bayan_youjidui__gzdis-zhangjiazhou.html",
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "3 条来源记录均未标为一手档案。所以只能说「当前库内来源这样记载」，不能声称「档案原件如此」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-008",
     "status": "consistent",
     "status_cn": "库内年份记载相合 · 未达定谳",
     "missing": [
      "需可核验的一手档案或命令原件，才能支持历史层面的定谳"
     ],
     "conservative": "库内 3 条来源记录均记载「1932年」；来源机构数不等于独立史源数。这只能说明当前库内记载口径相合，不能据此定谳。",
     "high_count": 0
    }
   ]
  },
  {
   "id": "case_kl_009",
   "case_no": "KL-009",
   "kind": "dispute",
   "title": "东北抗日联军总兵力究竟是多少",
   "claim_text": "东北抗日联军在1936年总兵力为 30,000 人（库内最低的一种说法）",
   "event_id": "evt_1936_kanglian_dingsheng",
   "predicate": "总兵力",
   "unit": "人",
   "values": [
    30000,
    45000
   ],
   "summary": "东北抗日联军编成11个军，进入鼎盛时期，活动范围遍及东南满、吉东、北满70余县。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。任何一个不成立，命题就不能成立。",
      "时点「鼎盛」「时期」，没有落到具体年月——这会是后面所有分歧的源头，因为不同来源可能各自指向不同年份。",
      "原文出现「余」，说明这个数字本身是约数。把它当成精确值来比较，方法上就已经失真。",
      "本案数值已出现互异主张；拆解展示的是库内记录精度，不将主张写成已证实事实。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "东北抗日联军",
       "state": "来源引文提及"
      },
      {
       "k": "时点",
       "v": "1936年（仅到年）",
       "state": "原文时点表述较宽"
      },
      {
       "k": "地点",
       "v": "中国东北（省级精度）",
       "state": "省级范围"
      },
      {
       "k": "数值",
       "v": "30,000 人",
       "state": "存在分歧且为约数"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 2 条记载，其中 2 条给出具体数字。以下原文逐字照录，未作改写。",
      "另有 1 条旁证不在本条事件下，但提到了同一主体的人数——它们决定了「鼎盛」这个时点到底指哪一年。"
     ],
     "evidence": [
      {
       "book": "人民日报《弘扬历久弥新的东北抗联精神》",
       "short": "人民日报",
       "page": "2021-10-28",
       "quote": "鼎盛时期，东北抗日联军共组建成11个军、3万余人，活动范围遍及东南满、吉东、北满70余县的广大地区。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": 30000,
       "unit": "人",
       "is_primary": false
      },
      {
       "book": "国家图书馆《抗联简史》（引孔令波《军事历史》1986年第4期）",
       "short": "国家图书馆",
       "page": "抗战胜利80周年专题",
       "quote": "东北抗联的11个军，鼎盛时期达四万五千余人，经一年多协同作战，给日伪军以沉重打击。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": 45000,
       "unit": "人",
       "is_primary": false
      }
     ],
     "side": [
      {
       "book": "新华社《八女投江：乌斯浑河畔的绝唱》",
       "short": "新华社",
       "quote": "1938年10月的一天，东北抗日联军第2路军西征回师队伍在牡丹江地区乌斯浑河渡口与日伪军千余人遭遇。",
       "year": "1938",
       "event": "第五军一师西征部队回返途中，在乌斯浑河渡口与敌遭遇，妇女团指导员冷云等8名女战士弹尽后投江殉国，史称“八女投江”。"
      }
     ]
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R1",
       "name": "时点无统一定义",
       "severity": "high",
       "text": "两条原文都用「鼎盛」指代时间，但没有一条给出起止年月。「鼎盛」在史学上没有公认区间，不同来源可能各自指向不同年份——这是分歧的根，不是数字本身。"
      },
      {
       "code": "R2",
       "name": "转引而非独立记载",
       "severity": "high",
       "text": "「国家图书馆」注明是转引（引孔令波《军事历史》1986年第4期）。转引不构成独立互证——两条记载看起来是两票，实际可能只有一票。"
      },
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "high",
       "text": "参与比对的所有记载均为 B/C 级（转述、报道、展陈），没有一条出自原始档案。这意味着无论数字多接近，都只能证明「有人这样写过」，不能证明「当时确实如此」。"
      },
      {
       "code": "R4",
       "name": "数值离散超出容差",
       "severity": "high",
       "text": "最高 45,000，最低 30,000，机械相除差 33%（这个百分比本身建立在约数换算上，只能看量级，见 R6）。这个量级不是四舍五入能解释的，是两个口径。"
      },
      {
       "code": "R6",
       "name": "约数被当作精确值",
       "severity": "medium",
       "text": "原文用的是「余」。把「三万余」换算成 30,000 再算百分比差异，方法上就已经失真——约数只能比量级，不能比个位。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-009",
     "status": "unresolved",
     "status_cn": "悬案 · 无法定谳",
     "missing": [
      "抗联各军兵力统计的原始报表或档案（现库内 0 条 A 级来源）",
      "「鼎盛时期」的起止年月，需权威辞书或军史给出界定",
      "精确到百位的统计口径说明（现有原文全为约数）"
     ],
     "conservative": "可以确定的是：编成 11 个军——这一点各条原文一致。数值上只能给出区间：30,000 至 45,000 人。在此区间内取任何单一数字，都是超出材料的判断。",
     "high_count": 4
    }
   ]
  },
  {
   "id": "case_kl_010",
   "case_no": "KL-010",
   "kind": "dispute",
   "title": "东北抗日义勇军总兵力究竟是多少",
   "claim_text": "东北抗日义勇军在1932年总兵力为 300,000 人（库内最低的一种说法）",
   "event_id": "evt_1932_yiyongjun_dingsheng",
   "predicate": "总兵力",
   "unit": "人",
   "values": [
    300000,
    500000
   ],
   "summary": "东北抗日义勇军进入鼎盛时期，总人数达到历史最高。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 4 个原子断言。任何一个不成立，命题就不能成立。",
      "时点「鼎盛」「时期」，没有落到具体年月——这会是后面所有分歧的源头，因为不同来源可能各自指向不同年份。",
      "原文出现「约」「一说」，说明这个数字本身是约数。把它当成精确值来比较，方法上就已经失真。",
      "本案数值已出现互异主张；拆解展示的是库内记录精度，不将主张写成已证实事实。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "东北抗日义勇军",
       "state": "主体需逐项核查"
      },
      {
       "k": "时点",
       "v": "1932年（仅到年）",
       "state": "原文时点表述较宽"
      },
      {
       "k": "地点",
       "v": "中国东北（省级精度）",
       "state": "省级范围"
      },
      {
       "k": "数值",
       "v": "300,000 人",
       "state": "存在分歧且为约数"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 3 条记载，其中 3 条给出具体数字。以下原文逐字照录，未作改写。",
      "另有 1 条旁证不在本条事件下，但提到了同一主体的人数——它们决定了「鼎盛」这个时点到底指哪一年。"
     ],
     "evidence": [
      {
       "book": "抗日战争纪念网《三十万人不解甲：东北抗日义勇军》",
       "short": "抗日战争纪念网",
       "page": "2018-03-21",
       "quote": "义勇军主动出击，部队迅速发展壮大，是年夏秋达鼎盛时期，总人数约50万（一说30万）。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "C",
       "reliability_cn": "回忆录/展陈/待核转述",
       "value": 500000,
       "unit": "人",
       "is_primary": false
      },
      {
       "book": "莆田市博物馆《抗战篇系列——东北抗日义勇军》",
       "short": "莆田市博物馆",
       "page": "2025-08-15",
       "quote": "东北义勇军的总兵力，在1932年全盛时期达到了30万人之多。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "C",
       "reliability_cn": "回忆录/展陈/待核转述",
       "value": 300000,
       "unit": "人",
       "is_primary": false
      },
      {
       "book": "国家图书馆《抗联简史》",
       "short": "国家图书馆",
       "page": "抗战胜利80周年专题",
       "quote": "1931年“九一八”事变后，东北人民和东北军队部分爱国官兵纷纷组成义勇军、救国军、自卫军等抗日武装，统称抗日义勇军，约50万人，在东北各地抵抗日军进攻。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": 500000,
       "unit": "人",
       "is_primary": false
      }
     ],
     "side": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "quote": "年底：东北抗日义勇军余部十余万人仍在坚持战斗。",
       "year": "1934",
       "event": "东北抗日义勇军余部十余万人仍在坚持战斗。"
      }
     ]
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R1",
       "name": "时点无统一定义",
       "severity": "high",
       "text": "两条原文都用「鼎盛」指代时间，但没有一条给出起止年月。「鼎盛」在史学上没有公认区间，不同来源可能各自指向不同年份——这是分歧的根，不是数字本身。"
      },
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "high",
       "text": "参与比对的所有记载均为 B/C 级（转述、报道、展陈），没有一条出自原始档案。这意味着无论数字多接近，都只能证明「有人这样写过」，不能证明「当时确实如此」。"
      },
      {
       "code": "R4",
       "name": "数值离散超出容差",
       "severity": "high",
       "text": "最高 500,000，最低 300,000，机械相除差 40%（这个百分比本身建立在约数换算上，只能看量级，见 R6）。这个量级不是四舍五入能解释的，是两个口径。"
      },
      {
       "code": "R6",
       "name": "约数被当作精确值",
       "severity": "medium",
       "text": "原文用的是「约」「一说」。把「三万余」换算成 30,000 再算百分比差异，方法上就已经失真——约数只能比量级，不能比个位。"
      },
      {
       "code": "R7",
       "name": "史料自认存在异说",
       "severity": "high",
       "text": "有一条原文自己就写着「一说」。这不是我们比对出来的分歧，是史料本身承认了它——这类分歧通常比外部比对更值得记。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-010",
     "status": "unresolved",
     "status_cn": "悬案 · 无法定谳",
     "missing": [
      "抗联各军兵力统计的原始报表或档案（现库内 0 条 A 级来源）",
      "「鼎盛时期」的起止年月，需权威辞书或军史给出界定",
      "精确到百位的统计口径说明（现有原文全为约数）"
     ],
     "conservative": "可以确定的是：各来源对「此时处于规模高点」这一定性并无分歧，分歧只在具体数字。数值上只能给出区间：300,000 至 500,000 人。在此区间内取任何单一数字，都是超出材料的判断。",
     "high_count": 4
    }
   ]
  },
  {
   "id": "case_kl_011",
   "case_no": "KL-011",
   "kind": "dispute",
   "title": "抗日同盟军作战于何时（整月分歧）",
   "claim_text": "抗日同盟军作战日期：1933-06-01（辽宁日报）vs 1933-07-12（察哈尔抗战遗址展陈（经百科转引））",
   "event_id": "evt_1933_duolun_shoufu",
   "predicate": "date.start",
   "unit": "date",
   "values": [
    "1933-06-01",
    "1933-07-12"
   ],
   "summary": "抗日同盟军收复多伦等地。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "「抗日同盟军作战于何时」拆成两条互斥的日期主张：",
      "主张甲：辽宁日报《大事记》 记 1933-06-01（精度：月）；",
      "主张乙：察哈尔抗战遗址展陈（经百科转引） 记 1933-07-12（精度：日）。",
      "两条主张相差 41 天（整月级），在本库的日期层级上不能同时成立。"
     ],
     "assertions": [
      {
       "k": "事件本体",
       "v": "抗日同盟军收复多伦等地。",
       "state": "确定"
      },
      {
       "k": "主张甲",
       "v": "1933-06-01（辽宁日报）",
       "state": "存疑"
      },
      {
       "k": "主张乙",
       "v": "1933-07-12（察哈尔抗战遗址展陈（经百科转引））",
       "state": "存疑"
      },
      {
       "k": "分歧量级",
       "v": "41 天",
       "state": "确定"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内对同一条事实给出了两条日期主张。以下原文逐字照录，未作改写。"
     ],
     "evidence": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "page": "",
       "quote": "6月：抗日同盟军收复多伦等地。",
       "reliability": "B",
       "value": "1933-06-01",
       "unit": "date",
       "is_primary": false
      },
      {
       "book": "察哈尔抗战遗址展陈（经百科转引）",
       "short": "察哈尔抗战遗址展陈",
       "page": "",
       "quote": "（该来源以日期主张入链，原文引文见事件层）",
       "reliability": "B",
       "value": "1933-07-12",
       "unit": "date",
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R9",
       "name": "整月级日期分歧",
       "severity": "high",
       "text": "辽宁日报 记 1933-06-01，察哈尔抗战遗址展陈（经百科转引） 记 1933-07-12，相差 41 天，超出精度误差能解释的范围——这是实质性分歧，不是「一个记约数一个记精确数」。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-011",
     "status": "unresolved",
     "status_cn": "悬案 · 整月分歧",
     "missing": [
      "事件所在省档案馆革命历史档案（闭架）",
      "当事人回忆录纸本或烈士传记的档案级引文"
     ],
     "conservative": "两说并陈：1933-06-01（辽宁日报）与 1933-07-12（察哈尔抗战遗址展陈（经百科转引））。本库按「不动原记载、不加权下结论」处置——机构权重倾向双方，但倾向不是定谳。任何一侧改字都会在系统里留下痕迹：这不是没能得出结论，而是**证据还没到能得出结论的程度**。",
     "high_count": 1
    }
   ]
  },
  {
   "id": "case_kl_012",
   "case_no": "KL-012",
   "kind": "dispute",
   "title": "童长荣牺牲于何时（整月分歧）",
   "claim_text": "童长荣牺牲日期：1934-04-21（抗日战争纪念网）vs 1934-03-21（国防部）",
   "event_id": "evt_1934_tongzhangrong_xisheng",
   "predicate": "date.start",
   "unit": "date",
   "values": [
    "1934-03-21",
    "1934-04-21"
   ],
   "summary": "中共东满特委书记童长荣率队在汪清十里坪庙沟附近与日伪军激战，壮烈牺牲。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "「童长荣牺牲于何时」拆成两条互斥的日期主张：",
      "主张甲：抗日战争纪念网《东北抗联大事记》 记 1934-04-21（精度：日）；",
      "主张乙：国防部《童长荣》 记 1934-03-21（精度：日）。",
      "两条主张相差 31 天（整月级），在本库的日期层级上不能同时成立。"
     ],
     "assertions": [
      {
       "k": "事件本体",
       "v": "中共东满特委书记童长荣率队在汪清十里坪庙沟附近与日伪军激战，壮烈牺牲。",
       "state": "确定"
      },
      {
       "k": "主张甲",
       "v": "1934-04-21（抗日战争纪念网）",
       "state": "存疑"
      },
      {
       "k": "主张乙",
       "v": "1934-03-21（国防部）",
       "state": "存疑"
      },
      {
       "k": "分歧量级",
       "v": "31 天",
       "state": "确定"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内对同一条事实给出了两条日期主张。以下原文逐字照录，未作改写。"
     ],
     "evidence": [
      {
       "book": "抗日战争纪念网《东北抗联大事记》",
       "short": "抗日战争纪念网",
       "page": "",
       "quote": "21日 中共东满特委书记童长荣率队在汪清十里坪庙沟附近与日伪军激战，壮烈牺牲。",
       "reliability": "B",
       "value": "1934-04-21",
       "unit": "date",
       "is_primary": false
      },
      {
       "book": "国防部《童长荣》",
       "short": "国防部",
       "page": "",
       "quote": "（该来源以日期主张入链，原文引文见事件层）",
       "reliability": "B",
       "value": "1934-03-21",
       "unit": "date",
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R9",
       "name": "整月级日期分歧",
       "severity": "high",
       "text": "抗日战争纪念网 记 1934-04-21，国防部 记 1934-03-21，相差 31 天，超出精度误差能解释的范围——这是实质性分歧，不是「一个记约数一个记精确数」。"
      },
      {
       "code": "R10",
       "name": "机构权重不对称",
       "severity": "mid",
       "text": "分歧一方为国防部门/官方纪念机构，另一方为媒体年表——但这不构成裁决：年表同样有档案出处，且单方权威转述也可能沿用一处笔误。权重只改变候选倾向，不替代证据。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-012",
     "status": "unresolved",
     "status_cn": "悬案 · 整月分歧",
     "missing": [
      "事件所在省档案馆革命历史档案（闭架）",
      "当事人回忆录纸本或烈士传记的档案级引文"
     ],
     "conservative": "两说并陈：1934-04-21（抗日战争纪念网）与 1934-03-21（国防部）。本库按「不动原记载、不加权下结论」处置——机构权重倾向主张乙，但倾向不是定谳。任何一侧改字都会在系统里留下痕迹：这不是没能得出结论，而是**证据还没到能得出结论的程度**。",
     "high_count": 1
    }
   ]
  },
  {
   "id": "case_kl_013",
   "case_no": "KL-013",
   "kind": "single",
   "title": "高兴亚：孤证怎么处置",
   "claim_text": "辽宁救国军旅长高兴亚牺牲。",
   "event_id": "evt_1934_gaoxingya_xisheng",
   "predicate": null,
   "unit": null,
   "values": [],
   "summary": "辽宁救国军旅长高兴亚牺牲。",
   "steps": [
    {
     "kind": "decompose",
     "agent": "拆解",
     "lines": [
      "命题拆成 3 个原子断言。库内只有 1 条来源可供比对。"
     ],
     "assertions": [
      {
       "k": "主体",
       "v": "高兴亚",
       "state": "确定"
      },
      {
       "k": "时点",
       "v": "1934年4月（仅到月）",
       "state": "较粗"
      },
      {
       "k": "地点",
       "v": "原文未载地点",
       "state": "缺失"
      }
     ]
    },
    {
     "kind": "retrieve",
     "agent": "辑录",
     "lines": [
      "库内共 1 条记载。原文逐字照录，未作改写。"
     ],
     "evidence": [
      {
       "book": "辽宁日报《大事记》",
       "short": "辽宁日报",
       "page": "2025-09-18",
       "quote": "4月：辽宁救国军旅长高兴亚牺牲。",
       "url": null,
       "archive": null,
       "archive_note": null,
       "reliability": "B",
       "reliability_cn": "学术著作/权威报道",
       "value": null,
       "unit": null,
       "is_primary": false
      }
     ],
     "side": []
    },
    {
     "kind": "examine",
     "agent": "对勘",
     "lines": [],
     "challenges": [
      {
       "code": "R5",
       "name": "孤证",
       "severity": "medium",
       "text": "库内只有一条记载，无法做独立互证。但请注意：这不等于史实存疑，只说明本库还没收录第二个来源。这两件事必须分开说。"
      },
      {
       "code": "R3",
       "name": "库内无一手档案",
       "severity": "medium",
       "text": "唯一来源属转述性质。它能证明「有人这样写过」，不足以单独支撑一条定谳结论。"
      }
     ]
    },
    {
     "kind": "register",
     "agent": "存疑",
     "case_no": "KL-013",
     "status": "insufficient",
     "status_cn": "库内证据不足",
     "missing": [
      "需补第二条独立来源（须不同于「辽宁日报」）"
     ],
     "conservative": "本条记载时点只到月、原文未载地点，但库内无第二条独立记载可比对。系统登记为「证据不足」，而不是「存疑」——前者说的是本库，后者说的是历史。",
     "high_count": 0
    }
   ]
  }
 ]
};
