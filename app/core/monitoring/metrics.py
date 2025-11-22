"""
Accessibility-focused monitoring and metrics tracking.
Tracks performance and quality metrics for accessibility features.
"""
import time
from datetime import datetime
from collections import defaultdict
from threading import Lock


class AccessibilityMetrics:
    """Service for tracking accessibility-specific metrics."""
    
    def __init__(self):
        """Initialize metrics storage."""
        self._metrics = defaultdict(list)
        self._lock = Lock()
    
    def track_video_performance(self, user_id, video_type, load_time):
        """
        Track video loading performance for accessibility.
        
        Important for users who rely on video content for sign language.
        
        Args:
            user_id: ID of the user
            video_type: Type of video (e.g., 'sign_language', 'tutorial')
            load_time: Time in seconds to load the video
        """
        with self._lock:
            self._metrics['video_performance'].append({
                'user_id': user_id,
                'video_type': video_type,
                'load_time': load_time,
                'timestamp': datetime.utcnow()
            })
    
    def track_sign_language_accuracy(self, user_id, translation_id, user_feedback):
        """
        Track sign language translation accuracy based on user feedback.
        
        Args:
            user_id: ID of the user
            translation_id: ID of the translation
            user_feedback: User's feedback (e.g., 'accurate', 'inaccurate', 'helpful')
        """
        with self._lock:
            self._metrics['sign_language_accuracy'].append({
                'user_id': user_id,
                'translation_id': translation_id,
                'feedback': user_feedback,
                'timestamp': datetime.utcnow()
            })
    
    def track_visual_density_usage(self, user_id, density_level):
        """
        Track visual density preferences usage.
        
        Args:
            user_id: ID of the user
            density_level: Visual density level (1-5)
        """
        with self._lock:
            self._metrics['visual_density'].append({
                'user_id': user_id,
                'density_level': density_level,
                'timestamp': datetime.utcnow()
            })
    
    def track_reading_level_usage(self, user_id, reading_level):
        """
        Track reading level preferences.
        
        Args:
            user_id: ID of the user
            reading_level: Reading level (1-5)
        """
        with self._lock:
            self._metrics['reading_level'].append({
                'user_id': user_id,
                'reading_level': reading_level,
                'timestamp': datetime.utcnow()
            })
    
    def track_page_load_time(self, user_id, page, load_time, accessibility_features):
        """
        Track page load times with accessibility features enabled.
        
        Args:
            user_id: ID of the user
            page: Page identifier
            load_time: Load time in seconds
            accessibility_features: List of enabled accessibility features
        """
        with self._lock:
            self._metrics['page_load'].append({
                'user_id': user_id,
                'page': page,
                'load_time': load_time,
                'accessibility_features': accessibility_features,
                'timestamp': datetime.utcnow()
            })
    
    def get_metrics(self, metric_type=None):
        """
        Get collected metrics.
        
        Args:
            metric_type: Optional specific metric type to retrieve
            
        Returns:
            Dictionary of metrics
        """
        with self._lock:
            if metric_type:
                return {metric_type: self._metrics.get(metric_type, [])}
            return dict(self._metrics)
    
    def get_average_video_load_time(self, video_type=None):
        """
        Calculate average video load time.
        
        Args:
            video_type: Optional filter by video type
            
        Returns:
            Average load time in seconds
        """
        with self._lock:
            metrics = self._metrics.get('video_performance', [])
            
            if video_type:
                metrics = [m for m in metrics if m['video_type'] == video_type]
            
            if not metrics:
                return 0
            
            total_time = sum(m['load_time'] for m in metrics)
            return total_time / len(metrics)
    
    def get_sign_language_accuracy_rate(self):
        """
        Calculate sign language accuracy rate based on user feedback.
        
        Returns:
            Accuracy rate as a percentage
        """
        with self._lock:
            metrics = self._metrics.get('sign_language_accuracy', [])
            
            if not metrics:
                return 0
            
            accurate_count = sum(
                1 for m in metrics 
                if m['feedback'] in ['accurate', 'helpful']
            )
            
            return (accurate_count / len(metrics)) * 100
    
    def clear_old_metrics(self, days=7):
        """
        Clear metrics older than specified days.
        
        Args:
            days: Number of days to keep
        """
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        with self._lock:
            for metric_type in self._metrics:
                self._metrics[metric_type] = [
                    m for m in self._metrics[metric_type]
                    if m['timestamp'] > cutoff_date
                ]


# Global metrics instance
accessibility_metrics = AccessibilityMetrics()


class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, metric_name=None):
        """
        Initialize performance timer.
        
        Args:
            metric_name: Optional name for the metric
        """
        self.metric_name = metric_name
        self.start_time = None
        self.end_time = None
        self.duration = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing and calculate duration."""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        
        if self.metric_name:
            # Could log or track this metric
            pass
        
        return False
    
    def get_duration(self):
        """Get duration in seconds."""
        return self.duration
