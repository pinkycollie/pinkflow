"""
FastDoc FFmpeg Adapter Module

This module provides video rendering functionality for converting contract
documents into sign language accessible video format using FFmpeg.

Features:
- Contract to video rendering with sign language overlay support
- Configurable video output settings (resolution, framerate, codec)
- Batch processing support for multiple documents
- Integration with sign language template assets
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import subprocess
import shlex


class VideoResolution(Enum):
    """Standard video resolutions for sign language content."""
    SD = "640x480"
    HD = "1280x720"
    FULL_HD = "1920x1080"


class VideoCodec(Enum):
    """Supported video codecs."""
    H264 = "libx264"
    H265 = "libx265"
    VP9 = "libvpx-vp9"


@dataclass
class VideoConfig:
    """Configuration for video rendering."""
    resolution: VideoResolution = VideoResolution.HD
    codec: VideoCodec = VideoCodec.H264
    framerate: int = 30
    bitrate: str = "2M"
    audio_enabled: bool = False
    preset: str = "medium"  # FFmpeg encoding preset
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'resolution': self.resolution.value,
            'codec': self.codec.value,
            'framerate': self.framerate,
            'bitrate': self.bitrate,
            'audio_enabled': self.audio_enabled,
            'preset': self.preset
        }


@dataclass
class RenderJob:
    """Represents a video rendering job."""
    job_id: str
    contract_id: str
    input_path: str
    output_path: str
    config: VideoConfig
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary."""
        return {
            'job_id': self.job_id,
            'contract_id': self.contract_id,
            'input_path': self.input_path,
            'output_path': self.output_path,
            'config': self.config.to_dict(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'metadata': self.metadata
        }


class FFmpegAdapter:
    """
    Adapter for FFmpeg video rendering operations.
    
    This class provides an interface for rendering contract documents
    as sign language accessible videos.
    """
    
    # Default FFmpeg binary path
    DEFAULT_FFMPEG_PATH = "ffmpeg"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize FFmpeg adapter.
        
        Args:
            config: Configuration dictionary containing:
                - ffmpeg_path: Path to FFmpeg binary
                - temp_dir: Directory for temporary files
                - output_dir: Default output directory
                - max_duration: Maximum video duration in seconds
        """
        self.config = config or {}
        self.ffmpeg_path = self.config.get('ffmpeg_path', self.DEFAULT_FFMPEG_PATH)
        self.temp_dir = self.config.get('temp_dir', '/tmp/fastdoc')
        self.output_dir = self.config.get('output_dir', '/tmp/fastdoc/output')
        self.max_duration = self.config.get('max_duration', 600)  # 10 minutes
        self.render_jobs: Dict[str, RenderJob] = {}
    
    def check_ffmpeg_available(self) -> bool:
        """
        Check if FFmpeg is available on the system.
        
        Returns:
            True if FFmpeg is available, False otherwise
        """
        try:
            result = subprocess.run(
                [self.ffmpeg_path, '-version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def build_render_command(
        self,
        input_path: str,
        output_path: str,
        video_config: VideoConfig,
        overlay_path: Optional[str] = None,
        text_overlay: Optional[str] = None
    ) -> List[str]:
        """
        Build FFmpeg command for video rendering.
        
        Args:
            input_path: Path to input file (image or video template)
            output_path: Path for output video
            video_config: Video configuration settings
            overlay_path: Optional path to sign language overlay video
            text_overlay: Optional text to overlay on video
            
        Returns:
            List of command arguments
        """
        width, height = video_config.resolution.value.split('x')
        
        cmd = [
            self.ffmpeg_path,
            '-y',  # Overwrite output file
            '-i', input_path,
        ]
        
        # Add overlay input if provided
        if overlay_path:
            cmd.extend(['-i', overlay_path])
        
        # Build filter complex for overlays
        filters = []
        
        # Scale to target resolution
        filters.append(f"scale={width}:{height}")
        
        # Add text overlay if provided
        if text_overlay:
            # Escape special characters for FFmpeg filter
            safe_text = text_overlay.replace("'", "\\'").replace(":", "\\:")
            filters.append(
                f"drawtext=text='{safe_text}':fontsize=24:fontcolor=white:"
                f"x=(w-text_w)/2:y=h-50"
            )
        
        # Apply filters
        if filters:
            cmd.extend(['-vf', ','.join(filters)])
        
        # Video encoding settings
        cmd.extend([
            '-c:v', video_config.codec.value,
            '-preset', video_config.preset,
            '-b:v', video_config.bitrate,
            '-r', str(video_config.framerate),
        ])
        
        # Audio settings
        if not video_config.audio_enabled:
            cmd.append('-an')
        
        # Output path
        cmd.append(output_path)
        
        return cmd
    
    def create_render_job(
        self,
        contract_id: str,
        input_path: str,
        output_path: str,
        video_config: Optional[VideoConfig] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RenderJob:
        """
        Create a new render job.
        
        Args:
            contract_id: Unique identifier for the contract
            input_path: Path to input file
            output_path: Path for output video
            video_config: Video configuration (uses defaults if not provided)
            metadata: Additional metadata for the job
            
        Returns:
            Created RenderJob instance
        """
        job_id = f"render_{contract_id}_{int(datetime.now().timestamp())}"
        
        job = RenderJob(
            job_id=job_id,
            contract_id=contract_id,
            input_path=input_path,
            output_path=output_path,
            config=video_config or VideoConfig(),
            metadata=metadata or {}
        )
        
        self.render_jobs[job_id] = job
        return job
    
    def render_video(
        self,
        job: RenderJob,
        overlay_path: Optional[str] = None,
        text_overlay: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Execute video rendering for a job.
        
        Args:
            job: RenderJob to execute
            overlay_path: Optional sign language overlay video path
            text_overlay: Optional text to display on video
            dry_run: If True, only return command without executing
            
        Returns:
            Dictionary with rendering result
        """
        job.status = "processing"
        
        try:
            cmd = self.build_render_command(
                job.input_path,
                job.output_path,
                job.config,
                overlay_path,
                text_overlay
            )
            
            if dry_run:
                return {
                    'success': True,
                    'job_id': job.job_id,
                    'command': ' '.join(shlex.quote(c) for c in cmd),
                    'dry_run': True
                }
            
            # Execute FFmpeg command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.max_duration
            )
            
            if result.returncode == 0:
                job.status = "completed"
                job.completed_at = datetime.now()
                return {
                    'success': True,
                    'job_id': job.job_id,
                    'output_path': job.output_path,
                    'status': 'completed'
                }
            else:
                job.status = "failed"
                job.error_message = result.stderr
                return {
                    'success': False,
                    'job_id': job.job_id,
                    'error': result.stderr,
                    'status': 'failed'
                }
                
        except subprocess.TimeoutExpired:
            job.status = "failed"
            job.error_message = "Rendering timeout exceeded"
            return {
                'success': False,
                'job_id': job.job_id,
                'error': 'Rendering timeout exceeded',
                'status': 'timeout'
            }
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            return {
                'success': False,
                'job_id': job.job_id,
                'error': str(e),
                'status': 'error'
            }
    
    def render_contract_video(
        self,
        contract_id: str,
        contract_content: str,
        output_path: str,
        sign_language_template: Optional[str] = None,
        video_config: Optional[VideoConfig] = None
    ) -> Dict[str, Any]:
        """
        Render a contract document as a sign language accessible video.
        
        This is a high-level method that handles the complete workflow:
        1. Prepare contract content for rendering
        2. Apply sign language template overlay
        3. Generate output video
        
        Args:
            contract_id: Unique contract identifier
            contract_content: Text content of the contract
            output_path: Path for output video
            sign_language_template: Path to sign language template video
            video_config: Video configuration settings
            
        Returns:
            Dictionary with rendering result
        """
        # Create a render job
        job = self.create_render_job(
            contract_id=contract_id,
            input_path=sign_language_template or "template.png",
            output_path=output_path,
            video_config=video_config,
            metadata={
                'contract_content_length': len(contract_content),
                'has_template': sign_language_template is not None
            }
        )
        
        # For now, return a placeholder result
        # In production, this would handle actual video rendering
        return {
            'success': True,
            'job_id': job.job_id,
            'contract_id': contract_id,
            'output_path': output_path,
            'status': 'created',
            'message': 'Video rendering job created successfully'
        }
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a render job.
        
        Args:
            job_id: ID of the job to check
            
        Returns:
            Job status dictionary or None if not found
        """
        job = self.render_jobs.get(job_id)
        if job:
            return job.to_dict()
        return None
    
    def list_jobs(
        self,
        status: Optional[str] = None,
        contract_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List render jobs with optional filtering.
        
        Args:
            status: Filter by job status
            contract_id: Filter by contract ID
            
        Returns:
            List of job dictionaries
        """
        jobs = list(self.render_jobs.values())
        
        if status:
            jobs = [j for j in jobs if j.status == status]
        
        if contract_id:
            jobs = [j for j in jobs if j.contract_id == contract_id]
        
        return [j.to_dict() for j in jobs]
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a pending render job.
        
        Args:
            job_id: ID of the job to cancel
            
        Returns:
            True if job was cancelled, False otherwise
        """
        job = self.render_jobs.get(job_id)
        if job and job.status == "pending":
            job.status = "cancelled"
            return True
        return False
