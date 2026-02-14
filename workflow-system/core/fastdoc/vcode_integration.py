"""
FastDoc vCODE Integration Module

This module provides integration with PinkSync vCODE for notary-grade
verification and digital signing for deaf users.

vCODE (Video-based Code Verification) is a signing mechanism designed
specifically for deaf users, enabling visual verification and signature
capture through video-based authentication.

Features:
- Video-based signature capture and verification
- Notary-grade digital signing workflow
- Integration with PinkSync real-time services
- Audit trail generation for compliance
- Multi-party signing support
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import json


class SignatureStatus(Enum):
    """Status of a signature request."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SIGNED = "signed"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class VerificationLevel(Enum):
    """Levels of verification for signatures."""
    BASIC = "basic"              # Simple video acknowledgment
    STANDARD = "standard"        # Video + identity check
    NOTARY = "notary"            # Full notary-grade verification
    LEGAL = "legal"              # Court-admissible verification


class SignerRole(Enum):
    """Role of the signer in the document."""
    PRIMARY = "primary"
    WITNESS = "witness"
    NOTARY = "notary"
    COUNTER_PARTY = "counter_party"


@dataclass
class SignerInfo:
    """Information about a document signer."""
    signer_id: str
    name: str
    email: Optional[str] = None
    role: SignerRole = SignerRole.PRIMARY
    deaf_user: bool = True
    preferred_language: str = "ASL"  # American Sign Language by default
    verification_level: VerificationLevel = VerificationLevel.STANDARD
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert signer info to dictionary."""
        return {
            'signer_id': self.signer_id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'deaf_user': self.deaf_user,
            'preferred_language': self.preferred_language,
            'verification_level': self.verification_level.value
        }


@dataclass
class VideoSignature:
    """Represents a video-based signature."""
    signature_id: str
    signer_id: str
    document_id: str
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: float = 0.0
    captured_at: datetime = field(default_factory=datetime.now)
    verified_at: Optional[datetime] = None
    verification_hash: Optional[str] = None
    ip_address: Optional[str] = None
    device_info: Optional[str] = None
    location: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert signature to dictionary."""
        return {
            'signature_id': self.signature_id,
            'signer_id': self.signer_id,
            'document_id': self.document_id,
            'video_url': self.video_url,
            'thumbnail_url': self.thumbnail_url,
            'duration': self.duration,
            'captured_at': self.captured_at.isoformat(),
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'verification_hash': self.verification_hash,
            'ip_address': self.ip_address,
            'device_info': self.device_info,
            'location': self.location,
            'metadata': self.metadata
        }
    
    def generate_verification_hash(self) -> str:
        """Generate a verification hash for the signature."""
        data = f"{self.signature_id}:{self.signer_id}:{self.document_id}:{self.captured_at.isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class SigningRequest:
    """Represents a signing request for a document."""
    request_id: str
    document_id: str
    document_title: str
    signers: List[SignerInfo]
    video_url: str  # URL to video version of document
    qr_code_url: Optional[str] = None
    status: SignatureStatus = SignatureStatus.PENDING
    verification_level: VerificationLevel = VerificationLevel.STANDARD
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    signatures: List[VideoSignature] = field(default_factory=list)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert signing request to dictionary."""
        return {
            'request_id': self.request_id,
            'document_id': self.document_id,
            'document_title': self.document_title,
            'signers': [s.to_dict() for s in self.signers],
            'video_url': self.video_url,
            'qr_code_url': self.qr_code_url,
            'status': self.status.value,
            'verification_level': self.verification_level.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'signatures': [s.to_dict() for s in self.signatures],
            'audit_trail': self.audit_trail,
            'metadata': self.metadata
        }
    
    def add_audit_entry(self, action: str, actor_id: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Add an entry to the audit trail."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'actor_id': actor_id,
            'details': details or {}
        }
        self.audit_trail.append(entry)
    
    def is_complete(self) -> bool:
        """Check if all signers have signed."""
        signed_ids = {s.signer_id for s in self.signatures}
        required_ids = {s.signer_id for s in self.signers}
        return required_ids.issubset(signed_ids)


class VCodeIntegration:
    """
    Integration layer for PinkSync vCODE signing system.
    
    This class provides the interface for managing video-based
    signatures for deaf users in the FastDoc ecosystem.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize vCODE integration.
        
        Args:
            config: Configuration dictionary containing:
                - pinksync_url: PinkSync service URL
                - api_key: API key for authentication
                - storage_url: Video storage service URL
                - default_expiration_hours: Default signing request expiration
                - enable_notifications: Enable real-time notifications
        """
        self.config = config or {}
        self.pinksync_url = self.config.get('pinksync_url', 'https://pinksync.example.com')
        self.api_key = self.config.get('api_key')
        self.storage_url = self.config.get('storage_url', 'https://storage.example.com')
        self.default_expiration_hours = self.config.get('default_expiration_hours', 72)
        self.enable_notifications = self.config.get('enable_notifications', True)
        
        self.signing_requests: Dict[str, SigningRequest] = {}
        self.signatures: Dict[str, VideoSignature] = {}
        
        # Callbacks for real-time events
        self._on_signature_received: Optional[Callable] = None
        self._on_request_completed: Optional[Callable] = None
    
    def create_signing_request(
        self,
        document_id: str,
        document_title: str,
        video_url: str,
        signers: List[SignerInfo],
        qr_code_url: Optional[str] = None,
        verification_level: VerificationLevel = VerificationLevel.STANDARD,
        expiration_hours: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SigningRequest:
        """
        Create a new signing request for a document.
        
        Args:
            document_id: Unique document identifier
            document_title: Human-readable document title
            video_url: URL to video version of document
            signers: List of signers required
            qr_code_url: Optional QR code URL for document access
            verification_level: Required verification level
            expiration_hours: Hours until request expires
            metadata: Additional metadata
            
        Returns:
            Created SigningRequest instance
        """
        request_id = f"sign_{document_id}_{int(datetime.now().timestamp())}"
        
        # Calculate expiration
        from datetime import timedelta
        hours = expiration_hours or self.default_expiration_hours
        expires_at = datetime.now() + timedelta(hours=hours)
        
        request = SigningRequest(
            request_id=request_id,
            document_id=document_id,
            document_title=document_title,
            signers=signers,
            video_url=video_url,
            qr_code_url=qr_code_url,
            verification_level=verification_level,
            expires_at=expires_at,
            metadata=metadata or {}
        )
        
        # Add creation audit entry
        request.add_audit_entry(
            action='request_created',
            actor_id='system',
            details={
                'signer_count': len(signers),
                'verification_level': verification_level.value
            }
        )
        
        self.signing_requests[request_id] = request
        
        # Send notifications to signers if enabled
        if self.enable_notifications:
            self._notify_signers(request)
        
        return request
    
    def _notify_signers(self, request: SigningRequest) -> None:
        """
        Send notifications to signers about pending request.
        
        Args:
            request: Signing request to notify about
        """
        # Placeholder for PinkSync notification integration
        for signer in request.signers:
            notification = {
                'type': 'signing_request',
                'request_id': request.request_id,
                'document_title': request.document_title,
                'signer_id': signer.signer_id,
                'video_url': request.video_url,
                'expires_at': request.expires_at.isoformat() if request.expires_at else None
            }
            # In production, this would publish to PinkSync
            print(f"[vCODE] Notification sent to {signer.signer_id}: {json.dumps(notification)}")
    
    def capture_signature(
        self,
        request_id: str,
        signer_id: str,
        video_url: str,
        duration: float,
        ip_address: Optional[str] = None,
        device_info: Optional[str] = None,
        location: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Capture a video signature from a signer.
        
        Args:
            request_id: Signing request ID
            signer_id: ID of the signer
            video_url: URL to the signature video
            duration: Duration of signature video in seconds
            ip_address: IP address of signer
            device_info: Device information
            location: Geographic location
            metadata: Additional metadata
            
        Returns:
            Result dictionary with signature details
        """
        request = self.signing_requests.get(request_id)
        if not request:
            return {
                'success': False,
                'error': f"Signing request '{request_id}' not found"
            }
        
        # Verify signer is part of the request
        signer = next((s for s in request.signers if s.signer_id == signer_id), None)
        if not signer:
            return {
                'success': False,
                'error': f"Signer '{signer_id}' not authorized for this request"
            }
        
        # Check if already signed
        existing = next((s for s in request.signatures if s.signer_id == signer_id), None)
        if existing:
            return {
                'success': False,
                'error': f"Signer '{signer_id}' has already signed this document"
            }
        
        # Check expiration
        if request.expires_at and datetime.now() > request.expires_at:
            request.status = SignatureStatus.EXPIRED
            return {
                'success': False,
                'error': 'Signing request has expired'
            }
        
        # Create signature
        signature_id = f"sig_{signer_id}_{int(datetime.now().timestamp())}"
        
        signature = VideoSignature(
            signature_id=signature_id,
            signer_id=signer_id,
            document_id=request.document_id,
            video_url=video_url,
            duration=duration,
            ip_address=ip_address,
            device_info=device_info,
            location=location,
            metadata=metadata or {}
        )
        
        # Generate verification hash
        signature.verification_hash = signature.generate_verification_hash()
        
        # Add to request
        request.signatures.append(signature)
        request.status = SignatureStatus.IN_PROGRESS
        
        # Add audit entry
        request.add_audit_entry(
            action='signature_captured',
            actor_id=signer_id,
            details={
                'signature_id': signature_id,
                'duration': duration,
                'ip_address': ip_address
            }
        )
        
        # Store signature
        self.signatures[signature_id] = signature
        
        # Check if request is complete
        if request.is_complete():
            request.status = SignatureStatus.SIGNED
            request.completed_at = datetime.now()
            request.add_audit_entry(
                action='signing_completed',
                actor_id='system',
                details={'total_signatures': len(request.signatures)}
            )
            
            if self._on_request_completed:
                self._on_request_completed(request)
        
        # Trigger callback if set
        if self._on_signature_received:
            self._on_signature_received(signature)
        
        return {
            'success': True,
            'signature_id': signature_id,
            'verification_hash': signature.verification_hash,
            'request_complete': request.is_complete(),
            'remaining_signers': [
                s.signer_id for s in request.signers
                if s.signer_id not in {sig.signer_id for sig in request.signatures}
            ]
        }
    
    def verify_signature(
        self,
        signature_id: str,
        verifier_id: str
    ) -> Dict[str, Any]:
        """
        Verify a captured signature.
        
        Args:
            signature_id: ID of the signature to verify
            verifier_id: ID of the person verifying
            
        Returns:
            Verification result dictionary
        """
        signature = self.signatures.get(signature_id)
        if not signature:
            return {
                'success': False,
                'error': f"Signature '{signature_id}' not found"
            }
        
        # Find the associated request
        request = None
        for req in self.signing_requests.values():
            if any(s.signature_id == signature_id for s in req.signatures):
                request = req
                break
        
        # Verify hash
        expected_hash = signature.generate_verification_hash()
        hash_valid = signature.verification_hash == expected_hash
        
        if hash_valid:
            signature.verified_at = datetime.now()
            
            if request:
                request.add_audit_entry(
                    action='signature_verified',
                    actor_id=verifier_id,
                    details={
                        'signature_id': signature_id,
                        'verification_hash': signature.verification_hash
                    }
                )
        
        return {
            'success': hash_valid,
            'signature_id': signature_id,
            'hash_valid': hash_valid,
            'verified_at': signature.verified_at.isoformat() if signature.verified_at else None,
            'signer_id': signature.signer_id,
            'document_id': signature.document_id
        }
    
    def get_signing_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a signing request.
        
        Args:
            request_id: Signing request ID
            
        Returns:
            Request dictionary or None if not found
        """
        request = self.signing_requests.get(request_id)
        if request:
            return request.to_dict()
        return None
    
    def get_signature(self, signature_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a signature.
        
        Args:
            signature_id: Signature ID
            
        Returns:
            Signature dictionary or None if not found
        """
        signature = self.signatures.get(signature_id)
        if signature:
            return signature.to_dict()
        return None
    
    def cancel_signing_request(
        self,
        request_id: str,
        cancelled_by: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cancel a signing request.
        
        Args:
            request_id: Signing request ID
            cancelled_by: ID of user cancelling
            reason: Optional cancellation reason
            
        Returns:
            Cancellation result dictionary
        """
        request = self.signing_requests.get(request_id)
        if not request:
            return {
                'success': False,
                'error': f"Signing request '{request_id}' not found"
            }
        
        if request.status in [SignatureStatus.SIGNED, SignatureStatus.VERIFIED]:
            return {
                'success': False,
                'error': 'Cannot cancel a completed signing request'
            }
        
        request.status = SignatureStatus.CANCELLED
        request.add_audit_entry(
            action='request_cancelled',
            actor_id=cancelled_by,
            details={'reason': reason}
        )
        
        return {
            'success': True,
            'request_id': request_id,
            'status': 'cancelled'
        }
    
    def list_signing_requests(
        self,
        document_id: Optional[str] = None,
        signer_id: Optional[str] = None,
        status: Optional[SignatureStatus] = None
    ) -> List[Dict[str, Any]]:
        """
        List signing requests with optional filtering.
        
        Args:
            document_id: Filter by document ID
            signer_id: Filter by signer ID
            status: Filter by status
            
        Returns:
            List of signing request dictionaries
        """
        requests = list(self.signing_requests.values())
        
        if document_id:
            requests = [r for r in requests if r.document_id == document_id]
        
        if signer_id:
            requests = [
                r for r in requests
                if any(s.signer_id == signer_id for s in r.signers)
            ]
        
        if status:
            requests = [r for r in requests if r.status == status]
        
        return [r.to_dict() for r in requests]
    
    def get_audit_trail(self, request_id: str) -> List[Dict[str, Any]]:
        """
        Get the audit trail for a signing request.
        
        Args:
            request_id: Signing request ID
            
        Returns:
            List of audit trail entries
        """
        request = self.signing_requests.get(request_id)
        if request:
            return request.audit_trail
        return []
    
    def on_signature_received(self, callback: Callable[[VideoSignature], None]) -> None:
        """
        Register callback for when a signature is received.
        
        Args:
            callback: Function to call with the signature
        """
        self._on_signature_received = callback
    
    def on_request_completed(self, callback: Callable[[SigningRequest], None]) -> None:
        """
        Register callback for when a signing request is completed.
        
        Args:
            callback: Function to call with the request
        """
        self._on_request_completed = callback
    
    def generate_certificate(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Generate a signing certificate for a completed request.
        
        Args:
            request_id: Signing request ID
            
        Returns:
            Certificate dictionary or None if not complete
        """
        request = self.signing_requests.get(request_id)
        if not request or request.status != SignatureStatus.SIGNED:
            return None
        
        certificate = {
            'certificate_id': f"cert_{request_id}",
            'document_id': request.document_id,
            'document_title': request.document_title,
            'issued_at': datetime.now().isoformat(),
            'signatures': [
                {
                    'signer_id': sig.signer_id,
                    'signed_at': sig.captured_at.isoformat(),
                    'verification_hash': sig.verification_hash
                }
                for sig in request.signatures
            ],
            'verification_level': request.verification_level.value,
            'total_signers': len(request.signers),
            'audit_trail_hash': hashlib.sha256(
                json.dumps(request.audit_trail).encode()
            ).hexdigest()
        }
        
        return certificate
