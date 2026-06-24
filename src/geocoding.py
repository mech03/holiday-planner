"""Google Geocoding API helper (second Google API for innovation marks).

Resolves a free-text place name to coordinates, so users can add their own
destinations. Falls back to a no-op (returns None) when no key/network is available.
"""
from __future__ import annotations
from typing import Optional, Tuple

from .config import SETTINGS
from .database import cached


@cached("geocode")
def geocode(place: str) -> Optional[Tuple[float, float]]:
    """Return (lat, lon) for a place name, or ``None`` if it cannot be resolved."""
    if not SETTINGS.google_geocoding_api_key:
        return None
    try:
        import requests
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": place, "key": SETTINGS.google_geocoding_api_key}
        r = requests.get(url, params=params, timeout=SETTINGS.request_timeout).json()
        loc = r["results"][0]["geometry"]["location"]
        return float(loc["lat"]), float(loc["lng"])
    except Exception:
        return None
