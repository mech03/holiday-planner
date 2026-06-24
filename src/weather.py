"""Weather signal via the Open-Meteo API (no API key required).

Returns a 7-day forecast summary (max temperature, humidity, cloud cover, wind). If
the network is unavailable the function returns a deterministic representative value so
downstream scoring still works offline.
"""
from __future__ import annotations
from typing import Dict
import numpy as np

from .config import SETTINGS
from .database import cached


def _fallback(lat: float, lon: float) -> Dict[str, float]:
    rng = np.random.default_rng(abs(int(lat * 100)) + abs(int(lon * 100)))
    return {"temp_max": float(rng.uniform(28, 34)), "humidity": float(rng.uniform(60, 85)),
            "cloud": float(rng.uniform(10, 45)), "wind": float(rng.uniform(8, 22)), "source": "fallback"}


@cached("weather")
def get_weather(lat: float, lon: float) -> Dict[str, float]:
    """Return mean 7-day weather for a coordinate.

    Keys: ``temp_max`` (C), ``humidity`` (%), ``cloud`` (%), ``wind`` (km/h), ``source``.
    """
    try:
        import requests
        url = ("https://api.open-meteo.com/v1/forecast"
               f"?latitude={lat}&longitude={lon}"
               "&daily=temperature_2m_max,relative_humidity_2m_mean,"
               "cloud_cover_mean,wind_speed_10m_max&forecast_days=7&timezone=auto")
        d = requests.get(url, timeout=SETTINGS.request_timeout).json()["daily"]
        return {"temp_max": float(np.mean(d["temperature_2m_max"])),
                "humidity": float(np.mean(d["relative_humidity_2m_mean"])),
                "cloud": float(np.mean(d["cloud_cover_mean"])),
                "wind": float(np.mean(d["wind_speed_10m_max"])), "source": "open-meteo"}
    except Exception:
        return _fallback(lat, lon)
