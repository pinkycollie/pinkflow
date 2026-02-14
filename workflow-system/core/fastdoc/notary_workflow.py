"""
FastDoc Notary Workflow Module

This module provides the complete document notarization workflow for
deaf users, integrating FFmpeg video generation, QR codes, and vCODE
signing into a cohesive workflow.

Features:
- End-to-end document notarization workflow
- Integration with FFmpeg for video rendering
- QR code generation for document linking
- vCODE signing for deaf user verification
- Complete audit trail from creation to execution
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .ffmpeg_adapter import FFmpegAdapter, VideoConfig, RenderJob
from .qr_generator import QRGenerator, QRCodeConfig, GeneratedQRCode
from .vcode_integration import (
    VCodeIntegration,
    SigningRequest,
    SignerInfo,
    VerificationLevel,
    SignatureStatus
)


class NotaryWorkflowStatus(Enum):
    """Status of the notary workflow."""
    DRAFT = "draft"
    VIDEO_RENDERING = "video_rendering"
    QR_GENERATED = "qr_generated"
    AWAITING_SIGNATURES = "awaiting_signatures"
    PARTIALLY_SIGNED = "partially_signed"
    FULLY_SIGNED = "fully_signed"
    NOTARIZED = "notarized"
    ARCHIVED = "archived"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DocumentType(Enum):
    """Types of documents supported for notarization."""
    CONTRACT = "contract"
    AGREEMENT = "agreement"
    CONSENT_FORM = "consent_form"
    AUTHORIZATION = "authorization"
    AFFIDAVIT = "affidavit"
    POWER_OF_ATTORNEY = "power_of_attorney"
    CUSTOM = "custom"


@dataclass
class NotaryDocument:
    """Represents a document in the notary workflow."""
    document_id: str
    title: str
    document_type: DocumentType
    content: str
    created_by: str
    template_id: Optional[str] = None
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            'document_id': self.document_id,
            'title': self.title,
            'document_type': self.document_type.value,
            'content': self.content,
            'created_by': self.created_by,
            'template_id': self.template_id,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class NotaryWorkflow:
    """Represents a complete notary workflow instance."""
    workflow_id: str
    document: NotaryDocument
    signers: List[SignerInfo]
    status: NotaryWorkflowStatus = NotaryWorkflowStatus.DRAFT
    verification_level: VerificationLevel = VerificationLevel.NOTARY
    
    # Generated artifacts
    video_job: Optional[RenderJob] = None
    video_url: Optional[str] = None
    qr_code: Optional[GeneratedQRCode] = None
    signing_request: Optional[SigningRequest] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    video_rendered_at: Optional[datetime] = None
    qr_generated_at: Optional[datetime] = None
    signing_started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notarized_at: Optional[datetime] = None
    
    # Audit trail
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)
    
    # Configuration
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary."""
        return {
            'workflow_id': self.workflow_id,
            'document': self.document.to_dict(),
            'signers': [s.to_dict() for s in self.signers],
            'status': self.status.value,
            'verification_level': self.verification_level.value,
            'video_url': self.video_url,
            'qr_code': self.qr_code.to_dict() if self.qr_code else None,
            'signing_request_id': self.signing_request.request_id if self.signing_request else None,
            'created_at': self.created_at.isoformat(),
            'video_rendered_at': self.video_rendered_at.isoformat() if self.video_rendered_at else None,
            'qr_generated_at': self.qr_generated_at.isoformat() if self.qr_generated_at else None,
            'signing_started_at': self.signing_started_at.isoformat() if self.signing_started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notarized_at': self.notarized_at.isoformat() if self.notarized_at else None,
            'audit_trail': self.audit_trail,
            'metadata': self.metadata
        }
    
    def add_audit_entry(self, action: str, actor_id: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Add an entry to the audit trail."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'actor_id': actor_id,
            'status': self.status.value,
            'details': details or {}
        }
        self.audit_trail.append(entry)


