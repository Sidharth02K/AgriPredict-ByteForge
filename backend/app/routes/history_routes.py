from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.prediction_model import PredictionRecord
from app.schemas.prediction_schema import (
    PredictionHistoryItem,
    PredictionHistoryResponse,
    PredictionResponse,
    SHAPDriver,
)
from app.services.risk_service import risk_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["History"],
)


@router.get(
    "/history",
    response_model=PredictionHistoryResponse,
)
def get_prediction_history(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number starting from 1.",
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of records per page.",
    ),
    db: Session = Depends(get_db),
) -> PredictionHistoryResponse:
    """
    Return paginated prediction history.

    Most recent predictions are returned first.
    """

    logger.info(
        "Prediction history requested: page=%s page_size=%s",
        page,
        page_size,
    )

    total = db.query(PredictionRecord).count()

    offset = (page - 1) * page_size

    records = (
        db.query(PredictionRecord)
        .order_by(PredictionRecord.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    logger.info(
        "Prediction history returned: total=%s items=%s",
        total,
        len(records),
    )

    items = [
        PredictionHistoryItem(
            id=record.id,
            location=record.location,
            crop_type=record.crop_type,
            season=record.season,
            expected_yield_tonnes_per_ha=record.expected_yield_tonnes_per_ha,
            total_production_tonnes=record.total_production_tonnes,
            risk_level=record.risk_level,
            created_at=record.created_at,
        )
        for record in records
    ]

    return PredictionHistoryResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


@router.get(
    "/history/{prediction_id}",
    response_model=PredictionResponse,
)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
) -> PredictionResponse:
    """
    Return the complete details of one prediction.
    """

    record = db.get(
        PredictionRecord,
        prediction_id,
    )

    logger.info(
        "Prediction detail requested: id=%s",
        prediction_id,
    )
    if record is None:
        logger.warning(
            "Prediction not found: id=%s",
            prediction_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction with ID {prediction_id} was not found.",
        )

    key_drivers = record.get_key_drivers()
    risk_factors = record.get_risk_factors()
    recommendations = record.get_recommendations()

    return PredictionResponse(
        id=record.id,
        expected_yield_tonnes_per_ha=record.expected_yield_tonnes_per_ha,
        total_production_tonnes=record.total_production_tonnes,
        risk_level=record.risk_level,
        risk_factors=risk_factors,
        key_drivers=[
            SHAPDriver(**driver)
            for driver in key_drivers
        ],
        actionable_recommendations=recommendations,
        created_at=record.created_at,
    )