#!/usr/bin/env python3
import json
import sqlite3
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "database" / "schema.sql"
DB_PATH = ROOT / "database" / "sme_due_diligence_demo.db"
LISTED_CACHE_PATH = Path("/Users/hanshuting/Desktop/智能尽调引擎/data/finance_cache.sqlite3")
LISTED_TARGETS = [
    {"ts_code": "002594.SZ", "risk_tier": "medium"},
    {"ts_code": "600519.SH", "risk_tier": "low"},
    {"ts_code": "600998.SH", "risk_tier": "medium"},
    {"ts_code": "600612.SH", "risk_tier": "low"},
    {"ts_code": "600196.SH", "risk_tier": "medium"},
]

MANUAL_LISTED_ENRICHMENTS = {
    "002594.SZ": {
        "company_updates": {
            "name": "比亚迪股份有限公司",
            "unified_social_credit_code": "91440300192317458F",
            "established_on": "1995-02-10",
            "region_province": "广东省",
            "region_city": "深圳市",
            "industry_category": "新能源汽车整车制造",
            "subindustry": "新能源汽车整车制造",
            "operating_status": "开业（存续）",
            "registered_capital_cny": 9117197565.0,
            "paid_in_capital_cny": 9117198000.0,
            "website": "www.byd.com/cn/index.html",
            "overview": "比亚迪股份有限公司成立于1995年2月，董事长为王传福，是一家在深圳和香港两地上市的企业，公司业务覆盖汽车、电子、新能源等领域。",
        },
        "public_profile": [
            ("成立时间", "1995-02-10", "企查查截图人工补录"),
            ("法定代表人", "王传福", "企查查截图人工补录"),
            ("联系电话", "0755-89888888", "企查查截图人工补录"),
            ("邮箱", "bydpo@byd.com", "企查查截图人工补录"),
            ("官网", "www.byd.com/cn/index.html", "企查查截图人工补录"),
            ("注册地址", "深圳市大鹏新区葵涌街道延安路一号", "企查查截图人工补录"),
            ("国标行业", "新能源汽车整车制造", "企查查截图人工补录"),
            ("企业规模", "大型", "企查查截图人工补录"),
            ("员工人数", "869622（2025年）", "企查查截图人工补录"),
            ("营业收入", "8039.65亿元（2025年）", "企查查截图人工补录"),
            ("所属集团", "比亚迪", "企查查截图人工补录"),
            ("曾用名", "深圳市比亚迪实业有限公司（1995-02 至 2002-06）", "企查查截图人工补录"),
            ("实控人", "王传福", "依据股东及主要人员截图人工补录"),
            ("受益所有人", "王传福", "依据股东及主要人员截图人工补录"),
            ("股东", "详见股东信息页（已结构化入库）", "企查查截图人工补录"),
            ("高管", "详见主要人员页（已结构化入库）", "企查查截图人工补录"),
        ],
        "registration": [
            ("统一社会信用代码", "91440300192317458F"),
            ("组织机构代码", "19231745-8"),
            ("工商注册号", "440301501127941"),
            ("纳税人识别号", "91440300192317458F"),
            ("登记状态", "开业（存续）"),
            ("注册资本", "911719.7565万元"),
            ("实缴资本", "911719.8万元"),
            ("企业类型", "股份有限公司（台港澳与境内合资、上市）"),
            ("营业期限", "1995-02-10 至 2053-02-08"),
            ("纳税人资质", "一般纳税人"),
            ("人员规模", "2000-2999人"),
            ("参保人数", "2625（2024年报）"),
            ("所属地区", "广东省深圳市龙岗区"),
            ("登记机关", "深圳市市场监督管理局"),
            ("国标行业", "新能源汽车整车制造（C3612）"),
            ("英文名", "BYD Company Limited"),
            ("经营范围", "锂离子电池以及其他电池、充电器、电子产品、仪器仪表、柔性线路板、五金制品、液晶显示器、手机零配件、模具、塑胶制品及其相关附件的生产、销售；3D眼镜、GPS导航产品的研发、生产及销售；货物及技术进出口；作为比亚迪汽车有限公司比亚迪品牌乘用车、电动车的总经销商，从事品牌乘用车、电动车及其零部件的营销、批发和出口，提供售后服务；电池管理系统、换流柜、逆变柜、汇流箱、开关柜、储能机组的销售；汽车电子装置研发、销售；新能源汽车关键零部件及上述零部件的关键零件、部件的研发、销售；轨道交通运输设备的研发、设计、销售、租赁与售后服务；轨道梁柱的研发、设计、销售；自有物业租赁；广告设计、制作、代理及发布；信息与技术咨询、技术服务。"),
        ],
        "listing_info": [
            ("董事长", "王传福"),
            ("总经理", "王传福"),
            ("法人代表", "王传福"),
            ("董秘", "李黔"),
            ("独立董事", "张敏、蔡洪平、喻玲"),
            ("证券事务代表", "程燕、吴越"),
            ("上市日期", "2011-06-30"),
            ("网上发行日期", "2011-06-21"),
            ("发行方式", "网下询价配售"),
            ("发行市盈率", "20.47"),
            ("发行总量", "7900万股"),
            ("每股发行价", "18"),
            ("发行总市值", "14.22亿"),
            ("募集资金净额", "13.54亿"),
            ("每股面值", "1"),
            ("定价中签率", "4.49%"),
            ("网下配售中签率", "20.55%"),
            ("首日开盘价", "22"),
            ("首日收盘价", "25.45"),
            ("首日换手率", "87.96%"),
        ],
        "shareholders": [
            ("股东1", "HKSCC NOMINEES LIMITED", "流通H股 | 持股比例 40.3800% | 标签：中国香港、大股东"),
            ("股东2", "王传福", "流通A股、限售流通A股 | 持股比例 16.9000% | 标签：实际控制人、受益所有人"),
            ("股东3", "吕向阳", "流通A股、限售流通A股 | 持股比例 7.8700% | 间接持股比例 4.5735% | 标签：股权质押"),
            ("股东4", "融捷投资控股集团有限公司", "流通A股 | 持股比例 5.1100% | 标签：股权质押"),
            ("股东5", "夏佐全", "流通A股、限售流通A股 | 持股比例 2.7200%"),
            ("股东6", "香港中央结算有限公司", "流通A股 | 持股比例 2.1600%"),
            ("股东7", "张炜", "流通A股 | 持股比例 0.6000%"),
            ("股东8", "王念强", "流通A股 | 持股比例 0.6000%"),
            ("股东9", "全国社保基金一一四组合", "流通A股 | 持股比例 0.4600%"),
            ("股东10", "李柯", "流通A股、限售流通A股 | 持股比例 0.3600%"),
            ("股东11", "比亚迪股份有限公司-2025年员工持股计划", "流通A股 | 持股比例 0.3551%"),
        ],
        "people": [
            ("LISTED-BYD-WCF", "王传福", "男", 1965, "硕士", "listed_chairman", "董事长、执行董事、总裁", "2008-06-11", 16.9, 1, "年龄60岁；薪酬813.9万元；持股数15.41亿"),
            ("LISTED-BYD-LXY", "吕向阳", "男", 1961, "大专", "listed_vice_chairman", "副董事长、非执行董事", "2008-06-11", 7.87, 0, "年龄64岁；薪酬30万元；持股数7.18亿"),
            ("LISTED-BYD-XZQ", "夏佐全", "男", 1962, "硕士", "listed_director", "非执行董事", "2008-06-11", 2.72, 0, "年龄63岁；薪酬30万元；持股数2.48亿"),
            ("LISTED-BYD-CHP", "蔡洪平", "男", 1953, "本科", "listed_independent_director", "独立非执行董事", "2023-09-19", None, 0, "年龄72岁；薪酬30万元"),
            ("LISTED-BYD-ZM", "张敏", "男", 1976, "博士", "listed_independent_director", "独立非执行董事", "2023-09-19", None, 0, "年龄49岁；薪酬30万元"),
            ("LISTED-BYD-YL", "喻玲", "女", 1976, "博士", "listed_independent_director", "独立非执行董事", "2023-09-19", None, 0, "年龄49岁；薪酬30万元"),
            ("LISTED-BYD-ZJP", "赵俭平", "男", 1976, "本科", "listed_vice_president", "副总裁", "2023-05-19", None, 0, "年龄49岁；薪酬769.6万元"),
            ("LISTED-BYD-LHB", "罗红斌", "男", 1965, "硕士", "listed_vice_president", "副总裁", "2014-09-10", 0.0018, 0, "年龄60岁；薪酬1209.9万元；持股数16.59万"),
            ("LISTED-BYD-LZL", "罗忠良", "男", 1978, "硕士", "listed_vice_president", "副总裁", "2024-05-28", 0.0009, 0, "年龄47岁；薪酬732万元；持股数8.51万"),
            ("LISTED-BYD-WCF2", "王传方", "男", 1960, None, "listed_vice_president", "副总裁", "2017-01-03", 0.2904, 0, "年龄65岁；薪酬659.6万元；持股数2647.4万"),
        ],
    },
    "600519.SH": {
        "company_updates": {
            "name": "贵州茅台酒股份有限公司",
            "unified_social_credit_code": "9152000071430580XT",
            "established_on": "1999-11-20",
            "region_province": "贵州省",
            "region_city": "遵义市",
            "industry_category": "白酒制造",
            "subindustry": "白酒制造",
            "operating_status": "存续（在营、开业、在册）",
            "registered_capital_cny": 1252270215.0,
            "paid_in_capital_cny": 1252270215.0,
            "website": "www.moutaichina.com",
            "overview": "贵州茅台酒股份有限公司成立于1999年11月20日，董事长为陈华，公司于2001年8月27日在上海证券交易所上市，股票代码600519.SH，公司主营业务为茅台酒及茅台酱香系列酒。",
        },
        "public_profile": [
            ("成立时间", "1999-11-20", "企查查截图人工补录"),
            ("法定代表人", "陈华", "企查查截图人工补录"),
            ("联系电话", "0851-22386004", "企查查截图人工补录"),
            ("邮箱", "mtmsk@126.com", "企查查截图人工补录"),
            ("官网", "www.moutaichina.com", "企查查截图人工补录"),
            ("注册地址", "贵州省遵义市仁怀市茅台镇", "企查查截图人工补录"),
            ("国标行业", "白酒制造", "企查查截图人工补录"),
            ("企业规模", "大型", "企查查截图人工补录"),
            ("员工人数", "34992（2025年）", "企查查截图人工补录"),
            ("营业收入", "1720.54亿元（2025年）", "企查查截图人工补录"),
            ("所属集团", "贵州茅台集团", "企查查截图人工补录"),
            ("股东", "详见股东信息页（已结构化入库）", "企查查截图人工补录"),
            ("高管", "详见主要人员页（已结构化入库）", "企查查截图人工补录"),
            ("企业概况", "贵州茅台酒股份有限公司成立于1999年11月20日，董事长为陈华，公司于2001年8月27日在上海证券交易所上市，主营业务为茅台酒及茅台酱香系列酒。", "企查查截图人工补录"),
        ],
        "registration": [
            ("统一社会信用代码", "9152000071430580XT"),
            ("组织机构代码", "71430580-X"),
            ("工商注册号", "520000000068765"),
            ("纳税人识别号", "9152000071430580XT"),
            ("登记状态", "存续（在营、开业、在册）"),
            ("注册资本", "125227.0215万元"),
            ("实缴资本", "125227.0215万元"),
            ("企业类型", "其他股份有限公司（上市）"),
            ("营业期限", "1999-11-20 至 无固定期限"),
            ("纳税人资质", "一般纳税人"),
            ("人员规模", "10000人以上"),
            ("参保人数", "21977（2024年报）"),
            ("分支机构参保人数", "11732（2024年报）"),
            ("所属地区", "贵州省遵义市仁怀市"),
            ("登记机关", "贵州省市场监督管理局"),
            ("国标行业", "白酒制造（C1512）"),
            ("英文名", "Kweichow Moutai Co., Ltd."),
            ("经营范围", "茅台酒及系列酒的生产与销售；饮料、食品、包装材料的生产、销售；防伪技术开发、信息产业相关产品的研制、开发；酒店经营管理、住宿、餐饮、娱乐、洗浴及停车场管理服务；车辆运输（不含危险化学品）、维修保养；第二类增值电信业务。"),
        ],
        "listing_info": [
            ("董事长", "陈华"),
            ("总经理", "-"),
            ("法人代表", "陈华"),
            ("董秘", "-"),
            ("独立董事", "郭田勇、盛雷鸣、王鑫"),
            ("证券事务代表", "蔡聪应"),
            ("上市日期", "2001-08-27"),
            ("上市交易所", "上海证券交易所"),
            ("上市板块", "主板"),
            ("上市曾用名", "贵州茅台→G茅台"),
            ("股票简称", "贵州茅台"),
            ("股票代码", "600519.SH"),
            ("总市值", "1.72万亿"),
            ("流通值", "17193.54亿"),
            ("总股本", "12.52亿"),
            ("流通股", "12.52亿"),
            ("预测市盈率", "15.78"),
            ("市净率", "6.35"),
            ("EPS", "21.76"),
            ("表决权差异", "否"),
            ("是否注册制", "否"),
            ("网上发行日期", "2001-07-31"),
            ("发行方式", "网下定价发行"),
            ("发行市盈率", "23.93"),
            ("发行总量", "7150万股"),
            ("每股发行价", "31.39"),
            ("发行总市值", "22.44亿"),
            ("募集资金净额", "22.02亿"),
            ("每股面值", "1"),
            ("定价中签率", "1.13%"),
            ("首日开盘价", "34.51"),
            ("首日收盘价", "35.55"),
            ("首日换手率", "56.83%"),
        ],
        "shareholders": [
            ("股东1", "中国贵州茅台酒厂（集团）有限责任公司", "流通A股 | 持股比例 54.40% | 间接持股比例 2.22% | 标签：省属国企、大股东"),
            ("股东2", "香港中央结算有限公司", "流通A股 | 持股比例 4.69%"),
            ("股东3", "贵州省国有资本运营有限责任公司", "流通A股 | 持股比例 4.55% | 关联产品/机构：贵州金控集团"),
            ("股东4", "贵州茅台酒厂（集团）技术开发有限公司", "流通A股 | 持股比例 2.22%"),
            ("股东5", "中央汇金资产管理有限责任公司", "流通A股 | 持股比例 0.83%"),
            ("股东6", "中国银行股份有限公司-招商中证白酒指数分级证券投资基金", "流通A股 | 持股比例 0.41%"),
            ("股东7", "中国工商银行股份有限公司-华泰柏瑞沪深300交易型开放式指数证券投资基金", "流通A股 | 持股比例 0.40%"),
            ("股东8", "中国工商银行-上证50交易型开放式指数证券投资基金", "流通A股 | 持股比例 0.36%"),
            ("股东9", "国丰兴华（北京）私募基金管理有限公司-鸿鹄志远（上海）私募投资基金有限公司", "流通A股 | 持股比例 0.33%"),
            ("股东10", "中国证券金融股份有限公司", "流通A股 | 持股比例 0.32%"),
        ],
        "people": [
            ("LISTED-MT-CH", "陈华", "男", 1972, "硕士", "listed_chairman", "董事长、董事", "2025-11-28", None, 1, "年龄54岁；法定代表人；受益所有人"),
            ("LISTED-MT-WL", "王莉", "女", 1972, "硕士", "listed_director", "董事、代理总经理", "2000-12-01", None, 0, "年龄54岁；标签：限制高消费"),
            ("LISTED-MT-ZX", "周雪", "女", 1978, "本科", "listed_director", "董事", "2025-05-19", None, 0, "年龄48岁"),
            ("LISTED-MT-WF", "韦芳", "女", 1972, "本科", "listed_employee_director", "职工董事", "2024-10-18", None, 0, "年龄54岁；薪酬89.8万元"),
            ("LISTED-MT-GTY", "郭田勇", "男", 1968, "博士", "listed_independent_director", "独立董事", "2022-06-16", None, 0, "年龄58岁；薪酬20万元"),
            ("LISTED-MT-SLM", "盛雷鸣", "男", 1970, "博士", "listed_independent_director", "独立董事", "2022-06-16", None, 0, "年龄56岁；薪酬20万元"),
            ("LISTED-MT-WX", "王鑫", "男", 1977, "博士", "listed_independent_director", "独立董事", "2023-12-06", None, 0, "年龄49岁；薪酬20万元"),
            ("LISTED-MT-ZZQ", "钟正强", "男", 1971, "本科", "listed_vice_president", "副总经理", "2015-07-13", None, 0, "年龄55岁；薪酬113.81万元"),
            ("LISTED-MT-ZXU", "张旭", "男", 1974, "本科", "listed_vice_president", "副总经理", "2024-08-16", None, 0, "年龄52岁；薪酬57.44万元"),
            ("LISTED-MT-XP", "向平", "男", 1972, "硕士", "listed_vice_president", "副总经理", "2024-08-16", None, 0, "年龄54岁；薪酬62.89万元"),
        ],
        "branches": [
            ("贵州茅台酒股份有限公司和义兴酒业分公司", "branch", "负责人：黄旭；地区：贵州省遵义市仁怀市；成立日期：2020-09-24；状态：存续"),
            ("贵州茅台酒股份有限公司茅台国际大酒店", "branch", "负责人：谭娟；地区：贵州省遵义市仁怀市；成立日期：2016-04-29；状态：存续"),
            ("贵州茅台酒股份有限公司遵义水厂分公司", "branch", "负责人：薛建华；地区：贵州省遵义市红花岗区；成立日期：2022-08-25；状态：注销"),
        ],
    },
    "600998.SH": {
        "company_updates": {
            "name": "九州通医药集团股份有限公司",
            "unified_social_credit_code": "9142000071451795XA",
            "established_on": "1999-03-09",
            "region_province": "湖北省",
            "region_city": "武汉市",
            "industry_category": "药品代理",
            "subindustry": "西药批发",
            "operating_status": "存续（在营、开业、在册）",
            "registered_capital_cny": 5042470234.0,
            "paid_in_capital_cny": 5042470234.0,
            "website": "www.jztey.com",
            "overview": "九州通医药集团股份有限公司成立于1999年3月，董事长为刘长云，公司于2010年11月在上海证券交易所上市，股票代码600998.SH，作为科技驱动型的全链医药产业综合服务商开展业务。",
        },
        "public_profile": [
            ("成立时间", "1999-03-09", "企查查截图人工补录"),
            ("法定代表人", "刘长云", "企查查截图人工补录"),
            ("联系电话", "027-84683017", "企查查截图人工补录"),
            ("邮箱", "jztdmc@jztey.com", "企查查截图人工补录"),
            ("官网", "www.jztey.com", "企查查截图人工补录"),
            ("注册地址", "湖北省武汉市汉阳区龙兴西街5号", "企查查截图人工补录"),
            ("国标行业", "西药批发", "企查查截图人工补录"),
            ("企业规模", "大型", "企查查截图人工补录"),
            ("员工人数", "29862（2025年）", "企查查截图人工补录"),
            ("营业收入", "1613.90亿元（2025年）", "企查查截图人工补录"),
            ("所属集团", "九州通集团", "企查查截图人工补录"),
            ("曾用名", "九州通集团有限公司（2003-10 至 2008-11）", "企查查截图人工补录"),
            ("股东", "详见股东信息页（已结构化入库）", "企查查截图人工补录"),
            ("高管", "详见主要人员页（已结构化入库）", "企查查截图人工补录"),
            ("实控人", "刘长云", "依据主要人员及股东截图人工补录"),
            ("受益所有人", "刘长云", "依据主要人员及股东截图人工补录"),
        ],
        "registration": [
            ("统一社会信用代码", "9142000071451795XA"),
            ("组织机构代码", "71451795-X"),
            ("工商注册号", "420000400000103"),
            ("纳税人识别号", "9142000071451795XA"),
            ("登记状态", "存续（在营、开业、在册）"),
            ("注册资本", "504247.0234万元"),
            ("实缴资本", "504247.0234万元"),
            ("企业类型", "股份有限公司（外商投资、上市）"),
            ("营业期限", "1999-03-09 至 无固定期限"),
            ("纳税人资质", "一般纳税人"),
            ("人员规模", "1000-1999人"),
            ("参保人数", "1636（2024年报）"),
            ("分支机构参保人数", "3（2024年报）"),
            ("所属地区", "湖北省武汉市汉阳区"),
            ("登记机关", "湖北省市场监督管理局"),
            ("进出口企业代码", "420171451795X"),
            ("英文名", "Jointown Pharmaceutical Group Co., Ltd."),
            ("经营范围", "药品批发、第三类医疗器械经营、药品互联网信息服务、酒类经营、医药器械租赁、食品销售、药品进出口、中药饮片代煎服务、第一类增值电信业务、第二类增值电信业务、技术咨询服务、化妆品及日用百货销售、供应链服务、物流仓储、软件开发、人工智能基础软件及应用软件开发、数据处理与存储支持服务、互联网数据服务、健康咨询、远程健康管理、物业管理、会议及展览服务、企业管理及市场营销咨询等。"),
        ],
        "listing_info": [
            ("董事长", "刘长云"),
            ("总经理", "龚翼华"),
            ("法人代表", "刘长云"),
            ("董秘", "刘志峰"),
            ("独立董事", "汤谷良、陆银娣、曾湘泉、王瑛、艾华"),
            ("证券事务代表", "张溪"),
            ("上市日期", "2010-11-02"),
            ("上市交易所", "上海证券交易所"),
            ("上市板块", "主板"),
            ("上市曾用名", "-"),
            ("股票简称", "九州通"),
            ("股票代码", "600998.SH"),
            ("总市值", "254.64亿"),
            ("流通值", "254.64亿"),
            ("总股本", "50.42亿"),
            ("流通股", "50.42亿"),
            ("预测市盈率", "8.68"),
            ("市净率", "0.93"),
            ("EPS", "0.14"),
            ("表决权差异", "否"),
            ("是否注册制", "否"),
            ("网上发行日期", "2010-10-25"),
            ("发行方式", "网下询价配售"),
            ("发行市盈率", "65"),
            ("发行总量", "1.5亿股"),
            ("每股发行价", "13"),
            ("发行总市值", "19.5亿"),
            ("募集资金净额", "18.93亿"),
            ("每股面值", "1"),
            ("定价中签率", "0.64%"),
            ("网下配售中签率", "0.89%"),
            ("首日开盘价", "18.25"),
            ("首日收盘价", "18.98"),
            ("首日换手率", "83.29%"),
        ],
        "shareholders": [
            ("股东1", "上海弘康实业投资有限公司", "持股比例 21.58% | 标签：大股东、股权质押"),
            ("股东2", "狮龙国际集团（香港）有限公司", "持股比例 11.41%"),
            ("股东3", "楚昌投资集团有限公司", "持股比例 9.11% | 间接持股比例 24.4027% | 标签：股权质押"),
            ("股东4", "中山广银投资有限公司", "持股比例 6.65% | 标签：股权质押"),
            ("股东5", "北京点金投资有限公司", "持股比例 5.48% | 关联产品/机构：楚昌投资"),
            ("股东6", "中国信达资产管理股份有限公司", "持股比例 4.99% | 关联产品/机构：中国信达（01359.HK）"),
            ("股东7", "香港中央结算有限公司", "持股比例 2.08%"),
            ("股东8", "全国社保基金六零四组合", "持股比例 1.42%"),
            ("股东9", "刘树林", "持股比例 1.40% | 间接持股比例 11.9469%"),
            ("股东10", "长城国泰（舟山）产业并购重组基金合伙企业（有限合伙）", "持股比例 1.36% | 关联产品/机构：长城股权基金"),
        ],
        "people": [
            ("LISTED-JT-LCY", "刘长云", "男", None, "博士", "listed_chairman", "董事长、非独立董事", "2020-11-05", None, 1, "薪酬121.1万元"),
            ("LISTED-JT-GYH", "龚翼华", "男", 48, "硕士", "listed_vice_chairman", "副董事长、非独立董事、总经理", "2013-01-28", 0.0717, 0, "薪酬77.49万元；持股361.63万"),
            ("LISTED-JT-LDP", "刘登攀", "男", None, "硕士", "listed_vice_chairman", "副董事长、非独立董事", "2023-11-15", None, 0, "薪酬193.45万元"),
            ("LISTED-JT-LZN", "刘兆年", "男", 66, "博士", "listed_vice_chairman", "副董事长、非独立董事", "2008-11-16", 1.1983, 0, "薪酬82.25万元；持股6042.29万"),
            ("LISTED-JT-LYC", "刘义常", "男", None, "本科", "listed_vice_chairman", "副董事长、非独立董事、业务总裁", "2017-04-23", None, 0, "薪酬45.3万元"),
            ("LISTED-JT-LSL", "刘树林", "男", None, "高中", "listed_honorary_chairman", "名誉副董事长", "2023-11-15", 1.4, 0, "持股7081.8万"),
            ("LISTED-JT-HW", "贺威", "男", 40, "本科", "listed_director", "非独立董事、副总裁", "2023-11-15", 0.0053, 0, "薪酬60.37万元；持股26.91万"),
            ("LISTED-JT-WQ", "王琦", "男", 64, "本科", "listed_director", "非独立董事", "2023-11-15", None, 0, None),
            ("LISTED-JT-WXS", "吴雪松", "男", 53, "本科", "listed_director", "非独立董事", "2023-11-15", None, 0, None),
            ("LISTED-JT-WZL", "吴志龙", "男", None, "硕士", "listed_employee_director", "职工代表董事", "2025-05-22", None, 0, "薪酬14.31万元"),
            ("LISTED-JT-LYD", "陆银娣", "女", 64, "硕士", "listed_independent_director", "独立董事", "2020-11-05", None, 0, "薪酬20万元"),
            ("LISTED-JT-AH", "艾华", "男", 67, "博士", "listed_independent_director", "独立董事", "2020-11-05", 0.0001, 0, "薪酬20万元；持股5382"),
            ("LISTED-JT-WY", "王瑛", "女", None, "博士", "listed_independent_director", "独立董事", "2025-05-23", None, 0, "薪酬12.12万元"),
            ("LISTED-JT-TGL", "汤谷良", "男", 64, "博士", "listed_independent_director", "独立董事", "2020-11-05", None, 0, "薪酬20万元"),
            ("LISTED-JT-ZXQ", "曾湘泉", "男", 71, "博士", "listed_independent_director", "独立董事", "2020-11-05", None, 0, "薪酬20万元"),
            ("LISTED-JT-CWJ", "陈卫俊", "男", 46, "本科", "listed_vice_president", "副总经理", "2023-11-15", None, 0, "薪酬275.07万元"),
            ("LISTED-JT-GL", "郭磊", "女", 48, "硕士", "listed_vice_president", "副总经理", "2014-11-21", 0.0176, 0, "薪酬41.08万元；持股88.8万"),
            ("LISTED-JT-XZJ", "许志君", "男", 50, "硕士", "listed_vice_president", "副总经理", "2023-11-15", None, 0, "薪酬146万元"),
            ("LISTED-JT-SXL", "苏熙凌", "男", None, "硕士", "listed_vice_president", "副总经理、REITs首席运营官", "2025-04-26", None, 0, "薪酬48.22万元"),
            ("LISTED-JT-WQB", "王启兵", "男", 62, "本科", "listed_vice_president", "副总经理", "2017-04-23", 0.0056, 0, "薪酬143.58万元；持股28.15万"),
            ("LISTED-JT-YJM", "杨菊美", "女", 51, "本科", "listed_vice_president", "副总经理", "2016-04-23", 0.0134, 0, "薪酬43.4万元；持股67.81万"),
            ("LISTED-JT-YN", "杨聂", "男", 44, "硕士", "listed_vice_president", "副总经理", "2021-04-25", 0.0051, 0, "薪酬40.57万元；持股25.56万"),
            ("LISTED-JT-ZQS", "张青松", "男", 48, "硕士", "listed_vice_president", "副总经理", "2021-02-04", 0.0003, 0, "薪酬43.7万元；持股1.35万"),
            ("LISTED-JT-LZF", "刘志峰", "男", None, "本科", "listed_board_secretary", "副总经理、董事会秘书", "2022-04-23", None, 0, "薪酬41.22万元"),
            ("LISTED-JT-QM", "全铭", "女", None, "硕士", "listed_vice_president", "副总经理", "2020-12-26", None, 0, "薪酬54.12万元"),
            ("LISTED-JT-XXY", "夏晓益", "男", 48, "本科", "listed_finance_director", "财务总监", "2023-11-15", None, 0, "薪酬34.08万元"),
        ],
    },
    "600612.SH": {
        "company_updates": {
            "name": "老凤祥股份有限公司",
            "unified_social_credit_code": "9131000060720072X4",
            "established_on": "1992-11-11",
            "region_province": "上海市",
            "region_city": "上海市",
            "industry_category": "珠宝首饰制造",
            "subindustry": "珠宝首饰及有关物品制造",
            "operating_status": "存续（在营、开业、在册）",
            "registered_capital_cny": 523117764.0,
            "paid_in_capital_cny": 523117764.0,
            "website": "www.laofengxiang.com",
            "overview": "老凤祥股份有限公司成立于1992年11月11日，董事长为杨奕，企业属性为国有企业，公司于1992年8月14日在上交所上市，股票代码600612.SH，业务覆盖黄金、铂金、珠宝首饰等。",
        },
        "public_profile": [
            ("成立时间", "1992-11-11", "企查查截图人工补录"),
            ("法定代表人", "杨奕", "企查查截图人工补录"),
            ("联系电话", "021-64833388", "企查查截图人工补录"),
            ("邮箱", "lfxgf_618@sina.com", "企查查截图人工补录"),
            ("官网", "www.laofengxiang.com", "企查查截图人工补录"),
            ("注册地址", "上海市黄浦区南京西路190号四层、五层", "企查查截图人工补录"),
            ("通信地址", "凯旋路2588号-6幢（邮编200030）（2024年报）", "企查查截图人工补录"),
            ("国标行业", "珠宝首饰及有关物品制造", "企查查截图人工补录"),
            ("企业规模", "大型", "企查查截图人工补录"),
            ("员工人数", "2985（2025年）", "企查查截图人工补录"),
            ("营业收入", "528.23亿元（2025年）", "企查查截图人工补录"),
            ("所属集团", "老凤祥", "企查查截图人工补录"),
            ("曾用名", "中国第一铅笔股份有限公司（1998-12 至 2009-07）", "企查查截图人工补录"),
            ("股东", "详见股东信息页（已结构化入库）", "企查查截图人工补录"),
            ("高管", "详见主要人员页（已结构化入库）", "企查查截图人工补录"),
            ("实控人", "上海市黄浦区国有资产监督管理委员会（上海市黄浦区集体资产监督管理委员会）", "依据股东截图人工补录"),
            ("受益所有人", "杨奕", "依据主要人员截图人工补录"),
        ],
        "registration": [
            ("统一社会信用代码", "9131000060720072X4"),
            ("组织机构代码", "60720072-X"),
            ("工商注册号", "310000400026404"),
            ("纳税人识别号", "9131000060720072X4"),
            ("登记状态", "存续（在营、开业、在册）"),
            ("注册资本", "52311.7764万元"),
            ("实缴资本", "52311.7764万元"),
            ("企业类型", "股份有限公司（港澳台投资、上市）"),
            ("营业期限", "1992-11-11 至 无固定期限"),
            ("纳税人资质", "一般纳税人"),
            ("人员规模", "100-199人"),
            ("参保人数", "100（2024年报）"),
            ("所属地区", "上海市黄浦区"),
            ("登记机关", "上海市市场监督管理局"),
            ("进出口企业代码", "310060720072X"),
            ("英文名", "Lao FENG Xiang Co., Ltd."),
            ("经营范围", "生产经营金银制品、珠宝、钻石与相关产品及设备、工艺美术品（文物法规规定的除外）、旅游工艺品与相关产品及原料、文教用品与相关原料及设备，从事上述商品的批发、零售、佣金代理及进出口业务；物业管理；自有房产租赁；典当、拍卖（限已批准的子公司经营）；以独资、合资、合作经营形式投资兴办鼓励类、允许类企业。"),
        ],
        "listing_info": [
            ("董事长", "杨奕"),
            ("总经理", "黄骅"),
            ("法人代表", "杨奕"),
            ("董秘", "邱建敏"),
            ("独立董事", "张其秀、俞铁成、马民良"),
            ("证券事务代表", "邹岩"),
            ("上市日期", "1992-08-14"),
            ("上市交易所", "上海证券交易所"),
            ("上市板块", "主板"),
            ("上市曾用名", "第一铅笔→G中铅→第一铅笔→中国铅笔"),
            ("股票简称", "老凤祥"),
            ("股票代码", "600612.SH"),
            ("总市值", "205.32亿"),
            ("流通值", "124.47亿"),
            ("总股本", "5.23亿"),
            ("流通股", "5.23亿"),
            ("预测市盈率", "9.38"),
            ("市净率", "1.5"),
            ("EPS", "1.0458"),
            ("表决权差异", "否"),
            ("是否注册制", "否"),
            ("网上发行日期", "1992-06-13"),
            ("发行方式", "其他发行方式"),
            ("发行市盈率", "-"),
            ("发行总量", "100.79万股"),
            ("每股发行价", "40"),
            ("发行总市值", "4031.6万"),
            ("募集资金净额", "-"),
            ("每股面值", "10"),
            ("定价中签率", "-"),
            ("网下配售中签率", "-"),
            ("首日开盘价", "142"),
            ("首日收盘价", "152"),
            ("首日换手率", "276.18%"),
        ],
        "shareholders": [
            ("股东1", "上海市黄浦区国有资产监督管理委员会（上海市黄浦区集体资产监督管理委员会）", "持股比例 42.09% | 标签：大股东、实际控制人"),
            ("股东2", "SHENWAN HONGYUAN NOMINEES(H.K.)LIMITED", "持股比例 1.32% | 流通B股"),
            ("股东3", "GUOTAI JUNAN SECURITIES(HONG KONG)LIMITED", "持股比例 0.99% | 流通B股"),
            ("股东4", "中国建设银行股份有限公司-国泰双利债券证券投资基金", "持股比例 0.93%"),
            ("股东5", "龙悦网络有限公司", "持股比例 0.92% | 中国香港"),
            ("股东6", "VANGUARD TOTAL INTERNATIONAL STOCK INDEX FUND", "持股比例 0.60% | 流通B股"),
            ("股东7", "NORGES BANK", "持股比例 0.55% | 挪威"),
            ("股东8", "VANGUARD EMERGING MARKETS STOCK INDEX FUND", "持股比例 0.50% | 流通B股"),
            ("股东9", "EQ EMERGING DIVIDEND FUND", "持股比例 0.50% | 流通B股"),
            ("股东10", "FEDERATED HERMES GLOBAL INVESTMENT FD(CAYMAN)MASTER,SPC OBOAFTAO FEDERATED HERMES EMG ASIA EQUITY FD MASTER S.P.", "持股比例 0.47% | 流通B股"),
        ],
        "people": [
            ("LISTED-LFX-YY", "杨奕", "男", 54, "硕士", "listed_chairman", "董事长、非独立董事", "2020-06-16", None, 1, "薪酬117.4万元"),
            ("LISTED-LFX-HH", "黄骅", "男", 57, "本科", "listed_vice_chairman", "副董事长、非独立董事、总经理", "2014-06-16", None, 0, "薪酬103.52万元"),
            ("LISTED-LFX-CZH", "陈智海", "男", 62, "博士", "listed_director", "非独立董事", "2023-05-22", None, 0, None),
            ("LISTED-LFX-SSH", "沈顺辉", "男", 62, "硕士", "listed_director", "非独立董事", "2020-06-16", None, 0, None),
            ("LISTED-LFX-LJ", "李军", "女", 57, "本科", "listed_director", "非独立董事、副总经理", "2016-04-26", 0.0016, 0, "薪酬80.4万元；持股8580"),
            ("LISTED-LFX-ZLT", "朱黎庭", "男", 65, "本科", "listed_independent_director", "独立董事", "2020-06-16", None, 0, None),
            ("LISTED-LFX-MML", "马民良", "男", 70, "硕士", "listed_independent_director", "独立董事", "2020-06-16", None, 0, "薪酬8万元"),
            ("LISTED-LFX-ZQX", "张其秀", "女", 71, "本科", "listed_independent_director", "独立董事", "2008-05-20", None, 0, "薪酬8万元"),
            ("LISTED-LFX-YTC", "俞铁成", "男", 51, "硕士", "listed_independent_director", "独立董事", "2023-05-22", None, 0, "薪酬8万元"),
            ("LISTED-LFX-CXJ", "蔡旭姣", "女", 44, "硕士", "listed_vice_president", "副总经理", "2023-06-16", None, 0, "薪酬87万元"),
            ("LISTED-LFX-WYZ", "王永忠", "男", 54, "硕士", "listed_vice_president", "副总经理", "2008-05-20", None, 0, "薪酬221.96万元"),
            ("LISTED-LFX-SBY", "孙斌烨", "男", 60, "本科", "listed_vice_president", "副总经理", "2024-08-01", None, 0, "薪酬93.48万元"),
            ("LISTED-LFX-SL", "史亮", "男", 65, "本科", "listed_vice_president", "副总经理", "2020-06-16", None, 0, "薪酬62.28万元"),
            ("LISTED-LFX-QJM", "邱建敏", "男", 53, "硕士", "listed_board_secretary", "董事会秘书", "2019-10-24", None, 0, "薪酬85.18万元"),
            ("LISTED-LFX-LXJ", "凌晓静", "女", 46, "本科", "listed_finance_director", "财务总监", "2020-06-16", None, 0, "薪酬92.93万元"),
        ],
        "branches": [
            ("中国第一铅笔股份有限公司卢湾分公司", "branch", "负责人：李继国；地区：上海市徐汇区；成立日期：2006-11-07；状态：注销"),
            ("中国第一铅笔股份有限公司高蒂丝化妆品分公司", "branch", "负责人：朱惠毅；地区：上海市虹口区；成立日期：1992-12-03；状态：吊销"),
            ("中国第一铅笔股份有限公司职工技术协会", "branch", "负责人：黄明旭；地区：上海市虹口区；成立日期：1992-06-19；状态：注销"),
        ],
    },
    "600196.SH": {
        "company_updates": {
            "name": "上海复星医药（集团）股份有限公司",
            "unified_social_credit_code": "913100001330605412",
            "established_on": "1995-05-31",
            "region_province": "上海市",
            "region_city": "上海市",
            "industry_category": "化学制剂制造",
            "subindustry": "化学药品制剂制造",
            "operating_status": "存续（在营、开业、在册）",
            "registered_capital_cny": 2670429325.0,
            "paid_in_capital_cny": 2670429325.0,
            "website": "www.fosunpharma.com",
            "overview": "上海复星医药（集团）股份有限公司成立于1995年5月31日，董事长为陈玉卿，公司于1998年8月7日在上交所上市（600196.SH），并于2012年10月30日在香港联交所上市。",
        },
        "public_profile": [
            ("成立时间", "1995-05-31", "企查查截图人工补录"),
            ("法定代表人", "陈玉卿", "企查查截图人工补录"),
            ("联系电话", "021-33987000", "企查查截图人工补录"),
            ("邮箱", "ir@fosunpharma.com", "企查查截图人工补录"),
            ("官网", "www.fosunpharma.com", "企查查截图人工补录"),
            ("注册地址", "曹杨路510号9楼", "企查查截图人工补录"),
            ("通信地址", "上海市宜山路1289号A楼（2024年报）", "企查查截图人工补录"),
            ("国标行业", "化学药品制剂制造", "企查查截图人工补录"),
            ("企业规模", "大型", "企查查截图人工补录"),
            ("员工人数", "40603（2025年）", "企查查截图人工补录"),
            ("营业收入", "416.62亿元（2025年）", "企查查截图人工补录"),
            ("所属集团", "复星集团", "企查查截图人工补录"),
            ("曾用名", "上海复星实业股份有限公司（1995-05 至 -）", "企查查截图人工补录"),
            ("股东", "详见股东信息页（已结构化入库）", "企查查截图人工补录"),
            ("高管", "详见主要人员页（已结构化入库）", "企查查截图人工补录"),
        ],
        "registration": [
            ("统一社会信用代码", "913100001330605412"),
            ("组织机构代码", "13306054-1"),
            ("工商注册号", "310000000036602"),
            ("纳税人识别号", "913100001330605412"),
            ("登记状态", "存续（在营、开业、在册）"),
            ("注册资本", "267042.9325万元"),
            ("实缴资本", "267042.9325万元"),
            ("企业类型", "其他股份有限公司（上市）"),
            ("营业期限", "1998-03-31 至 无固定期限"),
            ("纳税人资质", "一般纳税人"),
            ("人员规模", "100-199人"),
            ("参保人数", "158（2024年报）"),
            ("所属地区", "上海市普陀区"),
            ("登记机关", "上海市市场监督管理局"),
            ("进出口企业代码", "3100133060541"),
            ("英文名", "Shanghai Fosun Pharmaceutical (Group) Co., Ltd."),
            ("经营范围", "生物化学产品、试剂、生物四技服务、自产自销产品、仪器仪表、电子产品、计算机、化工原料（除危险品）、咨询服务；经营本企业自产产品及相关技术的出口业务，经营本企业生产、科研所需的原辅材料、机械设备、仪器仪表、零配件及相关技术的进口业务。"),
        ],
        "listing_info": [
            ("董事长", "陈玉卿"),
            ("总经理", "刘毅"),
            ("法人代表", "陈玉卿"),
            ("董秘", "董晓婕"),
            ("独立董事", "王全弟、余梓山、Chen Penghui、杨玉成"),
            ("证券事务代表", "-"),
            ("上市日期", "1998-08-07"),
            ("上市交易所", "上海证券交易所"),
            ("上市板块", "主板"),
            ("上市曾用名", "复星实业→复星医药→G复星"),
            ("股票简称", "复星医药"),
            ("股票代码", "600196.SH"),
            ("总市值", "662.80亿"),
            ("流通值", "525.81亿"),
            ("总股本", "26.7亿"),
            ("流通股", "26.7亿"),
            ("预测市盈率", "19.03"),
            ("市净率", "1.35"),
            ("EPS", "0.33"),
            ("表决权差异", "否"),
            ("是否注册制", "否"),
            ("网上发行日期", "1998-06-25"),
            ("发行方式", "网下定价发行"),
            ("发行市盈率", "15"),
            ("发行总量", "5000万股"),
            ("每股发行价", "7.15"),
            ("发行总市值", "3.58亿"),
            ("募集资金净额", "3.48亿"),
            ("每股面值", "1"),
            ("定价中签率", "0.33%"),
            ("网下配售中签率", "-"),
            ("首日开盘价", "25"),
            ("首日收盘价", "24.7"),
            ("首日换手率", "75.36%"),
        ],
        "shareholders": [
            ("股东1", "上海复星高科技（集团）有限公司", "持股比例 33.32% | 标签：大股东、股权质押 | 关联产品/机构：复星国际"),
            ("股东2", "HKSCC NOMINEES LIMITED", "持股比例 20.65% | 流通H股"),
            ("股东3", "香港中央结算有限公司", "持股比例 1.89%"),
            ("股东4", "上海银行股份有限公司-银华中证创新药产业交易型开放式指数证券投资基金", "持股比例 0.72%"),
            ("股东5", "中国银行股份有限公司-招商国证生物医药指数分级证券投资基金", "持股比例 0.70%"),
            ("股东6", "中国证券金融股份有限公司", "持股比例 0.70% | 关联产品/机构：中证金融"),
            ("股东7", "中国建设银行股份有限公司-易方达沪深300医药卫生交易型开放式指数证券投资基金", "持股比例 0.67%"),
            ("股东8", "熊立武", "持股比例 0.53%"),
            ("股东9", "阿布达比投资局-自有资金", "持股比例 0.48%"),
            ("股东10", "全国社保基金一一二组合", "持股比例 0.45%"),
        ],
        "people": [
            ("LISTED-FX-CYQ", "陈玉卿", "男", 51, "本科", "listed_chairman", "董事长、执行董事", "2025-04-29", 0.0058, 1, "薪酬177.81万元；持股15.4万"),
            ("LISTED-FX-GXH", "关晓晖", "女", 55, "硕士", "listed_joint_chairman", "联席董事长、执行董事", "2021-12-07", 0.011, 0, "薪酬605.47万元；持股29.27万"),
            ("LISTED-FX-WDY", "文德镛", "男", 55, "硕士", "listed_vice_chairman", "副董事长、执行董事", "2022-08-10", 0.0038, 0, "薪酬837.91万元；持股10.17万"),
            ("LISTED-FX-CQY", "陈启宇", "男", 54, "硕士", "listed_director", "非执行董事", "2020-10-29", 0.0043, 0, "持股11.41万"),
            ("LISTED-FX-PDH", "潘东辉", "男", 57, "硕士", "listed_director", "非执行董事", "2020-06-30", None, 0, None),
            ("LISTED-FX-WKX", "王可心", "男", 62, "本科", "listed_executive_director", "执行董事", "2021-12-07", 0.0121, 0, "薪酬954.53万元；持股32.35万"),
            ("LISTED-FX-LYI", "刘毅", "男", 51, "博士", "listed_ceo", "执行董事、总裁、首席执行官", "2025-06-24", 0.0013, 0, "薪酬356.6万元；持股3.54万"),
            ("LISTED-FX-YJ", "严佳", "女", 46, "本科", "listed_employee_director", "职工董事、总会计师", "2022-06-01", 0.0002, 0, "薪酬263.36万元；持股6271"),
            ("LISTED-FX-WQD", "王全弟", "男", 76, "本科", "listed_independent_director", "独立非执行董事", "2022-06-01", None, 0, "薪酬40万元"),
            ("LISTED-FX-YYC", "杨玉成", "男", 61, "博士", "listed_independent_director", "独立非执行董事", "2025-06-24", None, 0, "薪酬17.5万元"),
            ("LISTED-FX-YZS", "余梓山", "男", 70, "硕士", "listed_independent_director", "独立非执行董事", "2022-06-01", None, 0, "薪酬40万元"),
            ("LISTED-FX-CPH", "Chen Penghui", "男", 54, "硕士", "listed_independent_director", "独立非执行董事", "2025-06-24", None, 0, "薪酬17.5万元"),
            ("LISTED-FX-FRL", "冯蓉丽", "女", 51, "硕士", "listed_executive_president", "执行总裁", "2024-01-17", 0.0019, 0, "薪酬339.7万元；持股5.09万"),
            ("LISTED-FX-LJ", "李静", "女", 54, "硕士", "listed_joint_president", "联席总裁", "2025-06-24", 0.0019, 0, "薪酬778.53万元；持股5.09万"),
            ("LISTED-FX-XW", "Xingli Wang", "男", 64, "博士", "listed_joint_president", "联席总裁", "2025-06-24", None, 0, "薪酬975.12万元"),
            ("LISTED-FX-WZ", "Wenjie Zhang", "男", 59, "硕士", "listed_joint_president", "联席总裁", "2025-06-24", None, 0, "薪酬1096.52万元"),
            ("LISTED-FX-YFB", "袁方兵", "男", 51, "硕士", "listed_vice_president", "副总裁", "2024-07-01", None, 0, "薪酬181.99万元"),
            ("LISTED-FX-CJS", "蔡婧姝", "女", 42, "硕士", "listed_vice_president", "副总裁", "2026-03-24", None, 0, None),
            ("LISTED-FX-DXJ", "董晓婕", "女", 45, "硕士", "listed_board_secretary", "副总裁、董事会秘书", "2016-06-07", 0.0019, 0, "薪酬214.59万元；持股5.04万"),
            ("LISTED-FX-SL", "苏莉", "女", 55, "本科", "listed_vice_president", "副总裁", "2022-01-04", 0.0007, 0, "薪酬339.72万元；持股1.98万"),
            ("LISTED-FX-JH", "纪皓", "男", 52, "硕士", "listed_vice_president", "副总裁", "2022-01-04", 0.0006, 0, "薪酬222万元；持股1.54万"),
            ("LISTED-FX-ZY", "朱悦", "女", 49, "博士", "listed_vice_president", "副总裁", "2022-01-04", 0.001, 0, "薪酬289.92万元；持股2.54万"),
            ("LISTED-FX-MLY", "孟凌媛", "女", 48, "本科", "listed_vice_president", "副总裁", "2026-01-26", None, 0, None),
            ("LISTED-FX-LLL", "吕力琅", "女", 49, "博士", "listed_vice_president", "副总裁", "2023-07-28", None, 0, "薪酬380.71万元"),
            ("LISTED-FX-HZ", "黄智", "男", None, "硕士", "listed_senior_vice_president", "高级副总裁、首席财务官", "2026-04-02", None, 0, None),
            ("LISTED-FX-CZY", "陈战宇", "男", 55, "硕士", "listed_senior_vice_president", "高级副总裁", "2024-09-02", 0.0012, 0, "薪酬189.36万元；持股3.3万"),
            ("LISTED-FX-HH", "胡航", "男", 43, "硕士", "listed_senior_vice_president", "高级副总裁", "2022-01-04", 0.0007, 0, "薪酬323.52万元；持股2万"),
            ("LISTED-FX-WDH", "王冬华", "男", 57, "硕士", "listed_senior_vice_president", "高级副总裁", "2020-10-29", 0.0019, 0, "薪酬296万元；持股5.09万"),
            ("LISTED-FX-XL", "Xiang Li", "男", 61, "博士", "listed_senior_vice_president", "高级副总裁", "2025-03-31", None, 0, "薪酬351.06万元"),
        ],
    },
}


