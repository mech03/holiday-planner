"""Central configuration and API-key handling.

Keys are read from environment variables (or a local .env file if python-dotenv is
installed). Nothing secret is hard-coded; see .env.example for the variables used.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import Dict

try:  # optional convenience: load a local .env if present
    from dotenv import load_dotenv
    load_dotenv()
except Exception:  # pragma: no cover - dotenv is optional
    pass


@dataclass(frozen=True)
class Settings:
    """Runtime settings resolved from the environment."""
    google_places_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_PLACES_API_KEY", ""))
    google_geocoding_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_GEOCODING_API_KEY",
                                                                            os.getenv("GOOGLE_PLACES_API_KEY", "")))
    llm_api_key: str = field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "claude-haiku-4-5-20251001"))
    db_path: str = field(default_factory=lambda: os.getenv("HOLIDAY_DB_PATH", "holiday_cache.db"))
    cache_ttl_hours: int = field(default_factory=lambda: int(os.getenv("CACHE_TTL_HOURS", "24")))
    request_timeout: int = 15

    @property
    def has_places(self) -> bool:
        return bool(self.google_places_api_key)

    @property
    def has_llm(self) -> bool:
        return bool(self.llm_api_key)

    def status(self) -> Dict[str, bool]:
        """Quick diagnostic of which live integrations are enabled."""
        return {"google_places": self.has_places, "llm": self.has_llm}


SETTINGS = Settings()

# Default scoring weights (sum to 1.0). Exposed so the UI/notebook can tune them.
DEFAULT_WEIGHTS: Dict[str, float] = {
    "temp_comfort": 0.25,
    "low_cloud": 0.10,
    "calm_wind": 0.10,
    "nightlife": 0.35,
    "value": 0.20,
}
IDEAL_TEMP_C: float = 30.0
