# -*- coding: utf-8 -*-
"""复购品牌忠诚度服务：生存分析曲线、品牌平均停留、换品牌时间分布。"""
import numpy as np
import pandas as pd

from data_loader import get_brand_loyalty

CATEGORIES = ["纸尿裤", "奶粉"]
SWITCH_BINS = ["0-3月", "4-6月", "7-12月", "13-18月", "19-24月", "24月以上"]


def _kaplan_meier(stays, events, max_month=24):
    """简化 Kaplan-Meier 估计，输出逐月生存率。"""
    stays = np.asarray(stays, dtype=float)
    events = np.asarray(events, dtype=float)
    months = list(range(0, max_month + 1))
    survival = [1.0]
    s = 1.0
    for t in range(1, max_month + 1):
        at_risk = int(np.sum(stays >= t))
        d = int(np.sum((stays == t) & (events == 1)))
        if at_risk > 0:
            s = s * (1 - d / at_risk)
        survival.append(round(float(s), 4))
    return [{"month": m, "survival": sv} for m, sv in zip(months, survival)]


def get_loyalty_survival():
    df = get_brand_loyalty()
    survival_curves = {}
    brand_stay = {}
    for cat in CATEGORIES:
        sub = df[df["category"] == cat]
        survival_curves[cat] = _kaplan_meier(
            sub["stay_months"].values, sub["switched"].values)

        bs = sub.groupby("brand")["stay_months"].agg(["mean", "count"]).reset_index()
        brand_stay[cat] = [
            {"brand": r["brand"],
             "avg_stay_months": round(float(r["mean"]), 1),
             "count": int(r["count"])}
            for _, r in bs.sort_values("mean", ascending=False).iterrows()
        ]

    switched = df[df["switched"] == 1].copy()
    bins = [0, 3, 6, 12, 18, 24, 999]
    switched["bucket"] = pd.cut(switched["stay_months"], bins=bins,
                                labels=SWITCH_BINS, right=True,
                                include_lowest=True)
    counts = switched["bucket"].value_counts().reindex(SWITCH_BINS, fill_value=0)
    switch_time_distribution = [
        {"range": label, "count": int(counts[label])} for label in SWITCH_BINS
    ]

    return {"categories": CATEGORIES,
            "survival_curves": survival_curves,
            "brand_stay": brand_stay,
            "switch_time_distribution": switch_time_distribution}
