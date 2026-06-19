# -*- coding: utf-8 -*-
"""母婴市场消费分析看板 - 模拟数据生成脚本

生成 5 个 CSV 数据文件，覆盖 2010-2024 年母婴消费记录，数据分布符合
母婴市场真实特征（孕期囤货以营养品/待产包为主，0-3 月以奶粉/纸尿裤为主等）。

运行方式：python generate_data.py
"""
import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

RNG = np.random.default_rng(20240618)

# ---------------------------------------------------------------------------
# 维度定义
# ---------------------------------------------------------------------------
AGE_STAGES = ["孕期囤货", "0-3月", "3-6月", "6-12月", "1-3岁", "3-6岁"]

# 类目基础价格（元）与是否为高频消耗品
CATEGORIES = {
    "奶粉": {"base_price": 280, "consumable": True},
    "纸尿裤": {"base_price": 130, "consumable": True},
    "辅食": {"base_price": 85, "consumable": True},
    "营养品": {"base_price": 210, "consumable": True},
    "婴儿车": {"base_price": 1800, "consumable": False},
    "安全座椅": {"base_price": 2200, "consumable": False},
    "儿童安全床": {"base_price": 2500, "consumable": False},
    "待产包": {"base_price": 620, "consumable": False},
    "玩具": {"base_price": 160, "consumable": False},
    "服饰": {"base_price": 130, "consumable": False},
    "洗护用品": {"base_price": 95, "consumable": False},
}

# 各月龄阶段类目购买倾向权重（相对概率）
STAGE_CATEGORY_WEIGHTS = {
    "孕期囤货": {"待产包": 6, "营养品": 5, "婴儿车": 4, "安全座椅": 4,
                "儿童安全床": 4, "服饰": 4, "洗护用品": 4, "奶粉": 2, "纸尿裤": 2, "玩具": 1, "辅食": 0},
    "0-3月": {"奶粉": 7, "纸尿裤": 7, "洗护用品": 4, "服饰": 4, "营养品": 2, "玩具": 1, "待产包": 1},
    "3-6月": {"奶粉": 6, "纸尿裤": 6, "玩具": 4, "服饰": 3, "辅食": 2, "洗护用品": 2, "营养品": 1},
    "6-12月": {"奶粉": 6, "纸尿裤": 6, "辅食": 5, "玩具": 4, "服饰": 2, "营养品": 1, "洗护用品": 1},
    "1-3岁": {"辅食": 6, "玩具": 5, "奶粉": 4, "纸尿裤": 4, "服饰": 4, "营养品": 2, "洗护用品": 1},
    "3-6岁": {"玩具": 6, "服饰": 5, "营养品": 3, "安全座椅": 2, "洗护用品": 2, "奶粉": 1, "辅食": 1},
}

# 城市层级与价格系数
CITY_TIERS = {
    "一线城市": {"price_factor": 1.28, "weight": 0.25},
    "二线城市": {"price_factor": 1.02, "weight": 0.32},
    "三线及以下": {"price_factor": 0.76, "weight": 0.43},
}

# 高频消耗品品牌库
BRANDS = {
    "纸尿裤": ["帮宝适", "花王", "大王", "妈咪宝贝", "露安适", "好奇"],
    "奶粉": ["飞鹤", "爱他美", "美素佳儿", "君乐宝", "合生元", "惠氏"],
}

# 五大核心品类购买决策因素权重（百分比，和为100）
DECISION_WEIGHTS = {
    "婴儿车": {"安全性": 35, "品牌": 25, "价格": 16, "材质": 12, "口碑": 9, "KOL推荐": 3},
    "安全座椅": {"安全性": 46, "品牌": 20, "价格": 12, "材质": 10, "口碑": 8, "KOL推荐": 4},
    "儿童安全床": {"安全性": 36, "材质": 22, "品牌": 18, "价格": 12, "口碑": 8, "KOL推荐": 4},
    "奶粉": {"品牌": 30, "安全性": 24, "口碑": 20, "价格": 15, "材质": 8, "KOL推荐": 3},
    "纸尿裤": {"材质": 28, "品牌": 22, "价格": 20, "口碑": 15, "安全性": 10, "KOL推荐": 5},
}

# 全国出生人口（万人）2010-2024，贴近真实数据
BIRTH_RATE = {
    2010: 1592, 2011: 1604, 2012: 1635, 2013: 1640, 2014: 1687,
    2015: 1655, 2016: 1786, 2017: 1723, 2018: 1523, 2019: 1465,
    2020: 1200, 2021: 1062, 2022: 956, 2023: 902, 2024: 954,
}

SPECIAL_YEARS = {
    2012: "龙宝宝年份",
    2020: "疫情期间",
    2021: "疫情期间",
    2022: "疫情期间",
    2024: "龙宝宝年份",
}


# ---------------------------------------------------------------------------
# 1. 用户画像表 users.csv
# ---------------------------------------------------------------------------
def gen_users(n=6000):
    rows = []
    tier_choices = list(CITY_TIERS.keys())
    tier_probs = [CITY_TIERS[t]["weight"] for t in tier_choices]
    incomes = ["高收入", "中高收入", "中等收入", "中低收入"]
    income_probs = [0.18, 0.32, 0.35, 0.15]
    for i in range(n):
        uid = f"U{i + 1:06d}"
        stage = RNG.choice(AGE_STAGES)
        tier = RNG.choice(tier_choices, p=tier_probs)
        # 收入水平与城市层级弱相关
        inc = RNG.choice(incomes, p=income_probs)
        rows.append([uid, stage, tier, inc])
    return pd.DataFrame(rows, columns=["user_id", "age_stage", "city_tier", "income_level"])


