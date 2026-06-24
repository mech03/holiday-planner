"""Unit tests for the data-access layer (run with: pytest -q)."""
import pandas as pd
import pytest

from src.data_loader import (load_recommendations, load_weather, load_places,
                             rerank, recommend_text, SCORE_COMPONENTS)


def test_recommendations_load():
    rec = load_recommendations()
    assert len(rec) >= 1
    for col in ("destination", "final_recommendation_score", "estimated_trip_cost",
                *SCORE_COMPONENTS):
        assert col in rec.columns


def test_weather_dates_parsed():
    wx = load_weather()
    assert pd.api.types.is_datetime64_any_dtype(wx["forecast_date"])
    assert {"forecast_max_temp_c", "destination"} <= set(wx.columns)


def test_places_has_labels():
    pl = load_places()
    assert {"price_label", "category"} <= set(pl.columns)


def test_rerank_orders_by_user_score():
    rec = load_recommendations()
    out = rerank(rec, {"weather_score": 1, "nightlife_score": 0, "amenity_score": 0, "cost_score": 0})
    assert list(out["user_score"]) == sorted(out["user_score"], reverse=True)
    assert out["user_score"].between(0, 100).all()


def test_rerank_weights_change_top():
    rec = load_recommendations()
    cost_first = rerank(rec, {"weather_score": 0, "nightlife_score": 0,
                              "amenity_score": 0, "cost_score": 1}).iloc[0]
    # the cost-first top should have the maximum cost_score
    assert cost_first["cost_score"] == rec["cost_score"].max()


def test_recommend_text_mentions_destination():
    rec = load_recommendations()
    txt = recommend_text(rec.iloc[0])
    assert rec.iloc[0]["destination"] in txt
