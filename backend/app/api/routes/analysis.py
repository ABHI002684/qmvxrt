from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.integrations.elexon_client import ElexonAPIError
from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.get("/analysis", response_model=AnalysisResponse)
async def get_analysis(
    target_date: date = Query(alias="date"),
    cutoff: str = Query(
        default="10:00",
        pattern=r"^([01]\d|2[0-3]):[0-5]\d$",
    ),
):
    if not date(2026, 1, 1) <= target_date <= date(2026, 1, 31):
        raise HTTPException(
            status_code=422,
            detail="Date must be within January 2026",
        )

    try:
        return await AnalysisService().analyze(target_date, cutoff)
    except ElexonAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc