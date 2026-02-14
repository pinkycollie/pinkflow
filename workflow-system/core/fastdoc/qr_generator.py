"""
FastDoc QR Code Generator Module

This module provides QR code generation functionality for linking
physical documents to their video versions for deaf user accessibility.

Features:
- QR code generation with video URL embedding
- Customizable QR code styling and branding
- Batch QR code generation for multiple documents
- Integration with document signing workflow
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import hashlib
import base64


class QRErrorCorrectionLevel(Enum):
    """QR code error correction levels."""
    LOW = "L"        # 7% recovery
    MEDIUM = "M"     # 15% recovery
    QUARTILE = "Q"   # 25% recovery
    HIGH = "H"       # 30% recovery


class QRFormat(Enum):
    """Output format for QR codes."""
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"


@dataclass
class QRCodeConfig:
    """Configuration for QR code generation."""
    size: int = 256  # pixels
    error_correction: QRErrorCorrectionLevel = QRErrorCorrectionLevel.MEDIUM
    format: QRFormat = QRFormat.PNG
    border: int = 4  # quiet zone in modules
    foreground_color: str = "#000000"
    background_color: str = "#FFFFFF"
    include_logo: bool = False
    logo_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'size': self.size,
            'error_correction': self.error_correction.value,
            'format': self.format.value,
            'border': self.border,
            'foreground_color': self.foreground_color,
            'background_color': self.background_color,
            'include_logo': self.include_logo,
            'logo_path': self.logo_path
        }


@dataclass
class QRCodeData:
    """Data embedded in a QR code for document linking."""
    document_id: str
    video_url: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    signature: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert QR data to dictionary."""
        return {
            'document_id': self.document_id,
            'video_url': self.video_url,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'signature': self.signature,
            'metadata': self.metadata
        }
    
    def to_json(self) -> str:
        """Convert QR data to JSON string for embedding."""
        return json.dumps(self.to_dict())
    
    def generate_checksum(self) -> str:
        """Generate a checksum for data integrity verification."""
        data_str = f"{self.document_id}:{self.video_url}:{self.created_at.isoformat()}"
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]


@dataclass
class GeneratedQRCode:
    """Represents a generated QR code."""
    qr_id: str
    document_id: str
    data: QRCodeData
    config: QRCodeConfig
    image_data: Optional[bytes] = None
    image_base64: Optional[str] = None
    file_path: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excludes binary data)."""
        return {
            'qr_id': self.qr_id,
            'document_id': self.document_id,
            'data': self.data.to_dict(),
            'config': self.config.to_dict(),
            'file_path': self.file_path,
            'has_image_data': self.image_data is not None,
            'created_at': self.created_at.isoformat()
        }


class QRGenerator:
    """
    Generator for creating QR codes that link documents to video versions.
    
    This class provides functionality for creating QR codes that enable
    deaf users to scan and access sign language video versions of documents.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize QR generator.
        
        Args:
            config: Configuration dictionary containing:
                - base_url: Base URL for video links
                - output_dir: Directory for saving QR codes
                - default_expiration_days: Default expiration for QR codes
                - signing_key: Key for signing QR data (optional)
        """
        self.config = config or {}
        self.base_url = self.config.get('base_url', 'https://fastdoc.example.com/video')
        self.output_dir = self.config.get('output_dir', '/tmp/fastdoc/qrcodes')
        self.default_expiration_days = self.config.get('default_expiration_days', 365)
        self.signing_key = self.config.get('signing_key')
        self.generated_codes: Dict[str, GeneratedQRCode] = {}
    
    def generate_video_url(self, document_id: str, additional_params: Optional[Dict[str, str]] = None) -> str:
        """
        Generate a video URL for a document.
        
        Args:
            document_id: Unique document identifier
            additional_params: Additional URL parameters
            
        Returns:
            Full video URL
        """
        url = f"{self.base_url}/{document_id}"
        
        if additional_params:
            params = '&'.join(f"{k}={v}" for k, v in additional_params.items())
            url = f"{url}?{params}"
        
        return url
    
    def create_qr_data(
        self,
        document_id: str,
        video_url: Optional[str] = None,
        expiration_days: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> QRCodeData:
        """
        Create QR code data for a document.
        
        Args:
            document_id: Unique document identifier
            video_url: Video URL (generated if not provided)
            expiration_days: Days until expiration
            metadata: Additional metadata to embed
            
        Returns:
            QRCodeData instance
        """
        if video_url is None:
            video_url = self.generate_video_url(document_id)
        
        created_at = datetime.now()
        expires_at = None
        
        if expiration_days is not None or self.default_expiration_days:
            days = expiration_days or self.default_expiration_days
            from datetime import timedelta
            expires_at = created_at + timedelta(days=days)
        
        qr_data = QRCodeData(
            document_id=document_id,
            video_url=video_url,
            created_at=created_at,
            expires_at=expires_at,
            metadata=metadata or {}
        )
        
        # Sign the data if signing key is available
        if self.signing_key:
            qr_data.signature = self._sign_data(qr_data)
        
        return qr_data
    
    def _sign_data(self, qr_data: QRCodeData) -> str:
        """
        Sign QR data for integrity verification.
        
        Args:
            qr_data: QR code data to sign
            
        Returns:
            Signature string
        """
        if not self.signing_key:
            return ""
        
        data_str = f"{qr_data.document_id}:{qr_data.video_url}:{self.signing_key}"
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def verify_signature(self, qr_data: QRCodeData) -> bool:
        """
        Verify the signature of QR data.
        
        Args:
            qr_data: QR code data to verify
            
        Returns:
            True if signature is valid
        """
        if not self.signing_key or not qr_data.signature:
            return False
        
        expected_signature = self._sign_data(qr_data)
        return qr_data.signature == expected_signature
    
    def generate_qr_code(
        self,
        document_id: str,
        video_url: Optional[str] = None,
        qr_config: Optional[QRCodeConfig] = None,
        metadata: Optional[Dict[str, Any]] = None,
        save_to_file: bool = False
    ) -> GeneratedQRCode:
        """
        Generate a QR code for a document.
        
        Args:
            document_id: Unique document identifier
            video_url: Video URL to embed
            qr_config: QR code configuration
            metadata: Additional metadata
            save_to_file: Whether to save QR code to file
            
        Returns:
            GeneratedQRCode instance
        """
        qr_id = f"qr_{document_id}_{int(datetime.now().timestamp())}"
        
        # Create QR data
        qr_data = self.create_qr_data(
            document_id=document_id,
            video_url=video_url,
            metadata=metadata
        )
        
        config = qr_config or QRCodeConfig()
        
        # Generate placeholder QR code
        # In production, this would use a QR library like qrcode or segno
        qr_code = GeneratedQRCode(
            qr_id=qr_id,
            document_id=document_id,
            data=qr_data,
            config=config
        )
        
        # Generate placeholder image data
        # This represents the base64 encoded QR image
        placeholder_data = self._generate_placeholder_qr(qr_data, config)
        qr_code.image_base64 = placeholder_data
        
        if save_to_file:
            qr_code.file_path = f"{self.output_dir}/{qr_id}.{config.format.value}"
        
        self.generated_codes[qr_id] = qr_code
        return qr_code
    
    def _generate_placeholder_qr(
        self,
        qr_data: QRCodeData,
        config: QRCodeConfig
    ) -> str:
        """
        Generate placeholder QR code data.
        
        In production, this would use actual QR code generation.
        
        Args:
            qr_data: Data to encode
            config: QR configuration
            
        Returns:
            Base64 encoded placeholder
        """
        # Create a simple placeholder that encodes the essential data
        placeholder = json.dumps({
            'type': 'fastdoc_qr',
            'document_id': qr_data.document_id,
            'video_url': qr_data.video_url,
            'checksum': qr_data.generate_checksum()
        })
        
        return base64.b64encode(placeholder.encode()).decode()
    
    def batch_generate(
        self,
        documents: List[Dict[str, Any]],
        qr_config: Optional[QRCodeConfig] = None
    ) -> List[GeneratedQRCode]:
        """
        Generate QR codes for multiple documents.
        
        Args:
            documents: List of document dictionaries with 'document_id' and optional 'video_url'
            qr_config: Shared QR configuration
            
        Returns:
            List of generated QR codes
        """
        results = []
        
        for doc in documents:
            document_id = doc.get('document_id')
            if not document_id:
                continue
            
            qr_code = self.generate_qr_code(
                document_id=document_id,
                video_url=doc.get('video_url'),
                qr_config=qr_config,
                metadata=doc.get('metadata')
            )
            results.append(qr_code)
        
        return results
    
    def get_qr_code(self, qr_id: str) -> Optional[GeneratedQRCode]:
        """
        Retrieve a generated QR code by ID.
        
        Args:
            qr_id: QR code identifier
            
        Returns:
            GeneratedQRCode or None if not found
        """
        return self.generated_codes.get(qr_id)
    
    def list_qr_codes(
        self,
        document_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List generated QR codes with optional filtering.
        
        Args:
            document_id: Filter by document ID
            
        Returns:
            List of QR code dictionaries
        """
        codes = list(self.generated_codes.values())
        
        if document_id:
            codes = [c for c in codes if c.document_id == document_id]
        
        return [c.to_dict() for c in codes]
    
    def decode_qr_data(self, encoded_data: str) -> Optional[Dict[str, Any]]:
        """
        Decode QR data from base64 encoded string.
        
        Args:
            encoded_data: Base64 encoded QR data
            
        Returns:
            Decoded data dictionary or None if invalid
        """
        try:
            decoded = base64.b64decode(encoded_data).decode()
            return json.loads(decoded)
        except (ValueError, json.JSONDecodeError):
            return None
    
    def is_expired(self, qr_data: QRCodeData) -> bool:
        """
        Check if QR code data has expired.
        
        Args:
            qr_data: QR code data to check
            
        Returns:
            True if expired, False otherwise
        """
        if qr_data.expires_at is None:
            return False
        return datetime.now() > qr_data.expires_at
