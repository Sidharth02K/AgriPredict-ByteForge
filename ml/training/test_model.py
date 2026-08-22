import joblib
import pandas as pd
import shap
import os

def test_agripredict_model(model_path):
    print("Loading saved model...")
    # 1. Load the trained production model pipeline using the absolute path
    if not os.path.exists(model_path):
        print(f"❌ Error: Could not find model at {model_path}")
        print("Did you run train_model.py first?")
        return

    model = joblib.load(model_path)

    # 2. Define a sample farm input
    sample_input = {
        'Location': 'Rajasthan',
        'Crop Type': 'Wheat',
        'Season': 'Rabi',
        'Rainfall (mm)': 300.0,
        'Temperature (°C)': 37.0,
        'Soil pH': 6.8,
        'Nitrogen (kg/ha)': 1995.0,
        'Phosphorus (kg/ha)': 9000.0,
        'Potassium (kg/ha)': 105.0
    }

    # Convert to DataFrame
    df_sample = pd.DataFrame([sample_input])

    print("\n--- Running Prediction ---")
    # 3. Make the yield prediction
    predicted_yield = model.predict(df_sample)[0]
    print(f"🌾 Predicted Yield: {predicted_yield:.2f} tonnes/hectare")

    # 4. Simple Rule-Based Risk Assessment
    risk_level = "LOW"
    reasons = []
    if sample_input['Rainfall (mm)'] < 400:
        risk_level = "MEDIUM"
        reasons.append("Rainfall is below optimal range.")
    if sample_input['Nitrogen (kg/ha)'] < 60:
        risk_level = "HIGH" if risk_level == "MEDIUM" else "MEDIUM"
        reasons.append("Soil nitrogen is low.")
    
    if not reasons:
        reasons.append("Conditions are favorable.")

    print(f"⚠️ Risk Level: {risk_level}")
    for reason in reasons:
        print(f"   - {reason}")

    # 5. Extract SHAP Explainability
    try:
        preprocessor = model.named_steps['preprocessor']
        regressor = model.named_steps['regressor']
        
        transformed_data = preprocessor.transform(df_sample)
        
        explainer = shap.TreeExplainer(regressor)
        shap_values = explainer.shap_values(transformed_data)[0]
        
        numeric_features = [
            'Rainfall (mm)', 'Temperature (°C)', 'Soil pH',
            'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)'
        ]
        cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
        categorical_features = ['Location', 'Crop Type', 'Season']
        encoded_cat_names = list(cat_encoder.get_feature_names_out(categorical_features))
        all_feature_names = numeric_features + encoded_cat_names
        
        impacts = sorted(zip(all_feature_names, shap_values), key=lambda x: abs(x[1]), reverse=True)
        
        print("\n🔍 Key Influencing Factors (SHAP Explanation):")
        for feat, val in impacts[:3]:
            direction = "increased" if val > 0 else "decreased"
            print(f"   - {feat}: {direction} yield by {abs(val):.2f} tonnes/ha")
            
    except Exception as e:
        print(f"\n(SHAP explanation skipped for this run: {e})")

if __name__ == "__main__":
    # Get the exact folder where this test_model.py script lives
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build the absolute path to the models folder
    MODEL_FILE = os.path.join(script_dir, "../models/agripredict_production_model.pkl")
    
    test_agripredict_model(MODEL_FILE)