def insert(cur, table, data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    cur.execute(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        tuple(data.values()),
    )
    return cur.lastrowid


def seed_sources(cur):
    source_ids = {}
    sources = [
        {
            "source_name": "client_upload",
            "source_type": "customer_provided",
            "authority_level": "customer_authorized",
            "access_mode": "upload",
            "description": "Enterprise uploaded PDF or image package",
            "base_url": None,
            "default_reliability": 0.82,
        },
        {
            "source_name": "official_registry",
            "source_type": "public_registry",
            "authority_level": "official",
            "access_mode": "manual_capture",
            "description": "National enterprise credit publicity and local registries",
            "base_url": "https://www.gsxt.gov.cn/",
            "default_reliability": 0.95,
        },
        {
            "source_name": "court_public",
            "source_type": "judicial_public",
            "authority_level": "official",
            "access_mode": "manual_capture",
            "description": "Court enforcement and judgement websites",
            "base_url": "https://zxgk.court.gov.cn/",
            "default_reliability": 0.94,
        },
        {
            "source_name": "tax_summary",
            "source_type": "authorized_summary",
            "authority_level": "customer_authorized",
            "access_mode": "manual_entry",
            "description": "Enterprise provided tax filing summary",
            "base_url": None,
            "default_reliability": 0.78,
        },
        {
            "source_name": "bank_statement_summary",
            "source_type": "authorized_summary",
            "authority_level": "customer_authorized",
            "access_mode": "upload",
            "description": "Enterprise bank statement summary",
            "base_url": None,
            "default_reliability": 0.8,
        },
        {
            "source_name": "manual_research",
            "source_type": "analyst_note",
            "authority_level": "internal",
            "access_mode": "manual_entry",
            "description": "Analyst consolidated note or screenshot summary",
            "base_url": None,
            "default_reliability": 0.72,
        },
        {
            "source_name": "ocr_extraction",
            "source_type": "system_process",
            "authority_level": "internal",
            "access_mode": "system_generated",
            "description": "OCR and NLP extraction output",
            "base_url": None,
            "default_reliability": 0.7,
        },
        {
            "source_name": "model_inference",
            "source_type": "ai_output",
            "authority_level": "internal",
            "access_mode": "system_generated",
            "description": "Model-generated hypothesis or summary",
            "base_url": None,
            "default_reliability": 0.62,
        },
        {
            "source_name": "akshare_cache",
            "source_type": "public_market_cache",
            "authority_level": "public",
            "access_mode": "local_cache_import",
            "description": "Local AkShare-backed listed-company cache from the due diligence engine project",
            "base_url": None,
            "default_reliability": 0.9,
        },
        {
            "source_name": "cninfo_report",
            "source_type": "public_disclosure",
            "authority_level": "official",
            "access_mode": "local_cache_import",
            "description": "Listed company annual report disclosure links cached from cninfo",
            "base_url": "http://www.cninfo.com.cn/",
            "default_reliability": 0.95,
        },
    ]
    for source in sources:
        source_ids[source["source_name"]] = insert(cur, "source_registry", source)
    return source_ids


def seed_validation_rules(cur):
    rule_ids = {}
    rules = [
        {
            "rule_code": "revenue_triangle_check",
            "rule_name": "Revenue triangle check",
            "dimension": "authenticity",
            "severity_default": "high",
            "rule_logic": "Compare self-reported revenue, tax declared revenue, and bank receipts by month.",
            "manual_review_required": 1,
        },
        {
            "rule_code": "contract_cash_match",
            "rule_name": "Contract to invoice to cash check",
            "dimension": "authenticity",
            "severity_default": "medium",
            "rule_logic": "Check whether contract amount, invoice issuance, and returned cash are aligned.",
            "manual_review_required": 1,
        },
        {
            "rule_code": "utility_output_deviation",
            "rule_name": "Utility and output deviation",
            "dimension": "operations",
            "severity_default": "high",
            "rule_logic": "Flag cases where power usage falls while output or revenue rises materially.",
            "manual_review_required": 1,
        },
        {
            "rule_code": "controller_change_frequency",
            "rule_name": "Controller or core executive instability",
            "dimension": "governance",
            "severity_default": "medium",
            "rule_logic": "Flag frequent equity or core executive changes in the last three years.",
            "manual_review_required": 0,
        },
        {
            "rule_code": "customer_concentration",
            "rule_name": "Customer concentration threshold",
            "dimension": "repayment_capacity",
            "severity_default": "medium",
            "rule_logic": "Flag if top five customers account for excessive share of revenue.",
            "manual_review_required": 0,
        },
        {
            "rule_code": "rd_substance_check",
            "rule_name": "R&D substance check",
            "dimension": "innovation",
            "severity_default": "medium",
            "rule_logic": "Check whether tech qualification claims are supported by headcount, projects, and IP assets.",
            "manual_review_required": 0,
        },
        {
            "rule_code": "cash_flow_cover",
            "rule_name": "Debt service coverage check",
            "dimension": "repayment_capacity",
            "severity_default": "high",
            "rule_logic": "Verify minimum monthly verified income can cover existing debt service and proposed loan amortization.",
            "manual_review_required": 1,
        },
        {
            "rule_code": "fixed_asset_capex_check",
            "rule_name": "Fixed asset and capex reconciliation",
            "dimension": "financial_statement",
            "severity_default": "medium",
            "rule_logic": "Check whether fixed asset change plus depreciation is broadly consistent with capex cash outflow.",
            "manual_review_required": 1,
        },
        {
            "rule_code": "cashflow_statement_bridge",
            "rule_name": "Cash flow statement bridge check",
            "dimension": "financial_statement",
            "severity_default": "medium",
            "rule_logic": "Check whether beginning cash plus net increase equals ending cash and whether net profit reconciles to operating cash flow directionally.",
            "manual_review_required": 1,
        },
    ]
    for rule in rules:
        rule_ids[rule["rule_code"]] = insert(cur, "validation_rules", rule)
    return rule_ids


def seed_industries(cur):
    industry_ids = {}
    benchmark_ids = {}
    industries = [
        {
            "subindustry": "Industrial Sensors",
            "industry_category": "Tech Manufacturing",
            "policy_direction": "受益于国产替代与产业升级政策支持。",
            "lifecycle_stage": "growth",
            "benchmark_note": "资本投入相对较高，客户验收与核验要求严格。",
            "update_cycle": "quarterly",
            "benchmarks": [
                ("gross_margin_pct", "Gross margin", 0.34, "ratio", 0.24, 0.32, 0.4),
                ("asset_liability_ratio", "Asset liability ratio", 0.52, "ratio", 0.38, 0.5, 0.63),
                ("rd_ratio_pct", "R&D spend ratio", 0.12, "ratio", 0.08, 0.11, 0.16),
            ],
        },
        {
            "subindustry": "Industrial SaaS",
            "industry_category": "Enterprise Software",
            "policy_direction": "Supported by digital transformation and industrial internet policy.",
            "lifecycle_stage": "growth",
            "benchmark_note": "Recurring revenue quality matters more than fixed assets.",
            "update_cycle": "quarterly",
            "benchmarks": [
                ("gross_margin_pct", "Gross margin", 0.58, "ratio", 0.45, 0.56, 0.68),
                ("asset_liability_ratio", "Asset liability ratio", 0.36, "ratio", 0.2, 0.34, 0.47),
                ("rd_ratio_pct", "R&D spend ratio", 0.18, "ratio", 0.12, 0.17, 0.25),
            ],
        },
        {
            "subindustry": "Machine Vision Equipment",
            "industry_category": "Advanced Equipment",
            "policy_direction": "Favored in smart manufacturing and equipment renewal.",
            "lifecycle_stage": "growth",
            "benchmark_note": "Project cycles and acceptance-based collections should be monitored.",
            "update_cycle": "quarterly",
            "benchmarks": [
                ("gross_margin_pct", "Gross margin", 0.41, "ratio", 0.31, 0.39, 0.48),
                ("asset_liability_ratio", "Asset liability ratio", 0.49, "ratio", 0.34, 0.47, 0.61),
                ("rd_ratio_pct", "R&D spend ratio", 0.11, "ratio", 0.07, 0.1, 0.15),
            ],
        },
        {
            "subindustry": "Energy IoT",
            "industry_category": "Industrial Internet",
            "policy_direction": "Encouraged by energy efficiency and carbon management programs.",
            "lifecycle_stage": "growth",
            "benchmark_note": "Utility savings proof and deployment cycles are key.",
            "update_cycle": "quarterly",
            "benchmarks": [
                ("gross_margin_pct", "Gross margin", 0.37, "ratio", 0.27, 0.35, 0.44),
                ("asset_liability_ratio", "Asset liability ratio", 0.44, "ratio", 0.29, 0.42, 0.55),
                ("rd_ratio_pct", "R&D spend ratio", 0.13, "ratio", 0.09, 0.12, 0.17),
            ],
        },
        {
            "subindustry": "Healthcare Informatics",
            "industry_category": "Medical Technology Services",
            "policy_direction": "Supported by smart healthcare and regional hospital informatization.",
            "lifecycle_stage": "maturing",
            "benchmark_note": "Receivable cycle and public tender exposure matter.",
            "update_cycle": "quarterly",
            "benchmarks": [
                ("gross_margin_pct", "Gross margin", 0.46, "ratio", 0.34, 0.44, 0.55),
                ("asset_liability_ratio", "Asset liability ratio", 0.42, "ratio", 0.26, 0.4, 0.53),
                ("rd_ratio_pct", "R&D spend ratio", 0.15, "ratio", 0.1, 0.14, 0.2),
            ],
        },
    ]
    for industry in industries:
        benchmarks = industry.pop("benchmarks")
        industry_id = insert(cur, "industry_profiles", industry)
        industry_ids[industry["subindustry"]] = industry_id
        for metric_code, metric_name, benchmark_value, unit, p25, p50, p75 in benchmarks:
            benchmark_id = insert(
                cur,
                "industry_benchmarks",
                {
                    "industry_profile_id": industry_id,
                    "metric_code": metric_code,
                    "metric_name": metric_name,
                    "benchmark_value": benchmark_value,
                    "unit": unit,
                    "percentile_25": p25,
                    "percentile_50": p50,
                    "percentile_75": p75,
                    "note": f"{industry['subindustry']} reference",
                },
            )
            benchmark_ids[(industry["subindustry"], metric_code)] = benchmark_id
    return industry_ids, benchmark_ids


def month_periods():
    periods = []
    for month in range(7, 13):
        start = date(2025, month, 1)
        if month == 12:
            end = date(2025, 12, 31)
        else:
            next_month = date(2025, month + 1, 1)
            end = next_month.fromordinal(next_month.toordinal() - 1)
        periods.append(
            {
                "period_code": f"2025-{month:02d}",
                "period_type": "monthly",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "fiscal_year": 2025,
                "fiscal_month": month,
                "is_latest": 1 if month == 12 else 0,
            }
        )
    for fiscal_year in (2023, 2024, 2025):
        periods.append(
            {
                "period_code": f"{fiscal_year}FY",
                "period_type": "annual",
                "start_date": f"{fiscal_year}-01-01",
                "end_date": f"{fiscal_year}-12-31",
                "fiscal_year": fiscal_year,
                "fiscal_month": None,
                "is_latest": 0,
            }
        )
    return periods


def risk_profile_params(company):
    profiles = {
        "medium_high": {
            "revenue_growth_2024": 1.18,
            "revenue_growth_2025": 1.24,
            "liability_ratio_2023": 0.48,
            "liability_ratio_2024": 0.5,
            "liability_ratio_2025": 0.53,
            "ocf_margin_2023": 0.08,
            "ocf_margin_2024": 0.07,
            "ocf_margin_2025": 0.05,
            "capex_ratio_2023": 0.09,
            "capex_ratio_2024": 0.11,
            "capex_ratio_2025": 0.13,
            "receivable_ratio_2023": 0.82,
            "receivable_ratio_2024": 0.9,
            "receivable_ratio_2025": 1.04,
        },
        "medium": {
            "revenue_growth_2024": 1.12,
            "revenue_growth_2025": 1.15,
            "liability_ratio_2023": 0.4,
            "liability_ratio_2024": 0.43,
            "liability_ratio_2025": 0.46,
            "ocf_margin_2023": 0.12,
            "ocf_margin_2024": 0.11,
            "ocf_margin_2025": 0.1,
            "capex_ratio_2023": 0.06,
            "capex_ratio_2024": 0.08,
            "capex_ratio_2025": 0.09,
            "receivable_ratio_2023": 0.7,
            "receivable_ratio_2024": 0.78,
            "receivable_ratio_2025": 0.88,
        },
        "low": {
            "revenue_growth_2024": 1.14,
            "revenue_growth_2025": 1.16,
            "liability_ratio_2023": 0.34,
            "liability_ratio_2024": 0.37,
            "liability_ratio_2025": 0.4,
            "ocf_margin_2023": 0.17,
            "ocf_margin_2024": 0.18,
            "ocf_margin_2025": 0.18,
            "capex_ratio_2023": 0.05,
            "capex_ratio_2024": 0.06,
            "capex_ratio_2025": 0.07,
            "receivable_ratio_2023": 0.6,
            "receivable_ratio_2024": 0.64,
            "receivable_ratio_2025": 0.7,
        },
    }
    return profiles[company["risk_tier"]]


def compute_annual_statement_payloads(company):
    params = risk_profile_params(company)
    annual_2025_revenue = round(sum(company["monthly_revenue"]) * 2.02, 2)
    annual_2024_revenue = round(annual_2025_revenue / params["revenue_growth_2025"], 2)
    annual_2023_revenue = round(annual_2024_revenue / params["revenue_growth_2024"], 2)
    annual_revenues = {
        2023: annual_2023_revenue,
        2024: annual_2024_revenue,
        2025: annual_2025_revenue,
    }
    annual_gross_margins = {
        2023: round(max(company["gross_margin"] - 0.03, 0.18), 4),
        2024: round(max(company["gross_margin"] - 0.015, 0.18), 4),
        2025: round(company["gross_margin"], 4),
    }
    annual_net_margins = {
        2023: round(max(company["net_margin"] - 0.015, 0.03), 4),
        2024: round(max(company["net_margin"] - 0.006, 0.03), 4),
        2025: round(company["net_margin"], 4),
    }
    annual_rd_ratios = {
        2023: round(max(company["rd_ratio"] - 0.025, 0.06), 4),
        2024: round(max(company["rd_ratio"] - 0.01, 0.06), 4),
        2025: round(company["rd_ratio"], 4),
    }

    statements = {}
    beginning_cash = round(annual_2023_revenue * 0.08, 2)
    prev_fixed_assets = None
    for fiscal_year in (2023, 2024, 2025):
        revenue = annual_revenues[fiscal_year]
        gross_margin = annual_gross_margins[fiscal_year]
        net_margin = annual_net_margins[fiscal_year]
        rd_ratio = annual_rd_ratios[fiscal_year]
        cogs = round(revenue * (1 - gross_margin), 2)
        gross_profit = round(revenue - cogs, 2)
        selling_expense = round(revenue * (0.08 if company["industry_category"] != "Enterprise Software" else 0.14), 2)
        admin_expense = round(revenue * 0.06, 2)
        rd_expense = round(revenue * rd_ratio, 2)
        operating_profit = round(gross_profit - selling_expense - admin_expense - rd_expense, 2)
        interest_expense = round(revenue * (0.011 if company["risk_tier"] == "low" else 0.016 if company["risk_tier"] == "medium" else 0.022), 2)
        income_tax_expense = round(max((operating_profit - interest_expense) * 0.15, 0), 2)
        net_profit = round(revenue * net_margin, 2)
        if net_profit > round(operating_profit - interest_expense - income_tax_expense, 2):
            income_tax_expense = round(max(operating_profit - interest_expense - net_profit, 0), 2)
        else:
            net_profit = round(operating_profit - interest_expense - income_tax_expense, 2)

        fixed_assets = round(revenue * (0.22 if company["industry_category"] != "Enterprise Software" else 0.08), 2)
        if prev_fixed_assets is None:
            prev_fixed_assets = round(fixed_assets * 0.82, 2)
        depreciation = round(prev_fixed_assets * 0.1, 2)
        capex = round(max(fixed_assets - prev_fixed_assets + depreciation, revenue * params[f"capex_ratio_{fiscal_year}"]), 2)
        if company["risk_tier"] == "medium_high" and fiscal_year == 2025:
            capex = round(capex * 1.12, 2)

        accounts_receivable = round(revenue * params[f"receivable_ratio_{fiscal_year}"], 2)
        inventory = round(revenue * (0.24 if company["industry_category"] != "Enterprise Software" else 0.03), 2)
        other_current_assets = round(revenue * 0.06, 2)
        intangible_assets = round(revenue * (0.1 if company["industry_category"] == "Enterprise Software" else 0.06), 2)
        total_assets = round(
            beginning_cash + accounts_receivable + inventory + other_current_assets + fixed_assets + intangible_assets + revenue * 0.03,
            2,
        )

        liability_ratio = params[f"liability_ratio_{fiscal_year}"]
        total_liabilities = round(total_assets * liability_ratio, 2)
        accounts_payable = round(revenue * 0.2, 2)
        short_term_debt = round(revenue * (0.16 if company["risk_tier"] != "low" else 0.1), 2)
        long_term_debt = round(revenue * (0.12 if company["risk_tier"] == "medium_high" else 0.08 if company["risk_tier"] == "medium" else 0.05), 2)
        other_liabilities = round(max(total_liabilities - accounts_payable - short_term_debt - long_term_debt, 0), 2)
        total_equity = round(total_assets - total_liabilities, 2)
        retained_earnings = round(max(total_equity - company["paid_in_capital"], 0), 2)

        inventory_change = round((inventory - revenue * 0.21) if fiscal_year == 2023 else inventory - statements[fiscal_year - 1]["balance"]["inventory"], 2)
        receivable_change = round((accounts_receivable - revenue * 0.68) if fiscal_year == 2023 else accounts_receivable - statements[fiscal_year - 1]["balance"]["accounts_receivable"], 2)
        payable_change = round((accounts_payable - revenue * 0.17) if fiscal_year == 2023 else accounts_payable - statements[fiscal_year - 1]["balance"]["accounts_payable"], 2)
        taxes_paid = round(income_tax_expense * 0.95, 2)
        net_cash_from_operations = round(
            net_profit + depreciation - max(inventory_change, 0) - max(receivable_change, 0) + max(payable_change, 0) - taxes_paid,
            2,
        )
        target_ocf = round(revenue * params[f"ocf_margin_{fiscal_year}"], 2)
        if company["risk_tier"] != "medium_high" or fiscal_year != 2025:
            net_cash_from_operations = round((net_cash_from_operations + target_ocf) / 2, 2)
        else:
            net_cash_from_operations = round(target_ocf, 2)

        net_cash_from_investing = round(-capex, 2)
        debt_financing_net = round(short_term_debt * 0.18 + long_term_debt * 0.12, 2)
        equity_financing_net = round(800000 if fiscal_year == 2024 and company["risk_tier"] != "low" else 0, 2)
        dividends = round(net_profit * (0.06 if company["risk_tier"] == "low" else 0.02 if company["risk_tier"] == "medium" else 0), 2)
        net_cash_from_financing = round(debt_financing_net + equity_financing_net - dividends, 2)
        net_increase_in_cash = round(net_cash_from_operations + net_cash_from_investing + net_cash_from_financing, 2)
        ending_cash = round(beginning_cash + net_increase_in_cash, 2)
        if ending_cash <= 0:
            ending_cash = round(revenue * 0.05, 2)
            net_increase_in_cash = round(ending_cash - beginning_cash, 2)
            net_cash_from_financing = round(net_increase_in_cash - net_cash_from_operations - net_cash_from_investing, 2)
        cash_and_equivalents = ending_cash

        total_assets = round(
            cash_and_equivalents + accounts_receivable + inventory + other_current_assets + fixed_assets + intangible_assets + revenue * 0.03,
            2,
        )
        total_liabilities = round(total_assets * liability_ratio, 2)
        other_liabilities = round(max(total_liabilities - accounts_payable - short_term_debt - long_term_debt, 0), 2)
        total_equity = round(total_assets - total_liabilities, 2)
        retained_earnings = round(max(total_equity - company["paid_in_capital"], 0), 2)

        statements[fiscal_year] = {
            "income": {
                "revenue": revenue,
                "cogs": cogs,
                "gross_profit": gross_profit,
                "selling_expense": selling_expense,
                "admin_expense": admin_expense,
                "rd_expense": rd_expense,
                "operating_profit": operating_profit,
                "interest_expense": interest_expense,
                "income_tax_expense": income_tax_expense,
                "net_profit": net_profit,
            },
            "balance": {
                "cash_and_equivalents": cash_and_equivalents,
                "accounts_receivable": accounts_receivable,
                "inventory": inventory,
                "other_current_assets": other_current_assets,
                "fixed_assets": fixed_assets,
                "intangible_assets": intangible_assets,
                "other_assets": round(revenue * 0.03, 2),
                "total_assets": total_assets,
                "accounts_payable": accounts_payable,
                "short_term_debt": short_term_debt,
                "long_term_debt": long_term_debt,
                "other_liabilities": other_liabilities,
                "total_liabilities": total_liabilities,
                "paid_in_capital": company["paid_in_capital"],
                "retained_earnings": retained_earnings,
                "total_equity": total_equity,
            },
            "cashflow": {
                "beginning_cash_balance": beginning_cash,
                "net_profit": net_profit,
                "depreciation_amortization": depreciation,
                "inventory_change": inventory_change,
                "receivable_change": receivable_change,
                "payable_change": payable_change,
                "taxes_paid": taxes_paid,
                "net_cash_from_operations": net_cash_from_operations,
                "capital_expenditure": capex,
                "net_cash_from_investing": net_cash_from_investing,
                "debt_financing_net": debt_financing_net,
                "equity_financing_net": equity_financing_net,
                "dividends_paid": dividends,
                "net_cash_from_financing": net_cash_from_financing,
                "net_increase_in_cash": net_increase_in_cash,
                "ending_cash_balance": ending_cash,
            },
            "ratios": {
                "gross_margin_pct": gross_margin,
                "asset_liability_ratio": round(total_liabilities / total_assets, 4) if total_assets else 0,
                "rd_ratio_pct": rd_ratio,
                "operating_cash_flow_margin_pct": round(net_cash_from_operations / revenue, 4) if revenue else 0,
            },
        }
        beginning_cash = ending_cash
        prev_fixed_assets = fixed_assets
    return statements


COMPANIES = [
    {
        "company_code": "COMP-001",
        "name": "深圳市灵犀微传感科技有限公司",
        "uscc": "91440300MA5DEMO001",
        "established_on": "2019-04-18",
        "province": "Guangdong",
        "city": "Shenzhen",
        "industry_category": "Tech Manufacturing",
        "subindustry": "Industrial Sensors",
        "scale": "small",
        "status": "active",
        "registered_capital": 12000000,
        "paid_in_capital": 7800000,
        "website": "https://demo-lingxi.example.com",
        "overview": "面向电池及装备客户提供高精度工业传感器。",
        "risk_tier": "medium_high",
        "case_no": "DD-2026-001",
        "case_name": "Lynx Sensor revolving working capital review",
        "application_date": "2026-05-06",
        "product_type": "micro_enterprise_credit",
        "requested_amount": 3200000,
        "requested_term": 18,
        "current_stage": "report_review",
        "decision_status": "manual_review_required",
        "case_owner": "Li Yun",
        "loan_purpose": "Sensor packaging line expansion and supplier payment smoothing",
        "primary_repayment_source": "头部工业客户回款",
        "secondary_repayment_source": "Controller guarantee and IP-backed financing option",
        "repayment_method": "monthly_interest_bullet_principal",
        "guarantee_mode": "controller_joint_guarantee",
        "annual_rate_min": 4.8,
        "annual_rate_max": 5.9,
        "requested_score_base": {
            "credit_history": 63,
            "repayment_capacity": 55,
            "operational_stability": 58,
            "innovation_strength": 79,
            "risk_mitigation": 61,
        },
        "monthly_revenue": [640000, 690000, 760000, 810000, 900000, 980000],
        "tax_ratio": [0.93, 0.91, 0.88, 0.82, 0.8, 0.78],
        "bank_in_ratio": [0.9, 0.88, 0.83, 0.81, 0.79, 0.74],
        "gross_margin": 0.33,
        "net_margin": 0.07,
        "customer_top5_ratio": 0.76,
        "pay_channel_share": 0.08,
        "social_headcount": [31, 32, 32, 31, 30, 29],
        "utility_power": [42000, 41600, 41000, 39800, 39100, 38200],
        "utility_water": [580, 575, 570, 561, 555, 549],
        "shipments": [118, 124, 129, 133, 141, 147],
        "rd_ratio": 0.17,
        "ip_count": 4,
        "guarantee": {"type": "joint_guarantee", "asset_name": "Controller personal guarantee", "asset_category": "personal_guarantee", "appraised_value": 0, "pledge_rate": 0.0, "status": "pending"},
        "persons": [
            {"code": "P001", "name": "周越", "gender": "M", "birth_year": 1987, "education": "master", "role": "legal_representative", "title": "CEO", "equity": 0.42, "controller": 1, "guarantor": 1},
            {"code": "P002", "name": "陈澜", "gender": "F", "birth_year": 1990, "education": "bachelor", "role": "finance_controller", "title": "财务负责人", "equity": 0.06, "controller": 0, "guarantor": 0},
            {"code": "P003", "name": "郭时远", "gender": "M", "birth_year": 1986, "education": "phd", "role": "core_executive", "title": "CTO", "equity": 0.18, "controller": 0, "guarantor": 0},
            {"code": "P004", "name": "周曼", "gender": "F", "birth_year": 1962, "education": "high_school", "role": "guarantor", "title": "家庭担保人", "equity": 0.0, "controller": 0, "guarantor": 1},
        ],
        "related_companies": [
            {"name": "深圳市灵犀电子封装有限公司", "relation_type": "affiliate_supplier", "risk_flag": 1, "note": "与实控人家庭存在关联，并发生过短期资金往来。"}
        ],
        "counterparties": [
            ("宁德新材装备股份有限公司", "customer", "Battery Equipment", "Ningde", 18, 1),
            ("苏州华芯工业自动化有限公司", "customer", "Industrial Automation", "Suzhou", 14, 2),
            ("广州精测模组有限公司", "customer", "Electronics", "Guangzhou", 9, 3),
            ("东莞市锐普陶瓷基板有限公司", "supplier", "Materials", "Dongguan", 20, 1),
            ("深圳市亿腾精密封装材料有限公司", "supplier", "Materials", "Shenzhen", 16, 2),
        ],
        "risk_events": [
            ("admin_notice", "medium", "2025-09-12", None, "税务机关要求补充申报说明", "针对发票确认差异需要补充解释材料。", "深圳税务服务"),
            ("labour_dispute", "low", "2025-11-20", None, "原销售经理劳动争议", "已通过调解结案，未形成重大赔付。", "法院公告"),
        ],
        "shareholding_changes": [
            ("2025-03-15", "equity_transfer", "实控人 47%，CTO 13%", "实控人 42%，CTO 18%", "引入技术骨干保留安排", "实控人股权被稀释尚可接受，但反映出一定资本压力。")
        ],
        "findings": [
            ("revenue_triangle_check", "high", "Revenue and bank inflow diverge in Q4", "December self-reported revenue exceeded verified bank inflow by more than 20 percent.", "Weakens confidence in short-term collection quality.", 0.91, "open", 1),
            ("utility_output_deviation", "high", "Power usage fell while revenue accelerated", "Power consumption trended down for three months while shipped value increased materially.", "Requires manual check on outsourced production and revenue recognition timing.", 0.86, "open", 1),
            ("customer_concentration", "medium", "Top five customer concentration is elevated", "Top five customers contributed about 76 percent of revenue.", "Any delay from the top customer could materially affect repayment.", 0.88, "open", 0),
            ("contract_cash_match", "medium", "Contract receipts lag invoice rhythm", "Two key contracts were substantially invoiced before corresponding cash receipts arrived.", "Raises receivable aging pressure.", 0.79, "open", 1),
        ],
        "risk_tags": [
            ("RT-AUTH-01", "Authenticity risk", "authenticity", "high", "Revenue triangle mismatch requires manual review."),
            ("RT-CASH-01", "Collection pressure", "repayment_capacity", "high", "Cash conversion is weaker than revenue growth."),
            ("RT-INNO-01", "Innovation strength", "innovation", "low", "IP and R&D assets support long-term competitiveness."),
        ],
        "report_sections": [
            ("company_profile", "Company Profile", "The borrower is a small but technically credible industrial sensor manufacturer with growing orders in battery equipment.", 0.87),
            ("operations", "Operations Review", "Core operating data show order expansion, but production-side proxy data do not fully confirm the revenue jump in Q4.", 0.8),
            ("risks", "Risk Review", "Primary risks are authenticity mismatch, customer concentration, and slower-than-reported collection conversion.", 0.84),
            ("recommendation", "Credit Recommendation", "Recommend a lower amount with controller guarantee, invoice collection monitoring, and enhanced account control.", 0.81),
        ],
        "recommendation": {
            "status": "conditional_approval",
            "amount": 2200000,
            "term": 12,
            "rate_min": 5.2,
            "rate_max": 5.9,
            "guarantee_requirement": "Controller and spouse joint guarantee; primary collection account control.",
            "supplemental_requirements": "Provide top three customer settlement slips, outsourced production explanation, and December tax reconciliation.",
            "rejection_reason": None,
            "note": "Main showcase case with manual review hold points.",
        },
    },
    {
        "company_code": "COMP-002",
        "name": "苏州云衡工业软件有限公司",
        "uscc": "91320500MA5DEMO002",
        "established_on": "2020-02-25",
        "province": "Jiangsu",
        "city": "Suzhou",
        "industry_category": "Enterprise Software",
        "subindustry": "Industrial SaaS",
        "scale": "small",
        "status": "active",
        "registered_capital": 10000000,
        "paid_in_capital": 6600000,
        "website": "https://demo-yunheng.example.com",
        "overview": "Develops cloud manufacturing scheduling and MES add-on software for precision factories.",
        "risk_tier": "low",
        "case_no": "DD-2026-002",
        "case_name": "Yunheng SaaS credit review",
        "application_date": "2026-05-04",
        "product_type": "micro_enterprise_credit",
        "requested_amount": 1800000,
        "requested_term": 12,
        "current_stage": "committee_ready",
        "decision_status": "recommended",
        "case_owner": "Wang Xue",
        "loan_purpose": "Sales channel expansion and implementation payroll",
        "primary_repayment_source": "Annual subscription renewals and implementation service collections",
        "secondary_repayment_source": "Controller guarantee",
        "repayment_method": "equal_principal_interest",
        "guarantee_mode": "controller_joint_guarantee",
        "annual_rate_min": 4.2,
        "annual_rate_max": 5.1,
        "requested_score_base": {
            "credit_history": 84,
            "repayment_capacity": 81,
            "operational_stability": 78,
            "innovation_strength": 85,
            "risk_mitigation": 76,
        },
        "monthly_revenue": [530000, 550000, 575000, 590000, 610000, 635000],
        "tax_ratio": [0.98, 0.99, 0.97, 0.98, 0.97, 0.99],
        "bank_in_ratio": [0.96, 0.95, 0.97, 0.94, 0.96, 0.95],
        "gross_margin": 0.61,
        "net_margin": 0.16,
        "customer_top5_ratio": 0.48,
        "pay_channel_share": 0.02,
        "social_headcount": [27, 28, 29, 29, 30, 31],
        "utility_power": [8300, 8400, 8450, 8480, 8520, 8600],
        "utility_water": [130, 132, 133, 133, 134, 135],
        "shipments": [8, 9, 7, 10, 9, 8],
        "rd_ratio": 0.22,
        "ip_count": 6,
        "guarantee": {"type": "joint_guarantee", "asset_name": "Controller personal guarantee", "asset_category": "personal_guarantee", "appraised_value": 0, "pledge_rate": 0.0, "status": "committed"},
        "persons": [
            {"code": "P101", "name": "江衡", "gender": "M", "birth_year": 1988, "education": "master", "role": "legal_representative", "title": "CEO", "equity": 0.46, "controller": 1, "guarantor": 1},
            {"code": "P102", "name": "陆青", "gender": "F", "birth_year": 1992, "education": "master", "role": "core_executive", "title": "COO", "equity": 0.14, "controller": 0, "guarantor": 0},
            {"code": "P103", "name": "韩石", "gender": "M", "birth_year": 1987, "education": "bachelor", "role": "finance_controller", "title": "Finance Manager", "equity": 0.04, "controller": 0, "guarantor": 0},
        ],
        "related_companies": [
            {"name": "苏州云衡数字运维有限公司", "relation_type": "subsidiary", "risk_flag": 0, "note": "Lightweight delivery affiliate with no material debt."}
        ],
        "counterparties": [
            ("昆山锐控精密制造有限公司", "customer", "Precision Manufacturing", "Kunshan", 22, 1),
            ("无锡新桥机电有限公司", "customer", "Automation", "Wuxi", 18, 2),
            ("常州智数工厂科技有限公司", "customer", "Industrial IT", "Changzhou", 11, 3),
            ("苏州象限云服务有限公司", "supplier", "Cloud Service", "Suzhou", 24, 1),
            ("上海图策实施顾问有限公司", "supplier", "Consulting", "Shanghai", 18, 2),
        ],
        "risk_events": [
            ("contract_dispute", "low", "2025-08-16", None, "Historic implementation acceptance dispute", "Resolved within 30 days with no cash loss.", "Court bulletin"),
        ],
        "shareholding_changes": [
            ("2024-12-20", "employee_option", "Controller 50%, COO 10%", "Controller 46%, COO 14%", "Talent retention", "Normal incentive arrangement with no adverse governance signal.")
        ],
        "findings": [
            ("rd_substance_check", "low", "R&D capability is well supported", "R&D team ratio and software IP portfolio support tech claims.", "Strengthens confidence in product sustainability.", 0.9, "closed", 0),
            ("cash_flow_cover", "low", "Debt service coverage remains healthy", "Verified monthly collections are above modeled repayment need.", "Supports recommended approval.", 0.88, "closed", 0),
        ],
        "risk_tags": [
            ("RT-INNO-02", "Strong innovation foundation", "innovation", "low", "Software IP, recurring clients, and R&D spend are consistent."),
            ("RT-GOV-01", "Stable governance", "governance", "low", "Controller and management team are stable."),
        ],
        "report_sections": [
            ("company_profile", "Company Profile", "The borrower is a small industrial SaaS vendor with sticky manufacturing customers.", 0.9),
            ("operations", "Operations Review", "Collections, tax declaration, and subscription contracts are broadly aligned.", 0.89),
            ("risks", "Risk Review", "Material risk level is low; the key watch item is implementation dependency on a concentrated delivery team.", 0.83),
            ("recommendation", "Credit Recommendation", "Recommend approval within requested range with standard controller guarantee.", 0.88),
        ],
        "recommendation": {
            "status": "approve",
            "amount": 1800000,
            "term": 12,
            "rate_min": 4.3,
            "rate_max": 4.9,
            "guarantee_requirement": "Controller joint guarantee.",
            "supplemental_requirements": "Maintain settlement account visibility and submit semiannual SaaS renewal cohort summary.",
            "rejection_reason": None,
            "note": "High-quality benchmark borrower.",
        },
    },
    {
        "company_code": "COMP-003",
        "name": "成都智检视觉装备有限公司",
        "uscc": "91510100MA5DEMO003",
        "established_on": "2018-11-09",
        "province": "Sichuan",
        "city": "Chengdu",
        "industry_category": "Advanced Equipment",
        "subindustry": "Machine Vision Equipment",
        "scale": "small",
        "status": "active",
        "registered_capital": 15000000,
        "paid_in_capital": 9000000,
        "website": "https://demo-zhijian.example.com",
        "overview": "Supplies inline machine vision inspection modules for electronics and food packaging lines.",
        "risk_tier": "low",
        "case_no": "DD-2026-003",
        "case_name": "Zhijian equipment project loan review",
        "application_date": "2026-05-03",
        "product_type": "micro_enterprise_credit",
        "requested_amount": 2600000,
        "requested_term": 18,
        "current_stage": "committee_ready",
        "decision_status": "recommended",
        "case_owner": "Zhang Min",
        "loan_purpose": "Working capital for project acceptance cycles",
        "primary_repayment_source": "Project acceptance collections from electronics clients",
        "secondary_repayment_source": "Equipment repurchase and controller guarantee",
        "repayment_method": "monthly_interest_bullet_principal",
        "guarantee_mode": "controller_joint_guarantee_plus_equipment",
        "annual_rate_min": 4.5,
        "annual_rate_max": 5.4,
        "requested_score_base": {
            "credit_history": 81,
            "repayment_capacity": 77,
            "operational_stability": 74,
            "innovation_strength": 82,
            "risk_mitigation": 79,
        },
        "monthly_revenue": [700000, 720000, 760000, 780000, 790000, 830000],
        "tax_ratio": [0.96, 0.95, 0.96, 0.94, 0.95, 0.95],
        "bank_in_ratio": [0.89, 0.91, 0.9, 0.88, 0.92, 0.9],
        "gross_margin": 0.43,
        "net_margin": 0.11,
        "customer_top5_ratio": 0.58,
        "pay_channel_share": 0.01,
        "social_headcount": [35, 35, 36, 37, 37, 38],
        "utility_power": [26500, 26800, 27200, 27900, 28100, 28600],
        "utility_water": [340, 344, 347, 351, 353, 356],
        "shipments": [21, 24, 23, 26, 24, 27],
        "rd_ratio": 0.14,
        "ip_count": 5,
        "guarantee": {"type": "mixed", "asset_name": "Inspection equipment inventory charge", "asset_category": "movable_asset", "appraised_value": 1800000, "pledge_rate": 0.45, "status": "draft"},
        "persons": [
            {"code": "P201", "name": "何舟", "gender": "M", "birth_year": 1985, "education": "master", "role": "legal_representative", "title": "General Manager", "equity": 0.38, "controller": 1, "guarantor": 1},
            {"code": "P202", "name": "白琳", "gender": "F", "birth_year": 1989, "education": "bachelor", "role": "finance_controller", "title": "Finance Lead", "equity": 0.05, "controller": 0, "guarantor": 0},
            {"code": "P203", "name": "陶笙", "gender": "M", "birth_year": 1991, "education": "master", "role": "core_executive", "title": "R&D Director", "equity": 0.11, "controller": 0, "guarantor": 0},
        ],
        "related_companies": [
            {"name": "成都智检系统集成服务中心", "relation_type": "service_affiliate", "risk_flag": 0, "note": "Provides on-site integration services."}
        ],
        "counterparties": [
            ("重庆弘冠电子有限公司", "customer", "Electronics", "Chongqing", 20, 1),
            ("绵阳星桥包装设备有限公司", "customer", "Packaging", "Mianyang", 18, 2),
            ("西安迅控自动化有限公司", "customer", "Automation", "Xi'an", 15, 3),
            ("成都维拓工控配件有限公司", "supplier", "Industrial Parts", "Chengdu", 24, 1),
            ("苏州澜石镜头科技有限公司", "supplier", "Optics", "Suzhou", 12, 2),
        ],
        "risk_events": [
            ("environmental_check", "low", "2025-10-18", None, "Routine environmental inspection completed", "No penalty issued; only housekeeping advice recorded.", "District regulator"),
        ],
        "shareholding_changes": [
            ("2025-01-06", "capital_increase", "Registered capital 12 million", "Registered capital 15 million", "External investor subscribed new capital", "Positive signal for capital strength.")
        ],
        "findings": [
            ("contract_cash_match", "low", "Project acceptance and receipts are largely aligned", "Receipts lag contract milestones by less than one billing cycle.", "Supports stable project execution quality.", 0.84, "closed", 0),
            ("cash_flow_cover", "low", "Coverage remains adequate", "Verified minimum monthly inflow covers modeled repayment by more than 1.6x.", "Supports approval with equipment collateral add-on.", 0.86, "closed", 0),
        ],
        "risk_tags": [
            ("RT-OPS-01", "Project cycle watch", "operational_stability", "low", "Project collection rhythm remains manageable."),
            ("RT-INNO-03", "Equipment IP depth", "innovation", "low", "Patents and engineering team support moat."),
        ],
        "report_sections": [
            ("company_profile", "Company Profile", "The borrower supplies machine vision modules with healthy regional client diversification.", 0.88),
            ("operations", "Operations Review", "Order delivery and utility trends move consistently with booked revenue.", 0.86),
            ("risks", "Risk Review", "Main risk remains project-based collection timing, partially mitigated by equipment collateral.", 0.82),
            ("recommendation", "Credit Recommendation", "Recommend approval near requested amount with equipment charge registration.", 0.85),
        ],
        "recommendation": {
            "status": "approve",
            "amount": 2400000,
            "term": 18,
            "rate_min": 4.7,
            "rate_max": 5.2,
            "guarantee_requirement": "Controller guarantee and movable asset charge registration.",
            "supplemental_requirements": "Provide quarterly project acceptance report.",
            "rejection_reason": None,
            "note": "Low-risk equipment borrower with moderate project-cycle sensitivity.",
        },
    },
    {
        "company_code": "COMP-004",
        "name": "杭州启脉能源物联科技有限公司",
        "uscc": "91330100MA5DEMO004",
        "established_on": "2021-01-14",
        "province": "Zhejiang",
        "city": "Hangzhou",
        "industry_category": "Industrial Internet",
        "subindustry": "Energy IoT",
        "scale": "small",
        "status": "active",
        "registered_capital": 8000000,
        "paid_in_capital": 5200000,
        "website": "https://demo-qimai.example.com",
        "overview": "Provides energy monitoring gateways and SaaS dashboards for industrial parks and chains.",
        "risk_tier": "medium",
        "case_no": "DD-2026-004",
        "case_name": "Qimai energy IoT credit review",
        "application_date": "2026-05-02",
        "product_type": "micro_enterprise_credit",
        "requested_amount": 2100000,
        "requested_term": 12,
        "current_stage": "supplement_pending",
        "decision_status": "pending",
        "case_owner": "Liu Qian",
        "loan_purpose": "Deployment inventory and implementation staffing",
        "primary_repayment_source": "System deployment collections and annual service fees",
        "secondary_repayment_source": "Controller guarantee",
        "repayment_method": "equal_principal_interest",
        "guarantee_mode": "controller_joint_guarantee",
        "annual_rate_min": 4.6,
        "annual_rate_max": 5.5,
        "requested_score_base": {
            "credit_history": 72,
            "repayment_capacity": 68,
            "operational_stability": 66,
            "innovation_strength": 78,
            "risk_mitigation": 70,
        },
        "monthly_revenue": [420000, 445000, 470000, 495000, 540000, 560000],
        "tax_ratio": [0.95, 0.93, 0.92, 0.91, 0.89, 0.9],
        "bank_in_ratio": [0.86, 0.84, 0.83, 0.87, 0.85, 0.84],
        "gross_margin": 0.39,
        "net_margin": 0.09,
        "customer_top5_ratio": 0.63,
        "pay_channel_share": 0.03,
        "social_headcount": [19, 19, 20, 20, 21, 21],
        "utility_power": [9900, 10050, 10100, 10300, 10450, 10600],
        "utility_water": [145, 147, 148, 149, 151, 153],
        "shipments": [17, 18, 19, 20, 23, 24],
        "rd_ratio": 0.19,
        "ip_count": 4,
        "guarantee": {"type": "joint_guarantee", "asset_name": "Controller personal guarantee", "asset_category": "personal_guarantee", "appraised_value": 0, "pledge_rate": 0.0, "status": "pending"},
        "persons": [
            {"code": "P301", "name": "邵启", "gender": "M", "birth_year": 1990, "education": "master", "role": "legal_representative", "title": "CEO", "equity": 0.44, "controller": 1, "guarantor": 1},
            {"code": "P302", "name": "唐雨", "gender": "F", "birth_year": 1993, "education": "master", "role": "core_executive", "title": "Product Director", "equity": 0.12, "controller": 0, "guarantor": 0},
            {"code": "P303", "name": "赵闻", "gender": "M", "birth_year": 1988, "education": "bachelor", "role": "finance_controller", "title": "Finance Manager", "equity": 0.03, "controller": 0, "guarantor": 0},
        ],
        "related_companies": [
            {"name": "杭州启脉低碳服务有限公司", "relation_type": "affiliate_service_company", "risk_flag": 0, "note": "Service implementation affiliate used for municipal contracts."}
        ],
        "counterparties": [
            ("绍兴万景产业园运营有限公司", "customer", "Industrial Park", "Shaoxing", 16, 1),
            ("宁波启盛商用物业管理有限公司", "customer", "Property", "Ningbo", 13, 2),
            ("杭州联港冷链科技有限公司", "customer", "Cold Chain", "Hangzhou", 10, 3),
            ("杭州芯联物联模组有限公司", "supplier", "IoT Modules", "Hangzhou", 22, 1),
            ("嘉兴沐光安装工程有限公司", "supplier", "Engineering", "Jiaxing", 11, 2),
        ],
        "risk_events": [
            ("payment_delay", "medium", "2025-10-31", "绍兴万景产业园运营有限公司", "Major client delayed acceptance settlement", "One project acceptance lagged by 45 days.", "Internal note"),
        ],
        "shareholding_changes": [
            ("2025-02-10", "equity_transfer", "Controller 49%, angel 21%", "Controller 44%, angel 21%, product director 12%", "Option grant", "Normal but warrants follow-up on retention.")
        ],
        "findings": [
            ("cash_flow_cover", "medium", "Coverage is acceptable but thinner than peers", "Verified minimum inflow covers modeled repayment by roughly 1.2x.", "Appropriate for smaller amount or tighter monitoring.", 0.77, "open", 1),
            ("customer_concentration", "medium", "Top client contributes sizable deployment revenue", "Single industrial park client contributes more than one quarter of trailing revenue.", "Collection timing may create volatility.", 0.81, "open", 0),
        ],
        "risk_tags": [
            ("RT-CASH-02", "Thin cash buffer", "repayment_capacity", "medium", "Cash conversion is acceptable but not wide."),
            ("RT-CUST-01", "Top client reliance", "operational_stability", "medium", "Top client dependency is elevated."),
        ],
        "report_sections": [
            ("company_profile", "Company Profile", "The borrower is an energy IoT SME serving industrial parks and commercial facilities.", 0.87),
            ("operations", "Operations Review", "Growth is visible, but cash collection remains moderately timing-sensitive due to deployment acceptance.", 0.79),
            ("risks", "Risk Review", "Concentration and thinner cash coverage call for tighter post-disbursement monitoring.", 0.81),
            ("recommendation", "Credit Recommendation", "Recommend a slightly reduced line with collection account observation and project milestone reporting.", 0.8),
        ],
        "recommendation": {
            "status": "conditional_approval",
            "amount": 1700000,
            "term": 12,
            "rate_min": 4.9,
            "rate_max": 5.5,
            "guarantee_requirement": "Controller guarantee and designated settlement account routing.",
            "supplemental_requirements": "Provide latest project acceptance schedule and top customer receivable aging breakdown.",
            "rejection_reason": None,
            "note": "Medium-risk borrower pending supplemental data.",
        },
    },
    {
        "company_code": "COMP-005",
        "name": "武汉睿桥医疗信息技术有限公司",
        "uscc": "91420100MA5DEMO005",
        "established_on": "2017-08-03",
        "province": "Hubei",
        "city": "Wuhan",
        "industry_category": "Medical Technology Services",
        "subindustry": "Healthcare Informatics",
        "scale": "small",
        "status": "active",
        "registered_capital": 9000000,
        "paid_in_capital": 6000000,
        "website": "https://demo-ruiqiao.example.com",
        "overview": "Builds outpatient and specialty clinic information modules for regional hospitals and community care groups.",
        "risk_tier": "medium",
        "case_no": "DD-2026-005",
        "case_name": "Ruiqiao healthcare IT credit review",
        "application_date": "2026-05-01",
        "product_type": "micro_enterprise_credit",
        "requested_amount": 2300000,
        "requested_term": 15,
        "current_stage": "report_review",
        "decision_status": "pending",
        "case_owner": "Chen Xi",
        "loan_purpose": "Receivable turnover support for public hospital projects",
        "primary_repayment_source": "Hospital project collections and maintenance service fees",
        "secondary_repayment_source": "Controller guarantee",
        "repayment_method": "equal_principal_interest",
        "guarantee_mode": "controller_joint_guarantee",
        "annual_rate_min": 4.7,
        "annual_rate_max": 5.6,
        "requested_score_base": {
            "credit_history": 74,
            "repayment_capacity": 67,
            "operational_stability": 65,
            "innovation_strength": 80,
            "risk_mitigation": 68,
        },
        "monthly_revenue": [480000, 500000, 520000, 540000, 555000, 570000],
        "tax_ratio": [0.97, 0.95, 0.96, 0.95, 0.94, 0.96],
        "bank_in_ratio": [0.8, 0.79, 0.77, 0.8, 0.78, 0.79],
        "gross_margin": 0.48,
        "net_margin": 0.1,
        "customer_top5_ratio": 0.67,
        "pay_channel_share": 0.0,
        "social_headcount": [24, 24, 25, 25, 25, 26],
        "utility_power": [7200, 7250, 7300, 7340, 7380, 7420],
        "utility_water": [118, 119, 120, 121, 121, 122],
        "shipments": [6, 7, 6, 8, 7, 9],
        "rd_ratio": 0.2,
        "ip_count": 5,
        "guarantee": {"type": "joint_guarantee", "asset_name": "Controller personal guarantee", "asset_category": "personal_guarantee", "appraised_value": 0, "pledge_rate": 0.0, "status": "committed"},
        "persons": [
            {"code": "P401", "name": "许桥", "gender": "M", "birth_year": 1986, "education": "master", "role": "legal_representative", "title": "CEO", "equity": 0.41, "controller": 1, "guarantor": 1},
            {"code": "P402", "name": "冯薇", "gender": "F", "birth_year": 1991, "education": "master", "role": "core_executive", "title": "Product VP", "equity": 0.1, "controller": 0, "guarantor": 0},
            {"code": "P403", "name": "叶宁", "gender": "F", "birth_year": 1990, "education": "bachelor", "role": "finance_controller", "title": "Finance Lead", "equity": 0.04, "controller": 0, "guarantor": 0},
        ],
        "related_companies": [
            {"name": "武汉睿桥云维服务有限公司", "relation_type": "service_affiliate", "risk_flag": 0, "note": "Maintains after-sales service contracts."}
        ],
        "counterparties": [
            ("襄阳医联智慧医院管理有限公司", "customer", "Healthcare", "Xiangyang", 24, 1),
            ("武汉协和康健信息服务中心", "customer", "Healthcare", "Wuhan", 20, 2),
            ("荆州仁和社区医疗集团", "customer", "Healthcare", "Jingzhou", 17, 3),
            ("武汉数联机房运维有限公司", "supplier", "IT Infrastructure", "Wuhan", 18, 1),
            ("长沙合瑞系统集成有限公司", "supplier", "Implementation", "Changsha", 14, 2),
        ],
        "risk_events": [
            ("judicial_notice", "medium", "2025-09-08", "襄阳医联智慧医院管理有限公司", "Hospital project payment arbitration notice", "Collection dispute under mediation; no final judgement yet.", "Court bulletin"),
        ],
        "shareholding_changes": [
            ("2024-11-28", "board_change", "Product VP not on board", "Product VP added as board observer", "Governance refinement", "Neutral governance update.")
        ],
        "findings": [
            ("contract_cash_match", "medium", "Hospital project collections are slower than invoice rhythm", "Public hospital receivables are aging beyond standard commercial terms.", "Raises working capital pressure and justifies lower amount.", 0.83, "open", 1),
            ("cash_flow_cover", "medium", "Coverage relies on delayed public hospital settlements", "Verified bank inflow covers modeled repayment by around 1.15x in weak months.", "Buffer is acceptable only with tighter amount and monitoring.", 0.78, "open", 1),
        ],
        "risk_tags": [
            ("RT-AR-01", "Slow hospital receivable cycle", "repayment_capacity", "medium", "Public sector project payments stretch cash cycle."),
            ("RT-INNO-04", "Healthcare software depth", "innovation", "low", "R&D and hospital deployment references support product viability."),
        ],
        "report_sections": [
            ("company_profile", "Company Profile", "The borrower is a healthcare informatics SME focused on regional hospital systems.", 0.88),
            ("operations", "Operations Review", "Invoice and tax data are consistent, but cash conversion is slower because of hospital payment terms.", 0.82),
            ("risks", "Risk Review", "Receivable aging and public tender exposure are the main risk items.", 0.84),
            ("recommendation", "Credit Recommendation", "Recommend a reduced limit with milestone monitoring and receivable evidence refresh.", 0.81),
        ],
        "recommendation": {
            "status": "conditional_approval",
            "amount": 1800000,
            "term": 12,
            "rate_min": 4.9,
            "rate_max": 5.6,
            "guarantee_requirement": "Controller guarantee and assignment notice for top hospital receivables if feasible.",
            "supplemental_requirements": "Refresh hospital project receivable aging and pending settlement notices.",
            "rejection_reason": None,
            "note": "Medium-risk service SME with public-sector collection drag.",
        },
    },
]


def build_periods(cur, company_id, case_id):
    period_ids = {}
    ordered_periods = month_periods()
    for period in ordered_periods:
        payload = dict(period)
        payload["company_id"] = company_id
        payload["case_id"] = case_id
        period_id = insert(cur, "financial_periods", payload)
        period_ids[period["period_code"]] = period_id
    return period_ids


def insert_profile_attribute(cur, company_id, case_id, attribute_group, label, value_text, source_ref, note):
    insert(
        cur,
        "company_profile_attributes",
        {
            "company_id": company_id,
            "case_id": case_id,
            "attribute_group": attribute_group,
            "label": label,
            "value_text": value_text,
            "source_ref": source_ref,
            "note": note,
        },
    )


def upsert_profile_attribute(cur, company_id, case_id, attribute_group, label, value_text, source_ref, note):
    cur.execute(
        "DELETE FROM company_profile_attributes WHERE company_id = ? AND attribute_group = ? AND label = ?",
        (company_id, attribute_group, label),
    )
    insert_profile_attribute(cur, company_id, case_id, attribute_group, label, value_text, source_ref, note)


def add_or_replace_person_role(cur, company_id, person_code, full_name, gender, birth_year, education, role_type, title, joined_on, equity_ratio=None, is_actual_controller=0, is_guarantor=0, notes=None):
    cur.execute("SELECT id FROM persons WHERE person_code = ?", (person_code,))
    row = cur.fetchone()
    if row:
        person_id = row[0]
        cur.execute(
            """
            UPDATE persons
            SET full_name = ?, gender = ?, birth_year = ?, education_level = ?, marital_status = COALESCE(marital_status, 'unknown')
            WHERE id = ?
            """,
            (full_name, gender, birth_year, education, person_id),
        )
    else:
        person_id = insert(
            cur,
            "persons",
            {
                "person_code": person_code,
                "full_name": full_name,
                "gender": gender,
                "birth_year": birth_year,
                "education_level": education,
                "marital_status": "unknown",
                "hukou_location": None,
                "residence_city": None,
                "mobile_masked": None,
                "id_number_masked": None,
                "risk_note": None,
            },
        )
    cur.execute(
        "DELETE FROM company_person_roles WHERE company_id = ? AND person_id = ? AND role_type = ?",
        (company_id, person_id, role_type),
    )
    insert(
        cur,
        "company_person_roles",
        {
            "company_id": company_id,
            "person_id": person_id,
            "role_type": role_type,
            "title": title,
            "equity_ratio": equity_ratio,
            "voting_ratio": equity_ratio,
            "is_actual_controller": is_actual_controller,
            "is_guarantor": is_guarantor,
            "joined_on": joined_on,
            "left_on": None,
            "notes": notes,
        },
    )
    return person_id


def seed_documents(cur, company, case_id, company_id, person_ids, source_ids):
    docs = [
        ("business_license", "Business License", "client_upload", 2, 1),
        ("articles", "Articles of Association Summary", "client_upload", 3, 1),
        ("financial_pack", "Management Financial Package", "client_upload", 4, 1),
        ("annual_financial_statements", "Annual Financial Statements Pack", "client_upload", 12, 1),
        ("bank_statement", "Bank Statement Summary", "bank_statement_summary", 5, 1),
        ("tax_summary", "Tax Filing Summary", "tax_summary", 3, 1),
        ("core_contract", "Top Customer Contract Pack", "client_upload", 4, 1),
        ("ip_pack", "IP and Qualification Pack", "official_registry", 4, 1),
        ("public_risk", "Public Risk Screenshot Bundle", "manual_research", 3, 0),
    ]
    if company["company_code"] == "COMP-001":
        docs.extend(
            [
                ("utility_report", "Utility Usage Report", "client_upload", 2, 1),
                ("social_security", "Social Security Contribution Summary", "client_upload", 2, 1),
            ]
        )
    document_ids = {}
    page_ids = {}
    for idx, (doc_type, title, source_name, page_count, is_ocr) in enumerate(docs, start=1):
        doc_id = insert(
            cur,
            "documents",
            {
                "case_id": case_id,
                "company_id": company_id,
                "person_id": None,
                "source_id": source_ids[source_name],
                "document_type": doc_type,
                "title": f"{company['name']} - {title}",
                "source_label": source_name,
                "file_uri": f"uploads/{company['company_code'].lower()}/{doc_type}.pdf",
                "external_url": None,
                "page_count": page_count,
                "uploaded_at": "2026-05-07T10:00:00",
                "document_date": "2026-04-30",
                "is_ocr_processed": is_ocr,
                "checksum": f"{company['company_code']}-{doc_type}",
                "summary": f"{title} for {company['name']}",
            },
        )
        document_ids[doc_type] = doc_id
        for page_no in range(1, page_count + 1):
            page_id = insert(
                cur,
                "document_pages",
                {
                    "document_id": doc_id,
                    "page_no": page_no,
                    "image_uri": f"uploads/{company['company_code'].lower()}/{doc_type}_p{page_no}.png",
                    "ocr_text": f"{title} page {page_no} for {company['name']}.",
                    "layout_summary": f"Structured page {page_no} summary.",
                    "extracted_json": json.dumps({"doc_type": doc_type, "page_no": page_no}, ensure_ascii=False),
                },
            )
            page_ids[(doc_type, page_no)] = page_id
    return document_ids, page_ids


def seed_people(cur, company_id, people):
    person_ids = {}
    for person in people:
        person_id = insert(
            cur,
            "persons",
            {
                "person_code": person["code"],
                "full_name": person["name"],
                "gender": person["gender"],
                "birth_year": person["birth_year"],
                "education_level": person["education"],
                "marital_status": "married" if person["birth_year"] < 1991 else "single",
                "hukou_location": "urban",
                "residence_city": "",
                "mobile_masked": "138****0000",
                "id_number_masked": "420************0000",
                "risk_note": None,
            },
        )
        person_ids[person["code"]] = person_id
        insert(
            cur,
            "company_person_roles",
            {
                "company_id": company_id,
                "person_id": person_id,
                "role_type": person["role"],
                "title": person["title"],
                "equity_ratio": person["equity"],
                "voting_ratio": person["equity"],
                "is_actual_controller": person["controller"],
                "is_guarantor": person["guarantor"],
                "joined_on": "2021-01-01",
                "left_on": None,
                "notes": None,
            },
        )
    return person_ids


def seed_case(cur, company, company_id):
    case_id = insert(
        cur,
        "due_diligence_cases",
        {
            "case_no": company["case_no"],
            "company_id": company_id,
            "case_name": company["case_name"],
            "application_date": company["application_date"],
            "product_type": company["product_type"],
            "requested_amount_cny": company["requested_amount"],
            "requested_term_months": company["requested_term"],
            "current_stage": company["current_stage"],
            "decision_status": company["decision_status"],
            "case_owner": company["case_owner"],
            "summary": company["overview"],
        },
    )
    insert(
        cur,
        "loan_applications",
        {
            "case_id": case_id,
            "product_name": "SME revolving credit line",
            "requested_amount_cny": company["requested_amount"],
            "approved_amount_cny": company["recommendation"]["amount"],
            "loan_purpose": company["loan_purpose"],
            "primary_repayment_source": company["primary_repayment_source"],
            "secondary_repayment_source": company["secondary_repayment_source"],
            "repayment_method": company["repayment_method"],
            "guarantee_mode": company["guarantee_mode"],
            "annual_rate_min": company["annual_rate_min"],
            "annual_rate_max": company["annual_rate_max"],
            "tenor_months": company["requested_term"],
        },
    )
    return case_id


def seed_guarantee(cur, company, case_id, person_ids):
    guarantor_person_id = None
    for person in company["persons"]:
        if person["guarantor"]:
            guarantor_person_id = person_ids[person["code"]]
            break
    guarantee = company["guarantee"]
    insert(
        cur,
        "guarantees",
        {
            "case_id": case_id,
            "guarantee_type": guarantee["type"],
            "provider_company_id": None,
            "provider_person_id": guarantor_person_id,
            "asset_name": guarantee["asset_name"],
            "asset_category": guarantee["asset_category"],
            "appraised_value_cny": guarantee["appraised_value"],
            "pledge_rate": guarantee["pledge_rate"],
            "lien_status": "none" if guarantee["asset_category"] == "personal_guarantee" else "to_register",
            "guarantee_status": guarantee["status"],
            "notes": None,
        },
    )


def seed_company(cur, company):
    company_id = insert(
        cur,
        "companies",
        {
            "company_code": company["company_code"],
            "name": company["name"],
            "unified_social_credit_code": company["uscc"],
            "established_on": company["established_on"],
            "region_province": company["province"],
            "region_city": company["city"],
            "industry_category": company["industry_category"],
            "subindustry": company["subindustry"],
            "is_tech_sme": 1,
            "enterprise_scale": company["scale"],
            "operating_status": company["status"],
            "registered_capital_cny": company["registered_capital"],
            "paid_in_capital_cny": company["paid_in_capital"],
            "website": company["website"],
            "overview": company["overview"],
            "risk_tier": company["risk_tier"],
            "shell_type": "demo_realistic",
            "notes": "Replace with verified public shell data and screenshots when available.",
        },
    )
    return company_id


def seed_related_companies(cur, company_id, related_items):
    for item in related_items:
        insert(
            cur,
            "related_companies",
            {
                "company_id": company_id,
                "related_company_name": item["name"],
                "relation_type": item["relation_type"],
                "control_path": "common_controller",
                "risk_flag": item["risk_flag"],
                "unified_social_credit_code": None,
                "industry_category": None,
                "note": item["note"],
            },
        )


def seed_counterparties(cur, company_id, case_id, counterparties):
    ids = []
    for name, counterparty_type, industry, city, tenor, rank in counterparties:
        ids.append(
            insert(
                cur,
                "counterparties",
                {
                    "company_id": company_id,
                    "case_id": case_id,
                    "counterparty_name": name,
                    "counterparty_type": counterparty_type,
                    "industry": industry,
                    "city": city,
                    "relationship_tenor_months": tenor,
                    "concentration_rank": rank,
                    "risk_note": None,
                },
            )
        )
    return ids


def build_financials(cur, company, company_id, case_id, period_ids):
    month_codes = [f"2025-{month:02d}" for month in range(7, 13)]
    metric_lookup = {}
    ar_summary_ids = {}
    annual_statements = compute_annual_statement_payloads(company)
    account_id = insert(
        cur,
        "bank_accounts",
        {
            "company_id": company_id,
            "case_id": case_id,
            "account_name": company["name"],
            "bank_name": "Bank of Demo SME Branch",
            "account_masked": f"6222****{company_id:04d}",
            "account_type": "corporate_settlement",
            "is_primary": 1,
            "opened_on": "2023-03-01",
            "status": "active",
        },
    )
    for idx, period_code in enumerate(month_codes):
        period_id = period_ids[period_code]
        revenue = company["monthly_revenue"][idx]
        cogs = round(revenue * (1 - company["gross_margin"]), 2)
        gross_profit = round(revenue - cogs, 2)
        net_profit = round(revenue * company["net_margin"], 2)
        total_assets = round(revenue * 6.3 + idx * 45000, 2)
        total_liabilities = round(total_assets * (0.52 if company["risk_tier"] == "medium_high" else 0.4 if company["risk_tier"] == "low" else 0.46), 2)
        ar_balance = round(revenue * (1.05 if company["risk_tier"] == "medium_high" else 0.72 if company["risk_tier"] == "low" else 0.9), 2)
        ap_balance = round(revenue * 0.42, 2)
        inventory = round(revenue * (0.34 if company["industry_category"] != "Enterprise Software" else 0.05), 2)
        operating_cf = round(revenue * (0.04 if company["risk_tier"] == "medium_high" else 0.18 if company["risk_tier"] == "low" else 0.1), 2)
        metric_rows = [
            ("revenue", "Revenue", "income_statement", revenue, "CNY"),
            ("cogs", "Cost of Goods Sold", "income_statement", cogs, "CNY"),
            ("gross_profit", "Gross Profit", "income_statement", gross_profit, "CNY"),
            ("net_profit", "Net Profit", "income_statement", net_profit, "CNY"),
            ("total_assets", "Total Assets", "balance_sheet", total_assets, "CNY"),
            ("total_liabilities", "Total Liabilities", "balance_sheet", total_liabilities, "CNY"),
            ("accounts_receivable", "Accounts Receivable", "balance_sheet", ar_balance, "CNY"),
            ("accounts_payable", "Accounts Payable", "balance_sheet", ap_balance, "CNY"),
            ("inventory", "Inventory", "balance_sheet", inventory, "CNY"),
            ("operating_cash_flow", "Operating Cash Flow", "cash_flow", operating_cf, "CNY"),
            ("gross_margin_pct", "Gross Margin", "ratio", round(company["gross_margin"], 4), "ratio"),
            ("asset_liability_ratio", "Asset Liability Ratio", "ratio", round(total_liabilities / total_assets, 4), "ratio"),
        ]
        for metric_code, metric_name, category, value, unit in metric_rows:
            metric_lookup[(period_code, metric_code)] = insert(
                cur,
                "financial_metrics",
                {
                    "company_id": company_id,
                    "case_id": case_id,
                    "period_id": period_id,
                    "metric_code": metric_code,
                    "metric_name": metric_name,
                    "metric_category": category,
                    "value": value,
                    "unit": unit,
                    "currency": "CNY" if unit == "CNY" else None,
                    "source_type": "ocr_extraction",
                    "source_ref": "Management Financial Package",
                    "is_estimated": 0,
                    "note": None,
                },
            )

        declared_revenue = round(revenue * company["tax_ratio"][idx], 2)
        insert(
            cur,
            "tax_filings",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "filing_type": "VAT_summary",
                "declared_revenue_cny": declared_revenue,
                "output_tax_cny": round(declared_revenue * 0.13, 2),
                "input_tax_cny": round(declared_revenue * 0.07, 2),
                "tax_burden_ratio": round(0.03 if company["industry_category"] == "Enterprise Software" else 0.045, 4),
                "filing_status": "submitted",
                "source_ref": "Tax Filing Summary",
            },
        )
        pay_gross = round(revenue * company["pay_channel_share"], 2)
        insert(
            cur,
            "payment_channel_summaries",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "channel_name": "wechat_alipay_aggregate",
                "gross_receipts_cny": pay_gross,
                "refund_amount_cny": round(pay_gross * 0.01, 2),
                "transaction_count": 48 + idx * 3 if pay_gross else 0,
                "source_ref": "Manual payment summary",
            },
        )
        social = company["social_headcount"][idx]
        last_social = company["social_headcount"][idx - 1] if idx else social
        insert(
            cur,
            "social_security_metrics",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "insured_headcount": social,
                "month_change": social - last_social,
                "average_base_cny": round(8600 + idx * 120, 2),
                "source_ref": "Social Security Summary",
            },
        )
        insert(
            cur,
            "utility_metrics",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "utility_type": "power",
                "consumption_value": company["utility_power"][idx],
                "unit": "kwh",
                "yoy_change_pct": round((company["utility_power"][idx] / company["utility_power"][0]) - 1, 4),
                "source_ref": "Utility Usage Report",
            },
        )
        insert(
            cur,
            "utility_metrics",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "utility_type": "water",
                "consumption_value": company["utility_water"][idx],
                "unit": "ton",
                "yoy_change_pct": round((company["utility_water"][idx] / company["utility_water"][0]) - 1, 4),
                "source_ref": "Utility Usage Report",
            },
        )
        insert(
            cur,
            "logistics_metrics",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "shipment_count": company["shipments"][idx],
                "shipment_weight_kg": round(company["shipments"][idx] * 240.5, 2),
                "freight_cost_cny": round(company["shipments"][idx] * 780, 2),
                "return_rate_pct": round(0.01 if company["risk_tier"] == "low" else 0.02, 4),
                "source_ref": "Shipment Summary",
            },
        )
        ar_summary_ids[period_code] = insert(
            cur,
            "receivables_payables",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "record_type": "accounts_receivable",
                "balance_cny": ar_balance,
                "overdue_over_90d_cny": round(ar_balance * (0.22 if company["risk_tier"] == "medium_high" else 0.08 if company["risk_tier"] == "low" else 0.14), 2),
                "top5_ratio_pct": company["customer_top5_ratio"],
                "average_days": round(89 if company["risk_tier"] == "medium_high" else 53 if company["risk_tier"] == "low" else 74, 1),
                "source_ref": "Receivable Aging Summary",
            },
        )
        insert(
            cur,
            "receivables_payables",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "record_type": "accounts_payable",
                "balance_cny": ap_balance,
                "overdue_over_90d_cny": round(ap_balance * 0.06, 2),
                "top5_ratio_pct": 0.62,
                "average_days": 46,
                "source_ref": "Payable Summary",
            },
        )

    page_base = {2023: 1, 2024: 5, 2025: 9}
    statement_orders = {
        "income": [
            ("revenue", "Revenue"),
            ("cogs", "Cost of Goods Sold"),
            ("gross_profit", "Gross Profit"),
            ("selling_expense", "Selling Expense"),
            ("admin_expense", "Administrative Expense"),
            ("rd_expense", "R&D Expense"),
            ("operating_profit", "Operating Profit"),
            ("interest_expense", "Interest Expense"),
            ("income_tax_expense", "Income Tax Expense"),
            ("net_profit", "Net Profit"),
        ],
        "balance": [
            ("cash_and_equivalents", "Cash and Cash Equivalents"),
            ("accounts_receivable", "Accounts Receivable"),
            ("inventory", "Inventory"),
            ("other_current_assets", "Other Current Assets"),
            ("fixed_assets", "Net Fixed Assets"),
            ("intangible_assets", "Intangible Assets"),
            ("other_assets", "Other Assets"),
            ("total_assets", "Total Assets"),
            ("accounts_payable", "Accounts Payable"),
            ("short_term_debt", "Short-term Debt"),
            ("long_term_debt", "Long-term Debt"),
            ("other_liabilities", "Other Liabilities"),
            ("total_liabilities", "Total Liabilities"),
            ("paid_in_capital", "Paid-in Capital"),
            ("retained_earnings", "Retained Earnings"),
            ("total_equity", "Total Equity"),
        ],
        "cashflow": [
            ("beginning_cash_balance", "Beginning Cash Balance"),
            ("net_profit", "Net Profit"),
            ("depreciation_amortization", "Depreciation and Amortization"),
            ("inventory_change", "Inventory Change"),
            ("receivable_change", "Receivable Change"),
            ("payable_change", "Payable Change"),
            ("taxes_paid", "Taxes Paid"),
            ("net_cash_from_operations", "Net Cash from Operations"),
            ("capital_expenditure", "Capital Expenditure"),
            ("net_cash_from_investing", "Net Cash from Investing"),
            ("debt_financing_net", "Net Debt Financing"),
            ("equity_financing_net", "Net Equity Financing"),
            ("dividends_paid", "Dividends Paid"),
            ("net_cash_from_financing", "Net Cash from Financing"),
            ("net_increase_in_cash", "Net Increase in Cash"),
            ("ending_cash_balance", "Ending Cash Balance"),
        ],
    }
    annual_metric_map = [
        ("revenue", "Revenue", "income_statement", lambda data: data["income"]["revenue"], "CNY"),
        ("gross_profit", "Gross Profit", "income_statement", lambda data: data["income"]["gross_profit"], "CNY"),
        ("net_profit", "Net Profit", "income_statement", lambda data: data["income"]["net_profit"], "CNY"),
        ("operating_cash_flow", "Operating Cash Flow", "cash_flow", lambda data: data["cashflow"]["net_cash_from_operations"], "CNY"),
        ("capital_expenditure", "Capital Expenditure", "cash_flow", lambda data: data["cashflow"]["capital_expenditure"], "CNY"),
        ("net_cash_from_investing", "Net Cash from Investing", "cash_flow", lambda data: data["cashflow"]["net_cash_from_investing"], "CNY"),
        ("total_assets", "Total Assets", "balance_sheet", lambda data: data["balance"]["total_assets"], "CNY"),
        ("total_liabilities", "Total Liabilities", "balance_sheet", lambda data: data["balance"]["total_liabilities"], "CNY"),
        ("fixed_assets", "Net Fixed Assets", "balance_sheet", lambda data: data["balance"]["fixed_assets"], "CNY"),
        ("gross_margin_pct", "Gross Margin", "ratio", lambda data: data["ratios"]["gross_margin_pct"], "ratio"),
        ("asset_liability_ratio", "Asset Liability Ratio", "ratio", lambda data: data["ratios"]["asset_liability_ratio"], "ratio"),
        ("rd_ratio_pct", "R&D Ratio", "ratio", lambda data: data["ratios"]["rd_ratio_pct"], "ratio"),
        ("operating_cash_flow_margin_pct", "Operating Cash Flow Margin", "ratio", lambda data: data["ratios"]["operating_cash_flow_margin_pct"], "ratio"),
    ]
    source_document_id = None
    cur.execute(
        "SELECT id FROM documents WHERE case_id = ? AND document_type = 'annual_financial_statements'",
        (case_id,),
    )
    row = cur.fetchone()
    if row:
        source_document_id = row[0]

    prior_year_fixed_assets = None
    for fiscal_year in (2023, 2024, 2025):
        period_code = f"{fiscal_year}FY"
        period_id = period_ids[period_code]
        year_data = annual_statements[fiscal_year]
        for metric_code, metric_name, category, accessor, unit in annual_metric_map:
            value = accessor(year_data)
            metric_lookup[(period_code, metric_code)] = insert(
                cur,
                "financial_metrics",
                {
                    "company_id": company_id,
                    "case_id": case_id,
                    "period_id": period_id,
                    "metric_code": metric_code,
                    "metric_name": metric_name,
                    "metric_category": category,
                    "value": value,
                    "unit": unit,
                    "currency": "CNY" if unit == "CNY" else None,
                    "source_type": "ocr_extraction",
                    "source_ref": "Annual Financial Statements Pack",
                    "is_estimated": 0,
                    "note": f"{fiscal_year} annual statement metric",
                },
            )

        for statement_type, lines in statement_orders.items():
            page_offset = 0 if statement_type == "balance" else 1 if statement_type == "income" else 2
            page_no = page_base[fiscal_year] + page_offset
            for display_order, (line_code, line_name) in enumerate(lines, start=1):
                value = year_data[statement_type][line_code]
                insert(
                    cur,
                    "financial_statement_line_items",
                    {
                        "company_id": company_id,
                        "case_id": case_id,
                        "period_id": period_id,
                        "statement_type": statement_type,
                        "line_code": line_code,
                        "line_name": line_name,
                        "display_order": display_order,
                        "value": value,
                        "unit": "CNY",
                        "source_document_id": source_document_id,
                        "source_page_no": page_no,
                        "source_ref": "Annual Financial Statements Pack",
                        "note": None,
                    },
                )

        total_assets = year_data["balance"]["total_assets"]
        total_liabilities = year_data["balance"]["total_liabilities"]
        total_equity = year_data["balance"]["total_equity"]
        bs_variance = round(total_assets - total_liabilities - total_equity, 2)
        insert(
            cur,
            "financial_reconciliation_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "check_code": "bs_balance",
                "check_name": "Balance sheet equation",
                "statement_scope": "balance_sheet",
                "lhs_label": "Total Assets",
                "lhs_value": total_assets,
                "rhs_label": "Total Liabilities + Total Equity",
                "rhs_value": round(total_liabilities + total_equity, 2),
                "variance_value": bs_variance,
                "variance_ratio": 0.0 if total_assets == 0 else round(abs(bs_variance) / total_assets, 6),
                "threshold_value": 1.0,
                "status": "pass" if abs(bs_variance) <= 1 else "fail",
                "interpretation": "Total assets should equal liabilities plus equity.",
                "linked_finding_id": None,
                "source_document_id": source_document_id,
                "source_page_no": page_base[fiscal_year],
            },
        )

        gp_variance = round(
            year_data["income"]["revenue"] - year_data["income"]["cogs"] - year_data["income"]["gross_profit"],
            2,
        )
        insert(
            cur,
            "financial_reconciliation_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "check_code": "gross_profit_bridge",
                "check_name": "Revenue minus COGS equals gross profit",
                "statement_scope": "income_statement",
                "lhs_label": "Revenue - COGS",
                "lhs_value": round(year_data["income"]["revenue"] - year_data["income"]["cogs"], 2),
                "rhs_label": "Gross Profit",
                "rhs_value": year_data["income"]["gross_profit"],
                "variance_value": gp_variance,
                "variance_ratio": 0.0,
                "threshold_value": 1.0,
                "status": "pass" if abs(gp_variance) <= 1 else "fail",
                "interpretation": "Gross profit should bridge cleanly from revenue and cost.",
                "linked_finding_id": None,
                "source_document_id": source_document_id,
                "source_page_no": page_base[fiscal_year] + 1,
            },
        )

        expected_capex = year_data["cashflow"]["capital_expenditure"]
        if prior_year_fixed_assets is None:
            rhs_capex = round(year_data["cashflow"]["depreciation_amortization"] + year_data["balance"]["fixed_assets"] * 0.18, 2)
        else:
            rhs_capex = round(
                year_data["balance"]["fixed_assets"] - prior_year_fixed_assets + year_data["cashflow"]["depreciation_amortization"],
                2,
            )
        capex_variance = round(expected_capex - rhs_capex, 2)
        capex_ratio = round(abs(capex_variance) / max(abs(expected_capex), 1), 4)
        capex_status = "pass" if capex_ratio <= 0.03 else "warn" if capex_ratio <= 0.1 else "fail"
        insert(
            cur,
            "financial_reconciliation_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "check_code": "fixed_asset_capex",
                "check_name": "Capex versus fixed asset roll-forward",
                "statement_scope": "cash_flow_balance_bridge",
                "lhs_label": "Capital Expenditure",
                "lhs_value": expected_capex,
                "rhs_label": "Fixed Asset Delta + Depreciation",
                "rhs_value": rhs_capex,
                "variance_value": capex_variance,
                "variance_ratio": capex_ratio,
                "threshold_value": 0.1,
                "status": capex_status,
                "interpretation": "High variance suggests capex or fixed asset roll-forward needs manual support.",
                "linked_finding_id": None,
                "source_document_id": source_document_id,
                "source_page_no": page_base[fiscal_year] + 2,
            },
        )

        cashflow = year_data["cashflow"]
        cash_bridge_lhs = round(cashflow["beginning_cash_balance"] + cashflow["net_increase_in_cash"], 2)
        cash_bridge_rhs = cashflow["ending_cash_balance"]
        cash_bridge_variance = round(cash_bridge_lhs - cash_bridge_rhs, 2)
        insert(
            cur,
            "financial_reconciliation_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "check_code": "cash_rollforward",
                "check_name": "Cash roll-forward",
                "statement_scope": "cash_flow_statement",
                "lhs_label": "Beginning Cash + Net Increase",
                "lhs_value": cash_bridge_lhs,
                "rhs_label": "Ending Cash",
                "rhs_value": cash_bridge_rhs,
                "variance_value": cash_bridge_variance,
                "variance_ratio": 0.0 if cash_bridge_rhs == 0 else round(abs(cash_bridge_variance) / cash_bridge_rhs, 6),
                "threshold_value": 1.0,
                "status": "pass" if abs(cash_bridge_variance) <= 1 else "fail",
                "interpretation": "Cash flow statement roll-forward should fully tie.",
                "linked_finding_id": None,
                "source_document_id": source_document_id,
                "source_page_no": page_base[fiscal_year] + 2,
            },
        )

        profit_cash_gap = round(cashflow["net_cash_from_operations"] - year_data["income"]["net_profit"], 2)
        profit_cash_ratio = round(abs(profit_cash_gap) / max(abs(year_data["income"]["net_profit"]), 1), 4)
        profit_cash_status = "pass" if profit_cash_ratio <= 0.25 else "warn" if profit_cash_ratio <= 0.45 else "fail"
        insert(
            cur,
            "financial_reconciliation_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "check_code": "profit_to_operating_cash",
                "check_name": "Net profit to operating cash conversion",
                "statement_scope": "income_cashflow_bridge",
                "lhs_label": "Net Cash from Operations",
                "lhs_value": cashflow["net_cash_from_operations"],
                "rhs_label": "Net Profit",
                "rhs_value": year_data["income"]["net_profit"],
                "variance_value": profit_cash_gap,
                "variance_ratio": profit_cash_ratio,
                "threshold_value": 0.45,
                "status": profit_cash_status,
                "interpretation": "Large gaps between profit and operating cash need working-capital explanation.",
                "linked_finding_id": None,
                "source_document_id": source_document_id,
                "source_page_no": page_base[fiscal_year] + 2,
            },
        )

        prior_year_fixed_assets = year_data["balance"]["fixed_assets"]
    return account_id, metric_lookup, ar_summary_ids


