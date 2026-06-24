"""Data-access layer for the Holiday Planner app.

The app is **CSV-driven**: the data team's pipeline writes its outputs to ``data/`` and
this module loads, tidies and re-ranks them. Keeping all file access and the re-rank
logic here means the pages stay focused on presentation.

Files consumed (in ``data/``):
  * ``destination_recommendations.csv`` — one row per destination with weather/amenity
    aggregates, flight + accommodation costs and component scores (the main table).
  * ``weather.csv`` — daily forecast rows per destination (for the weather graphs).
  * ``places.csv`` — individual nearby places (for the map, heatmap and place lists).
  * ``destinations.csv`` — a simpler current-snapshot table (optional/secondary).
"""
from __future__ import annotations
import os
from typing import Dict, List
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Component scores that feed the recommendation, with friendly labels.
SCORE_COMPONENTS: Dict[str, str] = {
    "weather_score": "Weather",
    "nightlife_score": "Nightlife",
    "amenity_score": "Amenities",
    "cost_score": "Cost / value",
}

# Google price-level enum -> human-friendly symbol.
PRICE_LEVEL_MAP: Dict[str, str] = {
    "PRICE_LEVEL_INEXPENSIVE": "£",
    "PRICE_LEVEL_MODERATE": "££",
    "PRICE_LEVEL_EXPENSIVE": "£££",
    "PRICE_LEVEL_VERY_EXPENSIVE": "££££",
}

PLACE_TYPE_LABELS: Dict[str, str] = {
    "restaurant": "Restaurants",
    "bar": "Bars",
    "night_club": "Night clubs",
    "tourist_attraction": "Attractions",
    "lodging": "Places to stay",
}


def _path(name: str) -> str:
    return os.path.join(DATA_DIR, name)


def load_recommendations() -> pd.DataFrame:
    """Return the main per-destination recommendation table (one row per destination)."""
    df = pd.read_csv(_path("destination_recommendations.csv"))
    df["country"] = df["country"].fillna(df["destination"].str.split(",").str[-1].str.strip())
    return df


def load_weather() -> pd.DataFrame:
    """Return the daily weather forecast table (many rows per destination)."""
    df = pd.read_csv(_path("weather.csv"))
    df["forecast_date"] = pd.to_datetime(df["forecast_date"])
    return df.sort_values(["destination", "forecast_date"])


def load_places() -> pd.DataFrame:
    """Return the nearby-places table with a tidy price label."""
    df = pd.read_csv(_path("places.csv"))
    df["price_label"] = df["price_level"].map(PRICE_LEVEL_MAP).fillna("N/A")
    df["category"] = df["place_type_searched"].map(PLACE_TYPE_LABELS).fillna(df["place_type_searched"])
    return df


def load_snapshot() -> pd.DataFrame:
    """Return the optional current-snapshot table (may include extra destinations)."""
    return pd.read_csv(_path("destinations.csv"))


def destinations(rec: pd.DataFrame | None = None) -> List[str]:
    """List of destination names from the recommendation table."""
    rec = load_recommendations() if rec is None else rec
    return rec["destination"].tolist()


def rerank(rec: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    """Re-rank destinations using the precomputed component scores and user weights.

    The data team provides 0-100 component scores (weather, nightlife, amenities, cost).
    The app lets the user say what matters to them; we recompute a weighted ``user_score``
    so the recommendation reflects their preferences. Weights are renormalised, so the
    result is always on a 0-100 scale.
    """
    w = {k: float(weights.get(k, 0.0)) for k in SCORE_COMPONENTS}
    total = sum(w.values()) or 1.0
    w = {k: v / total for k, v in w.items()}
    out = rec.copy()
    out["user_score"] = sum(out[c].fillna(0) * w[c] for c in SCORE_COMPONENTS)
    return out.sort_values("user_score", ascending=False).reset_index(drop=True)


def recommend_text(row: pd.Series) -> str:
    """A short, user-facing recommendation sentence for the top destination."""
    country = str(row.get("country", "")).strip()
    flight = row.get("selected_flight_price")
    cost = row.get("estimated_trip_cost")
    stay = str(row.get("selected_accommodation_name", "")).strip()
    temp = row.get("avg_temp_c")
    parts = [f"**{row['destination']}** is your best match"]
    if pd.notna(temp):
        parts.append(f"averaging {temp:.0f}°C")
    if pd.notna(flight):
        parts.append(f"flights around £{flight:.0f}")
    if pd.notna(cost):
        parts.append(f"an estimated £{cost:.0f} total trip")
    sentence = ", ".join(parts) + "."
    if stay and stay.lower() != "nan":
        sentence += f" Where to stay: **{stay}**."
    return sentence
