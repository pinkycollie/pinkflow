#!/usr/bin/env python3
"""
PinkFlow Web Application - FastAPI Backend
Provides REST API for accessibility tools and model testing

Features:
- Model testing endpoints
- Accessibility tool endpoints (captions, transcription, alerts)
- Health check and status
- CORS support for frontend
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import uuid

# Import PinkFlow testing modules
from .pinkflow import PinkFlowTester, ModelTestResult, ModelTestStatus
from .pinkflow_mcp import run_test_on_repo, batch_test_repos, MCPGitHubTester
from .pubsub_service import (
    get_pubsub_service, EventType, NotificationPriority, Event
)
from .voting_service import (
    get_voting_service, VoteType, VotableItemType
)

# Backwards compatibility aliases
TestResult = ModelTestResult
TestStatus = ModelTestStatus


# ============================================
# Pydantic Models
# ============================================

class ToolCategory(str, Enum):
    """Categories of accessibility tools"""
    MODEL_TESTING = "model_testing"
    CAPTIONS = "captions"
    TRANSCRIPTION = "transcription"
    VISUAL_ALERTS = "visual_alerts"
    VIDEO_RELAY = "video_relay"
    SIGN_RECOGNITION = "sign_recognition"
    TEXT_TO_SIGN = "text_to_sign"


class ToolStatus(str, Enum):
    """Status of an accessibility tool"""
    AVAILABLE = "available"
    BETA = "beta"
    COMING_SOON = "coming_soon"
    MAINTENANCE = "maintenance"


class AccessibilityTool(BaseModel):
    """Accessibility tool information"""
    id: str
    name: str
    description: str
    category: ToolCategory
    status: ToolStatus
    icon: str
    features: List[str]
    deaf_first_score: Optional[float] = Field(None, ge=0, le=100)


class ModelTestRequest(BaseModel):
    """Request to test a model"""
    repo_url: str
    test_type: Optional[str] = "auto"
    save_results: bool = True


class ModelTestResponse(BaseModel):
    """Response from model testing"""
    id: str
    repo_url: str
    status: str
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    processing_time: Optional[float] = None
    errors: List[str] = []
    metadata: Dict[str, Any] = {}
    created_at: datetime
    passed: bool


class BatchTestRequest(BaseModel):
    """Request to test multiple repos"""
    repo_urls: List[str]


class BatchTestResponse(BaseModel):
    """Response from batch testing"""
    batch_id: str
    total: int
    passed: int
    failed: int
    results: List[ModelTestResponse]
    created_at: datetime


class CaptionRequest(BaseModel):
    """Request for caption generation"""
    video_url: Optional[str] = None
    text: Optional[str] = None
    language: str = "en"
    format: str = "srt"


class CaptionResponse(BaseModel):
    """Response with generated captions"""
    id: str
    status: str
    captions: Optional[str] = None
    format: str
    created_at: datetime


class TranscriptionRequest(BaseModel):
    """Request for audio transcription"""
    audio_url: Optional[str] = None
    language: str = "en"
    include_timestamps: bool = True


class TranscriptionResponse(BaseModel):
    """Response with transcription"""
    id: str
    status: str
    text: Optional[str] = None
    segments: Optional[List[Dict[str, Any]]] = None
    created_at: datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]


class VoteRequest(BaseModel):
    """Request to cast a vote"""
    item_id: str
    item_type: str  # model_test, feedback, proposal, contribution
    vote_type: str  # upvote, downvote, approve, reject


class VoteResponse(BaseModel):
    """Response with vote summary"""
    item_id: str
    total_votes: int
    upvotes: int
    downvotes: int
    approvals: int
    rejections: int
    score: float


class SubscriptionRequest(BaseModel):
    """Request to subscribe to topics"""
    subscriber_id: str
    topics: List[str]
    iot_enabled: bool = False
    vibration_enabled: bool = False


class NotificationRequest(BaseModel):
    """Request to send a notification"""
    topic: str
    event_type: str
    data: Dict[str, Any]
    priority: str = "normal"


# ============================================
# FastAPI Application
# ============================================

app = FastAPI(
    title="PinkFlow API",
    description="Deaf-First Accessibility Tools and Model Testing API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (use database in production)
test_results_store: Dict[str, ModelTestResponse] = {}
batch_results_store: Dict[str, BatchTestResponse] = {}


# ============================================
# Accessibility Tools Data
# ============================================

ACCESSIBILITY_TOOLS: List[AccessibilityTool] = [
    AccessibilityTool(
        id="model-testing",
        name="Model Testing",
        description="Test sign language AI models against real accessibility standards",
        category=ToolCategory.MODEL_TESTING,
        status=ToolStatus.AVAILABLE,
        icon="🧪",
        features=[
            "Test GitHub repos automatically",
            "ASL recognition testing",
            "Fingerspelling accuracy",
            "Caption quality scoring",
            "Performance benchmarks"
        ],
        deaf_first_score=98
    ),
    AccessibilityTool(
        id="captions",
        name="Smart Captions",
        description="Generate high-quality captions for video content",
        category=ToolCategory.CAPTIONS,
        status=ToolStatus.AVAILABLE,
        icon="📝",
        features=[
            "Real-time captioning",
            "Speaker identification",
            "Multiple languages",
            "Custom styling",
            "Export to SRT/VTT"
        ],
        deaf_first_score=95
    ),
    AccessibilityTool(
        id="transcription",
        name="Audio Transcription",
        description="Convert audio to text with high accuracy",
        category=ToolCategory.TRANSCRIPTION,
        status=ToolStatus.AVAILABLE,
        icon="🎤",
        features=[
            "Multi-speaker detection",
            "Timestamps",
            "Noise filtering",
            "Technical vocabulary",
            "Real-time mode"
        ],
        deaf_first_score=92
    ),
    AccessibilityTool(
        id="visual-alerts",
        name="Visual Alerts",
        description="Convert audio alerts to visual notifications",
        category=ToolCategory.VISUAL_ALERTS,
        status=ToolStatus.BETA,
        icon="🔔",
        features=[
            "Doorbell detection",
            "Phone ring detection",
            "Baby cry detection",
            "Smoke alarm detection",
            "Custom sound training"
        ],
        deaf_first_score=88
    ),
    AccessibilityTool(
        id="video-relay",
        name="Video Relay Service",
        description="Connect with sign language interpreters",
        category=ToolCategory.VIDEO_RELAY,
        status=ToolStatus.COMING_SOON,
        icon="📹",
        features=[
            "24/7 availability",
            "ASL interpreters",
            "International sign",
            "Emergency priority",
            "Business scheduling"
        ],
        deaf_first_score=None
    ),
    AccessibilityTool(
        id="sign-recognition",
        name="Sign Language Recognition",
        description="Real-time ASL to text translation",
        category=ToolCategory.SIGN_RECOGNITION,
        status=ToolStatus.BETA,
        icon="✋",
        features=[
            "Real-time processing",
            "ASL alphabet",
            "Common phrases",
            "Gesture detection",
            "Continuous signing"
        ],
        deaf_first_score=85
    ),
    AccessibilityTool(
        id="text-to-sign",
        name="Text to Sign",
        description="Convert text to sign language animations",
        category=ToolCategory.TEXT_TO_SIGN,
        status=ToolStatus.COMING_SOON,
        icon="🤟",
        features=[
            "Animated avatar",
            "Multiple sign languages",
            "Customizable speed",
            "Export to video",
            "API integration"
        ],
        deaf_first_score=None
    )
]


# ============================================
# Health and Status Endpoints
# ============================================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API info"""
    return {
        "name": "PinkFlow API",
        "version": "0.1.0",
        "description": "Deaf-First Accessibility Tools and Model Testing",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now(),
        services={
            "api": "running",
            "model_testing": "available",
            "captions": "available",
            "transcription": "available"
        }
    )


