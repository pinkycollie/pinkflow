"""
PinkFlow Sign Language Feedback Workflow Module

This module provides workflow orchestration for sign language feedback processing,
including video upload, storage, processing, and notification.

Features:
- Video file validation and upload
- Cloud storage integration (AWS S3, Firebase Storage, etc.)
- Video processing workflows
- Real-time notification via PubSub
- Deaf-First accessibility considerations
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class FeedbackStatus(Enum):
    """Status of feedback processing."""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    DELETED = "deleted"


class VideoFormat(Enum):
    """Supported video formats."""
    MP4 = "mp4"
    MOV = "mov"
    WEBM = "webm"


@dataclass
class FeedbackMetadata:
    """Metadata for sign language feedback."""
    user_id: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    status: FeedbackStatus = FeedbackStatus.UPLOADING
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: float = 0.0
    file_size: int = 0
    resolution: Optional[str] = None
    codec: Optional[str] = None
    frame_rate: Optional[int] = None
    views: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            'user_id': self.user_id,
            'description': self.description,
            'tags': self.tags,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status.value,
            'video_url': self.video_url,
            'thumbnail_url': self.thumbnail_url,
            'duration': self.duration,
            'file_size': self.file_size,
            'resolution': self.resolution,
            'codec': self.codec,
            'frame_rate': self.frame_rate,
            'views': self.views
        }


class VideoValidator:
    """Validates video files for sign language feedback."""
    
    # File size limits
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    MIN_DURATION = 1.0  # 1 second
    MAX_DURATION = 300.0  # 5 minutes
    
    # Supported formats
    SUPPORTED_FORMATS = {'.mp4', '.mov', '.webm'}
    
    @classmethod
    def validate_file_size(cls, file_size: int) -> tuple[bool, Optional[str]]:
        """
        Validate file size.
        
        Args:
            file_size: Size of the file in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if file_size <= 0:
            return False, "File is empty"
        if file_size > cls.MAX_FILE_SIZE:
            return False, f"File size exceeds {cls.MAX_FILE_SIZE / (1024*1024):.0f}MB limit"
        return True, None
    
    @classmethod
    def validate_format(cls, filename: str) -> tuple[bool, Optional[str]]:
        """
        Validate file format.
        
        Args:
            filename: Name of the file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        extension = f'.{extension}'
        
        if extension not in cls.SUPPORTED_FORMATS:
            supported = ', '.join(cls.SUPPORTED_FORMATS)
            return False, f"Unsupported format. Supported formats: {supported}"
        return True, None
    
    @classmethod
    def validate_duration(cls, duration: float) -> tuple[bool, Optional[str]]:
        """
        Validate video duration.
        
        Args:
            duration: Duration in seconds
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if duration < cls.MIN_DURATION:
            return False, f"Video too short. Minimum duration: {cls.MIN_DURATION}s"
        if duration > cls.MAX_DURATION:
            return False, f"Video too long. Maximum duration: {cls.MAX_DURATION}s"
        return True, None
    
    @classmethod
    def validate_all(cls, filename: str, file_size: int, duration: Optional[float] = None) -> tuple[bool, List[str]]:
        """
        Validate all aspects of the video file.
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
            duration: Duration in seconds (optional)
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate format
        is_valid, error = cls.validate_format(filename)
        if not is_valid:
            errors.append(error)
        
        # Validate size
        is_valid, error = cls.validate_file_size(file_size)
        if not is_valid:
            errors.append(error)
        
        # Validate duration if provided
        if duration is not None:
            is_valid, error = cls.validate_duration(duration)
            if not is_valid:
                errors.append(error)
        
        return len(errors) == 0, errors


class CloudStorageAdapter:
    """
    Abstract adapter for cloud storage services.
    
    This can be extended to support different storage providers:
    - AWS S3
    - Firebase Storage
    - Google Cloud Storage
    - Azure Blob Storage
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize storage adapter.
        
        Args:
            config: Configuration dictionary containing credentials and settings
        """
        self.config = config
        self.provider = config.get('provider', 'local')
    
    def upload_video(self, file_path: str, feedback_id: str) -> Dict[str, str]:
        """
        Upload video to cloud storage.
        
        Args:
            file_path: Local path to the video file
            feedback_id: Unique identifier for the feedback
            
        Returns:
            Dictionary with 'video_url' and 'thumbnail_url'
        """
        # Placeholder implementation
        # In production, this would use actual cloud storage SDKs
        base_url = self.config.get('base_url', 'https://storage.example.com')
        return {
            'video_url': f"{base_url}/feedback/{feedback_id}/video.mp4",
            'thumbnail_url': f"{base_url}/feedback/{feedback_id}/thumbnail.jpg"
        }
    
    def delete_video(self, video_url: str) -> bool:
        """
        Delete video from cloud storage.
        
        Args:
            video_url: URL of the video to delete
            
        Returns:
            True if deletion was successful
        """
        # Placeholder implementation
        return True
    
    def generate_signed_url(self, video_url: str, expiration: int = 3600) -> str:
        """
        Generate a signed URL for secure video access.
        
        Args:
            video_url: URL of the video
            expiration: Expiration time in seconds
            
        Returns:
            Signed URL
        """
        # Placeholder implementation
        return f"{video_url}?token=signed_token&expires={expiration}"


class PubSubNotifier:
    """
    Real-time notification system using PubSub pattern.
    
    Integrates with Phoenix PubSub or similar real-time systems.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize PubSub notifier.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.enabled = config.get('enabled', True)
    
    def notify_upload(self, feedback_metadata: FeedbackMetadata) -> bool:
        """
        Notify admins of new feedback upload.
        
        Args:
            feedback_metadata: Metadata of the uploaded feedback
            
        Returns:
            True if notification was sent
        """
        if not self.enabled:
            return False
        
        # Placeholder implementation
        # In production, this would publish to actual PubSub channel
        notification = {
            'event': 'feedback:uploaded',
            'data': feedback_metadata.to_dict()
        }
        print(f"[PubSub] Publishing: {json.dumps(notification, indent=2)}")
        return True
    
    def notify_processing_complete(self, feedback_id: str, status: FeedbackStatus, metadata: Dict[str, Any]) -> bool:
        """
        Notify when video processing is complete.
        
        Args:
            feedback_id: ID of the feedback
            status: Processing status
            metadata: Additional metadata
            
        Returns:
            True if notification was sent
        """
        if not self.enabled:
            return False
        
        notification = {
            'event': 'feedback:processed',
            'data': {
                'feedback_id': feedback_id,
                'status': status.value,
                **metadata
            }
        }
        print(f"[PubSub] Publishing: {json.dumps(notification, indent=2)}")
        return True
    
    def notify_deletion(self, feedback_id: str, deleted_by: str) -> bool:
        """
        Notify when feedback is deleted.
        
        Args:
            feedback_id: ID of the feedback
            deleted_by: User ID who deleted it
            
        Returns:
            True if notification was sent
        """
        if not self.enabled:
            return False
        
        notification = {
            'event': 'feedback:deleted',
            'data': {
                'feedback_id': feedback_id,
                'deleted_by': deleted_by,
                'timestamp': datetime.now().isoformat()
            }
        }
        print(f"[PubSub] Publishing: {json.dumps(notification, indent=2)}")
        return True


