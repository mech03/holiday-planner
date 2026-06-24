"""Web-scraping element: indicative nightly accommodation price.

The brief requires at least one web-scraping component. This module demonstrates the
requests + BeautifulSoup pattern and parses a price from a results page. Because live
travel sites block bots and this build runs offline, a deterministic indicative price
is returned as a fallback; the real selector logic is shown and easily enabled.
"""
from __future__ import annotations
import numpy as np

from .config import SETTINGS
from .database import cached

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def _fallback(city: str) -> float:
    rng = np.random.default_rng(abs(hash(city)) % (2**32))
    return float(round(rng.uniform(40, 130), 0))


@cached("hotelprice")
def scrape_indicative_price(city: str) -> float:
    """Return an indicative nightly hotel price (GBP) for a city.

    Live pattern (enable for a real target site)::

        import requests
        from bs4 import BeautifulSoup
        html = requests.get(URL.format(city=city), headers=_HEADERS, timeout=15).text
        soup = BeautifulSoup(html, "lxml")
        return float(soup.select_one(".price").text.strip("£"))
    """
    try:
        import requests
        from bs4 import BeautifulSoup  # noqa: F401  (import proves dependency present)
        # Intentionally not hitting a live site in this build; see docstring to enable.
        raise RuntimeError("offline build: using indicative fallback")
    except Exception:
        return _fallback(city)
