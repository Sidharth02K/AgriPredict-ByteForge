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
        
        # 🚨 ADDED: The new biological features are now expected by the model
        self.numeric_features = [
            'Rainfall (mm)', 'Temperature (°C)', 'Soil pH',
            'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)',
            'Total_NPK', 'N_Ratio', 'Heat_Water_Stress'
        ]
        self.categorical_features = ['Location', 'Crop Type', 'Season']
        self.target = 'Yield (tonnes/ha)'

    def add_biological_features(self, df):
        """Translates raw math into biological metrics for the AI to learn."""
        df = df.copy()
        
        # 1. Total Nutrient Availability
        df['Total_NPK'] = df['Nitrogen (kg/ha)'] + df['Phosphorus (kg/ha)'] + df['Potassium (kg/ha)']
        
        # 2. Nutrient Balance (Plants need a specific ratio)
        df['N_Ratio'] = df['Nitrogen (kg/ha)'] / (df['Total_NPK'] + 1) 
        
        # 3. Hydration Stress Index (High temp + low rain = severe stress)
        df['Heat_Water_Stress'] = df['Temperature (°C)'] / (df['Rainfall (mm)'] + 1)
        
        return df

    def load_data(self):
        """Loads, engineers, and validates the dataset."""
        print(f"Loading dataset from {self.dataset_path}...")
        df = pd.read_csv(self.dataset_path)
        df = df.dropna(subset=[self.target])
        
        # 🚨 APPLY BIOLOGICAL FEATURE ENGINEERING HERE
        df = self.add_biological_features(df)
        
        X = df[self.numeric_features + self.categorical_features]
        y = df[self.target]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def build_pipeline(self):
        """Builds a high-granularity preprocessing pipeline."""
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
        """Trains models with Biological Feature Engineering and Monotonic Constraints."""
        X_train, X_test, y_train, y_test = self.load_data()
        preprocessor = self.build_pipeline()

        # --- THE BIOLOGY ENFORCER ---
        X_train_transformed = preprocessor.fit_transform(X_train)
        total_features = X_train_transformed.shape[1]
        
        # 1 = MUST increase, -1 = MUST decrease, 0 = Unconstrained
        # Rainfall(1), Temp(0), pH(0), N(1), P(1), K(1), Total_NPK(1), N_Ratio(0), Stress(-1)
        num_categorical = total_features - 9
        biology_constraints = (1, 0, 0, 1, 1, 1, 1, 0, -1) + (0,) * num_categorical

        models = {
            "Baseline (Linear)": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42),
            "XGBoost": XGBRegressor(
                n_estimators=250, 
                learning_rate=0.05, 
                max_depth=9,
                monotone_constraints=biology_constraints,  
                random_state=42
            )
        }

        best_score = -float('inf')
        best_model_name = ""

        print("\n--- Training High-Accuracy Biological Models ---")
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
        print(f"💾 Biologically-anchored model safely saved to {self.model_output_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # THE FIX: Tell the script to go "up" one folder, then into the data/models folders
    DATASET_FILE = os.path.join(script_dir, "../data/agripredict_master_dataset.csv")
    MODEL_FILE = os.path.join(script_dir, "../models/agripredict_production_model.pkl")
    
    if not os.path.exists(DATASET_FILE):
        print(f"❌ Error: Could not find dataset at {DATASET_FILE}")
    else:
        trainer = AgriPredictTrainer(DATASET_FILE, MODEL_FILE)
        trainer.train_and_evaluate()