# ============================================
# Accessibility Tools Endpoints
# ============================================

@app.get("/api/tools", response_model=List[AccessibilityTool])
async def list_tools(
    category: Optional[ToolCategory] = None,
    status: Optional[ToolStatus] = None
):
    """List all accessibility tools"""
    tools = ACCESSIBILITY_TOOLS

    if category:
        tools = [t for t in tools if t.category == category]

    if status:
        tools = [t for t in tools if t.status == status]

    return tools


@app.get("/api/tools/{tool_id}", response_model=AccessibilityTool)
async def get_tool(tool_id: str):
    """Get a specific accessibility tool"""
    for tool in ACCESSIBILITY_TOOLS:
        if tool.id == tool_id:
            return tool
    raise HTTPException(status_code=404, detail="Tool not found")


# ============================================
# Model Testing Endpoints
# ============================================

@app.post("/api/test/model", response_model=ModelTestResponse)
async def test_model(request: ModelTestRequest, background_tasks: BackgroundTasks):
    """Test a model from a GitHub repository"""
    test_id = str(uuid.uuid4())
    pubsub_service = get_pubsub_service()

    # Broadcast test started event
    await pubsub_service.publish(
        topic="test.model",
        event_type=EventType.TEST_STARTED,
        data={
            'test_id': test_id,
            'repo_url': request.repo_url,
            'test_type': request.test_type
        },
        priority=NotificationPriority.NORMAL
    )

    try:
        # Use MCP tester for GitHub repos
        tester = MCPGitHubTester()
        result = tester.test_repo_with_mcp(request.repo_url)

        test_result = result.get('test_results', {})

        response = ModelTestResponse(
            id=test_id,
            repo_url=request.repo_url,
            status=TestStatus.GREEN.value if result.get('passed') else TestStatus.RED.value,
            accuracy=test_result.get('accuracy'),
            precision=test_result.get('precision'),
            recall=test_result.get('recall'),
            f1_score=test_result.get('f1_score'),
            processing_time=test_result.get('processing_time'),
            errors=[],
            metadata={
                'model_type': result.get('model_type'),
                'repo_info': result.get('repo_info'),
                'structure': result.get('structure')
            },
            created_at=datetime.now(),
            passed=result.get('passed', False)
        )

        if request.save_results:
            test_results_store[test_id] = response

        # Broadcast test completed event
        await pubsub_service.publish(
            topic="test.model",
            event_type=EventType.TEST_COMPLETED,
            data={
                'test_id': test_id,
                'repo_url': request.repo_url,
                'passed': response.passed,
                'accuracy': response.accuracy,
                'status': response.status
            },
            priority=NotificationPriority.HIGH if response.passed else NotificationPriority.URGENT
        )

        return response
    
    except Exception as e:
        # Broadcast test failed event
        await pubsub_service.publish(
            topic="test.model",
            event_type=EventType.TEST_FAILED,
            data={
                'test_id': test_id,
                'repo_url': request.repo_url,
                'error': str(e)
            },
            priority=NotificationPriority.URGENT
        )
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")


