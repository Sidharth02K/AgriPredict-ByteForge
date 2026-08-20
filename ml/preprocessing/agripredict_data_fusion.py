import pandas as pd
import numpy as np

def build_agripredict_dataset():
    print("--- AgriPredict Data Fusion Pipeline ---")
    
    # ==========================================
    # 1. LOAD THE DATASETS
    # ==========================================
    print("Loading raw CSV files...")
    df_yield = pd.read_csv('crop_yield.csv.csv')
    df_weather = pd.read_csv('state_weather_data_1997_2020.csv.csv')
    df_sensor = pd.read_csv('sensor_Crop_Dataset (1).csv')

    # ==========================================
    # 2. STANDARDIZE TEXT FOR MERGING
    # ==========================================
    # Convert state names to lowercase/strip to ensure weather and yield states match perfectly
    df_yield['state_clean'] = df_yield['state'].astype(str).str.lower().str.strip()
    df_weather['state_clean'] = df_weather['state'].astype(str).str.lower().str.strip()
    
    # Convert crop names to lowercase/strip to ensure soil and yield crops match perfectly
    df_yield['crop_clean'] = df_yield['crop'].astype(str).str.lower().str.strip()
    df_sensor['crop_clean'] = df_sensor['Crop'].astype(str).str.lower().str.strip()

    # ==========================================
    # 3. MERGE 1: YIELD + WEATHER
    # ==========================================
    print("Merging Yield Data with Historical Weather Data...")
    # Join on both State and Year so every crop gets the correct weather for that specific season
    merged_df = pd.merge(df_yield, df_weather, left_on=['state_clean', 'year'], right_on=['state_clean', 'year'], how='inner')

    # ==========================================
    # 4. CREATE SOIL PROFILES FROM SENSOR DATA
    # ==========================================
    print("Calculating baseline NPK & pH profiles from Sensor Dataset...")
    # Group the sensor data by crop to find the average required soil nutrients
    soil_profiles = df_sensor.groupby('crop_clean').agg({
        'Nitrogen': 'mean',
        'Phosphorus': 'mean',
        'Potassium': 'mean',
        'pH_Value': 'mean'
    }).reset_index()

    # ==========================================
    # 5. MERGE 2: (YIELD + WEATHER) + SOIL PROFILES
    # ==========================================
    print("Fusing agronomic soil data...")
    # Inner join ensures we only keep rows where we have BOTH weather and soil data
    final_df = pd.merge(merged_df, soil_profiles, on='crop_clean', how='inner')

    # ==========================================
    # 6. INJECT REALISTIC SOIL VARIANCE
    # ==========================================
    print("Injecting statistical variance into soil parameters...")
    # Soil is not identical across a whole state. We add a +/- 15% random variance.
    def add_variance(value, variance_pct=0.15):
        multiplier = np.random.uniform(1 - variance_pct, 1 + variance_pct)
        return round(value * multiplier, 2)

    final_df['Nitrogen (kg/ha)'] = final_df['Nitrogen'].apply(add_variance)
    final_df['Phosphorus (kg/ha)'] = final_df['Phosphorus'].apply(add_variance)
    final_df['Potassium (kg/ha)'] = final_df['Potassium'].apply(add_variance)
    final_df['Soil pH'] = final_df['pH_Value'].apply(add_variance)

    # ==========================================
    # 7. CLEANUP & FORMAT FOR THE ML MODEL
    # ==========================================
    print("Finalizing features...")
    # Rename columns to strictly match the requirements of the AgriPredict ML model
    final_df.rename(columns={
        'state_x': 'Location',
        'crop': 'Crop Type',
        'season': 'Season',
        'total_rainfall_mm': 'Rainfall (mm)',
        'avg_temp_c': 'Temperature (°C)',
        'yield': 'Yield (tonnes/ha)'
    }, inplace=True)

    # Select only the features the ML model expects
    columns_to_keep = [
        'Location', 'Crop Type', 'Season', 
        'Rainfall (mm)', 'Temperature (°C)', 'Soil pH', 
        'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)', 
        'Yield (tonnes/ha)'
    ]
    
    agripredict_dataset = final_df[columns_to_keep]

    # Save the master dataset
    output_filename = 'agripredict_master_dataset.csv'
    agripredict_dataset.to_csv(output_filename, index=False)
    print(f"✅ Success! Master dataset created with {len(agripredict_dataset)} records.")
    print(f"Dataset saved as: {output_filename}")

if __name__ == "__main__":
    build_agripredict_dataset()