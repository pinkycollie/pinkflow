"""
PinkFlow PubSub Broadcasting Service

Provides real-time broadcasting and subscription functionality for:
- Test container results and status updates
- Voting and feedback events
- Visual notifications for DeafAuth/PinkSync
- IoT device notifications (including Vibration API)
"""

from typing import Dict, List, Set, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import json
from collections import defaultdict


class EventType(Enum):
    """Types of events that can be broadcast"""
    TEST_STARTED = "test_started"
    TEST_PROGRESS = "test_progress"
    TEST_COMPLETED = "test_completed"
    TEST_FAILED = "test_failed"
    VOTE_CAST = "vote_cast"
    VOTE_UPDATED = "vote_updated"
    FEEDBACK_SUBMITTED = "feedback_submitted"
    NOTIFICATION = "notification"
    IOT_ALERT = "iot_alert"


class NotificationPriority(Enum):
    """Priority levels for notifications"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Event:
    """Base event structure"""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: NotificationPriority = NotificationPriority.NORMAL
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            'event_type': self.event_type.value,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority.value
        }
    
    def to_json(self) -> str:
        """Convert event to JSON string"""
        return json.dumps(self.to_dict())


@dataclass
class Subscriber:
    """Represents a subscriber to events"""
    id: str
    topics: Set[str] = field(default_factory=set)
    callback: Optional[Callable] = None
    iot_enabled: bool = False
    vibration_enabled: bool = False
    visual_only: bool = True  # Deaf-First: visual notifications by default
    
    def matches_topic(self, topic: str) -> bool:
        """Check if subscriber is interested in topic"""
        if '*' in self.topics:  # Wildcard subscription
            return True
        return topic in self.topics


class PubSubService:
    """
    PubSub service for real-time broadcasting and notifications.
    
    Deaf-First Design:
    - Visual notifications prioritized
    - No audio dependencies
    - Vibration API support for IoT devices
    - Clear, persistent banners for important events
    """
    
    def __init__(self):
        self.subscribers: Dict[str, Subscriber] = {}
        self.event_history: List[Event] = []
        self.topic_subscribers: Dict[str, Set[str]] = defaultdict(set)
        self.max_history = 1000
        
    def subscribe(
        self,
        subscriber_id: str,
        topics: List[str],
        callback: Optional[Callable] = None,
        iot_enabled: bool = False,
        vibration_enabled: bool = False
    ) -> Subscriber:
        """
        Subscribe to one or more topics.
        
        Args:
            subscriber_id: Unique identifier for subscriber
            topics: List of topics to subscribe to
            callback: Optional callback function for events
            iot_enabled: Enable IoT device notifications
            vibration_enabled: Enable vibration alerts
            
        Returns:
            Subscriber object
        """
        subscriber = Subscriber(
            id=subscriber_id,
            topics=set(topics),
            callback=callback,
            iot_enabled=iot_enabled,
            vibration_enabled=vibration_enabled
        )
        
        self.subscribers[subscriber_id] = subscriber
        
        # Register subscriber for each topic
        for topic in topics:
            self.topic_subscribers[topic].add(subscriber_id)
        
        return subscriber
    
    def unsubscribe(self, subscriber_id: str, topics: Optional[List[str]] = None):
        """
        Unsubscribe from topics or remove subscriber entirely.
        
        Args:
            subscriber_id: Subscriber to unsubscribe
            topics: Specific topics to unsubscribe from, or None for all
        """
        if subscriber_id not in self.subscribers:
            return
        
        if topics is None:
            # Remove from all topics
            subscriber = self.subscribers[subscriber_id]
            for topic in subscriber.topics:
                self.topic_subscribers[topic].discard(subscriber_id)
            del self.subscribers[subscriber_id]
        else:
            # Remove from specific topics
            subscriber = self.subscribers[subscriber_id]
            for topic in topics:
                subscriber.topics.discard(topic)
                self.topic_subscribers[topic].discard(subscriber_id)
    
    async def publish(
        self,
        topic: str,
        event_type: EventType,
        data: Dict[str, Any],
        priority: NotificationPriority = NotificationPriority.NORMAL
    ):
        """
        Publish an event to a topic.
        
        Args:
            topic: Topic to publish to
            event_type: Type of event
            data: Event data
            priority: Notification priority
        """
        event = Event(
            event_type=event_type,
            data=data,
            priority=priority
        )
        
        # Store in history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        # Notify subscribers
        await self._notify_subscribers(topic, event)
    
    async def _notify_subscribers(self, topic: str, event: Event):
        """Notify all subscribers of a topic"""
        # Get direct subscribers to this topic
        subscriber_ids = self.topic_subscribers.get(topic, set()).copy()
        
        # Add wildcard subscribers
        wildcard_subscribers = self.topic_subscribers.get('*', set())
        subscriber_ids.update(wildcard_subscribers)
        
        for subscriber_id in subscriber_ids:
            subscriber = self.subscribers.get(subscriber_id)
            if subscriber and subscriber.matches_topic(topic):
                await self._send_to_subscriber(subscriber, event)
    
    async def _send_to_subscriber(self, subscriber: Subscriber, event: Event):
        """Send event to a specific subscriber"""
        # Visual notification (always enabled for Deaf-First)
        if subscriber.visual_only:
            await self._send_visual_notification(subscriber, event)
        
        # IoT notification if enabled
        if subscriber.iot_enabled:
            await self._send_iot_notification(subscriber, event)
        
        # Vibration alert if enabled
        if subscriber.vibration_enabled:
            await self._send_vibration_alert(subscriber, event)
        
        # Call custom callback if provided
        if subscriber.callback:
            try:
                if asyncio.iscoroutinefunction(subscriber.callback):
                    await subscriber.callback(event)
                else:
                    subscriber.callback(event)
            except Exception as e:
                print(f"Error in subscriber callback: {e}")
    
    async def _send_visual_notification(self, subscriber: Subscriber, event: Event):
        """Send visual banner notification"""
        # Implementation would integrate with frontend notification system
        notification = {
            'subscriber_id': subscriber.id,
            'type': 'visual_banner',
            'event': event.to_dict(),
            'display_duration': self._get_display_duration(event.priority),
            'style': self._get_notification_style(event.priority)
        }
        # Store notification for frontend polling or WebSocket delivery
        pass
    
    async def _send_iot_notification(self, subscriber: Subscriber, event: Event):
        """Send notification to IoT device"""
        # Implementation would integrate with IoT platform
        iot_message = {
            'device_id': subscriber.id,
            'event_type': event.event_type.value,
            'priority': event.priority.value,
            'data': event.data,
            'timestamp': event.timestamp.isoformat()
        }
        # Send to IoT platform/broker
        pass
    
    async def _send_vibration_alert(self, subscriber: Subscriber, event: Event):
        """Send vibration alert using Vibration API"""
        # Implementation for Vibration API
        vibration_pattern = self._get_vibration_pattern(event.priority)
        alert = {
            'device_id': subscriber.id,
            'pattern': vibration_pattern,
            'event_type': event.event_type.value
        }
        # Trigger vibration on IoT device
        pass
    
    def _get_display_duration(self, priority: NotificationPriority) -> int:
        """Get notification display duration based on priority"""
        durations = {
            NotificationPriority.LOW: 3000,      # 3 seconds
            NotificationPriority.NORMAL: 5000,   # 5 seconds
            NotificationPriority.HIGH: 10000,    # 10 seconds
            NotificationPriority.URGENT: 0       # Persistent until dismissed
        }
        return durations.get(priority, 5000)
    
    def _get_notification_style(self, priority: NotificationPriority) -> Dict[str, str]:
        """Get visual styling based on priority"""
        styles = {
            NotificationPriority.LOW: {
                'color': 'blue',
                'icon': 'ℹ️',
                'animation': 'fade'
            },
            NotificationPriority.NORMAL: {
                'color': 'green',
                'icon': '✓',
                'animation': 'slide'
            },
            NotificationPriority.HIGH: {
                'color': 'orange',
                'icon': '⚠️',
                'animation': 'bounce'
            },
            NotificationPriority.URGENT: {
                'color': 'red',
                'icon': '🚨',
                'animation': 'pulse'
            }
        }
        return styles.get(priority, styles[NotificationPriority.NORMAL])
    
    def _get_vibration_pattern(self, priority: NotificationPriority) -> List[int]:
        """
        Get vibration pattern based on priority.
        Pattern format: [vibrate_ms, pause_ms, vibrate_ms, ...]
        """
        patterns = {
            NotificationPriority.LOW: [100],                    # Single short
            NotificationPriority.NORMAL: [200, 100, 200],       # Double
            NotificationPriority.HIGH: [300, 100, 300, 100, 300],  # Triple
            NotificationPriority.URGENT: [500, 200, 500, 200, 500, 200, 500]  # Intense
        }
        return patterns.get(priority, [200])
    
    def get_history(
        self,
        topic: Optional[str] = None,
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[Event]:
        """
        Get event history.
        
        Args:
            topic: Filter by topic
            event_type: Filter by event type
            limit: Maximum number of events to return
            
        Returns:
            List of events
        """
        filtered_events = self.event_history
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.event_type == event_type]
        
        return filtered_events[-limit:]
    
    def get_subscriber_count(self, topic: str) -> int:
        """Get number of subscribers for a topic"""
        return len(self.topic_subscribers.get(topic, set()))


# Global instance
_pubsub_service: Optional[PubSubService] = None


def get_pubsub_service() -> PubSubService:
    """Get or create global PubSub service instance"""
    global _pubsub_service
    if _pubsub_service is None:
        _pubsub_service = PubSubService()
    return _pubsub_service
