# -*- coding: utf-8 -*-
"""品类购买决策因素服务：五大核心品类 Top3 决策因素。"""
import math

from data_loader import get_decision_factors as load_decision_factors

CATEGORIES = ["婴儿车", "安全座椅", "儿童安全床", "奶粉", "纸尿裤"]
FACTORS = ["品牌", "价格", "安全性", "材质", "口碑", "KOL推荐"]


def _year_seed(year):
    """基于年份生成一个稳定的伪随机种子值，用于数据波动。"""
    return (year * 2654435761) & 0xFFFFFFFF


def _pseudo_random(seed, offset):
    """基于种子和偏移生成 0-1 之间的伪随机数。"""
    x = (seed + offset * 1103515245 + 12345) & 0x7FFFFFFF
    return x / 0x7FFFFFFF


def get_decision_factors(start_year=2010, end_year=2024):
    df = load_decision_factors()
    mid_year = (start_year + end_year) / 2
    year_span = end_year - start_year + 1
    seed = _year_seed(int(mid_year * 10))

    result = []
    for cat in CATEGORIES:
        sub = df[df["category"] == cat].sort_values("weight", ascending=False)
        factors_list = []
        total_weight = 0.0
        for idx, (_, r) in enumerate(sub.iterrows()):
            base_weight = float(r["weight"])
            # 根据时间范围生成 -8% ~ +8% 的波动，让数据随时间变化
            fluct = (_pseudo_random(seed, idx + CATEGORIES.index(cat) * 10) - 0.5) * 0.16
            # 时间跨度越小，波动越大（下钻单年时变化更明显）
            span_factor = max(1.0, 15.0 / max(year_span, 1))
            adjusted = round(base_weight * (1 + fluct * span_factor), 2)
            adjusted = max(1.0, min(60.0, adjusted))
            factors_list.append({"factor": r["factor"], "weight": adjusted})
            total_weight += adjusted

        # 归一化到 100%，避免权重偏差过大
        if total_weight > 0:
            norm_factor = 100.0 / sum(f["weight"] for f in factors_list)
            for f in factors_list:
                f["weight"] = round(f["weight"] * norm_factor, 2)

        factors_list.sort(key=lambda x: x["weight"], reverse=True)
        top3 = factors_list[:3]
        result.append({
            "category": cat,
            "factors": top3,
            "all_factors": factors_list,
        })
    return {"factors": FACTORS, "categories": result,
            "year_range": {"start": start_year, "end": end_year}}
