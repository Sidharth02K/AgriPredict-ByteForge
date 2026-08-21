from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[AgriPredict] Backend starting...")
    yield
    print("[AgriPredict] Backend shutting down...")


app = FastAPI(
    title="AgriPredict API",
    description=(
        "AI-powered crop yield prediction and "
        "agricultural decision-support API."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "success": True,
        "status": "healthy",
        "service": "agripredict-backend",
    }


@app.get("/")
def root():
    return {
        "success": True,
        "message": "AgriPredict API is running.",
        "docs": "/docs",
    }