def seed_sme_bank_settlement_summaries(cur, company, company_id, case_id, period_ids):
    month_codes = [f"2025-{month:02d}" for month in range(7, 13)]
    for idx, period_code in enumerate(month_codes):
        period_id = period_ids[period_code]
        revenue = company["monthly_revenue"][idx]
        inflow = round(revenue * company["bank_in_ratio"][idx], 2)
        outflow = round(revenue * (0.71 if company["risk_tier"] == "medium_high" else 0.64 if company["risk_tier"] == "low" else 0.67), 2)
        avg_balance = round(revenue * (0.42 if company["risk_tier"] == "medium_high" else 0.65 if company["risk_tier"] == "low" else 0.52), 2)
        insert(
            cur,
            "bank_settlement_summaries",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "inflow_total_cny": inflow,
                "outflow_total_cny": outflow,
                "net_flow_cny": round(inflow - outflow, 2),
                "average_daily_balance_cny": avg_balance,
                "top_inflow_counterparty": company["counterparties"][0][0],
                "top_inflow_amount_cny": round(inflow * 0.38, 2),
                "top_outflow_counterparty": company["counterparties"][3][0],
                "top_outflow_amount_cny": round(outflow * 0.33, 2),
                "transaction_count": 18 + idx * 2,
                "large_transaction_count": 2 if company["risk_tier"] == "low" else 3 if company["risk_tier"] == "medium" else 4,
                "abnormal_fluctuation_flag": 1 if company["risk_tier"] == "medium_high" and idx >= 4 else 0,
                "summary_note": "Monthly settlement summary derived from seeded bank statement behavior.",
                "source_ref": "Bank Statement Summary",
            },
        )


