from fastapi import APIRouter, Depends, HTTPException
from app.models import TestStart, TestStatusResponse
from app.services.test_runner import test_runner
from app.services.firebase import firebase_service
from app.middleware.deafauth import verify_deafauth_token
from datetime import datetime

router = APIRouter(prefix="/test", tags=["testing"])

@router.post("/start", status_code=202)
async def start_test(
    test: TestStart,
    user: dict = Depends(verify_deafauth_token)
):
    """Start model testing"""
    test_id = await test_runner.start_test(
        test.model_id,
        {
            "dataset": test.dataset,
            "compute_type": test.compute_type,
            "max_duration": test.max_duration
        }
    )
    
    firebase_service.update_model(test.model_id, {"status": "testing"})
    
    return {
        "test_id": test_id,
        "model_id": test.model_id,
        "status": "queued",
        "started_at": datetime.utcnow()
    }

@router.get("/{test_id}/status", response_model=TestStatusResponse)
async def get_test_status(
    test_id: str,
    user: dict = Depends(verify_deafauth_token)
):
    """Get test execution status"""
    test = firebase_service.get_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test
