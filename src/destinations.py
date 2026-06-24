"""Candidate destination catalogue.

The seed list lives in ``data/destinations.csv`` (tropical, nightlife-friendly spots).
Loading it from a file keeps the catalogue editable without touching code.
"""
from __future__ import annotations
import os
import pandas as pd

_DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "destinations.csv")


def load_destinations(path: str | None = None) -> pd.DataFrame:
    """Return the candidate destinations as a DataFrame.

    Parameters
    ----------
    path: optional override for the CSV location.
    """
    df = pd.read_csv(path or _DATA)
    required = {"city", "country", "lat", "lon", "avg_flight_gbp"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"destinations file missing columns: {missing}")
    return df
