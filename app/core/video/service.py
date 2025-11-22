"""
Async video service for processing sign language videos.
Uses Celery for background task processing.
"""
import os
import uuid
from celery import Celery
from flask import current_app
from app.models import User
from app.core.circuit_breaker import CircuitBreaker


def make_celery(app=None):
    """
    Create and configure Celery instance.
    
    Args:
        app: Flask application instance
        
    Returns:
        Configured Celery instance
    """
    celery = Celery(
        app.import_name if app else 'video_processing',
        broker=app.config['CELERY_BROKER_URL'] if app else None,
        backend=app.config['CELERY_RESULT_BACKEND'] if app else None
    )
    
    if app:
        celery.conf.update(app.config)
        
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        
        celery.Task = ContextTask
    
    return celery


# Global Celery instance (will be configured in app factory)
celery = Celery('video_processing')


class AsyncVideoService:
    """Service for asynchronous video processing."""
    
    def __init__(self):
        """Initialize async video service."""
        self.celery = celery
    
    @staticmethod
    @celery.task(bind=True)
    def process_sign_language_async(self, video_path, user_preferences):
        """
        Process sign language video asynchronously.
        
        This is a Celery task that processes videos in the background.
        
        Args:
            video_path: Path to the video file
            user_preferences: User's accessibility preferences
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Update task state
            self.update_state(state='PROCESSING', meta={'progress': 0})
            
            # Simulate video processing steps
            # In production, this would include:
            # - Video transcoding for different qualities
            # - Sign language recognition/analysis
            # - Subtitle generation
            # - Thumbnail creation
            
            # Step 1: Validate video
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            self.update_state(state='PROCESSING', meta={'progress': 25})
            
            # Step 2: Process based on preferences
            visual_density = user_preferences.get('visual_density', 3)
            
            # Adjust processing based on visual density
            processing_options = {
                'quality': 'high' if visual_density >= 4 else 'medium',
                'include_captions': True,
                'sign_language': user_preferences.get('preferred_sign_language', 'ASL')
            }
            
            self.update_state(state='PROCESSING', meta={'progress': 50})
            
            # Step 3: Generate output paths
            output_paths = {
                'processed_video': f"{video_path}.processed.mp4",
                'thumbnail': f"{video_path}.thumb.jpg",
                'captions': f"{video_path}.vtt"
            }
            
            self.update_state(state='PROCESSING', meta={'progress': 75})
            
            # Step 4: Complete processing
            result = {
                'status': 'completed',
                'video_path': video_path,
                'output_paths': output_paths,
                'processing_options': processing_options
            }
            
            self.update_state(state='SUCCESS', meta={'progress': 100})
            
            return result
            
        except Exception as e:
            self.update_state(state='FAILURE', meta={'error': str(e)})
            raise
    
    def queue_video_processing(self, video_file_path, user_id):
        """
        Queue video for background processing.
        
        Args:
            video_file_path: Path to the video file
            user_id: ID of the user who uploaded the video
            
        Returns:
            Dictionary with job information
        """
        user = User.query.get(user_id)
        if not user:
            return {
                'error': 'User not found',
                'status': 'failed'
            }
        
        # Queue the processing task
        job = self.process_sign_language_async.delay(
            video_file_path,
            user.accessibility_preferences
        )
        
        return {
            'job_id': job.id,
            'status': 'queued',
            'estimated_completion': 300  # seconds
        }
    
    def get_job_status(self, job_id):
        """
        Get the status of a video processing job.
        
        Args:
            job_id: Celery task ID
            
        Returns:
            Dictionary with job status and results
        """
        task = self.process_sign_language_async.AsyncResult(job_id)
        
        response = {
            'job_id': job_id,
            'state': task.state,
        }
        
        if task.state == 'PENDING':
            response['status'] = 'pending'
        elif task.state == 'PROCESSING':
            response['status'] = 'processing'
            response['progress'] = task.info.get('progress', 0)
        elif task.state == 'SUCCESS':
            response['status'] = 'completed'
            response['result'] = task.result
        elif task.state == 'FAILURE':
            response['status'] = 'failed'
            response['error'] = str(task.info)
        
        return response


class VideoService:
    """Synchronous video service for immediate operations."""
    
    circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
    
    @staticmethod
    @circuit_breaker
    def validate_video_upload(file, max_size_mb=100):
        """
        Validate a video upload.
        
        Args:
            file: File object from request
            max_size_mb: Maximum file size in megabytes
            
        Returns:
            Tuple of (valid, error_message)
        """
        if not file:
            return False, "No file provided"
        
        # Check file extension
        allowed_extensions = current_app.config.get(
            'VIDEO_ALLOWED_EXTENSIONS', 
            {'mp4', 'avi', 'mov', 'webm'}
        )
        
        filename = file.filename.lower()
        if not any(filename.endswith(f'.{ext}') for ext in allowed_extensions):
            return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        
        # Check file size (rough estimate from content length)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            return False, f"File too large. Maximum size: {max_size_mb}MB"
        
        return True, None
    
    @staticmethod
    def save_video(file, user_id):
        """
        Save an uploaded video file.
        
        Args:
            file: File object from request
            user_id: ID of the user uploading the video
            
        Returns:
            Path to saved file or None if failed
        """
        upload_folder = current_app.config.get('VIDEO_UPLOAD_FOLDER', '/tmp/videos')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate secure filename
        filename = f"{user_id}_{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        
        file.save(filepath)
        return filepath
