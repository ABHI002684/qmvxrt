from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.integrations.elexon_client import ElexonClient
from app.schemas.analysis import AnalysisResponse
from app.services.forecast_selection import (
    get_period_key,
    parse_timestamp,
    select_forecast_vintages,
)
from app.services.metrics import calculate_metrics


def period_key(record: dict) -> str | None:
    settlement_date = record.get("settlementDate")
    settlement_period = record.get("settlementPeriod")

    if settlement_date is not None and settlement_period is not None:
        return f"{settlement_date}:{settlement_period}"

    start_time = record.get("startTime")
    if start_time:
        return parse_timestamp(start_time).isoformat()

    return None


def generation_value(record: dict) -> float | None:
    value = record.get("generation")

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class AnalysisService:
    def __init__(self):
        self.client = ElexonClient()

    async def analyze(
        self,
        target_date: date,
        cutoff_time: str,
    ) -> AnalysisResponse:
        hour, minute = map(int, cutoff_time.split(":"))
        cutoff_date = target_date - timedelta(days=1)

        cutoff = datetime(
            cutoff_date.year,
            cutoff_date.month,
            cutoff_date.day,
            hour,
            minute,
            tzinfo=ZoneInfo("Europe/London"),
        )

        delivery_start = datetime(
            target_date.year,
            target_date.month,
            target_date.day,
            tzinfo=ZoneInfo("UTC"),
        )
        delivery_end = delivery_start + timedelta(days=1)

        actuals = await self.client.get_actuals(
            target_date.isoformat(),
            target_date.isoformat(),
        )

        forecasts = await self.client.get_wind_forecasts(
            cutoff_date.isoformat(),
            target_date.isoformat(),
        )

        wind_actuals = [
            record
            for record in actuals
            if str(record.get("fuelType", "")).strip().upper() == "WIND"
        ]

        selected_forecasts = select_forecast_vintages(forecasts, cutoff)

        actual_by_hour: dict[str, list[float]] = {}

        for record in wind_actuals:
            start_time = record.get("startTime")
            value = generation_value(record)

            if not start_time or value is None:
                continue

            try:
                timestamp = parse_timestamp(start_time)
            except (TypeError, ValueError):
                continue

            hour_key = timestamp.replace(
                minute=0,
                second=0,
                microsecond=0,
            ).isoformat()

            actual_by_hour.setdefault(hour_key, []).append(value)

        results = []

        for forecast in selected_forecasts:
            start_time = forecast.get("startTime")
            forecast_value = generation_value(forecast)
            publish_time = forecast.get("publishTime")

            if not start_time or forecast_value is None or not publish_time:
                continue

            try:
                timestamp = parse_timestamp(start_time)
            except (TypeError, ValueError):
                continue

            if not delivery_start <= timestamp < delivery_end:
                continue

            hour_key = timestamp.replace(
                minute=0,
                second=0,
                microsecond=0,
            ).isoformat()

            hourly_actuals = actual_by_hour.get(hour_key)

            if not hourly_actuals:
                continue

            actual_value = sum(hourly_actuals) / len(hourly_actuals)

            results.append({
                "period": hour_key,
                "actual_mw": actual_value,
                "forecast_mw": forecast_value,
                "error_mw": forecast_value - actual_value,
                "publish_time": publish_time,
            })

        results.sort(key=lambda item: item["period"])


        metrics = calculate_metrics(
            [item["actual_mw"] for item in results],
            [item["forecast_mw"] for item in results],
        )

        if not results:
            actual_fields = sorted(actuals[0].keys()) if actuals else []
            forecast_fields = sorted(forecasts[0].keys()) if forecasts else []

            raise ValueError(
                "No matching settlement periods. "
                f"Actual records: {len(actuals)}; "
                f"wind actual records: {len(wind_actuals)}; "
                f"forecast records: {len(forecasts)}; "
                f"eligible forecast periods: {len(selected_forecasts)}; "
                f"matched actual hours: {len(actual_by_hour)}. "
                f"Actual fields: {actual_fields}; "
                f"forecast fields: {forecast_fields}"
            )

        return AnalysisResponse(
            target_date=target_date.isoformat(),
            cutoff=cutoff.isoformat(),
            metrics=metrics,
            results=results,
        )