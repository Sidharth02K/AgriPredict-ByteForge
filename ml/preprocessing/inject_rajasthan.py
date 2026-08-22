import pandas as pd
import numpy as np
import os

def generate_rajasthan_data():
    # 1. Define exact columns to match the master dataset
    columns = [
        'Location', 'Crop Type', 'Season', 'Rainfall (mm)', 
        'Temperature (°C)', 'Soil pH', 'Nitrogen (kg/ha)', 
        'Phosphorus (kg/ha)', 'Potassium (kg/ha)', 'Yield (tonnes/ha)'
    ]
    
    # 2. Define realistic agronomic parameters for Rajasthan (semi-arid)
    crop_profiles = [
        {'crop': 'wheat', 'season': 'Rabi', 'rain': 350, 'temp': 22, 'ph': 7.8, 'N': 85, 'P': 45, 'K': 35, 'yield': 3.2},
        {'crop': 'maize', 'season': 'Kharif', 'rain': 450, 'temp': 28, 'ph': 7.6, 'N': 100, 'P': 40, 'K': 30, 'yield': 2.1},
        {'crop': 'rice', 'season': 'Kharif', 'rain': 600, 'temp': 30, 'ph': 7.5, 'N': 110, 'P': 50, 'K': 40, 'yield': 2.8},
        {'crop': 'sugarcane', 'season': 'Kharif', 'rain': 650, 'temp': 32, 'ph': 7.7, 'N': 140, 'P': 60, 'K': 50, 'yield': 55.0},
        {'crop': 'potato', 'season': 'Rabi', 'rain': 300, 'temp': 18, 'ph': 7.4, 'N': 120, 'P': 55, 'K': 45, 'yield': 18.5},
    ]

    new_rows = []
    
    # 3. Generate 100 variations per crop using statistical variance
    print("🚜 Generating synthetic data for Rajasthan...")
    for profile in crop_profiles:
        for _ in range(100):
            row = {
                'Location': 'Rajasthan',
                'Crop Type': profile['crop'],
                'Season': profile['season'],
                'Rainfall (mm)': round(np.random.normal(profile['rain'], profile['rain'] * 0.15), 1),
                'Temperature (°C)': round(np.random.normal(profile['temp'], 2.0), 1),
                'Soil pH': round(np.random.normal(profile['ph'], 0.3), 1),
                'Nitrogen (kg/ha)': round(np.random.normal(profile['N'], profile['N'] * 0.1), 1),
                'Phosphorus (kg/ha)': round(np.random.normal(profile['P'], profile['P'] * 0.1), 1),
                'Potassium (kg/ha)': round(np.random.normal(profile['K'], profile['K'] * 0.1), 1),
                'Yield (tonnes/ha)': round(np.random.normal(profile['yield'], profile['yield'] * 0.12), 2)
            }
            new_rows.append(row)

    df_rajasthan = pd.DataFrame(new_rows, columns=columns)
    
    # 4. Load master dataset, append, and save
    script_dir = os.path.dirname(os.path.abspath(__file__))
    master_path = os.path.join(script_dir, "../data/agripredict_master_dataset.csv")
    
    if os.path.exists(master_path):
        df_master = pd.read_csv(master_path)
        df_combined = pd.concat([df_master, df_rajasthan], ignore_index=True)
        df_combined.to_csv(master_path, index=False)
        print(f"✅ Successfully injected {len(df_rajasthan)} Rajasthan records into master dataset!")
    else:
        print(f"❌ Error: Could not find {master_path}")

if __name__ == "__main__":
    generate_rajasthan_data()