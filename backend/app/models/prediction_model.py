from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class PredictionRecord(Base):
    """
    Database record for one AgriPredict forecast.

    One row represents one prediction request and its complete
    decision-support result.
    """

    __tablename__ = "prediction_records"

    # ---------------------------------------------------------
    # Primary key
    # ---------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # ---------------------------------------------------------
    # Farm / crop input data
    # ---------------------------------------------------------

    location: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    crop_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    season: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    rainfall_mm: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    temperature_c: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    soil_ph: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    nitrogen_kgha: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    phosphorus_kgha: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    potassium_kgha: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    farm_area_ha: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    # ---------------------------------------------------------
    # Prediction results
    # ---------------------------------------------------------

    expected_yield_tonnes_per_ha: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total_production_tonnes: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Risk assessment
    # ---------------------------------------------------------

    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    # Stored as JSON strings.
    risk_factors_json: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    # ---------------------------------------------------------
    # Explainability
    # ---------------------------------------------------------

    # Stored as a JSON string containing SHAPDriver objects.
    key_drivers_json: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    # ---------------------------------------------------------
    # Recommendations
    # ---------------------------------------------------------

    # Stored as a JSON string containing recommendation strings.
    recommendations_json: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    # ---------------------------------------------------------
    # Timestamp
    # ---------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    def __repr__(self) -> str:
        return (
            f"<PredictionRecord "
            f"id={self.id} "
            f"location={self.location!r} "
            f"crop_type={self.crop_type!r} "
            f"yield={self.expected_yield_tonnes_per_ha:.2f}>"
        )