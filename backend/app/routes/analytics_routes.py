from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.prediction_schema import AnalyticsSummaryResponse
from app.services.analytics_service import analytics_service


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)

@router.get(
    "/summary",
    response_model=AnalyticsSummaryResponse,
)
def get_analytics_summary(
    db: Session = Depends(get_db),
) -> AnalyticsSummaryResponse:
    """
    Return aggregated statistics for the AgriPredict dashboard.
    """

    logger.info("Analytics summary requested")

    result = analytics_service.get_summary(db)

    logger.info(
        "Analytics summary generated: total_queries=%s average_yield=%.4f",
        result.total_queries,
        result.average_forecasted_yield,
    )

    return AnalyticsSummaryResponse(
        total_queries=result.total_queries,
        average_forecasted_yield=result.average_forecasted_yield,
        risk_distribution=result.risk_distribution,
        top_crops_evaluated=result.top_crops_evaluated,
    )