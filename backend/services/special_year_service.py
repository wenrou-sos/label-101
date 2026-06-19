# -*- coding: utf-8 -*-
"""特殊年份出生率影响服务：出生率波动、市场规模趋势、细分品类影响。"""
import pandas as pd

from data_loader import get_consumption, get_birth_rate

IMPACT_CATEGORIES = ["奶粉", "纸尿裤", "辅食", "营养品",
                     "婴儿车", "安全座椅", "玩具"]


def get_special_year_impact(start_year=2010, end_year=2024):
    birth = get_birth_rate().sort_values("year")
    birth = birth[(birth["year"] >= start_year) & (birth["year"] <= end_year)]
    df = get_consumption().copy()
    df["year"] = pd.to_datetime(df["order_date"]).dt.year
    df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    # 出生率趋势与同比
    birth_trend = []
    prev = None
    for _, r in birth.iterrows():
        bc = int(r["birth_count"])
        yoy = round((bc - prev) / prev * 100, 1) if prev else 0.0
        birth_trend.append({
            "year": int(r["year"]), "birth_count": bc,
            "special_tag": r["special_tag"], "yoy": yoy,
        })
        prev = bc

    special_years = [
        {"year": int(r["year"]), "tag": r["special_tag"]}
        for _, r in birth[birth["special_tag"] != ""].iterrows()
    ]

    # 市场规模趋势（消费总额）与同比
    ms = df.groupby("year")["amount"].sum().sort_index()
    market_size = []
    prev_ms = None
    for year, val in ms.items():
        yoy = round((val - prev_ms) / prev_ms * 100, 1) if prev_ms else 0.0
        market_size.append({
            "year": int(year), "market_size": round(float(val), 2), "yoy": yoy,
        })
        prev_ms = val

    # 特殊年份对细分品类的影响（该年该品类销售额同比变化）
    all_years = sorted(df["year"].unique())
    category_impact = []
    for sy in all_years:
        if sy - 1 not in all_years:
            continue
        cur = df[df["year"] == sy]
        prv = df[df["year"] == sy - 1]
        items = []
        for cat in IMPACT_CATEGORIES:
            c_amt = float(cur[cur["category"] == cat]["amount"].sum())
            p_amt = float(prv[prv["category"] == cat]["amount"].sum())
            yoy = round((c_amt - p_amt) / max(p_amt, 1) * 100, 1) if p_amt else 0.0
            items.append({"category": cat, "yoy": yoy,
                          "amount": round(c_amt, 2)})
        category_impact.append({"year": sy, "items": items})

    return {
        "birth_trend": birth_trend,
        "special_years": special_years,
        "market_size": market_size,
        "category_impact": category_impact,
        "impact_categories": IMPACT_CATEGORIES,
    }
