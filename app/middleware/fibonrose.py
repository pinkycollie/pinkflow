import httpx
from datetime import datetime
from app.config import settings

async def log_to_fibronrose(event: str, data: dict) -> dict:
    """Log event to Fibronrose for trust validation"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.FIBRONROSE_URL}/log",
                json={
                    "event": event,
                    "data": data,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "pinkflow"
                },
                headers={
                    "Authorization": f"Bearer {settings.FIBRONROSE_API_KEY}"
                },
                timeout=10.0
            )
            return response.json()
    except Exception as e:
        print(f"Fibronrose logging failed: {e}")
        return {}

async def calculate_trust_score(model_id: str, test_results: dict) -> dict:
    """Calculate and log trust score to Fibronrose"""
    base_score = (
        test_results.get("accuracy", 0) * 0.4 +
        test_results.get("deaf_score", 0) * 0.6
    )
    
    blockchain_result = await log_to_fibronrose("trust_score", {
        "model_id": model_id,
        "score": base_score,
        "metrics": test_results
    })
    
    return {
        "trust_score": base_score,
        "blockchain_hash": blockchain_result.get("hash"),
        "reputation_impact": "positive" if base_score >= 90 else "neutral" if base_score >= 70 else "negative"
    }
