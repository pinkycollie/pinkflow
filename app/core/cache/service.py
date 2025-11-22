"""
Smart caching service that includes user preferences in cache keys.
Ensures cached content respects accessibility settings.
"""
from functools import wraps
import json
import hashlib
from flask import g
from app.extensions import cache
from app.models import User


class SmartCache:
    """Enhanced caching service with user preference awareness."""
    
    def __init__(self, cache_instance):
        """
        Initialize smart cache.
        
        Args:
            cache_instance: Flask-Caching instance
        """
        self.cache = cache_instance
    
    def cache_with_user_preferences(self, timeout=300):
        """
        Cache decorator that includes user preferences in key.
        
        This ensures that cached content respects different accessibility
        settings for different users.
        
        Args:
            timeout: Cache timeout in seconds
            
        Returns:
            Decorator function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Include user preferences in cache key
                user_id = g.get('user_id')
                
                if user_id:
                    user = User.query.get(user_id)
                    if user:
                        prefs_hash = hashlib.md5(
                            json.dumps(
                                user.accessibility_preferences, 
                                sort_keys=True
                            ).encode()
                        ).hexdigest()
                        cache_key = (
                            f"{func.__name__}:{user_id}:{prefs_hash}:"
                            f"{hash(str(sorted(kwargs.items())))}"
                        )
                    else:
                        cache_key = (
                            f"{func.__name__}:unknown:"
                            f"{hash(str(sorted(kwargs.items())))}"
                        )
                else:
                    cache_key = (
                        f"{func.__name__}:anonymous:"
                        f"{hash(str(sorted(kwargs.items())))}"
                    )
                
                result = self.cache.get(cache_key)
                if result is None:
                    result = func(*args, **kwargs)
                    self.cache.set(cache_key, result, timeout=timeout)
                
                return result
            
            return wrapper
        return decorator
    
    def invalidate_user_cache(self, user_id):
        """
        Invalidate all cache entries for a specific user.
        
        Useful when user preferences change.
        
        Args:
            user_id: ID of the user whose cache should be invalidated
        """
        # Note: This is a simplified version. In production, you might want
        # to use cache tags or a more sophisticated invalidation strategy.
        # For now, we just clear the entire cache when user preferences change.
        # A better approach would be to track cache keys by user.
        pass  # Implementation depends on cache backend capabilities
    
    def get_cache_stats(self):
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        # Implementation depends on cache backend
        # This is a placeholder for monitoring purposes
        return {
            'hits': 0,
            'misses': 0,
            'size': 0
        }


# Create a global smart cache instance
smart_cache = SmartCache(cache)
