# -*- coding: utf-8 -*-
"""城市层级消费差异服务：一线 vs 下沉市场品类偏好与价格带分布。"""
from data_loader import get_consumption, get_users

CATEGORIES = ["奶粉", "纸尿裤", "辅食", "营养品", "婴儿车",
              "安全座椅", "儿童安全床", "玩具", "服饰", "洗护用品"]

TIER_MAP = {"一线城市": "一线城市", "二线城市": "二线城市", "三线及以下": "下沉市场"}
TIERS = ["一线城市", "二线城市", "下沉市场"]


def get_city_tier_comparison(start_year=2010, end_year=2024):
    df = get_consumption().copy()
    df["year"] = pd.to_datetime(df["order_date"]).dt.year
    df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]
    users = get_users()
    tier_user_count = users["city_tier"].map(TIER_MAP).value_counts().to_dict()

    # 品类偏好热力图：各城市层级下每个品类的人均消费金额
    df = df[df["city_tier"].isin(TIER_MAP.keys())].copy()
    df["tier_group"] = df["city_tier"].map(TIER_MAP)

    preference = []
    for cat in CATEGORIES:
        row = {"category": cat}
        for tier in TIERS:
            sub = df[(df["category"] == cat) & (df["tier_group"] == tier)]
            total = float(sub["amount"].sum())
            per_user = round(total / max(tier_user_count.get(tier, 1), 1), 2)
            row[tier] = per_user
        preference.append(row)

    # 价格带分布箱线图：各品类在每个层级的价格统计
    price_distribution = {tier: [] for tier in TIERS}
    for tier_src, tier_dst in TIER_MAP.items():
        sub_tier = df[df["city_tier"] == tier_src]
        for cat in CATEGORIES:
            s = sub_tier[sub_tier["category"] == cat]["amount"]
            if len(s) == 0:
                continue
            q = s.quantile([0.25, 0.5, 0.75]).to_dict()
            price_distribution[tier_dst].append({
                "category": cat,
                "min": round(float(s.min()), 2),
                "q1": round(float(q[0.25]), 2),
                "median": round(float(q[0.5]), 2),
                "q3": round(float(q[0.75]), 2),
                "max": round(float(s.max()), 2),
                "mean": round(float(s.mean()), 2),
                "count": int(len(s)),
            })

    return {"tiers": TIERS, "categories": CATEGORIES,
            "preference": preference,
            "price_distribution": price_distribution}
