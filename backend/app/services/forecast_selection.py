from datetime import datetime, timezone
from typing import Any


def parse_timestamp(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        timestamp = value
    else:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if timestamp.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")

    return timestamp.astimezone(timezone.utc)


def get_period_key(record: dict[str, Any]) -> str | None:
    start_time = record.get("startTime")

    if start_time:
        try:
            return parse_timestamp(start_time).isoformat()
        except (TypeError, ValueError):
            pass

    settlement_date = record.get("settlementDate")
    settlement_period = record.get("settlementPeriod")

    if settlement_date is not None and settlement_period is not None:
        return f"{settlement_date}:{settlement_period}"

    return None


def select_forecast_vintages(
    forecasts: list[dict[str, Any]],
    cutoff: datetime,
) -> list[dict[str, Any]]:
    cutoff_utc = parse_timestamp(cutoff)
    latest_by_period: dict[str, dict[str, Any]] = {}

    for forecast in forecasts:
        publish_time = forecast.get("publishTime")
        period_key = get_period_key(forecast)

        if not publish_time or not period_key:
            continue

        try:
            published_at = parse_timestamp(publish_time)
        except (TypeError, ValueError):
            continue

        if published_at > cutoff_utc:
            continue

        current = latest_by_period.get(period_key)

        if current is None or published_at > current["_published_at"]:
            latest_by_period[period_key] = {
                **forecast,
                "_published_at": published_at,
            }

    selected = []

    for record in latest_by_period.values():
        record.pop("_published_at", None)
        selected.append(record)

    return sorted(selected, key=lambda item: get_period_key(item) or "")