from datetime import datetime, timezone

from app.services.forecast_selection import select_forecast_vintages


def test_selects_latest_forecast_before_cutoff():
    forecasts = [
        {
            "publishTime": "2026-01-14T08:00:00Z",
            "settlementDate": "2026-01-15",
            "settlementPeriod": 1,
            "generation": 100,
        },
        {
            "publishTime": "2026-01-14T09:00:00Z",
            "settlementDate": "2026-01-15",
            "settlementPeriod": 1,
            "generation": 120,
        },
        {
            "publishTime": "2026-01-14T11:00:00Z",
            "settlementDate": "2026-01-15",
            "settlementPeriod": 1,
            "generation": 140,
        },
    ]

    cutoff = datetime(2026, 1, 14, 10, 0, tzinfo=timezone.utc)

    result = select_forecast_vintages(forecasts, cutoff)

    assert len(result) == 1
    assert result[0]["generation"] == 120


def test_excludes_forecasts_published_after_cutoff():
    forecasts = [
        {
            "publishTime": "2026-01-14T11:00:00Z",
            "settlementDate": "2026-01-15",
            "settlementPeriod": 1,
            "generation": 140,
        },
    ]

    cutoff = datetime(2026, 1, 14, 10, 0, tzinfo=timezone.utc)

    assert select_forecast_vintages(forecasts, cutoff) == []