import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class AgriPredictTrainer:
    def __init__(self, dataset_path, model_output_path):
        self.dataset_path = dataset_path
        self.model_output_path = model_output_path
        self.pipeline = None
        
        # Define exact features based on the fusion script output
        self.numeric_features = [
            'Rainfall (mm)', 'Temperature (°C)', 'Soil pH',
            'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)'
        ]
        self.categorical_features = ['Location', 'Crop Type', 'Season']
        self.target = 'Yield (tonnes/ha)'

    def load_data(self):
        """Loads and validates the dataset."""
        print(f"Loading dataset from {self.dataset_path}...")
        df = pd.read_csv(self.dataset_path)
        
        # Drop rows where the target yield is missing
        df = df.dropna(subset=[self.target])
        
        X = df[self.numeric_features + self.categorical_features]
        y = df[self.target]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def build_pipeline(self):
        """Builds a robust, dynamic preprocessing pipeline."""
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)
            ])
        
        return preprocessor

    def train_and_evaluate(self):
        """Trains multiple models and selects the best one."""
        X_train, X_test, y_train, y_test = self.load_data()
        preprocessor = self.build_pipeline()

        models = {
            "Baseline (Linear)": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
            "XGBoost": XGBRegressor(n_estimators=150, learning_rate=0.1, max_depth=6, random_state=42)
        }

        best_score = -float('inf')
        best_model_name = ""

        print("\n--- Training Models ---")
        for name, regressor in models.items():
            pipe = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', regressor)])
            pipe.fit(X_train, y_train)
            
            preds = pipe.predict(X_test)
            r2 = r2_score(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mae = mean_absolute_error(y_test, preds)
            
            print(f"{name}:")
            print(f"  -> R² Score: {r2:.4f} | RMSE: {rmse:.4f} | MAE: {mae:.4f}")

            if r2 > best_score:
                best_score = r2
                self.pipeline = pipe
                best_model_name = name

        print(f"\n✅ Selected Best Model: {best_model_name} with an R² of {best_score:.4f}")
        
        os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
        joblib.dump(self.pipeline, self.model_output_path)
        print(f"💾 Model successfully saved to {self.model_output_path}")

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build the absolute paths to the data and models folders
    DATASET_FILE = os.path.join(script_dir, "../data/agripredict_master_dataset.csv")
    MODEL_FILE = os.path.join(script_dir, "../models/agripredict_production_model.pkl")
    
    if not os.path.exists(DATASET_FILE):
        print(f"❌ Error: Could not find dataset at {DATASET_FILE}")
        print("Please make sure your dataset is in the ml/data/ folder!")
    else:
        trainer = AgriPredictTrainer(DATASET_FILE, MODEL_FILE)
        trainer.train_and_evaluate()