class FeedbackWorkflowOrchestrator:
    """
    Orchestrates the complete workflow for sign language feedback.
    
    Workflow stages:
    1. Validation
    2. Upload to cloud storage
    3. Video processing (transcoding, thumbnail generation)
    4. Database storage
    5. Real-time notification
    """
    
    def __init__(self, storage_config: Dict[str, Any], pubsub_config: Dict[str, Any]):
        """
        Initialize workflow orchestrator.
        
        Args:
            storage_config: Configuration for cloud storage
            pubsub_config: Configuration for PubSub notifications
        """
        self.storage = CloudStorageAdapter(storage_config)
        self.pubsub = PubSubNotifier(pubsub_config)
        self.validator = VideoValidator()
    
    def process_upload(self, 
                      file_path: str, 
                      filename: str, 
                      file_size: int,
                      user_id: str,
                      description: Optional[str] = None,
                      tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Process a new feedback upload.
        
        Args:
            file_path: Path to the uploaded file
            filename: Original filename
            file_size: File size in bytes
            user_id: ID of the user uploading
            description: Optional description
            tags: Optional tags
            
        Returns:
            Dictionary with processing result
        """
        # Initialize feedback metadata
        feedback_metadata = FeedbackMetadata(
            user_id=user_id,
            description=description,
            tags=tags or [],
            file_size=file_size
        )
        
        # Step 1: Validate
        is_valid, errors = self.validator.validate_all(filename, file_size)
        if not is_valid:
            feedback_metadata.status = FeedbackStatus.FAILED
            return {
                'success': False,
                'errors': errors,
                'metadata': feedback_metadata.to_dict()
            }
        
        # Step 2: Upload to cloud storage
        try:
            feedback_id = f"feedback_{user_id}_{int(datetime.now().timestamp())}"
            storage_result = self.storage.upload_video(file_path, feedback_id)
            
            feedback_metadata.video_url = storage_result['video_url']
            feedback_metadata.thumbnail_url = storage_result['thumbnail_url']
            feedback_metadata.status = FeedbackStatus.PROCESSING
            
        except Exception as e:
            feedback_metadata.status = FeedbackStatus.FAILED
            return {
                'success': False,
                'errors': [f"Upload failed: {str(e)}"],
                'metadata': feedback_metadata.to_dict()
            }
        
        # Step 3: Notify admins via PubSub
        self.pubsub.notify_upload(feedback_metadata)
        
        # Step 4: Queue for video processing
        # In production, this would trigger async video processing
        # (transcoding, thumbnail generation, duration extraction)
        
        feedback_metadata.status = FeedbackStatus.READY
        
        # Notify processing complete
        self.pubsub.notify_processing_complete(
            feedback_id,
            FeedbackStatus.READY,
            {
                'video_url': feedback_metadata.video_url,
                'thumbnail_url': feedback_metadata.thumbnail_url
            }
        )
        
        return {
            'success': True,
            'feedback_id': feedback_id,
            'metadata': feedback_metadata.to_dict()
        }
    
    def delete_feedback(self, feedback_id: str, video_url: str, deleted_by: str) -> Dict[str, Any]:
        """
        Delete feedback and associated video.
        
        Args:
            feedback_id: ID of the feedback to delete
            video_url: URL of the video to delete
            deleted_by: User ID performing deletion
            
        Returns:
            Dictionary with deletion result
        """
        try:
            # Delete from storage
            self.storage.delete_video(video_url)
            
            # Notify deletion
            self.pubsub.notify_deletion(feedback_id, deleted_by)
            
            return {
                'success': True,
                'feedback_id': feedback_id,
                'deleted_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Database schema documentation (to be implemented in actual database)
DATABASE_SCHEMA = """
-- Sign Language Feedback Table
CREATE TABLE sign_language_feedback (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    video_url TEXT NOT NULL,
    thumbnail_url TEXT,
    description TEXT,
    tags TEXT[],
    status VARCHAR(50) NOT NULL DEFAULT 'processing',
    duration FLOAT DEFAULT 0,
    file_size BIGINT DEFAULT 0,
    resolution VARCHAR(50),
    codec VARCHAR(50),
    frame_rate INTEGER,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_tags (tags)
);

-- Feedback Views Table (for analytics)
CREATE TABLE feedback_views (
    id SERIAL PRIMARY KEY,
    feedback_id VARCHAR(255) NOT NULL,
    viewer_id VARCHAR(255),
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_feedback
        FOREIGN KEY(feedback_id)
        REFERENCES sign_language_feedback(id)
        ON DELETE CASCADE
);
"""


# Configuration examples
EXAMPLE_AWS_S3_CONFIG = {
    'provider': 'aws_s3',
    'bucket': 'pinkflow-feedback',
    'region': 'us-east-1',
    'access_key_id': 'YOUR_ACCESS_KEY',
    'secret_access_key': 'YOUR_SECRET_KEY',
    'base_url': 'https://pinkflow-feedback.s3.amazonaws.com'
}

EXAMPLE_FIREBASE_CONFIG = {
    'provider': 'firebase',
    'bucket': 'pinkflow-feedback.appspot.com',
    'credentials_path': '/path/to/firebase-credentials.json',
    'base_url': 'https://firebasestorage.googleapis.com'
}

EXAMPLE_PUBSUB_CONFIG = {
    'enabled': True,
    'type': 'phoenix_pubsub',  # or 'redis_pubsub', 'kafka', etc.
    'channel': 'feedback:notifications',
    'admin_channel': 'admin:notifications'
}