@app.post("/api/test/batch", response_model=BatchTestResponse)
async def test_batch(request: BatchTestRequest):
    """Test multiple repositories at once"""
    batch_id = str(uuid.uuid4())
    results = []

    for repo_url in request.repo_urls:
        tester = MCPGitHubTester()
        result = tester.test_repo_with_mcp(repo_url)
        test_result = result.get('test_results', {})

        response = ModelTestResponse(
            id=str(uuid.uuid4()),
            repo_url=repo_url,
            status=TestStatus.GREEN.value if result.get('passed') else TestStatus.RED.value,
            accuracy=test_result.get('accuracy'),
            precision=test_result.get('precision'),
            recall=test_result.get('recall'),
            f1_score=test_result.get('f1_score'),
            processing_time=test_result.get('processing_time'),
            errors=[],
            metadata={'model_type': result.get('model_type')},
            created_at=datetime.now(),
            passed=result.get('passed', False)
        )
        results.append(response)

    batch_response = BatchTestResponse(
        batch_id=batch_id,
        total=len(results),
        passed=sum(1 for r in results if r.passed),
        failed=sum(1 for r in results if not r.passed),
        results=results,
        created_at=datetime.now()
    )

    batch_results_store[batch_id] = batch_response

    return batch_response


@app.get("/api/test/results/{test_id}", response_model=ModelTestResponse)
async def get_test_result(test_id: str):
    """Get a specific test result"""
    if test_id not in test_results_store:
        raise HTTPException(status_code=404, detail="Test result not found")
    return test_results_store[test_id]


