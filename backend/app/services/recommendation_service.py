from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RecommendationResult:
    """
    Contains practical recommendations generated from
    the farm's detected limiting factors.
    """

    recommendations: list[str] = field(default_factory=list)


class RecommendationService:
    """
    Rule-based agronomic decision-support layer.

    Important:
    This service does not replace an agronomist or soil test.
    It generates practical advisory suggestions from the
    indicators available to AgriPredict.
    """

    RAINFALL_THRESHOLD = 400.0
    RAINFALL_SEVERE_THRESHOLD = 300.0

    NITROGEN_THRESHOLD = 60.0
    PHOSPHORUS_THRESHOLD = 30.0
    POTASSIUM_THRESHOLD = 30.0

    PH_MIN = 5.5
    PH_MAX = 8.2

    def generate(
        self,
        *,
        rainfall_mm: float,
        soil_ph: float,
        nitrogen_kgha: float,
        phosphorus_kgha: float,
        potassium_kgha: float,
        predicted_yield_tonnes_per_ha: float,
        risk_level: str,
    ) -> RecommendationResult:
        """
        Generate recommendations from the supplied farm conditions.

        Recommendations are intentionally advisory rather than
        prescribing exact fertilizer quantities.
        """

        recommendations: list[str] = []

        # ---------------------------------------------------------
        # 1. Irrigation / rainfall
        # ---------------------------------------------------------

        if rainfall_mm < self.RAINFALL_SEVERE_THRESHOLD:
            recommendations.append(
                "Prioritize supplemental irrigation and monitor soil "
                "moisture closely because rainfall is severely deficient."
            )

        elif rainfall_mm < self.RAINFALL_THRESHOLD:
            recommendations.append(
                "Consider supplemental irrigation based on crop water "
                "requirements and current soil-moisture conditions."
            )

        # ---------------------------------------------------------
        # 2. Nitrogen
        # ---------------------------------------------------------

        if nitrogen_kgha < self.NITROGEN_THRESHOLD:
            recommendations.append(
                "Consider a soil-test-guided nitrogen management plan "
                "to address the detected low nitrogen level."
            )

        # ---------------------------------------------------------
        # 3. Phosphorus
        # ---------------------------------------------------------

        if phosphorus_kgha < self.PHOSPHORUS_THRESHOLD:
            recommendations.append(
                "Consider soil testing and a phosphorus management plan "
                "if phosphorus availability is confirmed to be low."
            )

        # ---------------------------------------------------------
        # 4. Potassium
        # ---------------------------------------------------------

        if potassium_kgha < self.POTASSIUM_THRESHOLD:
            recommendations.append(
                "Consider soil testing and potassium management because "
                "the measured potassium level is relatively low."
            )

        # ---------------------------------------------------------
        # 5. Soil pH
        # ---------------------------------------------------------

        if soil_ph < self.PH_MIN:
            recommendations.append(
                "Consider soil testing and an appropriate liming strategy "
                "to address acidic soil conditions."
            )

        elif soil_ph > self.PH_MAX:
            recommendations.append(
                "Consider soil testing and an appropriate soil amendment "
                "strategy to manage alkaline conditions."
            )

        # ---------------------------------------------------------
        # 6. Low predicted yield
        # ---------------------------------------------------------

        if predicted_yield_tonnes_per_ha < 2.0:
            recommendations.append(
                "The forecasted yield is low. Review irrigation, nutrient "
                "availability, soil condition, crop health, and pest or "
                "disease pressure before making management decisions."
            )

        # ---------------------------------------------------------
        # 7. High-level risk advice
        # ---------------------------------------------------------

        if risk_level == "HIGH":
            recommendations.append(
                "High-risk conditions detected. Prioritize the identified "
                "limiting factors and consider consulting a local "
                "agricultural expert before major interventions."
            )

        elif risk_level == "MEDIUM":
            recommendations.append(
                "Moderate-risk conditions detected. Monitor the identified "
                "limiting factors regularly and adjust farm management "
                "accordingly."
            )

        # ---------------------------------------------------------
        # 8. No limiting factors
        # ---------------------------------------------------------

        if not recommendations:
            recommendations.append(
                "Current measured conditions do not indicate a major "
                "limiting factor. Continue regular monitoring of soil "
                "moisture, nutrients, and crop health."
            )

        return RecommendationResult(
            recommendations=recommendations
        )


# Shared service instance.
recommendation_service = RecommendationService()