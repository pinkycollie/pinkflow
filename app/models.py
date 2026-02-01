from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

class TaskType(str, Enum):
    SLR = "SLR"
    SLT = "SLT"
    SLP = "SLP"
    POSE = "Pose"

class ModelStatus(str, Enum):
    QUEUED = "queued"
    TESTING = "testing"
    TESTED = "tested"
    FAILED = "failed"

class TestStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ModelCreate(BaseModel):
    name: str
    task: TaskType
    repo: HttpUrl
    paper: Optional[HttpUrl] = None
    dataset: Optional[str] = None
    pretrained_weights: Optional[HttpUrl] = None
    priority: Literal["low", "normal", "high"] = "normal"

class ModelResponse(BaseModel):
    id: str
    name: str
    task: TaskType
    repo: HttpUrl
    paper: Optional[HttpUrl] = None
    status: ModelStatus
    accuracy: Optional[float] = None
    fps: Optional[float] = None
    deaf_score: Optional[float] = None
    created_at: datetime
    tested_at: Optional[datetime] = None

class TestStart(BaseModel):
    model_id: str
    dataset: Literal["WLASL", "PHOENIX", "CSL", "MBTQ-Custom"] = "WLASL"
    compute_type: Literal["cpu", "cuda", "rocm"] = "cuda"
    max_duration: int = 3600

class TestStatusResponse(BaseModel):
    test_id: str
    model_id: str
    status: TestStatus
    progress: float = Field(ge=0, le=100)
    current_stage: Literal["setup", "inference", "evaluation", "logging"]
    logs: list[dict]

class DeploymentRequest(BaseModel):
    model_id: str
    endpoint: str
    region: Literal["us-east", "us-west", "eu", "asia"] = "us-east"
    auto_scale: bool = True
    max_instances: int = 3
