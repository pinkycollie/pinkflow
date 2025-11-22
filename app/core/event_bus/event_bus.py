"""
Event Bus for event-driven architecture.
Enables clean cross-module communication.
"""
from typing import Callable, Dict, List
import logging


class EventBus:
    """
    Simple event bus implementation for pub/sub pattern.
    Allows modules to communicate without tight coupling.
    """
    
    def __init__(self):
        """Initialize event bus with empty subscriber registry."""
        self._subscribers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger(__name__)
    
    def subscribe(self, event_name: str, handler: Callable):
        """
        Subscribe to an event.
        
        Args:
            event_name: Name of the event to subscribe to
            handler: Callable to handle the event
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        
        self._subscribers[event_name].append(handler)
        self.logger.debug(f"Handler {handler.__name__} subscribed to {event_name}")
    
    def unsubscribe(self, event_name: str, handler: Callable):
        """
        Unsubscribe from an event.
        
        Args:
            event_name: Name of the event
            handler: Handler to remove
        """
        if event_name in self._subscribers:
            try:
                self._subscribers[event_name].remove(handler)
                self.logger.debug(f"Handler {handler.__name__} unsubscribed from {event_name}")
            except ValueError:
                pass
    
    def publish(self, event_name: str, **data):
        """
        Publish an event to all subscribers.
        
        Args:
            event_name: Name of the event
            **data: Event data to pass to handlers
        """
        if event_name not in self._subscribers:
            self.logger.debug(f"No subscribers for event: {event_name}")
            return
        
        self.logger.info(f"Publishing event: {event_name}")
        
        for handler in self._subscribers[event_name]:
            try:
                handler(**data)
            except Exception as e:
                self.logger.error(
                    f"Error in event handler {handler.__name__} "
                    f"for event {event_name}: {str(e)}"
                )
    
    def clear(self):
        """Clear all subscribers."""
        self._subscribers.clear()
    
    def get_subscribers(self, event_name: str = None) -> Dict[str, List[Callable]]:
        """
        Get subscribers for an event or all events.
        
        Args:
            event_name: Optional specific event name
            
        Returns:
            Dictionary of event names to handler lists
        """
        if event_name:
            return {event_name: self._subscribers.get(event_name, [])}
        return self._subscribers.copy()


# Global event bus instance
event_bus = EventBus()


# Common event names (can be extended by modules)
class Events:
    """Standard event names used across the application."""
    
    # User events
    USER_CREATED = 'user.created'
    USER_UPDATED = 'user.updated'
    USER_DELETED = 'user.deleted'
    USER_LOGIN = 'user.login'
    USER_LOGOUT = 'user.logout'
    
    # Video events
    VIDEO_UPLOADED = 'video.uploaded'
    VIDEO_PROCESSING_STARTED = 'video.processing.started'
    VIDEO_PROCESSING_COMPLETED = 'video.processing.completed'
    VIDEO_PROCESSING_FAILED = 'video.processing.failed'
    
    # Accessibility events
    PREFERENCES_UPDATED = 'preferences.updated'
    VISUAL_DENSITY_CHANGED = 'visual_density.changed'
    
    # Module events
    MODULE_LOADED = 'module.loaded'
    MODULE_UNLOADED = 'module.unloaded'
    MODULE_ERROR = 'module.error'
