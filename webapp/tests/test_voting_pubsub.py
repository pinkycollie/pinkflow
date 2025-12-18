#!/usr/bin/env python3
"""
Tests for Voting and PubSub Services
"""

import pytest
import asyncio
from datetime import datetime
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from backend.voting_service import (
    VotingService, VoteType, VotableItemType, get_voting_service
)
from backend.pubsub_service import (
    PubSubService, EventType, NotificationPriority, get_pubsub_service
)


class TestVotingService:
    """Test voting service functionality"""

    def test_cast_vote(self):
        """Test casting a vote"""
        voting_service = VotingService()
        
        result = voting_service.cast_vote(
            user_id="user1",
            item_id="test1",
            item_type=VotableItemType.MODEL_TEST,
            vote_type=VoteType.UPVOTE
        )
        
        assert result['item_id'] == "test1"
        assert result['upvotes'] == 1
        assert result['total_votes'] == 1
        assert result['score'] > 0

    def test_update_vote(self):
        """Test updating an existing vote"""
        voting_service = VotingService()
        
        # Cast initial vote
        voting_service.cast_vote(
            user_id="user1",
            item_id="test1",
            item_type=VotableItemType.MODEL_TEST,
            vote_type=VoteType.UPVOTE
        )
        
        # Update to downvote
        result = voting_service.cast_vote(
            user_id="user1",
            item_id="test1",
            item_type=VotableItemType.MODEL_TEST,
            vote_type=VoteType.DOWNVOTE
        )
        
        assert result['upvotes'] == 0
        assert result['downvotes'] == 1
        assert result['total_votes'] == 1

    def test_remove_vote(self):
        """Test removing a vote"""
        voting_service = VotingService()
        
        # Cast vote
        voting_service.cast_vote(
            user_id="user1",
            item_id="test1",
            item_type=VotableItemType.MODEL_TEST,
            vote_type=VoteType.UPVOTE
        )
        
        # Remove vote
        result = voting_service.remove_vote("user1", "test1")
        
        assert result is not None
        assert result['upvotes'] == 0
        assert result['total_votes'] == 0

    def test_vote_privacy(self):
        """Test that vote summaries don't expose user info"""
        voting_service = VotingService()
        
        # Multiple users vote
        voting_service.cast_vote("user1", "test1", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user2", "test1", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user3", "test1", VotableItemType.MODEL_TEST, VoteType.DOWNVOTE)
        
        # Get public summary
        summary = voting_service.get_vote_summary("test1")
        
        # Should not contain user_id fields
        assert 'user_id' not in summary
        assert summary['upvotes'] == 2
        assert summary['downvotes'] == 1
        assert summary['total_votes'] == 3

    def test_fibonrose_metrics(self):
        """Test FibonRose trust metrics calculation"""
        voting_service = VotingService()
        
        # User casts multiple votes
        voting_service.cast_vote("user1", "test1", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user1", "test2", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user1", "test3", VotableItemType.FEEDBACK, VoteType.APPROVE)
        
        # Get metrics
        metrics = voting_service.get_user_fibonrose_metrics("user1")
        
        assert 'trust_score' in metrics
        assert 'consistency_score' in metrics
        assert 'participation_score' in metrics
        assert metrics['total_votes'] == 3
        assert metrics['trust_score'] >= 0
        assert metrics['trust_score'] <= 100

    def test_voting_history_consistency(self):
        """Test consistency score calculation"""
        voting_service = VotingService()
        
        # User casts all positive votes
        voting_service.cast_vote("user1", "test1", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user1", "test2", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user1", "test3", VotableItemType.MODEL_TEST, VoteType.APPROVE)
        
        metrics = voting_service.get_user_fibonrose_metrics("user1")
        
        # All positive votes should give 100% consistency
        assert metrics['consistency_score'] == 100.0

    def test_top_voted_items(self):
        """Test getting top voted items"""
        voting_service = VotingService()
        
        # Create votes on multiple items
        voting_service.cast_vote("user1", "test1", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user2", "test1", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
        voting_service.cast_vote("user1", "test2", VotableItemType.MODEL_TEST, VoteType.DOWNVOTE)
        
        top_items = voting_service.get_top_voted_items(
            item_type=VotableItemType.MODEL_TEST,
            limit=10
        )
        
        assert len(top_items) == 2
        assert top_items[0]['item_id'] == "test1"  # Should be first (higher score)
        assert top_items[0]['score'] > top_items[1]['score']


class TestPubSubService:
    """Test PubSub service functionality"""

    @pytest.mark.asyncio
    async def test_subscribe(self):
        """Test subscribing to topics"""
        pubsub = PubSubService()
        
        subscriber = pubsub.subscribe(
            subscriber_id="sub1",
            topics=["test.model", "test.feedback"]
        )
        
        assert subscriber.id == "sub1"
        assert "test.model" in subscriber.topics
        assert "test.feedback" in subscriber.topics

    @pytest.mark.asyncio
    async def test_publish_event(self):
        """Test publishing events"""
        pubsub = PubSubService()
        events_received = []
        
        def callback(event):
            events_received.append(event)
        
        pubsub.subscribe(
            subscriber_id="sub1",
            topics=["test.topic"],
            callback=callback
        )
        
        await pubsub.publish(
            topic="test.topic",
            event_type=EventType.TEST_COMPLETED,
            data={"test_id": "test1", "passed": True}
        )
        
        assert len(events_received) == 1
        assert events_received[0].event_type == EventType.TEST_COMPLETED

    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        """Test unsubscribing from topics"""
        pubsub = PubSubService()
        
        pubsub.subscribe(
            subscriber_id="sub1",
            topics=["test.topic"]
        )
        
        assert pubsub.get_subscriber_count("test.topic") == 1
        
        pubsub.unsubscribe("sub1")
        
        assert pubsub.get_subscriber_count("test.topic") == 0

    @pytest.mark.asyncio
    async def test_event_history(self):
        """Test event history tracking"""
        pubsub = PubSubService()
        
        await pubsub.publish(
            topic="test.topic",
            event_type=EventType.TEST_COMPLETED,
            data={"test_id": "test1"}
        )
        
        await pubsub.publish(
            topic="test.topic",
            event_type=EventType.TEST_STARTED,
            data={"test_id": "test2"}
        )
        
        history = pubsub.get_history(limit=10)
        
        assert len(history) == 2
        assert history[0].event_type == EventType.TEST_COMPLETED

    @pytest.mark.asyncio
    async def test_notification_priority(self):
        """Test notification priority handling"""
        pubsub = PubSubService()
        events_received = []
        
        def callback(event):
            events_received.append(event)
        
        pubsub.subscribe(
            subscriber_id="sub1",
            topics=["test.topic"],
            callback=callback
        )
        
        await pubsub.publish(
            topic="test.topic",
            event_type=EventType.NOTIFICATION,
            data={"message": "Urgent alert"},
            priority=NotificationPriority.URGENT
        )
        
        assert len(events_received) == 1
        assert events_received[0].priority == NotificationPriority.URGENT

    @pytest.mark.asyncio
    async def test_iot_subscription(self):
        """Test IoT device subscription"""
        pubsub = PubSubService()
        
        subscriber = pubsub.subscribe(
            subscriber_id="iot_device_1",
            topics=["iot.alerts"],
            iot_enabled=True,
            vibration_enabled=True
        )
        
        assert subscriber.iot_enabled is True
        assert subscriber.vibration_enabled is True

    @pytest.mark.asyncio
    async def test_wildcard_subscription(self):
        """Test wildcard topic subscription"""
        pubsub = PubSubService()
        events_received = []
        
        def callback(event):
            events_received.append(event)
        
        pubsub.subscribe(
            subscriber_id="sub1",
            topics=["*"],  # Subscribe to all topics
            callback=callback
        )
        
        await pubsub.publish(
            topic="test.model",
            event_type=EventType.TEST_COMPLETED,
            data={"test_id": "test1"}
        )
        
        await pubsub.publish(
            topic="feedback.submitted",
            event_type=EventType.FEEDBACK_SUBMITTED,
            data={"feedback_id": "fb1"}
        )
        
        assert len(events_received) == 2


class TestIntegration:
    """Test integration between voting and pubsub"""

    @pytest.mark.asyncio
    async def test_vote_broadcast(self):
        """Test that votes trigger broadcast events"""
        voting_service = VotingService()
        pubsub = PubSubService()
        events_received = []
        
        def callback(event):
            events_received.append(event)
        
        pubsub.subscribe(
            subscriber_id="vote_listener",
            topics=["votes.model_test"],
            callback=callback
        )
        
        # Cast a vote
        voting_service.cast_vote(
            user_id="user1",
            item_id="test1",
            item_type=VotableItemType.MODEL_TEST,
            vote_type=VoteType.UPVOTE
        )
        
        # Manually trigger broadcast (in real app, this happens in API endpoint)
        await pubsub.publish(
            topic="votes.model_test",
            event_type=EventType.VOTE_CAST,
            data={
                'item_id': "test1",
                'vote_counts': voting_service.get_vote_summary("test1")
            }
        )
        
        assert len(events_received) == 1
        assert events_received[0].event_type == EventType.VOTE_CAST


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