@app.get("/api/test/results", response_model=List[ModelTestResponse])
async def list_test_results(
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0)
):
    """List all test results"""
    results = list(test_results_store.values())
    results.sort(key=lambda x: x.created_at, reverse=True)
    return results[offset:offset + limit]


# ============================================
# Caption Endpoints
# ============================================

@app.post("/api/captions/generate", response_model=CaptionResponse)
async def generate_captions(request: CaptionRequest):
    """Generate captions for video or text"""
    caption_id = str(uuid.uuid4())

    # Demo response - in production, integrate with caption service
    demo_captions = """1
00:00:00,000 --> 00:00:03,000
Welcome to PinkFlow accessibility tools.

2
00:00:03,500 --> 00:00:07,000
This is a demonstration of our caption generation.

3
00:00:07,500 --> 00:00:11,000
Designed with the Deaf community in mind.
"""

    return CaptionResponse(
        id=caption_id,
        status="completed",
        captions=demo_captions,
        format=request.format,
        created_at=datetime.now()
    )


# ============================================
# Transcription Endpoints
# ============================================

@app.post("/api/transcription/generate", response_model=TranscriptionResponse)
async def generate_transcription(request: TranscriptionRequest):
    """Generate transcription from audio"""
    transcription_id = str(uuid.uuid4())

    # Demo response - in production, integrate with transcription service
    demo_segments = [
        {"start": 0.0, "end": 3.0, "text": "Welcome to PinkFlow."},
        {"start": 3.5, "end": 7.0, "text": "This is a demonstration of audio transcription."},
        {"start": 7.5, "end": 11.0, "text": "Designed for accessibility first."}
    ]

    return TranscriptionResponse(
        id=transcription_id,
        status="completed",
        text=" ".join([s["text"] for s in demo_segments]),
        segments=demo_segments if request.include_timestamps else None,
        created_at=datetime.now()
    )


# ============================================
# Statistics Endpoints
# ============================================

@app.get("/api/stats")
async def get_statistics():
    """Get overall statistics"""
    total_tests = len(test_results_store)
    passed_tests = sum(1 for r in test_results_store.values() if r.passed)

    return {
        "total_models_tested": total_tests,
        "passed": passed_tests,
        "failed": total_tests - passed_tests,
        "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
        "total_tools": len(ACCESSIBILITY_TOOLS),
        "available_tools": sum(1 for t in ACCESSIBILITY_TOOLS if t.status == ToolStatus.AVAILABLE),
        "beta_tools": sum(1 for t in ACCESSIBILITY_TOOLS if t.status == ToolStatus.BETA),
        "avg_deaf_score": sum(
            t.deaf_first_score for t in ACCESSIBILITY_TOOLS if t.deaf_first_score
        ) / sum(1 for t in ACCESSIBILITY_TOOLS if t.deaf_first_score) if any(
            t.deaf_first_score for t in ACCESSIBILITY_TOOLS
        ) else 0
    }


# ============================================
# Voting Endpoints
# ============================================