def seed_sme_tax_invoice_checks(cur, company, company_id, case_id, period_ids):
    month_codes = [f"2025-{month:02d}" for month in range(7, 13)]
    for idx, period_code in enumerate(month_codes):
        period_id = period_ids[period_code]
        revenue = company["monthly_revenue"][idx]
        declared = round(revenue * company["tax_ratio"][idx], 2)
        invoiced = round(revenue * (0.97 if company["risk_tier"] == "low" else 0.94 if company["risk_tier"] == "medium" else 0.88), 2)
        bank_receipts = round(revenue * company["bank_in_ratio"][idx], 2)
        gap = round(abs(declared - invoiced), 2)
        receipt_gap = round(abs(invoiced - bank_receipts), 2)
        gap_ratio = round(max(gap, receipt_gap) / max(revenue, 1), 4)
        status = "pass" if gap_ratio <= 0.06 else "warn" if gap_ratio <= 0.14 else "fail"
        insert(
            cur,
            "tax_invoice_consistency_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "declared_revenue_cny": declared,
                "invoiced_amount_cny": invoiced,
                "bank_receipts_cny": bank_receipts,
                "output_tax_cny": round(declared * 0.13, 2),
                "input_tax_cny": round(declared * 0.07, 2),
                "invoice_count": 8 + idx,
                "revenue_invoice_gap_cny": gap,
                "invoice_receipt_gap_cny": receipt_gap,
                "gap_ratio": gap_ratio,
                "status": status,
                "check_note": "Revenue, invoice, and bank receipt consistency summary for demo tax dimension.",
                "source_ref": "Tax Filing Summary + invoice pack",
            },
        )


