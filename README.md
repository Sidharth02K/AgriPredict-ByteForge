# 🌾 AgriPredict

### Predict. Understand. Plan. Grow.

AgriPredict is an AI-powered agricultural decision-support platform built by **Team ByteForge** for **Prasunethon 2.0**.

The platform combines agricultural inputs, a trained machine-learning model, risk assessment, explainability, recommendations, historical prediction storage, and analytics into a production-deployed web application.

---

## 🚀 Live Demo

**Web Application:**  
https://agri-predict-byte-forge.vercel.app

**Backend API:**  
https://agripredict-byteforge.onrender.com

**Interactive API Documentation:**  
https://agripredict-byteforge.onrender.com/docs

> The live frontend is the primary judge-facing entry point. The backend and database are deployed separately and communicate over HTTPS.

---

## 🎯 Problem

Agricultural decisions are influenced by multiple interacting factors such as crop choice, location, season, rainfall, temperature, and soil conditions.

Farmers and agricultural decision-makers need a practical way to turn these inputs into understandable forecasts and actions rather than relying only on raw historical information.

---

## 💡 Solution

AgriPredict provides a single workflow:

```text
Agricultural Inputs
        ↓
React Frontend
        ↓
FastAPI REST API
        ↓
ML Inference
        ↓
Yield Forecast
        ↓
Risk Assessment + Explainability
        ↓
Actionable Recommendations
        ↓
PostgreSQL Prediction History
        ↓
Analytics Dashboard
```

---

## ✨ Key Features

### 🌱 Crop Yield Prediction
Users provide:

- Location/state
- Crop type
- Season
- Rainfall
- Temperature
- Soil pH
- Nitrogen
- Phosphorus
- Potassium
- Farm area

The backend validates the request and returns an expected yield forecast.

### ⚠️ Risk Assessment
The prediction response includes a risk level:

- `LOW`
- `MEDIUM`
- `HIGH`

Risk factors are returned when the model/input conditions indicate important constraints.

### 🔍 Explainability
The backend returns model-derived key drivers with:

- Feature name
- Impact value
- Direction
- Human-readable explanation

This helps users understand which factors influenced the forecast.

### 💡 Actionable Recommendations
AgriPredict converts the prediction/risk result into practical recommendations for monitoring and decision support.

### 📚 Prediction History
Predictions are persisted in PostgreSQL and can be retrieved through the history API.

### 📊 Analytics
The analytics API provides summary information such as:

- Total prediction queries
- Average forecasted yield
- Risk distribution
- Top crops evaluated

---

## 🧠 Machine Learning

The deployed backend loads the trained production ML artifact and performs inference through the backend ML service.

The currently deployed application reports:

```text
Model: RandomForestRegressor
```

The backend is responsible for consuming the trained artifact rather than retraining the model for every request.

The prediction pipeline is integrated with the application's risk, explainability, and recommendation services.

---

## 🏗️ System Architecture

```text
┌──────────────────────────────┐
│          User / Judge        │
└──────────────┬───────────────┘
               │ HTTPS
               ▼
┌──────────────────────────────┐
│      Vercel React Frontend   │
│                              │
│  Prediction UI               │
│  History                     │
│  Analytics                   │
└──────────────┬───────────────┘
               │ REST / JSON
               ▼
┌──────────────────────────────┐
│      Render FastAPI API      │
│                              │
│  /api/v1/predict             │
│  /api/v1/history             │
│  /api/v1/analytics/summary   │
│  /health                     │
└───────┬─────────┬────────────┘
        │         │
        │         └─────────────────┐
        ▼                           ▼
┌───────────────────┐     ┌────────────────────┐
│ ML / Decision     │     │ Supabase PostgreSQL│
│ Services          │     │                    │
│                   │     │ Prediction records │
│ Yield prediction  │     │ History            │
│ Risk assessment   │     │ Analytics source   │
│ Explainability    │     │                    │
│ Recommendations   │     └────────────────────┘
└───────────────────┘
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for more detail.

---

## 🧩 Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Recharts
- Lucide React

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy

### Machine Learning

- Python
- NumPy
- Pandas
- Scikit-learn
- XGBoost
- Joblib
- SHAP

### Database

- PostgreSQL
- Supabase

### Deployment

- Vercel — frontend
- Render — backend API
- Supabase — PostgreSQL database

---

## 📁 Project Structure

```text
AgriPredict-ByteForge/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── ml/
│   ├── data/
│   ├── models/
│   ├── preprocessing/
│   ├── training/
│   └── test_model.py
│
└── docs/
    └── ARCHITECTURE.md
```

---

## 🔌 API Overview

### Health

```http
GET /health
```

Example:

```json
{
  "status": "healthy",
  "service": "AgriPredict Backend",
  "model_loaded": true,
  "model_type": "RandomForestRegressor"
}
```

### Prediction

```http
POST /api/v1/predict
```

Request fields include:

```json
{
  "location": "Gujarat",
  "crop_type": "Wheat",
  "season": "Rabi",
  "rainfall_mm": 800,
  "temperature_c": 24,
  "soil_ph": 6.8,
  "nitrogen_kgha": 75,
  "phosphorus_kgha": 40,
  "potassium_kgha": 35,
  "farm_area_ha": 1
}
```

The response includes the prediction ID, expected yield, total production, risk level, risk factors, key drivers, recommendations, and creation timestamp.

### History

```http
GET /api/v1/history?page=1&page_size=10
```

### Single Prediction History

```http
GET /api/v1/history/{prediction_id}
```

### Analytics

```http
GET /api/v1/analytics/summary
```

For complete request/response schemas, use the live Swagger documentation:

https://agripredict-byteforge.onrender.com/docs

---

## 🛠️ Local Development

### Backend

```bash
cd backend

python -m venv .venv
```

Activate the environment on Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create `backend/.env` with the PostgreSQL connection string:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/postgres
```

Run the API:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

For local development, the frontend can use:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

For production, the deployed frontend uses:

```env
VITE_API_BASE_URL=https://agripredict-byteforge.onrender.com
```

Do not commit `.env` or `.env.local` files containing credentials.

---

## 🔐 Configuration

Environment-specific configuration is kept outside source control.

Important variables include:

```text
DATABASE_URL
VITE_API_BASE_URL
```

Secrets such as database passwords must never be committed to GitHub.

---

## 🧪 Production Verification

The production system has been verified through:

- Backend `/health` check
- Production prediction request
- Production history request
- Production analytics request
- PostgreSQL persistence
- ML model loading
- Frontend-to-backend HTTPS communication
- CORS configuration
- Cross-device testing from another laptop

The final public frontend was tested without relying on a locally running backend.

---

## 👥 Team ByteForge

- **Anshul Dixit** — AI/ML & Data
- **Sidharth Kumar** — Backend
- **Shivam Gupta** — Frontend

Built for **Prasunethon 2.0**.

---

## 🔮 Future Scope

Potential extensions include:

- Weather API integration for live forecasts
- Satellite/remote-sensing data
- More regional and crop-specific training data
- Time-series crop forecasting
- IoT soil sensor integration
- Multilingual farmer assistance
- Mobile/PWA support
- Better model calibration and validation
- Automated alerts for high-risk conditions

---

## ⚠️ Disclaimer

AgriPredict is a decision-support prototype intended for demonstration and experimentation. Predictions should not be treated as a substitute for professional agronomic advice or field-specific measurements.
