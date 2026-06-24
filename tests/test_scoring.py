"""Unit tests for the scoring engine (run with: pytest -q)."""
import pandas as pd
import pytest
from src.scoring import score_destinations, _minmax
from src.pipeline import build_recommendations


def _sample():
    return pd.DataFrame({
        "city": ["A", "B", "C"], "country": ["X", "Y", "Z"],
        "lat": [0, 1, 2], "lon": [0, 1, 2],
        "avg_flight_gbp": [500, 600, 700], "avg_hotel_gbp": [50, 60, 70],
        "temp_max": [30, 25, 34], "cloud": [10, 50, 30], "wind": [10, 20, 15],
        "night_clubs": [20, 2, 10], "bars": [40, 5, 20], "restaurants": [50, 10, 30],
    })


def test_minmax_bounds():
    s = _minmax(pd.Series([1, 2, 3]))
    assert s.min() == pytest.approx(0, abs=1e-6) and s.max() == pytest.approx(1, abs=1e-6)


def test_minmax_invert():
    s = _minmax(pd.Series([1, 2, 3]), invert=True)
    assert s.iloc[0] == pytest.approx(1, abs=1e-6) and s.iloc[-1] == pytest.approx(0, abs=1e-6)


def test_score_range_and_order():
    out = score_destinations(_sample())
    assert out["adventure_score"].between(0, 100).all()
    # results are sorted descending
    assert list(out["adventure_score"]) == sorted(out["adventure_score"], reverse=True)


def test_weights_renormalised():
    # unnormalised weights should still yield 0-100 scores
    out = score_destinations(_sample(), weights={"temp_comfort": 2, "low_cloud": 2,
                                                 "calm_wind": 2, "nightlife": 2, "value": 2})
    assert out["adventure_score"].max() <= 100.0001


def test_pipeline_runs_offline():
    df = build_recommendations()
    assert len(df) >= 5
    assert "adventure_score" in df.columns