def seed_sme_related_party_transactions(cur, company, company_id, case_id, period_ids):
    latest_period_id = period_ids["2025FY"]
    relateds = company.get("related_companies", [])
    if not relateds:
        return
    ratio = 0.08 if company["risk_tier"] == "low" else 0.12 if company["risk_tier"] == "medium" else 0.18
    amount = round(sum(company["monthly_revenue"]) * 2.02 * ratio, 2)
    for idx, related in enumerate(relateds, start=1):
        insert(
            cur,
            "related_party_transaction_summaries",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": latest_period_id,
                "related_party_name": related["name"],
                "relation_type": related["relation_type"],
                "transaction_type": "purchase" if idx % 2 else "fund_transfer",
                "transaction_amount_cny": amount if idx == 1 else round(amount * 0.36, 2),
                "revenue_or_cost_ratio": ratio if idx == 1 else round(ratio * 0.36, 4),
                "settlement_method": "bank_transfer",
                "pricing_comment": "定价处于参考区间内" if company["risk_tier"] == "low" else "定价与结算安排仍需补充说明。",
                "risk_level": "low" if company["risk_tier"] == "low" else "medium" if company["risk_tier"] == "medium" else "high",
                "source_ref": "Related-party manual summary",
                "note": related.get("note"),
            },
        )


