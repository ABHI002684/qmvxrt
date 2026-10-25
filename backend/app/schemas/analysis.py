from pydantic import BaseModel


class AnalysisMetrics(BaseModel):
    periods: int
    mae: float | None
    rmse: float | None
    bias: float | None
    wape: float | None


class SettlementPeriodResult(BaseModel):
    period: str
    actual_mw: float
    forecast_mw: float
    error_mw: float
    publish_time: str


class AnalysisResponse(BaseModel):
    target_date: str
    cutoff: str
    metrics: AnalysisMetrics
    results: list[SettlementPeriodResult]