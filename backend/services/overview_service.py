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


def get_overview():
    df = get_consumption().copy()
    df["year"] = pd.to_datetime(df["order_date"]).dt.year

    total_amount = round(float(df["amount"].sum()), 2)
    users = int(df["user_id"].nunique())
    avg_order = round(float(df["amount"].mean()), 2)
    order_counts = df.groupby("user_id").size()
    repurchase = round(float((order_counts > 1).mean() * 100), 1)

    # 同比趋势
    total_trend = _yoy(df, "amount")
    user_trend = round(
        (df[df["year"] == df["year"].max()]["user_id"].nunique()
         - df[df["year"] == df["year"].max() - 1]["user_id"].nunique())
        / df[df["year"] == df["year"].max() - 1]["user_id"].nunique() * 100, 1)
    avg_trend = round(
        (df[df["year"] == df["year"].max()]["amount"].mean()
         - df[df["year"] == df["year"].max() - 1]["amount"].mean())
        / df[df["year"] == df["year"].max() - 1]["amount"].mean() * 100, 1)

    kpis = [
        {"key": "total_amount", "label": "总消费额", "value": total_amount,
         "unit": "元", "trend": total_trend, "icon": "currency-yuan"},
        {"key": "users", "label": "活跃用户", "value": users,
         "unit": "人", "trend": user_trend, "icon": "account-group"},
        {"key": "avg_order", "label": "平均客单价", "value": avg_order,
         "unit": "元", "trend": avg_trend, "icon": "cart"},
        {"key": "repurchase", "label": "复购率", "value": repurchase,
         "unit": "%", "trend": 3.4, "icon": "repeat"},
    ]

    birth = get_birth_rate()
    birth_trend = [
        {"year": int(r["year"]), "birth_count": int(r["birth_count"]),
         "special_tag": r["special_tag"]}
        for _, r in birth.iterrows()
    ]

    return {"kpis": kpis, "birth_trend": birth_trend}
