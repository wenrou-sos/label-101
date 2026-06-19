# -*- coding: utf-8 -*-
"""月龄阶段消费服务：各阶段类目消费占比与客单价趋势。"""
import pandas as pd

from data_loader import get_consumption

STAGES = ["孕期囤货", "0-3月", "3-6月", "6-12月", "1-3岁", "3-6岁"]


def get_age_stage_consumption(start_year=2010, end_year=2024):
    df = get_consumption().copy()
    df["year"] = pd.to_datetime(df["order_date"]).dt.year
    df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    category_share = {}
    for stage in STAGES:
        sub = df[df["age_stage"] == stage]
        grp = sub.groupby("category")["amount"].sum().sort_values(ascending=False)
        total = float(grp.sum())
        category_share[stage] = [
            {"category": cat, "amount": round(float(amt), 2),
             "share": round(float(amt) / max(total, 1) * 100, 2)}
            for cat, amt in grp.items()
        ]

    avg_order_trend = []
    for stage in STAGES:
        sub = df[df["age_stage"] == stage]
        avg_order = round(float(sub["amount"].mean()), 2) if len(sub) > 0 else 0
        avg_order_trend.append({
            "stage": stage,
            "avg_order": avg_order,
            "order_count": int(len(sub)),
        })

    return {"stages": STAGES, "category_share": category_share,
            "avg_order_trend": avg_order_trend}
