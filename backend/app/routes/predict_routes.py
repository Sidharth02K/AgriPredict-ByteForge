from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.prediction_model import PredictionRecord
from app.schemas.prediction_schema import (
    PredictionRequest,
    PredictionResponse,
)
from app.services.ml_service import ml_service
from app.services.recommendation_service import recommendation_service
from app.services.risk_service import risk_service


router = APIRouter(
    prefix="/api/v1",
    tags=["Predictions"],
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db),
) -> PredictionResponse:
    """
    Generate a crop-yield forecast and complete decision-support result.

    Processing pipeline:

        Request
          ↓
        ML prediction
          ↓
        SHAP explanation
          ↓
        Risk assessment
          ↓
        Recommendations
          ↓
        Database persistence
          ↓
        Response
    """

    # ---------------------------------------------------------
    # 1. Check ML model availability
    # ---------------------------------------------------------

    if not ml_service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Production ML model is not loaded.",
        )

    try:
        # -----------------------------------------------------
        # 2. Convert validated request to a plain dictionary
        # -----------------------------------------------------

        input_data = request.model_dump()

        # -----------------------------------------------------
        # 3. Run ML prediction
        # -----------------------------------------------------

        predicted_yield = ml_service.predict(input_data)

        # Prevent invalid numerical results from entering
        # the database/API response.
        if predicted_yield < 0:
            predicted_yield = 0.0

        # -----------------------------------------------------
        # 4. Calculate total farm production
        # -----------------------------------------------------

        total_production = (
            predicted_yield * request.farm_area_ha
        )

        # -----------------------------------------------------
        # 5. Generate SHAP explanations
        # -----------------------------------------------------

        key_drivers = ml_service.explain(
            input_data,
            top_n=8,
        )

        # -----------------------------------------------------
        # 6. Assess agricultural risk
        # -----------------------------------------------------

        risk_result = risk_service.assess(
            rainfall_mm=request.rainfall_mm,
            nitrogen_kgha=request.nitrogen_kgha,
            soil_ph=request.soil_ph,
            predicted_yield_tonnes_per_ha=predicted_yield,
        )

        # -----------------------------------------------------
        # 7. Generate recommendations
        # -----------------------------------------------------

        recommendation_result = recommendation_service.generate(
            rainfall_mm=request.rainfall_mm,
            soil_ph=request.soil_ph,
            nitrogen_kgha=request.nitrogen_kgha,
            phosphorus_kgha=request.phosphorus_kgha,
            potassium_kgha=request.potassium_kgha,
            predicted_yield_tonnes_per_ha=predicted_yield,
            risk_level=risk_result.risk_level,
        )

        # -----------------------------------------------------
        # 8. Convert SHAP drivers into Pydantic objects
        # -----------------------------------------------------

        # ml_service already returns dictionaries matching
        # SHAPDriver's schema.
        driver_objects = [
            {
                "feature": driver["feature"],
                "impact_value": float(driver["impact_value"]),
                "direction": driver["direction"],
                "description": driver["description"],
            }
            for driver in key_drivers
        ]

        # -----------------------------------------------------
        # 9. Save complete prediction to database
        # -----------------------------------------------------

        record = PredictionRecord(
            location=request.location,
            crop_type=request.crop_type,
            season=request.season,
            rainfall_mm=request.rainfall_mm,
            temperature_c=request.temperature_c,
            soil_ph=request.soil_ph,
            nitrogen_kgha=request.nitrogen_kgha,
            phosphorus_kgha=request.phosphorus_kgha,
            potassium_kgha=request.potassium_kgha,
            farm_area_ha=request.farm_area_ha,
            expected_yield_tonnes_per_ha=predicted_yield,
            total_production_tonnes=total_production,
            risk_level=risk_result.risk_level,
            risk_factors_json=json.dumps(
                risk_result.risk_factors
            ),
            key_drivers_json=json.dumps(
                driver_objects
            ),
            recommendations_json=json.dumps(
                recommendation_result.recommendations
            ),
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        # -----------------------------------------------------
        # 10. Return frontend-friendly response
        # -----------------------------------------------------

        return PredictionResponse(
            id=record.id,
            expected_yield_tonnes_per_ha=round(
                predicted_yield,
                4,
            ),
            total_production_tonnes=round(
                total_production,
                4,
            ),
            risk_level=risk_result.risk_level,
            risk_factors=risk_result.risk_factors,
            key_drivers=driver_objects,
            actionable_recommendations=(
                recommendation_result.recommendations
            ),
            created_at=record.created_at,
        )

    except HTTPException:
        raise

    except Exception as exc:
        # Roll back the database transaction if anything failed
        # after the transaction began.
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction processing failed: {exc}",
        ) from exc