from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RiskResult:
    """
    Result produced by the rule-based agricultural risk engine.
    """

    risk_level: str
    risk_factors: list[str] = field(default_factory=list)


class RiskService:
    """
    Rule-based risk assessment layer for AgriPredict.

    This service deliberately does not run the ML model.
    It receives the already calculated predicted yield and
    evaluates agricultural risk indicators independently.
    """

    # Thresholds based on the AgriPredict project specification.
    RAINFALL_MEDIUM_THRESHOLD = 400.0
    RAINFALL_HIGH_THRESHOLD = 300.0

    NITROGEN_THRESHOLD = 60.0

    PH_MIN = 5.5
    PH_MAX = 8.2

    YIELD_HIGH_THRESHOLD = 2.0

    def assess(
        self,
        *,
        rainfall_mm: float,
        nitrogen_kgha: float,
        soil_ph: float,
        predicted_yield_tonnes_per_ha: float,
    ) -> RiskResult:
        """
        Evaluate the supplied farm conditions and predicted yield.

        Risk levels:
            LOW
            MEDIUM
            HIGH

        Multiple risk factors can be detected simultaneously.
        The final risk level is the highest severity detected.
        """

        risk_factors: list[str] = []
        severity_scores: list[int] = []

        # ---------------------------------------------------------
        # 1. Rainfall risk
        # ---------------------------------------------------------

        if rainfall_mm < self.RAINFALL_HIGH_THRESHOLD:
            severity_scores.append(3)

            risk_factors.append(
                f"Severe rainfall deficit: {rainfall_mm:.1f} mm. "
                "The farm may face significant water stress."
            )

        elif rainfall_mm < self.RAINFALL_MEDIUM_THRESHOLD:
            severity_scores.append(2)

            risk_factors.append(
                f"Low rainfall: {rainfall_mm:.1f} mm. "
                "Additional irrigation may be required."
            )

        # ---------------------------------------------------------
        # 2. Nitrogen risk
        # ---------------------------------------------------------

        if nitrogen_kgha < self.NITROGEN_THRESHOLD:
            # Very low nitrogen receives HIGH severity.
            if nitrogen_kgha < 30:
                severity_scores.append(3)

                risk_factors.append(
                    f"Severe nitrogen deficiency: "
                    f"{nitrogen_kgha:.1f} kg/ha. "
                    "Crop growth and yield may be significantly affected."
                )

            else:
                severity_scores.append(2)

                risk_factors.append(
                    f"Low soil nitrogen: {nitrogen_kgha:.1f} kg/ha. "
                    "Nitrogen availability may limit crop growth."
                )

        # ---------------------------------------------------------
        # 3. Soil pH risk
        # ---------------------------------------------------------

        if soil_ph < self.PH_MIN:
            # Extremely acidic soil.
            if soil_ph < 4.5:
                severity_scores.append(3)

                risk_factors.append(
                    f"Severely acidic soil pH: {soil_ph:.2f}. "
                    "Nutrient availability may be strongly affected."
                )

            else:
                severity_scores.append(2)

                risk_factors.append(
                    f"Acidic soil pH: {soil_ph:.2f}. "
                    "Soil treatment may be required."
                )

        elif soil_ph > self.PH_MAX:
            # Extremely alkaline soil.
            if soil_ph > 9.0:
                severity_scores.append(3)

                risk_factors.append(
                    f"Severely alkaline soil pH: {soil_ph:.2f}. "
                    "Nutrient availability may be strongly affected."
                )

            else:
                severity_scores.append(2)

                risk_factors.append(
                    f"Alkaline soil pH: {soil_ph:.2f}. "
                    "Soil treatment may be required."
                )

        # ---------------------------------------------------------
        # 4. Predicted yield risk
        # ---------------------------------------------------------

        if predicted_yield_tonnes_per_ha < self.YIELD_HIGH_THRESHOLD:
            severity_scores.append(3)

            risk_factors.append(
                f"Low predicted yield: "
                f"{predicted_yield_tonnes_per_ha:.2f} tonnes/ha."
            )

        # ---------------------------------------------------------
        # 5. Determine final risk level
        # ---------------------------------------------------------

        if not severity_scores:
            return RiskResult(
                risk_level="LOW",
                risk_factors=[],
            )

        highest_severity = max(severity_scores)

        if highest_severity >= 3:
            risk_level = "HIGH"
        elif highest_severity == 2:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return RiskResult(
            risk_level=risk_level,
            risk_factors=risk_factors,
        )


# Shared service instance.
risk_service = RiskService()