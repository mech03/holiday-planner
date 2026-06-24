"""End-to-end pipeline: catalogue -> enrich (weather/places/price) -> score.

This single entry point is used by both the Streamlit app and the analysis notebook so
the logic stays in one place (DRY) and is easy to test.
"""
from __future__ import annotations
from typing import Dict
import pandas as pd

from .destinations import load_destinations
from .weather import get_weather
from .places import count_amenities
from .scraping import scrape_indicative_price
from .scoring import score_destinations


def build_recommendations(weights: Dict[str, float] | None = None,
                          ideal_temp: float = 30.0,
                          trip_nights: int = 7,
                          path: str | None = None) -> pd.DataFrame:
    """Return a fully scored, ranked DataFrame of destinations."""
    df = load_destinations(path)
    wx = df.apply(lambda r: pd.Series(get_weather(r["lat"], r["lon"])), axis=1)
    am = df.apply(lambda r: pd.Series(count_amenities(r["lat"], r["lon"])), axis=1)
    df["avg_hotel_gbp"] = df["city"].apply(scrape_indicative_price)
    enriched = pd.concat([df, wx.drop(columns=["source"], errors="ignore"),
                          am.drop(columns=["source"], errors="ignore")], axis=1)
    return score_destinations(enriched, weights=weights, ideal_temp=ideal_temp, trip_nights=trip_nights)
