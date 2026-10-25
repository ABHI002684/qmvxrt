from fastapi import APIRouter, HTTPException

from app.integrations.elexon_client import ElexonAPIError, ElexonClient

router = APIRouter()


@router.get("/debug/elexon")
async def debug_elexon():
    client = ElexonClient()

    try:
        actuals = await client.get_actuals("2026-01-15", "2026-01-15")
        forecasts = await client.get_wind_forecasts(
            "2026-01-14",
            "2026-01-15",
        )
        target_date = "2026-01-15"

        forecast_delivery_samples = [
            item for item in forecasts
            if item.get("startTime", "").startswith(target_date)
        ][:10]
    except ElexonAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {
        "actuals": {
            "count": len(actuals),
            "fields": sorted(actuals[0].keys()) if actuals else [],
            "samples": actuals[:2],
        },
        "forecasts": {
            "count": len(forecasts),
            "fields": sorted(forecasts[0].keys()) if forecasts else [],
            "samples": forecasts[:2],
        },
        "forecast_delivery_samples": forecast_delivery_samples,
    }