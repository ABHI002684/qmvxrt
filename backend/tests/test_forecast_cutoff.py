
from datetime import datetime, timezone

from app.services.forecast_selection import select_forecast_vintages


CUTOFF = datetime(2026, 1, 14, 10, 0, tzinfo=timezone.utc)


def make_forecast(start_time: str, publish_time: str, generation: float) -> dict:
    return {
        "startTime": start_time,
        "publishTime": publish_time,
        "generation": generation,
    }


def test_excludes_forecasts_published_after_cutoff():
    forecasts = [
        make_forecast(
            "2026-01-15T00:00:00Z",
            "2026-01-14T09:30:00Z",
            15000,
        ),
        make_forecast(
            "2026-01-15T00:00:00Z",
            "2026-01-14T10:30:00Z",
            16000,
        ),
    ]

    selected = select_forecast_vintages(forecasts, CUTOFF)

    assert len(selected) == 1
    assert selected[0]["generation"] == 15000


def test_selects_latest_vintage_before_cutoff():
    forecasts = [
        make_forecast(
            "2026-01-15T01:00:00Z",
            "2026-01-14T08:00:00Z",
            14000,
        ),
        make_forecast(
            "2026-01-15T01:00:00Z",
            "2026-01-14T09:30:00Z",
            15500,
        ),
        make_forecast(
            "2026-01-15T01:00:00Z",
            "2026-01-14T10:30:00Z",
            17000,
        ),
    ]

    selected = select_forecast_vintages(forecasts, CUTOFF)

    assert len(selected) == 1
    assert selected[0]["generation"] == 15500
    assert selected[0]["publishTime"] == "2026-01-14T09:30:00Z"


def test_keeps_different_delivery_hours_separate():
    forecasts = [
        make_forecast(
            "2026-01-15T00:00:00Z",
            "2026-01-14T09:30:00Z",
            15000,
        ),
        make_forecast(
            "2026-01-15T01:00:00Z",
            "2026-01-14T09:30:00Z",
            14500,
        ),
    ]

    selected = select_forecast_vintages(forecasts, CUTOFF)

    assert len(selected) == 2
    assert {item["startTime"] for item in selected} == {
        "2026-01-15T00:00:00Z",
        "2026-01-15T01:00:00Z",
    }
