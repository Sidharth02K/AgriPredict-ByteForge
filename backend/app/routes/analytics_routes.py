from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.prediction_schema import AnalyticsSummaryResponse
from app.services.analytics_service import analytics_service


router = APIRouter(
    prefix="/api/v1",
    tags=["Analytics"],
)


@router.get(
    "/analytics/summary",
    response_model=AnalyticsSummaryResponse,
)
def get_analytics_summary(
    db: Session = Depends(get_db),
) -> AnalyticsSummaryResponse:
    """
    Return aggregated statistics for the AgriPredict dashboard.
    """

    result = analytics_service.get_summary(db)

    return AnalyticsSummaryResponse(
        total_queries=result.total_queries,
        average_forecasted_yield=result.average_forecasted_yield,
        risk_distribution=result.risk_distribution,
        top_crops_evaluated=result.top_crops_evaluated,
    )