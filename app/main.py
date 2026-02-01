from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import models, testing

app = FastAPI(
    title="PinkFlow API",
    description="Sign Language Model Testing & Validation",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pinkflow.mbtq.dev", "https://mbtq.dev", "https://vr4deaf.org", "https://pinksync.io", "https://360magicians.com", "https://mbtqproperties.com", "WWW.MBTQUNIVERSE.COM""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(models.router, prefix=settings.API_PREFIX)
app.include_router(testing.router, prefix=settings.API_PREFIX)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pinkflow"}

@app.get(f"{settings.API_PREFIX}/stats")
async def get_stats():
    """Platform statistics"""
    models = firebase_service.get_models()
    tested = [m for m in models if m["status"] == "tested"]
    
    return {
        "total_models": len(models),
        "tested_models": len(tested),
        "avg_accuracy": sum(m.get("accuracy", 0) for m in tested) / len(tested) if tested else 0,
        "avg_deaf_score": sum(m.get("deaf_score", 0) for m in tested) / len(tested) if tested else 0
    }