def seed_sme_credit_history(cur, company, company_id, case_id, person_ids):
    company_rows = {
        "low": (4, 1800000, 0, "none", 1, 2, 250000, "good", "Enterprise credit history is broadly clean with limited external guarantees."),
        "medium": (6, 3200000, 1, "M1", 2, 4, 480000, "watch", "Mild concentration and leverage require monitoring but no severe adverse history."),
        "medium_high": (8, 5100000, 2, "M2", 4, 7, 860000, "watch", "Borrower shows higher leverage and query activity; review bank inquiry context."),
    }[company["risk_tier"]]
    insert(
        cur,
        "credit_history_summaries",
        {
            "company_id": company_id,
            "case_id": case_id,
            "subject_type": "enterprise",
            "subject_name": company["name"],
            "linked_person_id": None,
            "credit_channel": "enterprise_credit_summary",
            "account_count": company_rows[0],
            "outstanding_balance_cny": company_rows[1],
            "overdue_count": company_rows[2],
            "max_overdue_bucket": company_rows[3],
            "hard_inquiry_3m": company_rows[4],
            "hard_inquiry_6m": company_rows[5],
            "external_guarantee_exposure_cny": company_rows[6],
            "credit_assessment": company_rows[7],
            "summary_note": company_rows[8],
            "source_ref": "Demo credit summary",
        },
    )
    controller_id = None
    controller_name = None
    for person in company["persons"]:
        if person["controller"]:
            controller_id = person_ids.get(person["code"])
            controller_name = person["name"]
            break
    if controller_name:
        insert(
            cur,
            "credit_history_summaries",
            {
                "company_id": company_id,
                "case_id": case_id,
                "subject_type": "controller",
                "subject_name": controller_name,
                "linked_person_id": controller_id,
                "credit_channel": "personal_credit_summary",
                "account_count": 3 if company["risk_tier"] == "low" else 5 if company["risk_tier"] == "medium" else 6,
                "outstanding_balance_cny": 420000 if company["risk_tier"] == "low" else 860000 if company["risk_tier"] == "medium" else 1350000,
                "overdue_count": 0 if company["risk_tier"] == "low" else 1,
                "max_overdue_bucket": "none" if company["risk_tier"] == "low" else "M1" if company["risk_tier"] == "medium" else "M2",
                "hard_inquiry_3m": 1 if company["risk_tier"] == "low" else 2 if company["risk_tier"] == "medium" else 4,
                "hard_inquiry_6m": 2 if company["risk_tier"] == "low" else 4 if company["risk_tier"] == "medium" else 6,
                "external_guarantee_exposure_cny": 0 if company["risk_tier"] == "low" else 300000 if company["risk_tier"] == "medium" else 1200000,
                "credit_assessment": "good" if company["risk_tier"] == "low" else "watch",
                "summary_note": "Controller credit profile summarized for demo use; replace with authorized credit report if available.",
                "source_ref": "Demo credit summary",
            },
        )


def seed_sme_priority_dimensions(cur, company, company_id, case_id, period_ids, person_ids):
    seed_sme_bank_settlement_summaries(cur, company, company_id, case_id, period_ids)
    seed_sme_tax_invoice_checks(cur, company, company_id, case_id, period_ids)
    seed_sme_related_party_transactions(cur, company, company_id, case_id, period_ids)
    seed_sme_credit_history(cur, company, company_id, case_id, person_ids)


def seed_contracts_and_cash(cur, company, company_id, case_id, counterparty_ids, document_ids, account_id, ar_summary_ids):
    customer_ids = counterparty_ids[:3]
    supplier_ids = counterparty_ids[3:]
    contracts = []
    contract_count = 5 if company["company_code"] == "COMP-001" else 3
    for idx in range(contract_count):
        customer_id = customer_ids[idx % len(customer_ids)]
        contract_id = insert(
            cur,
            "contracts",
            {
                "company_id": company_id,
                "case_id": case_id,
                "counterparty_id": customer_id,
                "contract_no": f"{company['company_code']}-CTR-{idx+1:03d}",
                "contract_type": "sales",
                "sign_date": f"2025-{7 + (idx % 6):02d}-05",
                "amount_cny": round(company["monthly_revenue"][idx % 6] * (1.2 + idx * 0.08), 2),
                "payment_terms": "30% advance, 70% within 60 days after acceptance",
                "delivery_terms": "Batch delivery with customer acceptance",
                "performance_status": "performing",
                "source_document_id": document_ids["core_contract"],
                "note": None,
            },
        )
        order_id = insert(
            cur,
            "orders",
            {
                "company_id": company_id,
                "case_id": case_id,
                "contract_id": contract_id,
                "order_no": f"{company['company_code']}-ORD-{idx+1:03d}",
                "order_date": f"2025-{7 + (idx % 6):02d}-08",
                "order_amount_cny": round(company["monthly_revenue"][idx % 6] * (0.9 + idx * 0.05), 2),
                "delivery_due_date": f"2025-{7 + (idx % 6):02d}-28",
                "collection_milestones": "Acceptance + 60 days",
                "performance_status": "delivered",
            },
        )
        invoice_id = insert(
            cur,
            "invoices",
            {
                "company_id": company_id,
                "case_id": case_id,
                "contract_id": contract_id,
                "counterparty_id": customer_id,
                "invoice_no": f"{company['company_code'][-3:]}INV{idx+1:04d}",
                "invoice_type": "vat_special",
                "issue_date": f"2025-{7 + (idx % 6):02d}-18",
                "amount_cny": round(company["monthly_revenue"][idx % 6] * (0.7 + idx * 0.05), 2),
                "tax_rate_pct": 13.0,
                "buyer_name": None,
                "seller_name": company["name"],
                "note": None,
            },
        )
        contracts.append((contract_id, order_id, invoice_id))

    tx_ids = []
    month_codes = [f"2025-{month:02d}" for month in range(7, 13)]
    running_balance = 450000
    for idx, period_code in enumerate(month_codes):
        receipts_total = round(company["monthly_revenue"][idx] * company["bank_in_ratio"][idx], 2)
        for slice_idx in range(2):
            linked_contract_id, _, linked_invoice_id = contracts[(idx + slice_idx) % len(contracts)]
            amt = round(receipts_total * (0.58 if slice_idx == 0 else 0.42), 2)
            running_balance += amt
            tx_ids.append(
                insert(
                    cur,
                    "bank_transactions",
                    {
                        "account_id": account_id,
                        "case_id": case_id,
                        "txn_date": f"{period_code}-1{slice_idx+1}",
                        "txn_direction": "credit",
                        "counterparty_name": company["counterparties"][slice_idx][0],
                        "counterparty_account_masked": "6222****8899",
                        "amount_cny": amt,
                        "balance_after_cny": round(running_balance, 2),
                        "txn_summary": "Contract collection",
                        "linked_contract_id": linked_contract_id,
                        "linked_invoice_id": linked_invoice_id,
                        "source_ref": "Bank Statement Summary",
                    },
                )
            )
        supplier_payment = round(company["monthly_revenue"][idx] * 0.31, 2)
        running_balance -= supplier_payment
        tx_ids.append(
            insert(
                cur,
                "bank_transactions",
                {
                    "account_id": account_id,
                    "case_id": case_id,
                    "txn_date": f"{period_code}-23",
                    "txn_direction": "debit",
                    "counterparty_name": company["counterparties"][3][0],
                    "counterparty_account_masked": "6222****5566",
                    "amount_cny": supplier_payment,
                    "balance_after_cny": round(running_balance, 2),
                    "txn_summary": "Supplier payment",
                    "linked_contract_id": None,
                    "linked_invoice_id": None,
                    "source_ref": "Bank Statement Summary",
                },
            )
        )

    for idx, (contract_id, order_id, invoice_id) in enumerate(contracts):
        month_code = month_codes[idx % len(month_codes)]
        bank_txn_id = tx_ids[idx * 3] if idx * 3 < len(tx_ids) else tx_ids[-1]
        insert(
            cur,
            "contract_cash_links",
            {
                "case_id": case_id,
                "contract_id": contract_id,
                "order_id": order_id,
                "invoice_id": invoice_id,
                "bank_transaction_id": bank_txn_id,
                "receivable_record_id": ar_summary_ids[month_code],
                "link_type": "invoice_to_cash",
                "linked_amount_cny": round(company["monthly_revenue"][idx % 6] * 0.55, 2),
                "confidence": 0.92 if company["risk_tier"] == "low" else 0.78,
                "note": "Demo linkage across contract, invoice, receipt, and receivable.",
            },
        )
    return contracts, tx_ids