class NotaryWorkflowOrchestrator:
    """
    Orchestrator for the complete document notarization workflow.
    
    This class coordinates the entire process from document creation
    to final notarization:
    
    1. Document Creation/Import
    2. Video Rendering (FFmpeg)
    3. QR Code Generation
    4. Signing Request (vCODE)
    5. Signature Collection
    6. Verification & Notarization
    7. Certificate Generation
    """
    
    def __init__(
        self,
        ffmpeg_config: Optional[Dict[str, Any]] = None,
        qr_config: Optional[Dict[str, Any]] = None,
        vcode_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the notary workflow orchestrator.
        
        Args:
            ffmpeg_config: Configuration for FFmpeg adapter
            qr_config: Configuration for QR generator
            vcode_config: Configuration for vCODE integration
        """
        self.ffmpeg = FFmpegAdapter(ffmpeg_config)
        self.qr_generator = QRGenerator(qr_config)
        self.vcode = VCodeIntegration(vcode_config)
        
        self.workflows: Dict[str, NotaryWorkflow] = {}
        
        # Register vCODE callbacks
        self.vcode.on_signature_received(self._on_signature_received)
        self.vcode.on_request_completed(self._on_signing_completed)
    
    def create_workflow(
        self,
        document_id: str,
        title: str,
        content: str,
        document_type: DocumentType,
        created_by: str,
        signers: List[SignerInfo],
        verification_level: VerificationLevel = VerificationLevel.NOTARY,
        template_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> NotaryWorkflow:
        """
        Create a new notary workflow.
        
        Args:
            document_id: Unique document identifier
            title: Document title
            content: Document content
            document_type: Type of document
            created_by: ID of creator
            signers: List of required signers
            verification_level: Required verification level
            template_id: Optional template ID
            metadata: Additional metadata
            
        Returns:
            Created NotaryWorkflow instance
        """
        workflow_id = f"notary_{document_id}_{int(datetime.now().timestamp())}"
        
        document = NotaryDocument(
            document_id=document_id,
            title=title,
            content=content,
            document_type=document_type,
            created_by=created_by,
            template_id=template_id,
            metadata=metadata or {}
        )
        
        workflow = NotaryWorkflow(
            workflow_id=workflow_id,
            document=document,
            signers=signers,
            verification_level=verification_level,
            metadata=metadata or {}
        )
        
        workflow.add_audit_entry(
            action='workflow_created',
            actor_id=created_by,
            details={
                'document_type': document_type.value,
                'signer_count': len(signers),
                'verification_level': verification_level.value
            }
        )
        
        self.workflows[workflow_id] = workflow
        return workflow
    
    def render_video(
        self,
        workflow_id: str,
        video_config: Optional[VideoConfig] = None,
        sign_language_template: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Render the document as a sign language video.
        
        Args:
            workflow_id: Workflow ID
            video_config: Video configuration
            sign_language_template: Path to sign language template
            
        Returns:
            Rendering result dictionary
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {
                'success': False,
                'error': f"Workflow '{workflow_id}' not found"
            }
        
        workflow.status = NotaryWorkflowStatus.VIDEO_RENDERING
        
        output_path = f"/tmp/fastdoc/output/{workflow.document.document_id}.mp4"
        
        result = self.ffmpeg.render_contract_video(
            contract_id=workflow.document.document_id,
            contract_content=workflow.document.content,
            output_path=output_path,
            sign_language_template=sign_language_template,
            video_config=video_config
        )
        
        if result.get('success'):
            workflow.video_url = result.get('output_path')
            workflow.video_rendered_at = datetime.now()
            workflow.add_audit_entry(
                action='video_rendered',
                actor_id='system',
                details={
                    'output_path': output_path,
                    'job_id': result.get('job_id')
                }
            )
        else:
            workflow.status = NotaryWorkflowStatus.FAILED
            workflow.add_audit_entry(
                action='video_render_failed',
                actor_id='system',
                details={'error': result.get('error')}
            )
        
        return result
    
    def generate_qr_code(
        self,
        workflow_id: str,
        qr_config: Optional[QRCodeConfig] = None
    ) -> Dict[str, Any]:
        """
        Generate QR code for the document video.
        
        Args:
            workflow_id: Workflow ID
            qr_config: QR code configuration
            
        Returns:
            QR generation result dictionary
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {
                'success': False,
                'error': f"Workflow '{workflow_id}' not found"
            }
        
        if not workflow.video_url:
            return {
                'success': False,
                'error': 'Video must be rendered before generating QR code'
            }
        
        qr_code = self.qr_generator.generate_qr_code(
            document_id=workflow.document.document_id,
            video_url=workflow.video_url,
            qr_config=qr_config,
            metadata={
                'workflow_id': workflow_id,
                'document_title': workflow.document.title
            }
        )
        
        workflow.qr_code = qr_code
        workflow.qr_generated_at = datetime.now()
        workflow.status = NotaryWorkflowStatus.QR_GENERATED
        
        workflow.add_audit_entry(
            action='qr_code_generated',
            actor_id='system',
            details={
                'qr_id': qr_code.qr_id,
                'video_url': workflow.video_url
            }
        )
        
        return {
            'success': True,
            'qr_id': qr_code.qr_id,
            'qr_code': qr_code.to_dict()
        }
    
    def start_signing(
        self,
        workflow_id: str,
        expiration_hours: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Start the signing process for the workflow.
        
        Args:
            workflow_id: Workflow ID
            expiration_hours: Hours until signing expires
            
        Returns:
            Signing start result dictionary
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {
                'success': False,
                'error': f"Workflow '{workflow_id}' not found"
            }
        
        if not workflow.video_url:
            return {
                'success': False,
                'error': 'Video must be rendered before starting signing'
            }
        
        signing_request = self.vcode.create_signing_request(
            document_id=workflow.document.document_id,
            document_title=workflow.document.title,
            video_url=workflow.video_url,
            signers=workflow.signers,
            qr_code_url=workflow.qr_code.file_path if workflow.qr_code else None,
            verification_level=workflow.verification_level,
            expiration_hours=expiration_hours,
            metadata={
                'workflow_id': workflow_id,
                'document_type': workflow.document.document_type.value
            }
        )
        
        workflow.signing_request = signing_request
        workflow.signing_started_at = datetime.now()
        workflow.status = NotaryWorkflowStatus.AWAITING_SIGNATURES
        
        workflow.add_audit_entry(
            action='signing_started',
            actor_id='system',
            details={
                'request_id': signing_request.request_id,
                'signers': [s.signer_id for s in workflow.signers]
            }
        )
        
        return {
            'success': True,
            'request_id': signing_request.request_id,
            'signing_request': signing_request.to_dict()
        }
    
    def _on_signature_received(self, signature) -> None:
        """
        Handle signature received callback.
        
        Args:
            signature: The received signature
        """
        # Find the workflow for this signature
        for workflow in self.workflows.values():
            if (workflow.signing_request and
                any(s.signer_id == signature.signer_id for s in workflow.signers)):
                
                workflow.status = NotaryWorkflowStatus.PARTIALLY_SIGNED
                workflow.add_audit_entry(
                    action='signature_received',
                    actor_id=signature.signer_id,
                    details={
                        'signature_id': signature.signature_id
                    }
                )
                break
    
    def _on_signing_completed(self, signing_request: SigningRequest) -> None:
        """
        Handle signing completed callback.
        
        Args:
            signing_request: The completed signing request
        """
        # Find the workflow for this request
        for workflow in self.workflows.values():
            if (workflow.signing_request and
                workflow.signing_request.request_id == signing_request.request_id):
                
                workflow.status = NotaryWorkflowStatus.FULLY_SIGNED
                workflow.completed_at = datetime.now()
                workflow.add_audit_entry(
                    action='all_signatures_collected',
                    actor_id='system',
                    details={
                        'total_signatures': len(signing_request.signatures)
                    }
                )
                break
    
    def notarize(
        self,
        workflow_id: str,
        notary_id: str
    ) -> Dict[str, Any]:
        """
        Complete the notarization of a fully signed document.
        
        Args:
            workflow_id: Workflow ID
            notary_id: ID of the notary performing notarization
            
        Returns:
            Notarization result dictionary
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {
                'success': False,
                'error': f"Workflow '{workflow_id}' not found"
            }
        
        if workflow.status != NotaryWorkflowStatus.FULLY_SIGNED:
            return {
                'success': False,
                'error': f"Workflow must be fully signed before notarization. Current status: {workflow.status.value}"
            }
        
        # Verify all signatures
        if workflow.signing_request:
            for signature in workflow.signing_request.signatures:
                verify_result = self.vcode.verify_signature(
                    signature.signature_id,
                    notary_id
                )
                if not verify_result.get('success'):
                    return {
                        'success': False,
                        'error': f"Signature verification failed for {signature.signer_id}"
                    }
        
        # Generate certificate
        certificate = None
        if workflow.signing_request:
            certificate = self.vcode.generate_certificate(
                workflow.signing_request.request_id
            )
        
        workflow.status = NotaryWorkflowStatus.NOTARIZED
        workflow.notarized_at = datetime.now()
        
        workflow.add_audit_entry(
            action='document_notarized',
            actor_id=notary_id,
            details={
                'certificate_id': certificate.get('certificate_id') if certificate else None
            }
        )
        
        return {
            'success': True,
            'workflow_id': workflow_id,
            'status': 'notarized',
            'notarized_at': workflow.notarized_at.isoformat(),
            'certificate': certificate
        }
    
    def archive(
        self,
        workflow_id: str,
        archived_by: str
    ) -> Dict[str, Any]:
        """
        Archive a completed workflow.
        
        Args:
            workflow_id: Workflow ID
            archived_by: ID of user archiving
            
        Returns:
            Archive result dictionary
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {
                'success': False,
                'error': f"Workflow '{workflow_id}' not found"
            }
        
        if workflow.status not in [NotaryWorkflowStatus.NOTARIZED, NotaryWorkflowStatus.CANCELLED]:
            return {
                'success': False,
                'error': 'Only notarized or cancelled workflows can be archived'
            }
        
        workflow.status = NotaryWorkflowStatus.ARCHIVED
        
        workflow.add_audit_entry(
            action='workflow_archived',
            actor_id=archived_by,
            details={}
        )
        
        return {
            'success': True,
            'workflow_id': workflow_id,
            'status': 'archived'
        }
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get workflow details.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow dictionary or None if not found
        """
        workflow = self.workflows.get(workflow_id)
        if workflow:
            return workflow.to_dict()
        return None
    
    def list_workflows(
        self,
        status: Optional[NotaryWorkflowStatus] = None,
        created_by: Optional[str] = None,
        document_type: Optional[DocumentType] = None
    ) -> List[Dict[str, Any]]:
        """
        List workflows with optional filtering.
        
        Args:
            status: Filter by status
            created_by: Filter by creator
            document_type: Filter by document type
            
        Returns:
            List of workflow dictionaries
        """
        workflows = list(self.workflows.values())
        
        if status:
            workflows = [w for w in workflows if w.status == status]
        
        if created_by:
            workflows = [w for w in workflows if w.document.created_by == created_by]
        
        if document_type:
            workflows = [w for w in workflows if w.document.document_type == document_type]
        
        return [w.to_dict() for w in workflows]
    
    def get_audit_trail(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get the complete audit trail for a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            List of audit trail entries
        """
        workflow = self.workflows.get(workflow_id)
        if workflow:
            return workflow.audit_trail
        return []
    
    def cancel_workflow(
        self,
        workflow_id: str,
        cancelled_by: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cancel a workflow in progress.
        
        Args:
            workflow_id: Workflow ID
            cancelled_by: ID of user cancelling
            reason: Optional cancellation reason
            
        Returns:
            Cancellation result dictionary
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {
                'success': False,
                'error': f"Workflow '{workflow_id}' not found"
            }
        
        if workflow.status in [NotaryWorkflowStatus.NOTARIZED, NotaryWorkflowStatus.ARCHIVED]:
            return {
                'success': False,
                'error': 'Cannot cancel a notarized or archived workflow'
            }
        
        # Cancel signing request if exists
        if workflow.signing_request:
            self.vcode.cancel_signing_request(
                workflow.signing_request.request_id,
                cancelled_by,
                reason
            )
        
        workflow.status = NotaryWorkflowStatus.CANCELLED
        
        workflow.add_audit_entry(
            action='workflow_cancelled',
            actor_id=cancelled_by,
            details={'reason': reason}
        )
        
        return {
            'success': True,
            'workflow_id': workflow_id,
            'status': 'cancelled'
        }
    
    def run_full_workflow(
        self,
        document_id: str,
        title: str,
        content: str,
        document_type: DocumentType,
        created_by: str,
        signers: List[SignerInfo],
        video_config: Optional[VideoConfig] = None,
        qr_config: Optional[QRCodeConfig] = None,
        sign_language_template: Optional[str] = None,
        verification_level: VerificationLevel = VerificationLevel.NOTARY
    ) -> Dict[str, Any]:
        """
        Run the complete workflow from document creation to signing request.
        
        This is a convenience method that executes all steps in sequence:
        1. Create workflow
        2. Render video
        3. Generate QR code
        4. Start signing
        
        Args:
            document_id: Document identifier
            title: Document title
            content: Document content
            document_type: Type of document
            created_by: Creator ID
            signers: List of signers
            video_config: Video configuration
            qr_config: QR configuration
            sign_language_template: Sign language template path
            verification_level: Verification level
            
        Returns:
            Complete workflow result dictionary
        """
        # Step 1: Create workflow
        workflow = self.create_workflow(
            document_id=document_id,
            title=title,
            content=content,
            document_type=document_type,
            created_by=created_by,
            signers=signers,
            verification_level=verification_level
        )
        
        results = {
            'workflow_id': workflow.workflow_id,
            'steps': {}
        }
        
        # Step 2: Render video
        video_result = self.render_video(
            workflow.workflow_id,
            video_config,
            sign_language_template
        )
        results['steps']['video_render'] = video_result
        
        if not video_result.get('success'):
            return {
                'success': False,
                'workflow_id': workflow.workflow_id,
                'error': 'Video rendering failed',
                'results': results
            }
        
        # Step 3: Generate QR code
        qr_result = self.generate_qr_code(workflow.workflow_id, qr_config)
        results['steps']['qr_generation'] = qr_result
        
        # Step 4: Start signing
        signing_result = self.start_signing(workflow.workflow_id)
        results['steps']['signing_start'] = signing_result
        
        if not signing_result.get('success'):
            return {
                'success': False,
                'workflow_id': workflow.workflow_id,
                'error': 'Failed to start signing process',
                'results': results
            }
        
        return {
            'success': True,
            'workflow_id': workflow.workflow_id,
            'status': workflow.status.value,
            'results': results,
            'workflow': workflow.to_dict()
        }
