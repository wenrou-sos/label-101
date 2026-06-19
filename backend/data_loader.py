# -*- coding: utf-8 -*-
"""数据加载层：读取 CSV 文件并做模块级缓存，避免每次请求重复 IO。"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

_CACHE = {}


def _load(name):
    if name not in _CACHE:
        path = os.path.join(DATA_DIR, name)
        _CACHE[name] = pd.read_csv(path, encoding="utf-8-sig")
    return _CACHE[name]


def get_consumption():
    return _load("consumption.csv")


def get_users():
    return _load("users.csv")


def get_brand_loyalty():
    return _load("brand_loyalty.csv")


def get_decision_factors():
    return _load("decision_factors.csv")


def get_birth_rate():
    df = _load("birth_rate.csv")
    return df.fillna({"special_tag": ""})


def ok(data):
    """统一响应封装。"""
    return {"code": 200, "message": "success", "data": data}
