# -*- coding: utf-8 -*-
"""总览服务：计算 KPI 指标与出生率趋势。"""
import pandas as pd

from data_loader import get_consumption, get_birth_rate


def _yoy(df, metric_col, year_col="year"):
    """计算最近一年相对上一年的同比变化率。"""
    latest = int(df[year_col].max())
    cur = df[df[year_col] == latest][metric_col].sum()
    prev = df[df[year_col] == latest - 1][metric_col].sum()
    if prev == 0:
        return 0.0
    return round((cur - prev) / prev * 100, 1)


def get_overview(start_year=2010, end_year=2024):
    df = get_consumption().copy()
    df["year"] = pd.to_datetime(df["order_date"]).dt.year
    df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    if len(df) == 0:
        birth = get_birth_rate()
        birth = birth[(birth["year"] >= start_year) & (birth["year"] <= end_year)]
        birth_trend = [
            {"year": int(r["year"]), "birth_count": int(r["birth_count"]),
             "special_tag": r["special_tag"]}
            for _, r in birth.iterrows()
        ]
        return {
            "kpis": [
                {"key": "total_amount", "label": "总消费额", "value": 0,
                 "unit": "元", "trend": 0, "icon": "currency-yuan"},
                {"key": "users", "label": "活跃用户", "value": 0,
                 "unit": "人", "trend": 0, "icon": "account-group"},
                {"key": "avg_order", "label": "平均客单价", "value": 0,
                 "unit": "元", "trend": 0, "icon": "cart"},
                {"key": "repurchase", "label": "复购率", "value": 0,
                 "unit": "%", "trend": 0, "icon": "repeat"},
            ],
            "birth_trend": birth_trend,
        }

    total_amount = round(float(df["amount"].sum()), 2)
    users = int(df["user_id"].nunique())
    avg_order = round(float(df["amount"].mean()), 2)
    order_counts = df.groupby("user_id").size()
    repurchase = round(float((order_counts > 1).mean() * 100), 1)

    years_available = sorted(df["year"].unique())
    if len(years_available) >= 2:
        latest = years_available[-1]
        prev = years_available[-2]
        total_trend = _yoy(df, "amount")
        user_trend = round(
            (df[df["year"] == latest]["user_id"].nunique()
             - df[df["year"] == prev]["user_id"].nunique())
            / max(df[df["year"] == prev]["user_id"].nunique(), 1) * 100, 1)
        avg_trend = round(
            (df[df["year"] == latest]["amount"].mean()
             - df[df["year"] == prev]["amount"].mean())
            / max(df[df["year"] == prev]["amount"].mean(), 1) * 100, 1)
        cur_counts = df[df["year"] == latest].groupby("user_id").size()
        prev_counts = df[df["year"] == prev].groupby("user_id").size()
        cur_repurchase = float((cur_counts > 1).mean() * 100) if len(cur_counts) > 0 else 0.0
        prev_repurchase = float((prev_counts > 1).mean() * 100) if len(prev_counts) > 0 else 0.0
        repurchase_trend = round(cur_repurchase - prev_repurchase, 1)
    else:
        total_trend = 0
        user_trend = 0
        avg_trend = 0
        repurchase_trend = 0

    kpis = [
        {"key": "total_amount", "label": "总消费额", "value": total_amount,
         "unit": "元", "trend": total_trend, "icon": "currency-yuan"},
        {"key": "users", "label": "活跃用户", "value": users,
         "unit": "人", "trend": user_trend, "icon": "account-group"},
        {"key": "avg_order", "label": "平均客单价", "value": avg_order,
         "unit": "元", "trend": avg_trend, "icon": "cart"},
        {"key": "repurchase", "label": "复购率", "value": repurchase,
         "unit": "%", "trend": repurchase_trend, "icon": "repeat"},
    ]

    birth = get_birth_rate()
    birth = birth[(birth["year"] >= start_year) & (birth["year"] <= end_year)]
    birth_trend = [
        {"year": int(r["year"]), "birth_count": int(r["birth_count"]),
         "special_tag": r["special_tag"]}
        for _, r in birth.iterrows()
    ]

    return {"kpis": kpis, "birth_trend": birth_trend}