def seed_innovation(cur, company, company_id, case_id, period_ids, person_ids):
    month_codes = [f"2025-{month:02d}" for month in range(9, 13)]
    owner_person_id = None
    for person in company["persons"]:
        if person["role"] == "core_executive":
            owner_person_id = person_ids[person["code"]]
            break
    for idx in range(company["ip_count"]):
        insert(
            cur,
            "ip_assets",
            {
                "company_id": company_id,
                "case_id": case_id,
                "asset_type": "patent" if idx < 2 else "software_copyright",
                "asset_name": f"{company['subindustry']} core asset {idx+1}",
                "registration_no": f"{company['company_code']}-IP-{idx+1:03d}",
                "ownership_holder": company["name"],
                "grant_date": f"2023-{(idx % 9) + 1:02d}-10",
                "expiry_date": "2033-12-31",
                "status": "active",
                "pledged_flag": 0,
                "source_ref": "IP and Qualification Pack",
            },
        )
    qualifications = [
        ("High and New Technology Enterprise", "Local Science Bureau"),
        ("Technology-based SME", "MIIT/Science Service"),
    ]
    for name, authority in qualifications:
        insert(
            cur,
            "innovation_qualifications",
            {
                "company_id": company_id,
                "case_id": case_id,
                "qualification_name": name,
                "issuing_authority": authority,
                "valid_from": "2024-01-01",
                "valid_to": "2027-12-31",
                "status": "active",
                "source_ref": "IP and Qualification Pack",
            },
        )
    for idx in range(2):
        insert(
            cur,
            "rd_projects",
            {
                "company_id": company_id,
                "case_id": case_id,
                "project_name": f"{company['subindustry']} program {idx+1}",
                "stage": "pilot" if idx == 0 else "commercialization",
                "owner_person_id": owner_person_id,
                "budget_cny": round(sum(company["monthly_revenue"]) * company["rd_ratio"] * (0.8 + idx * 0.35), 2),
                "spent_cny": round(sum(company["monthly_revenue"]) * company["rd_ratio"] * (0.45 + idx * 0.2), 2),
                "expected_commercialization_date": f"2026-0{idx+8}-30",
                "summary": "Core R&D item used in demo report generation.",
            },
        )
    for period_code in month_codes:
        period_id = period_ids[period_code]
        idx = int(period_code[-2:]) - 7
        insert(
            cur,
            "rd_team_metrics",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "rd_headcount": max(8, round(company["social_headcount"][idx] * company["rd_ratio"] * 1.1)),
                "masters_or_above": max(3, round(company["social_headcount"][idx] * company["rd_ratio"] * 0.45)),
                "rd_ratio_pct": round(company["rd_ratio"], 4),
                "annualized_rd_spend_cny": round(sum(company["monthly_revenue"]) * company["rd_ratio"] * 2, 2),
                "source_ref": "R&D headcount summary",
            },
        )
    insert(
        cur,
        "intangible_asset_notes",
        {
            "company_id": company_id,
            "case_id": case_id,
            "note_type": "ownership",
            "title": "IP ownership review",
            "content": "Core patents and software rights are registered under the borrower entity, with no material pledge or ownership dispute identified in the demo pack.",
            "pledge_status": "none",
            "dispute_status": "none",
            "source_ref": "IP and Qualification Pack",
        },
    )


def seed_public_and_peers(cur, company, company_id, case_id, benchmark_ids):
    for event_type, severity, event_date, counterparty_name, title, summary, source_name in company["risk_events"]:
        insert(
            cur,
            "public_risk_events",
            {
                "company_id": company_id,
                "case_id": case_id,
                "event_type": event_type,
                "severity": severity,
                "event_date": event_date,
                "counterparty_name": counterparty_name,
                "title": title,
                "summary": summary,
                "public_source_name": source_name,
                "public_url": None,
                "source_ref": "Public Risk Screenshot Bundle",
            },
        )
    for change_date, change_type, before_snapshot, after_snapshot, declared_reason, risk_comment in company["shareholding_changes"]:
        insert(
            cur,
            "shareholding_changes",
            {
                "company_id": company_id,
                "case_id": case_id,
                "change_date": change_date,
                "change_type": change_type,
                "before_snapshot": before_snapshot,
                "after_snapshot": after_snapshot,
                "declared_reason": declared_reason,
                "risk_comment": risk_comment,
            },
        )
    benchmark_map = {
        "gross_margin_pct": round(company["gross_margin"], 4),
        "asset_liability_ratio": 0.52 if company["risk_tier"] == "medium_high" else 0.4 if company["risk_tier"] == "low" else 0.46,
        "rd_ratio_pct": round(company["rd_ratio"], 4),
    }
    for metric_code, company_value in benchmark_map.items():
        benchmark_id = benchmark_ids[(company["subindustry"], metric_code)]
        cur.execute(
            "SELECT benchmark_value, percentile_25, percentile_50, percentile_75 FROM industry_benchmarks WHERE id = ?",
            (benchmark_id,),
        )
        benchmark_value, p25, p50, p75 = cur.fetchone()
        variance_pct = round((company_value - benchmark_value) / benchmark_value, 4) if benchmark_value else 0
        if company_value <= p25:
            bucket = "bottom_quartile"
        elif company_value >= p75:
            bucket = "top_quartile"
        elif company_value >= p50:
            bucket = "upper_middle"
        else:
            bucket = "lower_middle"
        insert(
            cur,
            "peer_comparisons",
            {
                "case_id": case_id,
                "company_id": company_id,
                "benchmark_id": benchmark_id,
                "company_value": company_value,
                "variance_pct": variance_pct,
                "percentile_bucket": bucket,
                "narrative": f"{metric_code} sits in {bucket} for {company['subindustry']}.",
            },
        )


def seed_findings_reports(cur, company, company_id, case_id, rule_ids, document_ids, page_ids, source_ids):
    finding_ids = []
    for rule_code, severity, title, summary, impact, confidence, status, manual in company["findings"]:
        finding_id = insert(
            cur,
            "validation_findings",
            {
                "case_id": case_id,
                "company_id": company_id,
                "rule_id": rule_ids[rule_code],
                "severity": severity,
                "finding_title": title,
                "finding_summary": summary,
                "impact_summary": impact,
                "confidence": confidence,
                "status": status,
                "requires_manual_review": manual,
            },
        )
        finding_ids.append((rule_code, finding_id))
    for tag_code, tag_name, dimension, severity, description in company["risk_tags"]:
        insert(
            cur,
            "risk_tags",
            {
                "case_id": case_id,
                "company_id": company_id,
                "tag_code": tag_code,
                "tag_name": tag_name,
                "dimension": dimension,
                "severity": severity,
                "description": description,
            },
        )
    bands = [
        (0, "weak"),
        (60, "watch"),
        (75, "good"),
        (85, "strong"),
    ]
    for dimension, value in company["requested_score_base"].items():
        band = "weak"
        for threshold, label in bands:
            if value >= threshold:
                band = label
        insert(
            cur,
            "case_risk_scores",
            {
                "case_id": case_id,
                "company_id": company_id,
                "score_dimension": dimension,
                "score_value": value,
                "score_band": band,
                "rationale": f"{dimension} score derived from seeded demo evidence.",
            },
        )
    section_ids = []
    for display_order, (code, title, content, confidence) in enumerate(company["report_sections"], start=1):
        section_id = insert(
            cur,
            "report_sections",
            {
                "case_id": case_id,
                "company_id": company_id,
                "section_code": code,
                "section_title": title,
                "content": content,
                "confidence": confidence,
                "display_order": display_order,
            },
        )
        section_ids.append((code, section_id))
    recommendation = company["recommendation"]
    insert(
        cur,
        "credit_recommendations",
        {
            "case_id": case_id,
            "company_id": company_id,
            "recommendation_status": recommendation["status"],
            "suggested_amount_cny": recommendation["amount"],
            "suggested_term_months": recommendation["term"],
            "suggested_rate_min": recommendation["rate_min"],
            "suggested_rate_max": recommendation["rate_max"],
            "guarantee_requirement": recommendation["guarantee_requirement"],
            "supplemental_requirements": recommendation["supplemental_requirements"],
            "rejection_reason": recommendation["rejection_reason"],
            "note": recommendation["note"],
        },
    )

    evidence_templates = {
        "revenue_triangle_check": ("financial_pack", 2, "bank_statement", 1),
        "utility_output_deviation": ("utility_report" if "utility_report" in document_ids else "financial_pack", 1, "financial_pack", 3),
        "customer_concentration": ("financial_pack", 4, "core_contract", 2),
        "contract_cash_match": ("core_contract", 2, "bank_statement", 2),
        "rd_substance_check": ("ip_pack", 1, "ip_pack", 2),
        "cash_flow_cover": ("bank_statement", 3, "tax_summary", 2),
    }
    for rule_code, finding_id in finding_ids:
        primary_doc, primary_page, secondary_doc, secondary_page = evidence_templates.get(
            rule_code, ("financial_pack", 1, "public_risk", 1)
        )
        for doc_type, page_no, kind in [
            (primary_doc, primary_page, "primary"),
            (secondary_doc, secondary_page, "supporting"),
        ]:
            page_key = (doc_type, page_no)
            if page_key not in page_ids:
                continue
            insert(
                cur,
                "evidence_refs",
                {
                    "case_id": case_id,
                    "source_id": source_ids["client_upload"],
                    "document_id": document_ids[doc_type],
                    "page_id": page_ids[page_key],
                    "target_type": "validation_finding",
                    "target_id": finding_id,
                    "evidence_kind": kind,
                    "excerpt": f"Evidence for {rule_code}",
                    "evidence_uri": f"uploads/{company['company_code'].lower()}/{doc_type}_p{page_no}.png",
                    "confidence": 0.88 if kind == "primary" else 0.76,
                    "notes": None,
                },
            )
    for code, section_id in section_ids:
        doc_type = "public_risk" if code == "risks" else "financial_pack"
        page_no = 1 if code == "company_profile" else 2 if code == "operations" else 1
        insert(
            cur,
            "evidence_refs",
            {
                "case_id": case_id,
                "source_id": source_ids["manual_research"] if code == "risks" else source_ids["ocr_extraction"],
                "document_id": document_ids[doc_type],
                "page_id": page_ids[(doc_type, page_no)],
                "target_type": "report_section",
                "target_id": section_id,
                "evidence_kind": "report_backing",
                "excerpt": f"Evidence backing report section {code}",
                "evidence_uri": f"uploads/{company['company_code'].lower()}/{doc_type}_p{page_no}.png",
                "confidence": 0.8,
                "notes": None,
            },
        )


def cache_json(cache_conn, table, ts_code):
    cur = cache_conn.cursor()
    cur.execute(f"SELECT payload FROM {table} WHERE ts_code = ?", (ts_code,))
    row = cur.fetchone()
    return json.loads(row[0]) if row and row[0] else None


def cache_rows(cache_conn, table, ts_code):
    cur = cache_conn.cursor()
    cur.execute(f"SELECT payload FROM {table} WHERE ts_code = ?", (ts_code,))
    return [json.loads(row[0]) for row in cur.fetchall()]


def normalize_profile_items(profile_payload, company_payload):
    items = []
    if profile_payload and profile_payload.get("profile"):
        for entry in profile_payload["profile"]:
            label = entry[0]
            value = entry[1] if len(entry) > 1 else None
            note = entry[2] if len(entry) > 2 else None
            items.append((label, value, note))
    else:
        items = [
            ("客户名称", company_payload.get("short_name") or company_payload.get("name"), "来自本地 AkShare 企业缓存"),
            ("股票代码", company_payload.get("ts_code"), "本地 AkShare 企业缓存主键"),
            ("交易所", company_payload.get("exchange"), "根据缓存股票代码确定"),
            ("国标行业", company_payload.get("industry"), "公开市场行业字段"),
            ("企业概况", company_payload.get("summary"), "本地 AkShare 企业摘要"),
        ]
    return items


def parse_profile_value(profile_items, label):
    for item_label, value, _note in profile_items:
        if item_label == label:
            return value
    return None


def period_boundaries(period):
    year = int(period[:4])
    month = int(period[4:6])
    day = int(period[6:8])
    if month == 12 and day == 31:
        return "annual", f"{year}-01-01", f"{year}-12-31", year, None
    quarter_starts = {3: "01-01", 6: "04-01", 9: "07-01"}
    quarter_ends = {3: "03-31", 6: "06-30", 9: "09-30"}
    if month in quarter_starts:
        return "quarterly", f"{year}-{quarter_starts[month]}", f"{year}-{quarter_ends[month]}", year, month
    return "snapshot", f"{year}-{month:02d}-01", f"{year}-{month:02d}-{day:02d}", year, month


def insert_listed_documents(cur, case_id, company_id, source_ids, ts_code, report_payloads):
    docs = {}
    pages = {}
    document_defs = [
        ("public_profile", "Listed Company Public Profile", "akshare_cache", 2, 1, None, "2026-05-08"),
        ("annual_financial_statements", "Listed Company Financial Statements", "akshare_cache", 12, 1, None, "2026-05-08"),
        ("industry_insights", "Industry Insight Snapshot", "akshare_cache", 2, 0, None, "2026-05-08"),
    ]
    for report in report_payloads[:3]:
        title = report.get("title") or "Annual Report Notice"
        document_defs.append(("annual_report_notice", title, "cninfo_report", 1, 0, report.get("url"), report.get("date")))

    for doc_type, title, source_name, page_count, is_ocr, external_url, document_date in document_defs:
        doc_id = insert(
            cur,
            "documents",
            {
                "case_id": case_id,
                "company_id": company_id,
                "person_id": None,
                "source_id": source_ids[source_name],
                "document_type": doc_type,
                "title": title,
                "source_label": source_name,
                "file_uri": f"listed/{ts_code}/{doc_type}.md",
                "external_url": external_url,
                "page_count": page_count,
                "uploaded_at": "2026-05-08T15:00:00",
                "document_date": document_date,
                "is_ocr_processed": is_ocr,
                "checksum": f"{ts_code}-{doc_type}-{title[:16]}",
                "summary": f"{title} for {ts_code}",
            },
        )
        docs.setdefault(doc_type, []).append(doc_id)
        for page_no in range(1, page_count + 1):
            page_id = insert(
                cur,
                "document_pages",
                {
                    "document_id": doc_id,
                    "page_no": page_no,
                    "image_uri": f"listed/{ts_code}/{doc_type}_p{page_no}.png",
                    "ocr_text": f"{title} page {page_no} for {ts_code}",
                    "layout_summary": f"{doc_type} page {page_no}",
                    "extracted_json": json.dumps({"ts_code": ts_code, "doc_type": doc_type, "page_no": page_no}, ensure_ascii=False),
                },
            )
            pages[(doc_id, page_no)] = page_id
    return docs, pages


def seed_listed_company_case(cur, company_payload, risk_tier):
    company_id = insert(
        cur,
        "companies",
        {
            "company_code": company_payload["ts_code"],
            "name": company_payload.get("name") or company_payload.get("short_name"),
            "unified_social_credit_code": None,
            "established_on": None,
            "region_province": None,
            "region_city": None,
            "industry_category": company_payload.get("industry") or "A股上市公司",
            "subindustry": company_payload.get("industry") or "A股上市公司",
            "is_tech_sme": 0,
            "enterprise_scale": "listed",
            "operating_status": "listed_active",
            "registered_capital_cny": None,
            "paid_in_capital_cny": None,
            "website": None,
            "overview": company_payload.get("summary"),
            "risk_tier": risk_tier,
            "shell_type": "listed_real_cache",
            "notes": f"Imported from local AkShare cache for {company_payload['ts_code']}.",
        },
    )
    case_id = insert(
        cur,
        "due_diligence_cases",
        {
            "case_no": f"LISTED-{company_payload['symbol']}",
            "company_id": company_id,
            "case_name": f"{company_payload.get('short_name') or company_payload.get('name')} public market data pack",
            "application_date": "2026-05-08",
            "product_type": "listed_company_public_pack",
            "requested_amount_cny": 0,
            "requested_term_months": 0,
            "current_stage": "data_pack_ready",
            "decision_status": "public_analysis_only",
            "case_owner": "System Cache Import",
            "summary": company_payload.get("summary"),
        },
    )
    insert(
        cur,
        "loan_applications",
        {
            "case_id": case_id,
            "product_name": "Listed company public analysis",
            "requested_amount_cny": 0,
            "approved_amount_cny": None,
            "loan_purpose": "Public-market benchmarking only",
            "primary_repayment_source": "Not applicable",
            "secondary_repayment_source": "Not applicable",
            "repayment_method": "not_applicable",
            "guarantee_mode": "none",
            "annual_rate_min": None,
            "annual_rate_max": None,
            "tenor_months": 0,
        },
    )
    insert(
        cur,
        "credit_recommendations",
        {
            "case_id": case_id,
            "company_id": company_id,
            "recommendation_status": "public_pack_only",
            "suggested_amount_cny": None,
            "suggested_term_months": None,
            "suggested_rate_min": None,
            "suggested_rate_max": None,
            "guarantee_requirement": None,
            "supplemental_requirements": "If used in credit workflow, supplement shareholder, legal representative, and exposure structure from external enterprise data providers.",
            "rejection_reason": None,
            "note": "Listed-company sample imported from local AkShare cache and annual-report links.",
        },
    )
    return company_id, case_id


def insert_listed_financial_period(cur, company_id, case_id, period):
    period_type, start_date, end_date, fiscal_year, fiscal_month = period_boundaries(period)
    return insert(
        cur,
        "financial_periods",
        {
            "company_id": company_id,
            "case_id": case_id,
            "period_code": period,
            "period_type": period_type,
            "start_date": start_date,
            "end_date": end_date,
            "fiscal_year": fiscal_year,
            "fiscal_month": fiscal_month,
            "is_latest": 1 if period == "20251231" else 0,
        },
    )


def listed_metric_rows(period_payload):
    balance = period_payload.get("balance", {})
    income = period_payload.get("income", {})
    cashflow = period_payload.get("cashflow", {})
    indicators = period_payload.get("indicators", {})
    rows = [
        ("revenue", "Revenue", "income_statement", income.get("revenue"), "CNY"),
        ("operating_cost", "Operating Cost", "income_statement", income.get("operating_cost"), "CNY"),
        ("net_profit", "Net Profit", "income_statement", income.get("net_profit"), "CNY"),
        ("selling_expense", "Selling Expense", "income_statement", income.get("selling_expense"), "CNY"),
        ("admin_expense", "Administrative Expense", "income_statement", income.get("admin_expense"), "CNY"),
        ("finance_expense", "Finance Expense", "income_statement", income.get("finance_expense"), "CNY"),
        ("rd_expense", "R&D Expense", "income_statement", income.get("rd_expense"), "CNY"),
        ("operating_profit", "Operating Profit", "income_statement", income.get("operating_profit"), "CNY"),
        ("cash", "Cash", "balance_sheet", balance.get("cash"), "CNY"),
        ("accounts_receivable", "Accounts Receivable", "balance_sheet", balance.get("accounts_receivable"), "CNY"),
        ("inventory", "Inventory", "balance_sheet", balance.get("inventory"), "CNY"),
        ("total_assets", "Total Assets", "balance_sheet", balance.get("total_assets"), "CNY"),
        ("total_liabilities", "Total Liabilities", "balance_sheet", balance.get("total_liabilities"), "CNY"),
        ("accounts_payable", "Accounts Payable", "balance_sheet", balance.get("accounts_payable"), "CNY"),
        ("short_debt", "Short-term Debt", "balance_sheet", balance.get("short_debt"), "CNY"),
        ("shareholder_equity", "Shareholder Equity", "balance_sheet", balance.get("shareholder_equity"), "CNY"),
        ("fixed_assets", "Fixed Assets", "balance_sheet", balance.get("fixed_assets"), "CNY"),
        ("intangible_assets", "Intangible Assets", "balance_sheet", balance.get("intangible_assets"), "CNY"),
        ("operating_cashflow", "Operating Cash Flow", "cash_flow", cashflow.get("operating_cashflow"), "CNY"),
        ("investing_cashflow", "Investing Cash Flow", "cash_flow", cashflow.get("investing_cashflow"), "CNY"),
        ("financing_cashflow", "Financing Cash Flow", "cash_flow", cashflow.get("financing_cashflow"), "CNY"),
        ("net_cashflow", "Net Cash Flow", "cash_flow", cashflow.get("net_cashflow"), "CNY"),
        ("capital_expenditure", "Capital Expenditure", "cash_flow", cashflow.get("capex"), "CNY"),
        ("sales_cash_received", "Sales Cash Received", "cash_flow", cashflow.get("sales_cash_received"), "CNY"),
        ("gross_margin_pct", "Gross Margin", "ratio", indicators.get("gross_margin"), "percent"),
        ("net_margin_pct", "Net Margin", "ratio", indicators.get("net_margin"), "percent"),
        ("roe_pct", "ROE", "ratio", indicators.get("roe"), "percent"),
        ("roa_pct", "ROA", "ratio", indicators.get("roa"), "percent"),
        ("debt_to_assets_pct", "Debt to Assets", "ratio", indicators.get("debt_to_assets"), "percent"),
        ("current_ratio", "Current Ratio", "ratio", indicators.get("current_ratio"), "ratio"),
        ("quick_ratio", "Quick Ratio", "ratio", indicators.get("quick_ratio"), "ratio"),
        ("asset_turnover", "Asset Turnover", "ratio", indicators.get("asset_turnover"), "ratio"),
        ("cfo_to_net_profit", "Operating Cash Flow / Net Profit", "ratio", indicators.get("cfo_to_net_profit"), "ratio"),
    ]
    return [row for row in rows if row[3] is not None]


def insert_listed_statement_lines(cur, company_id, case_id, period_id, period_payload, doc_id, page_base):
    groups = {
        "balance": [
            ("cash", "Cash"),
            ("accounts_receivable", "Accounts Receivable"),
            ("inventory", "Inventory"),
            ("total_assets", "Total Assets"),
            ("total_liabilities", "Total Liabilities"),
            ("accounts_payable", "Accounts Payable"),
            ("short_debt", "Short-term Debt"),
            ("shareholder_equity", "Shareholder Equity"),
            ("fixed_assets", "Fixed Assets"),
            ("intangible_assets", "Intangible Assets"),
        ],
        "income": [
            ("revenue", "Revenue"),
            ("operating_cost", "Operating Cost"),
            ("selling_expense", "Selling Expense"),
            ("admin_expense", "Administrative Expense"),
            ("finance_expense", "Finance Expense"),
            ("rd_expense", "R&D Expense"),
            ("operating_profit", "Operating Profit"),
            ("net_profit", "Net Profit"),
        ],
        "cashflow": [
            ("sales_cash_received", "Sales Cash Received"),
            ("operating_cashflow", "Operating Cash Flow"),
            ("investing_cashflow", "Investing Cash Flow"),
            ("financing_cashflow", "Financing Cash Flow"),
            ("net_cashflow", "Net Cash Flow"),
            ("capex", "Capital Expenditure"),
        ],
    }
    for statement_type, mappings in groups.items():
        source_group = period_payload.get(statement_type if statement_type != "cashflow" else "cashflow", {})
        page_no = page_base if statement_type == "balance" else page_base + 1 if statement_type == "income" else page_base + 2
        order = 1
        for line_code, line_name in mappings:
            value = source_group.get(line_code)
            if value is None:
                continue
            insert(
                cur,
                "financial_statement_line_items",
                {
                    "company_id": company_id,
                    "case_id": case_id,
                    "period_id": period_id,
                    "statement_type": statement_type,
                    "line_code": line_code,
                    "line_name": line_name,
                    "display_order": order,
                    "value": value,
                    "unit": "CNY",
                    "source_document_id": doc_id,
                    "source_page_no": page_no,
                    "source_ref": "AkShare cache",
                    "note": None,
                },
            )
            order += 1


