from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """
    Input received from the frontend for a crop yield prediction.
    """

    location: str = Field(..., examples=["Gujarat"])
    crop_type: str = Field(..., examples=["Wheat"])
    season: str = Field(..., examples=["Rabi"])

    rainfall_mm: float = Field(..., examples=[480.0])
    temperature_c: float = Field(..., examples=[24.0])
    soil_ph: float = Field(..., examples=[6.8])

    nitrogen_kgha: float = Field(..., examples=[75.0])
    phosphorus_kgha: float = Field(..., examples=[40.0])
    potassium_kgha: float = Field(..., examples=[35.0])

    farm_area_ha: Optional[float] = Field(
        default=1.0,
        gt=0,
        examples=[1.0],
        description="Farm area in hectares.",
    )


class SHAPDriver(BaseModel):
    """
    Clean, frontend-friendly representation of a model feature's
    SHAP contribution.
    """

    feature: str
    impact_value: float
    direction: str
    description: str


class PredictionResponse(BaseModel):
    """
    Complete result returned after a prediction.
    """

    id: int

    expected_yield_tonnes_per_ha: float
    total_production_tonnes: float

    risk_level: str
    risk_factors: List[str]

    key_drivers: List[SHAPDriver]

    actionable_recommendations: List[str]

    created_at: datetime


class AnalyticsSummaryResponse(BaseModel):
    """
    Aggregated statistics for the dashboard.
    """

    total_queries: int
    average_forecasted_yield: float

    risk_distribution: dict[str, int]

    top_crops_evaluated: List[dict[str, object]]