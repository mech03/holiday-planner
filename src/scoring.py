"""Transparent, explainable destination scoring.

The Adventure Score (0-100) blends five normalised signals with tunable weights:
warmth comfort, low cloud, calm wind, nightlife density and value (total cost). Keeping
the model simple and auditable is deliberate - users can see *why* a place ranks highly.
"""
from __future__ import annotations
from typing import Dict
import numpy as np
import pandas as pd

from .config import DEFAULT_WEIGHTS, IDEAL_TEMP_C


def _minmax(s: pd.Series, invert: bool = False) -> pd.Series:
    rng = s.max() - s.min()
    out = (s - s.min()) / (rng + 1e-9)
    return 1 - out if invert else out


def score_destinations(df: pd.DataFrame,
                       weights: Dict[str, float] | None = None,
                       ideal_temp: float = IDEAL_TEMP_C,
                       trip_nights: int = 7) -> pd.DataFrame:
    """Return ``df`` with engineered signals and an ``adventure_score`` column.

    Expects columns: temp_max, cloud, wind, night_clubs, bars, restaurants,
    avg_flight_gbp, avg_hotel_gbp. Weights default to ``config.DEFAULT_WEIGHTS`` and are
    renormalised so the score is always on a 0-100 scale regardless of the inputs.
    """
    w = dict(DEFAULT_WEIGHTS if weights is None else weights)
    total = sum(w.values()) or 1.0
    w = {k: v / total for k, v in w.items()}

    d = df.copy()
    d["total_cost"] = d["avg_flight_gbp"] + d["avg_hotel_gbp"] * trip_nights
    # comfort peaks at the ideal temperature and decays linearly
    d["temp_comfort"] = 1 - (d["temp_max"] - ideal_temp).abs() / 10
    d["nightlife"] = (_minmax(d["night_clubs"]) * 0.5
                      + _minmax(d["bars"]) * 0.3
                      + _minmax(d["restaurants"]) * 0.2)

    d["adventure_score"] = (
        _minmax(d["temp_comfort"]) * w["temp_comfort"]
        + _minmax(d["cloud"], invert=True) * w["low_cloud"]
        + _minmax(d["wind"], invert=True) * w["calm_wind"]
        + d["nightlife"] * w["nightlife"]
        + _minmax(d["total_cost"], invert=True) * w["value"]
    ) * 100
    return d.sort_values("adventure_score", ascending=False).reset_index(drop=True)


def explain(row: pd.Series) -> str:
    """One-line, user-facing rationale for a destination's ranking."""
    return (f"{row['city']}, {row['country']}: ~{row['temp_max']:.0f}°C, "
            f"{int(row['night_clubs'])} clubs & {int(row['bars'])} bars nearby, "
            f"~£{int(row['total_cost'])} total for the trip.")