def insert_listed_recon_checks(cur, company_id, case_id, period_id, period_payload, doc_id):
    balance = period_payload.get("balance", {})
    income = period_payload.get("income", {})
    cashflow = period_payload.get("cashflow", {})
    checks = []
    total_assets = balance.get("total_assets")
    total_liabilities = balance.get("total_liabilities")
    shareholder_equity = balance.get("shareholder_equity")
    if None not in (total_assets, total_liabilities, shareholder_equity):
        variance = round(total_assets - total_liabilities - shareholder_equity, 2)
        checks.append(
            {
                "check_code": "listed_bs_balance",
                "check_name": "Listed balance sheet equation",
                "statement_scope": "balance_sheet",
                "lhs_label": "Total Assets",
                "lhs_value": total_assets,
                "rhs_label": "Total Liabilities + Shareholder Equity",
                "rhs_value": round(total_liabilities + shareholder_equity, 2),
                "variance_value": variance,
                "variance_ratio": 0.0 if total_assets == 0 else round(abs(variance) / total_assets, 6),
                "threshold_value": 1.0,
                "status": "pass" if abs(variance) <= 1 else "fail",
                "interpretation": "Public balance-sheet totals should tie out.",
                "source_page_no": 1,
            }
        )
    revenue = income.get("revenue")
    cost = income.get("operating_cost")
    gross_margin = period_payload.get("indicators", {}).get("gross_margin")
    if None not in (revenue, cost, gross_margin):
        rhs = round(revenue - cost, 2)
        lhs = round(revenue * gross_margin / 100, 2)
        variance = round(lhs - rhs, 2)
        checks.append(
            {
                "check_code": "listed_gross_margin_bridge",
                "check_name": "Gross margin consistency",
                "statement_scope": "income_statement",
                "lhs_label": "Revenue * Gross Margin",
                "lhs_value": lhs,
                "rhs_label": "Revenue - Operating Cost",
                "rhs_value": rhs,
                "variance_value": variance,
                "variance_ratio": 0.0 if rhs == 0 else round(abs(variance) / abs(rhs), 6),
                "threshold_value": 0.08,
                "status": "pass" if abs(variance) / max(abs(rhs), 1) <= 0.08 else "warn",
                "interpretation": "A loose bridge between disclosed gross margin and revenue-cost spread.",
                "source_page_no": 2,
            }
        )
    if None not in (cashflow.get("net_cashflow"), cashflow.get("operating_cashflow"), cashflow.get("investing_cashflow"), cashflow.get("financing_cashflow")):
        rhs = round(cashflow["operating_cashflow"] + cashflow["investing_cashflow"] + cashflow["financing_cashflow"], 2)
        variance = round(cashflow["net_cashflow"] - rhs, 2)
        checks.append(
            {
                "check_code": "listed_cashflow_bridge",
                "check_name": "Net cash flow bridge",
                "statement_scope": "cash_flow_statement",
                "lhs_label": "Net Cash Flow",
                "lhs_value": cashflow["net_cashflow"],
                "rhs_label": "Operating + Investing + Financing",
                "rhs_value": rhs,
                "variance_value": variance,
                "variance_ratio": 0.0 if rhs == 0 else round(abs(variance) / abs(rhs), 6),
                "threshold_value": 0.05,
                "status": "pass" if abs(variance) / max(abs(rhs), 1) <= 0.05 else "warn",
                "interpretation": "Net cash flow should broadly reconcile to the three cash flow sections.",
                "source_page_no": 3,
            }
        )
    if None not in (cashflow.get("operating_cashflow"), income.get("net_profit")):
        ratio = None if abs(income["net_profit"]) < 1 else round(cashflow["operating_cashflow"] / income["net_profit"], 4)
        checks.append(
            {
                "check_code": "listed_profit_cash_conversion",
                "check_name": "Profit to operating cash conversion",
                "statement_scope": "income_cashflow_bridge",
                "lhs_label": "Operating Cash Flow",
                "lhs_value": cashflow["operating_cashflow"],
                "rhs_label": "Net Profit",
                "rhs_value": income["net_profit"],
                "variance_value": round(cashflow["operating_cashflow"] - income["net_profit"], 2),
                "variance_ratio": abs(ratio) if ratio is not None else None,
                "threshold_value": 0.8,
                "status": "fail" if ratio is not None and ratio < 0 else "warn" if ratio is not None and ratio < 0.8 else "pass",
                "interpretation": "Cash conversion below 0.8x or negative should trigger follow-up.",
                "source_page_no": 3,
            }
        )
    for check in checks:
        insert(
            cur,
            "financial_reconciliation_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "check_code": check["check_code"],
                "check_name": check["check_name"],
                "statement_scope": check["statement_scope"],
                "lhs_label": check["lhs_label"],
                "lhs_value": check["lhs_value"],
                "rhs_label": check["rhs_label"],
                "rhs_value": check["rhs_value"],
                "variance_value": check["variance_value"],
                "variance_ratio": check["variance_ratio"],
                "threshold_value": check["threshold_value"],
                "status": check["status"],
                "interpretation": check["interpretation"],
                "linked_finding_id": None,
                "source_document_id": doc_id,
                "source_page_no": check["source_page_no"],
            },
        )


def seed_listed_bank_settlement_summaries(cur, company_id, case_id, period_rows, period_id_map):
    for row in period_rows[:6]:
        period = row.get("period")
        if period not in period_id_map:
            continue
        income = row.get("income", {})
        cashflow = row.get("cashflow", {})
        revenue = income.get("revenue") or 0
        operating_cf = cashflow.get("operating_cashflow") or 0
        sales_cash = cashflow.get("sales_cash_received") or round(revenue * 0.92, 2)
        investing_cf = abs(cashflow.get("investing_cashflow") or 0)
        financing_cf = abs(cashflow.get("financing_cashflow") or 0)
        outflow = round(max(sales_cash - operating_cf, 0) + investing_cf * 0.35 + financing_cf * 0.25, 2)
        inflow = round(sales_cash + max(cashflow.get("financing_cashflow") or 0, 0) * 0.4, 2)
        insert(
            cur,
            "bank_settlement_summaries",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id_map[period],
                "inflow_total_cny": inflow,
                "outflow_total_cny": outflow,
                "net_flow_cny": round(inflow - outflow, 2),
                "average_daily_balance_cny": round((row.get("balance", {}).get("cash") or 0) * 0.82, 2) if row.get("balance", {}).get("cash") is not None else None,
                "top_inflow_counterparty": "Public disclosure aggregate receipts",
                "top_inflow_amount_cny": round(inflow * 0.28, 2),
                "top_outflow_counterparty": "Suppliers and financing cash outflows",
                "top_outflow_amount_cny": round(outflow * 0.31, 2),
                "transaction_count": 180 if period.endswith("1231") else 130,
                "large_transaction_count": 18 if period.endswith("1231") else 12,
                "abnormal_fluctuation_flag": 1 if operating_cf < 0 else 0,
                "summary_note": "Public-company settlement proxy derived from cash flow statement and revenue disclosures.",
                "source_ref": "AkShare cache",
            },
        )


def seed_listed_tax_invoice_checks(cur, company_id, case_id, period_rows, period_id_map):
    for row in period_rows[:6]:
        period = row.get("period")
        if period not in period_id_map:
            continue
        income = row.get("income", {})
        cashflow = row.get("cashflow", {})
        revenue = income.get("revenue") or 0
        sales_cash = cashflow.get("sales_cash_received")
        if sales_cash is None:
            sales_cash = round(revenue * 0.94, 2)
        invoiced = round(revenue * 0.985, 2)
        declared = round(revenue * 0.978, 2)
        revenue_invoice_gap = round(abs(revenue - invoiced), 2)
        invoice_receipt_gap = round(abs(invoiced - sales_cash), 2)
        gap_ratio = round(max(revenue_invoice_gap, invoice_receipt_gap) / max(revenue, 1), 4)
        insert(
            cur,
            "tax_invoice_consistency_checks",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id_map[period],
                "declared_revenue_cny": declared,
                "invoiced_amount_cny": invoiced,
                "bank_receipts_cny": sales_cash,
                "output_tax_cny": round(declared * 0.13, 2),
                "input_tax_cny": round(declared * 0.082, 2),
                "invoice_count": 120 if period.endswith("1231") else 86,
                "revenue_invoice_gap_cny": revenue_invoice_gap,
                "invoice_receipt_gap_cny": invoice_receipt_gap,
                "gap_ratio": gap_ratio,
                "status": "pass" if gap_ratio <= 0.05 else "warn" if gap_ratio <= 0.12 else "fail",
                "check_note": "Listed-company tax and invoice proxy built from public revenue and cash-receipt disclosures.",
                "source_ref": "AkShare cache + demo proxy",
            },
        )


def seed_listed_related_party_transactions(cur, company_id, case_id, period_id, ts_code):
    defaults = {
        "002594.SZ": [
            ("融捷投资控股集团有限公司", "shareholder", "equity_relation", 620000000, 0.021, "bank_transfer", "Needs related-party pricing memo", "medium"),
            ("深圳市灵犀电子封装有限公司", "affiliate_supply_chain", "component_purchase", 380000000, 0.013, "bank_transfer", "Related procurement exposure remains manageable", "low"),
        ],
        "600519.SH": [
            ("中国贵州茅台酒厂（集团）有限责任公司", "controlling_shareholder", "brand_license_and_group_service", 910000000, 0.0053, "internal_settlement", "State-owned group transactions should follow formal pricing approvals", "medium"),
            ("贵州茅台酒厂（集团）技术开发有限公司", "affiliate", "procurement_and_service", 245000000, 0.0014, "bank_transfer", "Monitor overlap between operating entities", "low"),
        ],
        "600998.SH": [
            ("上海弘康实业投资有限公司", "major_shareholder", "capital_support", 560000000, 0.0035, "bank_transfer", "Capital support and related borrowings need board-level disclosure review", "medium"),
            ("楚昌投资集团有限公司", "shareholder_group", "fund_transfer", 1280000000, 0.0079, "bank_transfer", "Group funding arrangements require related-party cap monitoring", "high"),
        ],
        "600612.SH": [
            ("上海市黄浦区国有资产监督管理委员会（上海市黄浦区集体资产监督管理委员会）", "actual_controller", "state_owned_coordination", 0, 0.0, "policy_coordination", "No direct operating transaction captured; controller influence reflected in governance layer", "low"),
            ("龙悦网络有限公司", "shareholder", "channel_settlement", 88000000, 0.0017, "bank_transfer", "Cross-border settlement pricing should be reviewed periodically", "low"),
        ],
        "600196.SH": [
            ("上海复星高科技（集团）有限公司", "controlling_shareholder", "capital_and_service", 1520000000, 0.0081, "bank_transfer", "Related-party capital and shared-service transactions warrant formal arm's-length testing", "high"),
            ("复星国际", "group_affiliate", "management_service", 460000000, 0.0025, "bank_transfer", "Group service fees should be benchmarked annually", "medium"),
        ],
    }
    for related_party_name, relation_type, transaction_type, amount, ratio, settlement_method, pricing_comment, risk_level in defaults.get(ts_code, []):
        insert(
            cur,
            "related_party_transaction_summaries",
            {
                "company_id": company_id,
                "case_id": case_id,
                "period_id": period_id,
                "related_party_name": related_party_name,
                "relation_type": relation_type,
                "transaction_type": transaction_type,
                "transaction_amount_cny": amount,
                "revenue_or_cost_ratio": ratio,
                "settlement_method": settlement_method,
                "pricing_comment": pricing_comment,
                "risk_level": risk_level,
                "source_ref": "Qichacha + demo related-party summary",
                "note": None,
            },
        )


def seed_listed_credit_history(cur, company_id, case_id, company_payload, latest_annual):
    balance = latest_annual.get("balance", {})
    indicators = latest_annual.get("indicators", {})
    debt = balance.get("short_debt") or 0
    assessment = "good" if (indicators.get("debt_to_assets") or 0) < 55 else "watch"
    insert(
        cur,
        "credit_history_summaries",
        {
            "company_id": company_id,
            "case_id": case_id,
            "subject_type": "enterprise",
            "subject_name": company_payload.get("name"),
            "linked_person_id": None,
            "credit_channel": "public_financial_debt_profile",
            "account_count": 12,
            "outstanding_balance_cny": debt,
            "overdue_count": 0,
            "max_overdue_bucket": "none",
            "hard_inquiry_3m": 0,
            "hard_inquiry_6m": 0,
            "external_guarantee_exposure_cny": round((balance.get("total_liabilities") or 0) * 0.03, 2),
            "credit_assessment": assessment,
            "summary_note": "Listed-company credit history proxy summarized from public leverage, debt, and disclosure context.",
            "source_ref": "Public annual reports + demo credit summary",
        },
    )


def seed_listed_priority_dimensions(cur, company_id, case_id, company_payload, periods, period_id_map, latest_annual):
    seed_listed_bank_settlement_summaries(cur, company_id, case_id, periods, period_id_map)
    seed_listed_tax_invoice_checks(cur, company_id, case_id, periods, period_id_map)
    annual_period = next((p for p in periods if p.get("period", "").endswith("1231") and p.get("period") in period_id_map), None)
    if annual_period:
        seed_listed_related_party_transactions(cur, company_id, case_id, period_id_map[annual_period["period"]], company_payload["ts_code"])
    seed_listed_credit_history(cur, company_id, case_id, company_payload, latest_annual)


def apply_manual_listed_enrichment(cur, company_id, case_id, ts_code):
    enrichment = MANUAL_LISTED_ENRICHMENTS.get(ts_code)
    if not enrichment:
        return

    updates = enrichment.get("company_updates", {})
    if updates:
        assignments = ", ".join([f"{key} = ?" for key in updates.keys()])
        cur.execute(
            f"UPDATE companies SET {assignments} WHERE id = ?",
            tuple(updates.values()) + (company_id,),
        )

    for label, value, note in enrichment.get("public_profile", []):
        upsert_profile_attribute(cur, company_id, case_id, "public_profile", label, value, "Qichacha manual capture", note)

    for label, value in enrichment.get("registration", []):
        upsert_profile_attribute(cur, company_id, case_id, "registration", label, value, "Qichacha manual capture", None)

    for label, value in enrichment.get("listing_info", []):
        upsert_profile_attribute(cur, company_id, case_id, "listing_info", label, value, "Qichacha manual capture", None)

    for label, value, note in enrichment.get("shareholders", []):
        upsert_profile_attribute(cur, company_id, case_id, "shareholder_summary", label, value, "Qichacha manual capture", note)

    for person_code, full_name, gender, birth_year, education, role_type, title, joined_on, equity_ratio, is_actual_controller, notes in enrichment.get("people", []):
        add_or_replace_person_role(
            cur,
            company_id,
            person_code,
            full_name,
            gender,
            birth_year,
            education,
            role_type,
            title,
            joined_on,
            equity_ratio=equity_ratio,
            is_actual_controller=is_actual_controller,
            notes=notes,
        )

    for name, relation_type, note in enrichment.get("branches", []):
        cur.execute(
            "DELETE FROM related_companies WHERE company_id = ? AND related_company_name = ? AND relation_type = ?",
            (company_id, name, relation_type),
        )
        insert(
            cur,
            "related_companies",
            {
                "company_id": company_id,
                "related_company_name": name,
                "relation_type": relation_type,
                "control_path": None,
                "risk_flag": 0 if "存续" in note else 1 if "注销" in note else 0,
                "unified_social_credit_code": None,
                "industry_category": None,
                "note": note,
            },
        )


def seed_listed_findings(cur, company_id, case_id, latest_annual, rule_ids):
    findings = []
    indicators = latest_annual.get("indicators", {})
    cashflow = latest_annual.get("cashflow", {})
    income = latest_annual.get("income", {})
    if indicators.get("debt_to_assets") is not None and indicators["debt_to_assets"] >= 65:
        findings.append(
            ("cash_flow_cover", "medium", "Leverage remains elevated for public-company sample", f"Latest debt-to-assets ratio is about {indicators['debt_to_assets']:.2f}%.", "Public leverage level warrants peer-based interpretation.", 0.86, "open", 0)
        )
    cfo_profit = indicators.get("cfo_to_net_profit")
    if cfo_profit is not None and cfo_profit < 0.8:
        severity = "high" if cfo_profit < 0 else "medium"
        findings.append(
            ("cashflow_statement_bridge", severity, "Operating cash conversion is weaker than net profit", f"Operating cash flow to net profit ratio is about {cfo_profit:.2f}x.", "Weak cash conversion can reduce confidence in profit quality.", 0.9, "open", 1)
        )
    if None not in (income.get("revenue"), cashflow.get("capital_expenditure"), cashflow.get("operating_cashflow")) and cashflow.get("capital_expenditure") is not None:
        if cashflow["capital_expenditure"] > abs(cashflow.get("operating_cashflow") or 0) * 1.2:
            findings.append(
                ("fixed_asset_capex_check", "medium", "Capex scale exceeds operating cash support", "Capital expenditure in the latest annual period is materially above operating cash flow.", "Large capex may require financing support or balance-sheet explanation.", 0.8, "open", 1)
            )
    for rule_code, severity, title, summary, impact, confidence, status, manual in findings:
        insert(
            cur,
            "validation_findings",
            {
                "case_id": case_id,
                "company_id": company_id,
                "rule_id": rule_ids[rule_code],
                "severity": severity,
                "finding_title": title,
                "finding_summary": summary,
                "impact_summary": impact,
                "confidence": confidence,
                "status": status,
                "requires_manual_review": manual,
            },
        )


def seed_listed_scores_sections(cur, company_id, case_id, company_payload, latest_annual):
    indicators = latest_annual.get("indicators", {})
    debt_to_assets = indicators.get("debt_to_assets") or 0
    cfo_profit = indicators.get("cfo_to_net_profit")
    gross_margin = indicators.get("gross_margin") or 0
    score_rows = [
        ("public_financial_quality", 88 if cfo_profit and cfo_profit >= 1 else 76 if cfo_profit and cfo_profit >= 0.8 else 62, "Financial quality from public statements"),
        ("public_leverage", 82 if debt_to_assets < 50 else 70 if debt_to_assets < 65 else 58, "Leverage read from public balance sheet"),
        ("public_profitability", 90 if gross_margin >= 35 else 78 if gross_margin >= 15 else 66, "Profitability read from public indicators"),
    ]
    for dimension, value, rationale in score_rows:
        band = "strong" if value >= 85 else "good" if value >= 75 else "watch" if value >= 60 else "weak"
        insert(
            cur,
            "case_risk_scores",
            {
                "case_id": case_id,
                "company_id": company_id,
                "score_dimension": dimension,
                "score_value": value,
                "score_band": band,
                "rationale": rationale,
            },
        )
    revenue = latest_annual.get("income", {}).get("revenue")
    op_cf = latest_annual.get("cashflow", {}).get("operating_cashflow")
    report_sections = [
        ("company_profile", "Company Profile", f"{company_payload.get('name')} is a listed company sample imported from the local AkShare cache. Public profile and annual-report links are stored for reuse.", 0.93),
        ("operations", "Financial Snapshot", f"Latest disclosed revenue is {revenue} and operating cash flow is {op_cf}. Public-company sample emphasizes real financial statements over synthetic internal operating data.", 0.9),
        ("risks", "Public Financial Risks", "Key focus areas come from public financial quality, leverage, and cash-conversion signals rather than SME-style document triangulation.", 0.88),
        ("recommendation", "Usage Recommendation", "Use this sample for public-company benchmarking, industry comparison, and real financial statement walkthroughs in the demo.", 0.9),
    ]
    for display_order, (code, title, content, confidence) in enumerate(report_sections, start=1):
        insert(
            cur,
            "report_sections",
            {
                "case_id": case_id,
                "company_id": company_id,
                "section_code": code,
                "section_title": title,
                "content": content,
                "confidence": confidence,
                "display_order": display_order,
            },
        )


def seed_listed_cache_companies(cur, source_ids, rule_ids):
    if not LISTED_CACHE_PATH.exists():
        return
    cache_conn = sqlite3.connect(LISTED_CACHE_PATH)
    for target in LISTED_TARGETS:
        ts_code = target["ts_code"]
        company_payload = cache_json(cache_conn, "companies", ts_code)
        financial_payload = cache_json(cache_conn, "financials", ts_code)
        if not company_payload or not financial_payload:
            continue
        profile_payload = cache_json(cache_conn, "profiles", ts_code)
        industry_payload = cache_json(cache_conn, "industries", ts_code)
        report_payloads = cache_rows(cache_conn, "reports", ts_code)

        company_id, case_id = seed_listed_company_case(cur, company_payload, target["risk_tier"])
        profile_items = normalize_profile_items(profile_payload, company_payload)
        for label, value, note in profile_items:
            insert_profile_attribute(cur, company_id, case_id, "public_profile", label, None if value is None else str(value), "AkShare cache", note)
        if industry_payload:
            for card in industry_payload.get("cards", []):
                insert_profile_attribute(
                    cur,
                    company_id,
                    case_id,
                    "industry_insight",
                    card.get("title") or "Industry Card",
                    card.get("body"),
                    "AkShare cache",
                    None,
                )
        company_reports = report_payloads[:3]
        docs, pages = insert_listed_documents(cur, case_id, company_id, source_ids, ts_code, company_reports)

        established = parse_profile_value(profile_items, "成立时间") or parse_profile_value(profile_items, "上市时间")
        if established and str(established) != "暂无信息":
            cur.execute("UPDATE companies SET established_on = ? WHERE id = ?", (str(established), company_id))
        registered_capital = parse_profile_value(profile_items, "注册资本")
        if registered_capital and "暂无信息" not in str(registered_capital):
            cur.execute("UPDATE companies SET notes = COALESCE(notes,'') || ? WHERE id = ?", (f" Registered capital reference: {registered_capital}.", company_id))

        annual_doc_id = docs["annual_financial_statements"][0]
        periods = financial_payload.get("periods", [])
        annual_period_ids = []
        period_id_map = {}
        for row in periods:
            period = row.get("period")
            if not period:
                continue
            period_id = insert_listed_financial_period(cur, company_id, case_id, period)
            period_id_map[period] = period_id
            for metric_code, metric_name, category, value, unit in listed_metric_rows(row):
                insert(
                    cur,
                    "financial_metrics",
                    {
                        "company_id": company_id,
                        "case_id": case_id,
                        "period_id": period_id,
                        "metric_code": metric_code,
                        "metric_name": metric_name,
                        "metric_category": category,
                        "value": value,
                        "unit": unit,
                        "currency": "CNY" if unit == "CNY" else None,
                        "source_type": "akshare_cache",
                        "source_ref": "Local AkShare financial cache",
                        "is_estimated": 0,
                        "note": f"Imported from cached period {period}",
                    },
                )
            if period.endswith("1231"):
                annual_period_ids.append((period, period_id, row))

        annual_period_ids = sorted(annual_period_ids, key=lambda item: item[0], reverse=True)[:3]
        for index, (_period, period_id, row) in enumerate(annual_period_ids, start=1):
            insert_listed_statement_lines(cur, company_id, case_id, period_id, row, annual_doc_id, page_base=(index - 1) * 4 + 1)
            insert_listed_recon_checks(cur, company_id, case_id, period_id, row, annual_doc_id)

        apply_manual_listed_enrichment(cur, company_id, case_id, ts_code)
        latest_annual = annual_period_ids[0][2] if annual_period_ids else periods[0]
        seed_listed_priority_dimensions(cur, company_id, case_id, company_payload, periods, period_id_map, latest_annual)
        seed_listed_findings(cur, company_id, case_id, latest_annual, rule_ids)
        seed_listed_scores_sections(cur, company_id, case_id, company_payload, latest_annual)
        seed_placeholders(cur, company_id, case_id)
    cache_conn.close()


def seed_placeholders(cur, company_id, case_id):
    insert(
        cur,
        "field_visit_tasks",
        {
            "case_id": case_id,
            "company_id": company_id,
            "visit_date": None,
            "visitor_name": None,
            "status": "not_started",
            "checklist_json": json.dumps({"photos": False, "inventory_check": False}),
            "findings_summary": "Reserved for future field visit module.",
        },
    )
    insert(
        cur,
        "post_loan_monitoring_events",
        {
            "case_id": case_id,
            "company_id": company_id,
            "monitor_date": None,
            "event_type": "placeholder",
            "severity": "info",
            "summary": "Reserved for post-loan monitoring extension.",
        },
    )


def build_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(SCHEMA_PATH.read_text())
    cur = conn.cursor()

    source_ids = seed_sources(cur)
    rule_ids = seed_validation_rules(cur)
    _, benchmark_ids = seed_industries(cur)

    for company in COMPANIES:
        company_id = seed_company(cur, company)
        person_ids = seed_people(cur, company_id, company["persons"])
        case_id = seed_case(cur, company, company_id)
        seed_guarantee(cur, company, case_id, person_ids)
        seed_related_companies(cur, company_id, company["related_companies"])
        document_ids, page_ids = seed_documents(cur, company, case_id, company_id, person_ids, source_ids)
        period_ids = build_periods(cur, company_id, case_id)
        account_id, _, ar_summary_ids = build_financials(cur, company, company_id, case_id, period_ids)
        counterparty_ids = seed_counterparties(cur, company_id, case_id, company["counterparties"])
        seed_contracts_and_cash(cur, company, company_id, case_id, counterparty_ids, document_ids, account_id, ar_summary_ids)
        seed_innovation(cur, company, company_id, case_id, period_ids, person_ids)
        seed_public_and_peers(cur, company, company_id, case_id, benchmark_ids)
        seed_sme_priority_dimensions(cur, company, company_id, case_id, period_ids, person_ids)
        seed_findings_reports(cur, company, company_id, case_id, rule_ids, document_ids, page_ids, source_ids)
        seed_placeholders(cur, company_id, case_id)

    seed_listed_cache_companies(cur, source_ids, rule_ids)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    build_database()
    print(f"Built demo database at {DB_PATH}")
