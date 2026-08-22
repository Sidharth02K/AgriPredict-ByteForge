from __future__ import annotations

from dataclasses import dataclass
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.prediction_model import PredictionRecord


@dataclass
class AnalyticsResult:
    """
    Aggregated analytics calculated from prediction history.
    """

    total_queries: int
    average_forecasted_yield: float
    risk_distribution: dict[str, int]
    top_crops_evaluated: list[dict[str, object]]


class AnalyticsService:
    """
    Service responsible for calculating dashboard analytics
    from stored AgriPredict prediction records.
    """

    RISK_LEVELS = ("LOW", "MEDIUM", "HIGH")

    def get_summary(self, db: Session) -> AnalyticsResult:
        """
        Calculate the complete analytics summary.
        """

        # ---------------------------------------------------------
        # Total prediction queries
        # ---------------------------------------------------------

        total_queries = (
            db.query(func.count(PredictionRecord.id))
            .scalar()
            or 0
        )

        # ---------------------------------------------------------
        # Average forecasted yield
        # ---------------------------------------------------------

        average_yield = (
            db.query(
                func.avg(
                    PredictionRecord.expected_yield_tonnes_per_ha
                )
            )
            .scalar()
        )

        average_forecasted_yield = (
            float(average_yield)
            if average_yield is not None
            else 0.0
        )

        # ---------------------------------------------------------
        # Risk distribution
        # ---------------------------------------------------------

        risk_distribution = {
            level: 0
            for level in self.RISK_LEVELS
        }

        risk_rows = (
            db.query(
                PredictionRecord.risk_level,
                func.count(PredictionRecord.id),
            )
            .group_by(PredictionRecord.risk_level)
            .all()
        )

        for risk_level, count in risk_rows:
            normalized_level = str(risk_level).upper()

            if normalized_level in risk_distribution:
                risk_distribution[normalized_level] = int(count)

        # ---------------------------------------------------------
        # Top crops evaluated
        # ---------------------------------------------------------

        crop_rows = (
            db.query(
                PredictionRecord.crop_type,
                func.count(PredictionRecord.id).label("count"),
            )
            .group_by(PredictionRecord.crop_type)
            .order_by(
                func.count(PredictionRecord.id).desc()
            )
            .limit(5)
            .all()
        )

        top_crops_evaluated = [
            {
                "crop_type": str(crop_type),
                "count": int(count),
            }
            for crop_type, count in crop_rows
        ]

        # ---------------------------------------------------------
        # Return complete result
        # ---------------------------------------------------------

        return AnalyticsResult(
            total_queries=int(total_queries),
            average_forecasted_yield=average_forecasted_yield,
            risk_distribution=risk_distribution,
            top_crops_evaluated=top_crops_evaluated,
        )


analytics_service = AnalyticsService()