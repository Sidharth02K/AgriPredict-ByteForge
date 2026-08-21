from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import unhandled_exception_handler
from app.database.session import Base, engine
from app.models.prediction_model import PredictionRecord
from app.routes.predict_routes import router as predict_router
from app.routes.history_routes import router as history_router
from app.routes.analytics_routes import router as analytics_router
from app.services.ml_service import ml_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.

    Startup:
    - Creates database tables if they do not exist.
    - Verifies that the ML service is loaded.

    Shutdown:
    - FastAPI handles application cleanup.
    """

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Verify ML model
    if not ml_service.is_loaded:
        print("WARNING: Production ML model is not loaded.")
    else:
        print(
            f"AgriPredict ML model loaded: "
            f"{ml_service.model_type}"
        )

    yield


app = FastAPI(
    title="AgriPredict API",
    description=(
        "AI-powered crop yield forecasting, "
        "risk assessment, and agricultural decision support."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

app.include_router(predict_router)
app.include_router(history_router)
app.include_router(analytics_router)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health", tags=["System"])
def health_check():
    """
    Basic backend and ML model health check.
    """

    return {
        "status": "healthy",
        "service": "AgriPredict Backend",
        "model_loaded": ml_service.is_loaded,
        "model_type": ml_service.model_type,
    }


@app.get("/", tags=["System"])
def root():
    return {
        "message": "AgriPredict API is running",
        "docs": "/docs",
        "health": "/health",
    }