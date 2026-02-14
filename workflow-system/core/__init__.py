"""
PinkFlow Workflow System - Core Module

This module provides the core functionality for creating and managing
dynamic workflows with node-based routing and conditional logic.

Includes FastDoc for accessible document workflows:
- Video-based contract rendering (FFmpeg)
- QR code linking for document access
- vCODE integration for deaf user signing
- Notary-grade document verification
"""

from .workflow import (
    Workflow,
    WorkflowBuilder,
    Node,
    Edge,
    EdgeCondition,
    NodeType,
    Environment,
    EdgeConditionType,
    NodeMetadata
)
from .workflow_manager import (
    WorkflowManager,
    WorkflowRegistry
)
from .feedback_workflow import (
    FeedbackWorkflowOrchestrator,
    FeedbackMetadata,
    FeedbackStatus,
    VideoValidator,
    VideoFormat,
    CloudStorageAdapter,
    PubSubNotifier
)
from .fastdoc import (
    # FFmpeg Adapter
    FFmpegAdapter,
    VideoConfig,
    VideoResolution,
    VideoCodec,
    RenderJob,
    # QR Generator
    QRGenerator,
    QRCodeConfig,
    QRCodeData,
    QRErrorCorrectionLevel,
    QRFormat,
    GeneratedQRCode,
    # vCODE Integration
    VCodeIntegration,
    SignerInfo,
    SignerRole,
    SigningRequest,
    VideoSignature,
    SignatureStatus,
    VerificationLevel,
    # Notary Workflow
    NotaryWorkflowOrchestrator,
    NotaryWorkflow,
    NotaryDocument,
    NotaryWorkflowStatus,
    DocumentType,
)

__all__ = [
    # Workflow Core
    'Workflow',
    'WorkflowBuilder',
    'Node',
    'Edge',
    'EdgeCondition',
    'NodeType',
    'Environment',
    'EdgeConditionType',
    'NodeMetadata',
    'WorkflowManager',
    'WorkflowRegistry',
    # Feedback Workflow
    'FeedbackWorkflowOrchestrator',
    'FeedbackMetadata',
    'FeedbackStatus',
    'VideoValidator',
    'VideoFormat',
    'CloudStorageAdapter',
    'PubSubNotifier',
    # FastDoc - FFmpeg Adapter
    'FFmpegAdapter',
    'VideoConfig',
    'VideoResolution',
    'VideoCodec',
    'RenderJob',
    # FastDoc - QR Generator
    'QRGenerator',
    'QRCodeConfig',
    'QRCodeData',
    'QRErrorCorrectionLevel',
    'QRFormat',
    'GeneratedQRCode',
    # FastDoc - vCODE Integration
    'VCodeIntegration',
    'SignerInfo',
    'SignerRole',
    'SigningRequest',
    'VideoSignature',
    'SignatureStatus',
    'VerificationLevel',
    # FastDoc - Notary Workflow
    'NotaryWorkflowOrchestrator',
    'NotaryWorkflow',
    'NotaryDocument',
    'NotaryWorkflowStatus',
    'DocumentType',
]

__version__ = '1.0.0'
