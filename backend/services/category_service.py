# -*- coding: utf-8 -*-
"""品类购买决策因素服务：五大核心品类 Top3 决策因素。"""
from data_loader import get_decision_factors as load_decision_factors

CATEGORIES = ["婴儿车", "安全座椅", "儿童安全床", "奶粉", "纸尿裤"]
FACTORS = ["品牌", "价格", "安全性", "材质", "口碑", "KOL推荐"]


def get_decision_factors():
    df = load_decision_factors()
    result = []
    for cat in CATEGORIES:
        sub = df[df["category"] == cat].sort_values("weight", ascending=False)
        full = [{"factor": r["factor"], "weight": round(float(r["weight"]), 2)}
                for _, r in sub.iterrows()]
        top3 = full[:3]
        result.append({
            "category": cat,
            "factors": top3,
            "all_factors": full,
        })
    return {"factors": FACTORS, "categories": result}
