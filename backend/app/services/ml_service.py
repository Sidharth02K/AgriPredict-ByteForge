from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import shap


MODEL_FILENAME = "agripredict_production_model.pkl"

NUMERIC_FEATURES = [
    "Rainfall (mm)",
    "Temperature (°C)",
    "Soil pH",
    "Nitrogen (kg/ha)",
    "Phosphorus (kg/ha)",
    "Potassium (kg/ha)",
]

CATEGORICAL_FEATURES = [
    "Location",
    "Crop Type",
    "Season",
]

MODEL_FEATURES = [
    "Location",
    "Crop Type",
    "Season",
    "Rainfall (mm)",
    "Temperature (°C)",
    "Soil pH",
    "Nitrogen (kg/ha)",
    "Phosphorus (kg/ha)",
    "Potassium (kg/ha)",
    "Total_NPK",
    "N_Ratio",
    "Heat_Water_Stress",
]


class MLServiceError(Exception):
    """Base exception for ML service failures."""


class ModelNotFoundError(MLServiceError):
    """Raised when the production model cannot be located."""


class ModelPredictionError(MLServiceError):
    """Raised when model prediction fails."""


class MLService:
    """
    Central service responsible for loading the trained AgriPredict model,
    preparing inference data, generating predictions, and producing SHAP
    explanations.

    The serialized model is expected to contain:
        - preprocessor
        - regressor

    The preprocessing pipeline remains inside the serialized model.
    """

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = self._resolve_model_path(model_path)
        self.model: Any | None = None
        self._load_model()

    @staticmethod
    def _resolve_model_path(model_path: str | None) -> Path:
        """
        Resolve the model location.

        Priority:
        1. Explicit MODEL_PATH argument
        2. MODEL_PATH environment variable
        3. Repository ml/models directory
        4. backend/app/models directory
        """

        candidates: list[Path] = []

        if model_path:
            candidates.append(Path(model_path))

        environment_path = os.getenv("MODEL_PATH")
        if environment_path:
            candidates.append(Path(environment_path))

        # ml/models/ from repository root.
        repository_root = Path(__file__).resolve().parents[3]
        candidates.append(
            repository_root / "ml" / "models" / MODEL_FILENAME
        )

        # Optional local model location.
        candidates.append(
            Path(__file__).resolve().parent.parent
            / "models"
            / MODEL_FILENAME
        )

        for candidate in candidates:
            resolved = candidate.expanduser().resolve()
            if resolved.is_file():
                return resolved

        searched_paths = "\n".join(
            f"  - {candidate.expanduser().resolve()}"
            for candidate in candidates
        )

        raise ModelNotFoundError(
            f"Could not locate {MODEL_FILENAME}.\n"
            f"Searched:\n{searched_paths}"
        )

    def _load_model(self) -> None:
        """Load the serialized production model into memory."""

        try:
            self.model = joblib.load(self.model_path)
        except Exception as exc:
            raise MLServiceError(
                f"Failed to load model from "
                f"{self.model_path}: {exc}"
            ) from exc

        if not hasattr(self.model, "predict"):
            raise MLServiceError(
                "Loaded model does not expose a predict() method."
            )

        if not hasattr(self.model, "named_steps"):
            raise MLServiceError(
                "Loaded model is expected to be a scikit-learn "
                "Pipeline with named_steps."
            )

        required_steps = {"preprocessor", "regressor"}
        available_steps = set(self.model.named_steps.keys())

        missing_steps = required_steps - available_steps

        if missing_steps:
            raise MLServiceError(
                "Production model is missing required pipeline "
                f"steps: {sorted(missing_steps)}"
            )

    @property
    def is_loaded(self) -> bool:
        """Return whether the model is currently loaded."""

        return self.model is not None

    @property
    def model_type(self) -> str | None:
        """Return the actual estimator class used by the artifact."""

        if self.model is None:
            return None

        regressor = self.model.named_steps.get("regressor")

        if regressor is None:
            return None

        return type(regressor).__name__

    def build_dataframe(self, input_data: dict) -> pd.DataFrame:
        """
        Convert API input into the exact feature structure expected
        by the production ML pipeline.

        The three biological features below MUST match the formulas
        used during model training.
        """

        nitrogen = float(input_data["nitrogen_kgha"])
        phosphorus = float(input_data["phosphorus_kgha"])
        potassium = float(input_data["potassium_kgha"])
        rainfall = float(input_data["rainfall_mm"])
        temperature = float(input_data["temperature_c"])

        # ---------------------------------------------------------
        # Biological feature engineering
        # MUST match ml/training/train_model.py
        # ---------------------------------------------------------

        total_npk = nitrogen + phosphorus + potassium

        n_ratio = nitrogen / (total_npk + 1)

        heat_water_stress = temperature / (rainfall + 1)

        row = {
            "Location": input_data["location"],
            "Crop Type": input_data["crop_type"],
            "Season": input_data["season"],
            "Rainfall (mm)": rainfall,
            "Temperature (°C)": temperature,
            "Soil pH": float(input_data["soil_ph"]),
            "Nitrogen (kg/ha)": nitrogen,
            "Phosphorus (kg/ha)": phosphorus,
            "Potassium (kg/ha)": potassium,
            "Total_NPK": total_npk,
            "N_Ratio": n_ratio,
            "Heat_Water_Stress": heat_water_stress,
        }

        return pd.DataFrame(
            [row],
            columns=MODEL_FEATURES,
        )

    def predict(self, input_data: dict[str, Any]) -> float:
        """
        Generate a yield prediction in tonnes/hectare.
        """

        if self.model is None:
            raise MLServiceError("ML model is not loaded.")

        df_sample = self.build_dataframe(input_data)

        try:
            prediction = self.model.predict(df_sample)[0]
        except Exception as exc:
            raise ModelPredictionError(
                f"Model prediction failed: {exc}"
            ) from exc

        return float(prediction)

    def explain(
        self,
        input_data: dict[str, Any],
        top_n: int = 8,
    ) -> list[dict[str, Any]]:
        """
        Generate SHAP-based feature explanations.

        Numeric features are preserved directly.

        One-hot encoded categorical features are grouped back into
        their original categorical feature names so the frontend
        does not have to understand the internal encoding.
        """

        if self.model is None:
            raise MLServiceError("ML model is not loaded.")

        df_sample = self.build_dataframe(input_data)

        try:
            preprocessor = self.model.named_steps["preprocessor"]
            regressor = self.model.named_steps["regressor"]

            transformed_data = preprocessor.transform(df_sample)

            explainer = shap.TreeExplainer(regressor)
            shap_values = explainer.shap_values(transformed_data)

            # SHAP can return:
            #   array shape (samples, features)
            # or, depending on model/version,
            #   a list of arrays.
            if isinstance(shap_values, list):
                shap_array = shap_values[0]
            else:
                shap_array = shap_values

            shap_row = shap_array[0]

            feature_names = self._get_transformed_feature_names(
                preprocessor
            )

            if len(feature_names) != len(shap_row):
                raise MLServiceError(
                    "SHAP feature count does not match transformed "
                    "model feature count."
                )

            raw_impacts = [
                (feature_name, float(shap_value))
                for feature_name, shap_value, actual_value in zip(
                    feature_names,
                    shap_row,
                    transformed_data[0],
                )
                if not (
                    feature_name.startswith("cat__")
                    and actual_value == 0.0
                )
            ]

            grouped_impacts = self._group_shap_impacts(
                raw_impacts
            )

            grouped_impacts.sort(
                key=lambda item: abs(item["impact_value"]),
                reverse=True,
            )

            return grouped_impacts[:top_n]

        except MLServiceError:
            raise

        except Exception as exc:
            raise MLServiceError(
                f"SHAP explanation failed: {exc}"
            ) from exc

    @staticmethod
    def _get_transformed_feature_names(
        preprocessor: Any,
    ) -> list[str]:
        """
        Recover the exact feature names produced by the fitted
        ColumnTransformer.

        The fitted preprocessor is the single source of truth.
        """

        return list(
            preprocessor.get_feature_names_out()
        )

    @staticmethod
    def _group_shap_impacts(
        raw_impacts: list[tuple[str, float]],
    ) -> list[dict[str, Any]]:
        """
        Convert OneHotEncoder feature names into clean frontend
        feature groups.

        Example:

            Crop Type_Sugarcane
            Crop Type_Wheat
            Crop Type_Potato

        become one aggregated:

            Crop Type
        """

        grouped: dict[str, float] = {}

        for feature_name, impact in raw_impacts:
            clean_name = MLService._clean_feature_name(
                feature_name
            )

            grouped[clean_name] = (
                grouped.get(clean_name, 0.0)
                + float(impact)
            )

        result: list[dict[str, Any]] = []

        for feature, impact in grouped.items():
            impact_value = float(impact)

            direction = (
                "POSITIVE"
                if impact_value >= 0
                else "NEGATIVE"
            )

            absolute_impact = abs(impact_value)

            if direction == "POSITIVE":
                description = (
                    f"Increased expected yield by "
                    f"approximately {absolute_impact:.2f} "
                    f"tonnes/ha according to the model."
                )
            else:
                description = (
                    f"Decreased expected yield by "
                    f"approximately {absolute_impact:.2f} "
                    f"tonnes/ha according to the model."
                )

            result.append(
                {
                    "feature": feature,
                    "impact_value": impact_value,
                    "direction": direction,
                    "description": description,
                }
            )

        return result

    @staticmethod
    def _clean_feature_name(feature_name: str) -> str:
        """Map transformed model features to UI-friendly names."""

        for categorical_feature in CATEGORICAL_FEATURES:
            prefix = f"cat__{categorical_feature}_"

            if feature_name.startswith(prefix):
                return categorical_feature

        mapping = {
            "num__Rainfall (mm)": "Rainfall",
            "num__Temperature (°C)": "Temperature",
            "num__Soil pH": "Soil pH",
            "num__Nitrogen (kg/ha)": "Soil Nitrogen",
            "num__Phosphorus (kg/ha)": "Soil Phosphorus",
            "num__Potassium (kg/ha)": "Soil Potassium",
            "num__Total_NPK": "Total NPK",
            "num__N_Ratio": "N Ratio",
            "num__Heat_Water_Stress": "Heat Water Stress",
        }

        return mapping.get(
            feature_name,
            feature_name,
        )


# One shared service instance.
#
# Loading the model once prevents us from repeatedly loading the
# 4 MB artifact for every HTTP request.
ml_service = MLService()