# ---------------------------------------------------------------------------
# 2. 消费明细表 consumption.csv
# ---------------------------------------------------------------------------
def gen_consumption(users, orders_per_year):
    rows = []
    years = list(BIRTH_RATE.keys())
    tier_names = list(CITY_TIERS.keys())
    for year in years:
        n_orders = orders_per_year
        # 婴儿出生量影响订单量
        birth_factor = BIRTH_RATE[year] / 1600.0
        n_orders = int(n_orders * birth_factor)
        for _ in range(n_orders):
            uid = RNG.choice(users["user_id"].values)
            urow = users[users["user_id"] == uid].iloc[0]
            stage = urow["age_stage"]
            tier = urow["city_tier"]
            weights = STAGE_CATEGORY_WEIGHTS[stage]
            cats = list(weights.keys())
            w = list(weights.values())
            category = RNG.choice(cats, p=np.array(w) / sum(w))
            base = CATEGORIES[category]["base_price"]
            pf = CITY_TIERS[tier]["price_factor"]
            # 单品数量（消耗品可能多件）
            qty = int(RNG.integers(1, 6)) if CATEGORIES[category]["consumable"] else 1
            amount = round(float(base * pf * qty * RNG.lognormal(0, 0.22)), 2)
            month = int(RNG.integers(1, 13))
            day = int(RNG.integers(1, 29))
            date = f"{year}-{month:02d}-{day:02d}"
            rows.append([
                f"O{len(rows) + 1:08d}", uid, stage, category,
                amount, tier, date,
            ])
    df = pd.DataFrame(rows, columns=[
        "order_id", "user_id", "age_stage", "category",
        "amount", "city_tier", "order_date",
    ])
    return df


# ---------------------------------------------------------------------------
# 3. 品牌忠诚度表 brand_loyalty.csv
# ---------------------------------------------------------------------------
def gen_brand_loyalty(users, n=4500):
    rows = []
    cats = ["纸尿裤", "奶粉"]
    for cat in cats:
        brands = BRANDS[cat]
        for _ in range(n // 2):
            uid = RNG.choice(users["user_id"].values)
            brand = RNG.choice(brands)
            # 停留月数：对数正态，均值约 8-10 个月
            stay = int(np.clip(RNG.lognormal(2.0, 0.6), 1, 36))
            # 约 55% 已换品牌（事件发生），45% 仍在使用（删失）
            switched = RNG.random() < 0.55
            if switched:
                sw_year = int(RNG.choice([2018, 2019, 2020, 2021, 2022, 2023, 2024]))
                sw_month = int(RNG.integers(1, 13))
                switch_to_date = f"{sw_year}-{sw_month:02d}-15"
            else:
                switch_to_date = ""
            rows.append([
                f"L{len(rows) + 1:07d}", uid, cat, brand, stay,
                int(switched), switch_to_date,
            ])
    return pd.DataFrame(rows, columns=[
        "loyalty_id", "user_id", "category", "brand", "stay_months",
        "switched", "switch_to_date",
    ])


# ---------------------------------------------------------------------------
# 4. 决策因素表 decision_factors.csv
# ---------------------------------------------------------------------------
def gen_decision_factors():
    rows = []
    for cat, fw in DECISION_WEIGHTS.items():
        for factor, weight in fw.items():
            # 加入轻微随机扰动，便于体现样本差异
            w = round(float(weight) + RNG.normal(0, 0.8), 2)
            rows.append([cat, factor, w])
    return pd.DataFrame(rows, columns=["category", "factor", "weight"])


# ---------------------------------------------------------------------------
# 5. 出生率统计表 birth_rate.csv
# ---------------------------------------------------------------------------
def gen_birth_rate():
    rows = []
    for year, count in BIRTH_RATE.items():
        rows.append([year, count, SPECIAL_YEARS.get(year, "")])
    return pd.DataFrame(rows, columns=["year", "birth_count", "special_tag"])


def main():
    print("[1/5] 生成用户画像表 ...")
    users = gen_users(6000)
    users.to_csv(os.path.join(DATA_DIR, "users.csv"), index=False, encoding="utf-8-sig")

    print("[2/5] 生成消费明细表 ...")
    consumption = gen_consumption(users, orders_per_year=1600)
    consumption.to_csv(os.path.join(DATA_DIR, "consumption.csv"), index=False, encoding="utf-8-sig")

    print("[3/5] 生成品牌忠诚度表 ...")
    loyalty = gen_brand_loyalty(users, n=4500)
    loyalty.to_csv(os.path.join(DATA_DIR, "brand_loyalty.csv"), index=False, encoding="utf-8-sig")

    print("[4/5] 生成决策因素表 ...")
    decisions = gen_decision_factors()
    decisions.to_csv(os.path.join(DATA_DIR, "decision_factors.csv"), index=False, encoding="utf-8-sig")

    print("[5/5] 生成出生率统计表 ...")
    birth = gen_birth_rate()
    birth.to_csv(os.path.join(DATA_DIR, "birth_rate.csv"), index=False, encoding="utf-8-sig")

    print("\n数据生成完成：")
    for f in ["users.csv", "consumption.csv", "brand_loyalty.csv",
              "decision_factors.csv", "birth_rate.csv"]:
        p = os.path.join(DATA_DIR, f)
        print(f"  - {f}: {os.path.getsize(p)} bytes")


if __name__ == "__main__":
    main()
