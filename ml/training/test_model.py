import joblib
import pandas as pd
import shap
import os

def test_agripredict_model(model_path):
    print(f"Loading saved model from: {model_path}")
    if not os.path.exists(model_path):
        print(f"❌ Error: Could not find model at {model_path}")
        return

    model = joblib.load(model_path)

    # 1. SAMPLE INPUTS (Testing abnormal toxic NPK)
    sample_input = {
        'Location': 'Rajasthan',
        'Crop Type': 'Wheat',
        'Season': 'Rabi',
        'Rainfall (mm)': 550.0,
        'Temperature (°C)': 25.0,
        'Soil pH': 7.0,
        'Nitrogen (kg/ha)': 70.0,   # ABNORMAL: Toxically high
        'Phosphorus (kg/ha)': 600.0,
        'Potassium (kg/ha)': 750.0
    }

    # 2. STRICT INPUT VALIDATION (The Guardrails)
    VALIDATION_LIMITS = {
        'Rainfall (mm)': (0.0, 3000.0),
        'Temperature (°C)': (-5.0, 50.0),
        'Soil pH': (3.0, 10.0),
        'Nitrogen (kg/ha)': (0.0, 500.0),
        'Phosphorus (kg/ha)': (0.0, 250.0),
        'Potassium (kg/ha)': (0.0, 300.0)
    }

    errors = []
    for feature, (min_val, max_val) in VALIDATION_LIMITS.items():
        val = sample_input.get(feature)
        if val is not None and (val < min_val or val > max_val):
            errors.append(f"   - {feature}: {val} is physically impossible. Must be between {min_val} and {max_val}.")
            
    if errors:
        print("\n🚨 SYSTEM HALTED: INVALID DATA DETECTED 🚨")
        for error in errors:
            print(error)
        return

    # 3. BIOLOGICAL FEATURE ENGINEERING
    df_sample = pd.DataFrame([sample_input])
    df_sample['Total_NPK'] = df_sample['Nitrogen (kg/ha)'] + df_sample['Phosphorus (kg/ha)'] + df_sample['Potassium (kg/ha)']
    df_sample['N_Ratio'] = df_sample['Nitrogen (kg/ha)'] / (df_sample['Total_NPK'] + 1)
    df_sample['Heat_Water_Stress'] = df_sample['Temperature (°C)'] / (df_sample['Rainfall (mm)'] + 1)

    # 4. COMPREHENSIVE RISK LOGIC
    risk_level = "LOW"
    reasons = []
    
    # Weather
    rf = sample_input['Rainfall (mm)']
    if rf < 400:
        risk_level = "HIGH"
        reasons.append(f"Low Rainfall ({rf} mm): Severe drought stress risk.")
    elif rf > 1200:
        risk_level = "HIGH"
        reasons.append(f"Excess Rainfall ({rf} mm): High risk of waterlogging.")

    temp = sample_input['Temperature (°C)']
    if temp < 10.0:
        risk_level = "HIGH"
        reasons.append(f"Low Temp ({temp}°C): Frost risk stalling development.")
    elif temp > 35.0:
        risk_level = "HIGH"
        reasons.append(f"High Temp ({temp}°C): Heat stress impairing yield.")

    # Soil NPK
    n = sample_input['Nitrogen (kg/ha)']
    if n < 60:
        risk_level = "HIGH"
        reasons.append(f"Low Nitrogen ({n}): Stunted growth and yellowing.")
    elif n > 250:
        risk_level = "HIGH"
        reasons.append(f"High Nitrogen ({n}): Toxically high! Severe risk of crop burn.")

    p = sample_input['Phosphorus (kg/ha)']
    if p < 20:
        risk_level = "HIGH" if risk_level != "HIGH" else "HIGH"
        reasons.append(f"Low Phosphorus ({p}): Impaired root growth.")
    elif p > 80:
        risk_level = "MEDIUM" if risk_level == "LOW" else risk_level
        reasons.append(f"High Phosphorus ({p}): Inhibits micronutrient absorption.")

    k = sample_input['Potassium (kg/ha)']
    if k < 40:
        risk_level = "HIGH" if risk_level != "HIGH" else "HIGH"
        reasons.append(f"Low Potassium ({k}): Weak stems and disease vulnerability.")
    elif k > 150:
        risk_level = "MEDIUM" if risk_level == "LOW" else risk_level
        reasons.append(f"High Potassium ({k}): May trigger magnesium deficiencies.")

    ph = sample_input['Soil pH']
    if ph < 6.0:
        risk_level = "HIGH"
        reasons.append(f"Acidic Soil (pH {ph}): Nutrient availability locked.")
    elif ph > 7.5:
        risk_level = "HIGH"
        reasons.append(f"Alkaline Soil (pH {ph}): Risk of Iron deficiencies.")

    if not reasons:
        reasons.append("All metrics are within optimal agricultural ranges.")

    # 4.5 BIOLOGICAL YIELD PENALTY (The Fix!)
    raw_yield = model.predict(df_sample)[0]
    final_yield = raw_yield

    if risk_level == "HIGH":
        final_yield = raw_yield * 0.45  # 55% crop loss due to severe conditions
    elif risk_level == "MEDIUM":
        final_yield = raw_yield * 0.85  # 15% crop loss due to suboptimal conditions

    print("\n--- Running Prediction ---")
    print(f"🧠 AI Raw Math Prediction: {raw_yield:.2f} tonnes/hectare")
    
    if risk_level != "LOW":
        print(f"📉 Biological Penalty Applied (-{100 - int((final_yield/raw_yield)*100)}%): Adjusting for {risk_level} risk conditions.")
        
    print(f"🌾 FINAL ADJUSTED YIELD: {final_yield:.2f} tonnes/hectare")

    print(f"\n⚠️ Risk Level: {risk_level}")
    for reason in reasons:
        print(f"   - {reason}")

    # 5. SHAP EXPLAINABILITY
    try:
        preprocessor = model.named_steps['preprocessor']
        regressor = model.named_steps['regressor']
        
        transformed_data = preprocessor.transform(df_sample)
        explainer = shap.TreeExplainer(regressor)
        shap_values = explainer.shap_values(transformed_data)[0]
        
        numeric_features = [
            'Rainfall (mm)', 'Temperature (°C)', 'Soil pH',
            'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)',
            'Total_NPK', 'N_Ratio', 'Heat_Water_Stress'
        ]
        cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
        categorical_features = ['Location', 'Crop Type', 'Season']
        encoded_cat_names = list(cat_encoder.get_feature_names_out(categorical_features))
        all_feature_names = numeric_features + encoded_cat_names
        
        print("\n🔍 Key Influencing Factors (SHAP Explanation):")
        impacts = sorted(zip(all_feature_names, shap_values, transformed_data[0]), key=lambda x: abs(x[1]), reverse=True)
        
        shown_count = 0
        for feat, shap_val, actual_val in impacts:
            if "_" in feat and actual_val == 0.0:
                continue
            direction = "increased" if shap_val > 0 else "decreased"
            print(f"   - {feat}: {direction} yield by {abs(shap_val):.2f} tonnes/ha")
            shown_count += 1
            if shown_count >= 6: 
                break
    except Exception as e:
        print(f"\n(SHAP explanation skipped for this run: {e})")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # THE FIX: Point to the 'models' folder instead of the current 'training' folder
    MODEL_FILE = os.path.join(script_dir, "../models/agripredict_production_model.pkl")
    
    test_agripredict_model(MODEL_FILE)