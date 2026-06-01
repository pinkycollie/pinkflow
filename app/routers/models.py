from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.models import ModelCreate, ModelResponse
from app.services.firebase import firebase_service
from app.middleware.deafauth import verify_deafauth_token
from app.middleware.fibronrose import log_to_fibronrose
from datetime import datetime

router = APIRouter(prefix="/models", tags=["models"])

@router.get("", response_model=dict)
async def list_models(
    status: Optional[str] = Query("all"),
    task: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50),
    user: dict = Depends(verify_deafauth_token)
):
    """List all models with filters"""
    filters = {}
    if status != "all":
        filters["status"] = status
    if task:
        filters["task"] = task
    
    models = firebase_service.get_models(filters)
    
    # Client-side search
    if search:
        models = [m for m in models if search.lower() in m["name"].lower()]
    
    return {
        "models": models[:limit],
        "total": len(models),
        "page": {
            "limit": limit,
            "offset": 0,
            "has_next": len(models) > limit
        }
    }

@router.post("", response_model=ModelResponse, status_code=201)
async def create_model(
    model: ModelCreate,
    user: dict = Depends(verify_deafauth_token)
):
    """Add new model to testing queue"""
    model_data = {
        **model.dict(),
        "status": "queued",
        "accuracy": None,
        "fps": None,
        "deaf_score": None,
        "created_at": datetime.utcnow(),
        "tested_at": None,
        "created_by": user["uid"]
    }
    
    model_id = firebase_service.add_model(model_data)
    
    await log_to_fibronrose("model_added", {
        "model_id": model_id,
        "name": model.name,
        "user": user["uid"]
    })
    
    return {"id": model_id, **model_data}

@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: str,
    user: dict = Depends(verify_deafauth_token)
):
    """Get model details"""
    model = firebase_service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
