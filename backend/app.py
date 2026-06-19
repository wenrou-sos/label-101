# -*- coding: utf-8 -*-
"""母婴市场消费分析看板 - Flask 主应用入口。

启动：python app.py  （默认 http://127.0.0.1:5000）
"""
import os
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from data_loader import ok  # noqa: E402
from services import (  # noqa: E402
    overview_service,
    age_stage_service,
    category_service,
    city_tier_service,
    loyalty_service,
    special_year_service,
)

app = Flask(__name__)
CORS(app)

MIN_YEAR = 2010
MAX_YEAR = 2024


def get_year_range():
    start = request.args.get("start_year", type=int, default=MIN_YEAR)
    end = request.args.get("end_year", type=int, default=MAX_YEAR)
    start = max(MIN_YEAR, min(start, MAX_YEAR))
    end = max(MIN_YEAR, min(end, MAX_YEAR))
    if start > end:
        start, end = end, start
    return start, end


@app.errorhandler(500)
def handle_500(e):
    return jsonify({"code": 500, "message": str(e), "data": None}), 500


@app.route("/api/health")
def health():
    return ok({"status": "ok", "min_year": MIN_YEAR, "max_year": MAX_YEAR})


@app.route("/api/overview")
def overview():
    start, end = get_year_range()
    return ok(overview_service.get_overview(start, end))


@app.route("/api/age-stage/consumption")
def age_stage_consumption():
    start, end = get_year_range()
    return ok(age_stage_service.get_age_stage_consumption(start, end))


@app.route("/api/category/decision-factors")
def category_decision_factors():
    start, end = get_year_range()
    return ok(category_service.get_decision_factors(start, end))


@app.route("/api/city-tier/comparison")
def city_tier_comparison():
    start, end = get_year_range()
    return ok(city_tier_service.get_city_tier_comparison(start, end))


@app.route("/api/loyalty/survival")
def loyalty_survival():
    start, end = get_year_range()
    return ok(loyalty_service.get_loyalty_survival(start, end))


@app.route("/api/special-year/impact")
def special_year_impact():
    start, end = get_year_range()
    return ok(special_year_service.get_special_year_impact(start, end))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
