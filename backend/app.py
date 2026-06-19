# -*- coding: utf-8 -*-
"""母婴市场消费分析看板 - Flask 主应用入口。

启动：python app.py  （默认 http://127.0.0.1:5000）
"""
import os
import sys

from flask import Flask, jsonify
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


@app.errorhandler(500)
def handle_500(e):
    return jsonify({"code": 500, "message": str(e), "data": None}), 500


@app.route("/api/health")
def health():
    return ok({"status": "ok"})


@app.route("/api/overview")
def overview():
    return ok(overview_service.get_overview())


@app.route("/api/age-stage/consumption")
def age_stage_consumption():
    return ok(age_stage_service.get_age_stage_consumption())


@app.route("/api/category/decision-factors")
def category_decision_factors():
    return ok(category_service.get_decision_factors())


@app.route("/api/city-tier/comparison")
def city_tier_comparison():
    return ok(city_tier_service.get_city_tier_comparison())


@app.route("/api/loyalty/survival")
def loyalty_survival():
    return ok(loyalty_service.get_loyalty_survival())


@app.route("/api/special-year/impact")
def special_year_impact():
    return ok(special_year_service.get_special_year_impact())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
