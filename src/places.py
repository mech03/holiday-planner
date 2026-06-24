"""Nightlife/amenity signal via the Google Places API.

Counts nearby night clubs, bars and restaurants. Requires GOOGLE_PLACES_API_KEY; falls
back to a deterministic representative count when the key or network is unavailable.
"""
from __future__ import annotations
from typing import Dict
import numpy as np

from .config import SETTINGS
from .database import cached


def _fallback(lat: float, lon: float) -> Dict[str, int]:
    rng = np.random.default_rng(abs(int(lat * 97)) + abs(int(lon * 53)))
    return {"night_clubs": int(rng.integers(3, 25)), "bars": int(rng.integers(10, 60)),
            "restaurants": int(rng.integers(20, 60)), "source": "fallback"}


@cached("places")
def count_amenities(lat: float, lon: float, radius: int = 4000) -> Dict[str, int]:
    """Return counts of nearby night clubs, bars and restaurants within ``radius`` metres."""
    if not SETTINGS.has_places:
        return _fallback(lat, lon)
    try:
        import requests
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        out: Dict[str, int] = {}
        for kind in ("night_club", "bar", "restaurant"):
            params = {"location": f"{lat},{lon}", "radius": radius,
                      "type": kind, "key": SETTINGS.google_places_api_key}
            r = requests.get(url, params=params, timeout=SETTINGS.request_timeout).json()
            out[kind + "s"] = len(r.get("results", []))
        out["source"] = "google-places"
        return out
    except Exception:
        return _fallback(lat, lon)