@app.post("/api/vote", response_model=VoteResponse)
async def cast_vote(request: VoteRequest, user_id: str = Query(..., description="User ID")):
    """
    Cast or update a vote on an item.
    Vote counts are public, but individual voter identities are private.
    """
    voting_service = get_voting_service()
    pubsub_service = get_pubsub_service()
    
    try:
        # Validate and convert enums
        item_type = VotableItemType(request.item_type)
        vote_type = VoteType(request.vote_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid type: {str(e)}")
    
    # Cast vote
    result = voting_service.cast_vote(
        user_id=user_id,
        item_id=request.item_id,
        item_type=item_type,
        vote_type=vote_type
    )
    
    # Broadcast vote event via PubSub
    await pubsub_service.publish(
        topic=f"votes.{request.item_type}",
        event_type=EventType.VOTE_CAST,
        data={
            'item_id': request.item_id,
            'vote_counts': result
        },
        priority=NotificationPriority.NORMAL
    )
    
    return VoteResponse(**result)


@app.delete("/api/vote/{item_id}")
async def remove_vote(item_id: str, user_id: str = Query(..., description="User ID")):
    """Remove a user's vote from an item"""
    voting_service = get_voting_service()
    
    result = voting_service.remove_vote(user_id=user_id, item_id=item_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    return result


@app.get("/api/vote/{item_id}", response_model=VoteResponse)
async def get_vote_summary(item_id: str):
    """Get vote summary for an item (public, no user info)"""
    voting_service = get_voting_service()
    result = voting_service.get_vote_summary(item_id)
    return VoteResponse(**result)


@app.get("/api/vote/{item_id}/status")
async def get_user_vote_status(item_id: str, user_id: str = Query(..., description="User ID")):
    """Get user's vote status for a specific item"""
    voting_service = get_voting_service()
    status = voting_service.get_user_voting_status(user_id, item_id)
    
    if status is None:
        return {"has_voted": False}
    
    return status


@app.get("/api/vote/top/{item_type}")
async def get_top_voted_items(
    item_type: str,
    limit: int = Query(default=10, le=100)
):
    """Get top voted items by score"""
    voting_service = get_voting_service()
    
    try:
        item_type_enum = VotableItemType(item_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid item_type: {item_type}")
    
    return voting_service.get_top_voted_items(item_type=item_type_enum, limit=limit)


# ============================================
# FibonRose Metrics Endpoints
# ============================================

@app.get("/api/fibonrose/metrics/{user_id}")
async def get_user_fibonrose_metrics(user_id: str):
    """
    Get FibonRose trust metrics for a user based on voting history.
    Uses Fibonacci-inspired weighting for trust calculations.
    """
    voting_service = get_voting_service()
    return voting_service.get_user_fibonrose_metrics(user_id)


# ============================================
# PubSub Endpoints
# ============================================

@app.post("/api/subscribe")
async def subscribe_to_topics(request: SubscriptionRequest):
    """
    Subscribe to topics for real-time notifications.
    Supports IoT devices and Vibration API.
    """
    pubsub_service = get_pubsub_service()
    
    subscriber = pubsub_service.subscribe(
        subscriber_id=request.subscriber_id,
        topics=request.topics,
        iot_enabled=request.iot_enabled,
        vibration_enabled=request.vibration_enabled
    )
    
    return {
        "subscriber_id": subscriber.id,
        "topics": list(subscriber.topics),
        "iot_enabled": subscriber.iot_enabled,
        "vibration_enabled": subscriber.vibration_enabled,
        "message": "Successfully subscribed to topics"
    }


@app.delete("/api/subscribe/{subscriber_id}")
async def unsubscribe_from_topics(
    subscriber_id: str,
    topics: Optional[List[str]] = Query(None)
):
    """Unsubscribe from topics or remove subscriber entirely"""
    pubsub_service = get_pubsub_service()
    pubsub_service.unsubscribe(subscriber_id, topics)
    
    return {
        "subscriber_id": subscriber_id,
        "message": "Successfully unsubscribed"
    }


@app.post("/api/broadcast")
async def broadcast_notification(request: NotificationRequest):
    """
    Broadcast a notification to subscribers.
    Creates visual banners, IoT alerts, and vibration notifications.
    """
    pubsub_service = get_pubsub_service()
    
    try:
        event_type = EventType(request.event_type)
        priority = NotificationPriority(request.priority)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid type: {str(e)}")
    
    await pubsub_service.publish(
        topic=request.topic,
        event_type=event_type,
        data=request.data,
        priority=priority
    )
    
    subscriber_count = pubsub_service.get_subscriber_count(request.topic)
    
    return {
        "topic": request.topic,
        "event_type": event_type.value,
        "priority": priority.value,
        "subscribers_notified": subscriber_count,
        "message": "Notification broadcast successfully"
    }


@app.get("/api/broadcast/history")
async def get_broadcast_history(
    event_type: Optional[str] = None,
    limit: int = Query(default=100, le=1000)
):
    """Get event broadcast history"""
    pubsub_service = get_pubsub_service()
    
    event_type_enum = None
    if event_type:
        try:
            event_type_enum = EventType(event_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid event_type: {event_type}")
    
    history = pubsub_service.get_history(event_type=event_type_enum, limit=limit)
    
    return {
        "total": len(history),
        "events": [event.to_dict() for event in history]
    }


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
