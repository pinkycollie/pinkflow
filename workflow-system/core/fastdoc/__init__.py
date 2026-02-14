"""
FastDoc - Lightweight Document Platform for PinkSync's Deaf User Ecosystem

FastDoc provides accessible document workflows for deaf users, featuring:
- Video-based contract rendering using FFmpeg
- QR code linking for easy document access
- vCODE integration for notary-grade verification
- Complete audit trail for compliance

The module integrates with PinkSync for real-time collaboration and
vCODE for video-based digital signatures.

Video Contract Flow:
    Traditional Contract → FastDoc Template → FFmpeg Video → QR Code → Deaf User Signs via vCODE

Example Usage:
    from workflow_system.core.fastdoc import (
        NotaryWorkflowOrchestrator,
        SignerInfo,
        DocumentType,
        VerificationLevel
    )
    
    # Initialize orchestrator
    orchestrator = NotaryWorkflowOrchestrator()
    
    # Create signers
    signers = [
        SignerInfo(
            signer_id="user_123",
            name="John Doe",
            email="john@example.com",
            deaf_user=True
        )
    ]
    
    # Run full workflow
    result = orchestrator.run_full_workflow(
        document_id="contract_001",
        title="Service Agreement",
        content="Contract content here...",
        document_type=DocumentType.CONTRACT,
        created_by="admin",
        signers=signers
    )
"""

# FFmpeg Adapter exports
from .ffmpeg_adapter import (
    FFmpegAdapter,
    VideoConfig,
    VideoResolution,
    VideoCodec,
    RenderJob
)

# QR Generator exports
from .qr_generator import (
    QRGenerator,
    QRCodeConfig,
    QRCodeData,
    QRErrorCorrectionLevel,
    QRFormat,
    GeneratedQRCode
)

# vCODE Integration exports
from .vcode_integration import (
    VCodeIntegration,
    SignerInfo,
    SignerRole,
    SigningRequest,
    VideoSignature,
    SignatureStatus,
    VerificationLevel
)

# Notary Workflow exports
from .notary_workflow import (
    NotaryWorkflowOrchestrator,
    NotaryWorkflow,
    NotaryDocument,
    NotaryWorkflowStatus,
    DocumentType
)

__all__ = [
    # FFmpeg Adapter
    'FFmpegAdapter',
    'VideoConfig',
    'VideoResolution',
    'VideoCodec',
    'RenderJob',
    
    # QR Generator
    'QRGenerator',
    'QRCodeConfig',
    'QRCodeData',
    'QRErrorCorrectionLevel',
    'QRFormat',
    'GeneratedQRCode',
    
    # vCODE Integration
    'VCodeIntegration',
    'SignerInfo',
    'SignerRole',
    'SigningRequest',
    'VideoSignature',
    'SignatureStatus',
    'VerificationLevel',
    
    # Notary Workflow
    'NotaryWorkflowOrchestrator',
    'NotaryWorkflow',
    'NotaryDocument',
    'NotaryWorkflowStatus',
    'DocumentType',
]

__version__ = '1.0.0'
