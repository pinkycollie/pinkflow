"""
Example Integration: Voting, Broadcasting, and Notifications

This script demonstrates how to use the voting and broadcasting system
together with test containers and notifications.

Run this example:
    python examples/voting_broadcasting_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'webapp' / 'backend'))

from voting_service import (
    get_voting_service, VoteType, VotableItemType
)
from pubsub_service import (
    get_pubsub_service, EventType, NotificationPriority
)


async def main():
    """Main example function"""
    
    # Initialize services
    voting = get_voting_service()
    pubsub = get_pubsub_service()
    
    print("=" * 60)
    print("PinkFlow Voting & Broadcasting System Example")
    print("=" * 60)
    
    # Example 1: Test Container Broadcasting
    print("\n[1] Test Container Broadcasting")
    print("-" * 40)
    
    # Subscribe to test events
    def test_callback(event):
        print(f"  📢 Event received: {event.event_type.value}")
        print(f"     Data: {event.data}")
    
    pubsub.subscribe(
        subscriber_id="test_listener",
        topics=["test.model"],
        callback=test_callback
    )
    
    # Simulate test lifecycle
    test_id = "test_123"
    
    # Test started
    await pubsub.publish(
        topic="test.model",
        event_type=EventType.TEST_STARTED,
        data={"test_id": test_id, "repo": "github.com/user/asl-model"},
        priority=NotificationPriority.NORMAL
    )
    
    # Test completed
    await pubsub.publish(
        topic="test.model",
        event_type=EventType.TEST_COMPLETED,
        data={
            "test_id": test_id,
            "accuracy": 95.5,
            "passed": True,
            "processing_time": 45.2
        },
        priority=NotificationPriority.HIGH
    )
    
    # Example 2: Voting on Test Results
    print("\n[2] Voting on Test Results")
    print("-" * 40)
    
    # Users vote on the test result
    print("\n  Users casting votes...")
    
    result1 = voting.cast_vote(
        user_id="user_1",
        item_id=test_id,
        item_type=VotableItemType.MODEL_TEST,
        vote_type=VoteType.UPVOTE
    )
    print(f"  👍 User 1 upvoted - Total upvotes: {result1['upvotes']}")
    
    result2 = voting.cast_vote(
        user_id="user_2",
        item_id=test_id,
        item_type=VotableItemType.MODEL_TEST,
        vote_type=VoteType.UPVOTE
    )
    print(f"  👍 User 2 upvoted - Total upvotes: {result2['upvotes']}")
    
    result3 = voting.cast_vote(
        user_id="user_3",
        item_id=test_id,
        item_type=VotableItemType.MODEL_TEST,
        vote_type=VoteType.DOWNVOTE
    )
    print(f"  👎 User 3 downvoted - Total downvotes: {result3['downvotes']}")
    
    # Get final vote summary
    summary = voting.get_vote_summary(test_id)
    print(f"\n  Final Results:")
    print(f"    Total votes: {summary['total_votes']}")
    print(f"    Score: {summary['score']:.1f}")
    print(f"    Upvotes: {summary['upvotes']}, Downvotes: {summary['downvotes']}")
    
    # Broadcast vote update
    await pubsub.publish(
        topic="votes.model_test",
        event_type=EventType.VOTE_UPDATED,
        data={"item_id": test_id, "vote_summary": summary},
        priority=NotificationPriority.NORMAL
    )
    
    # Example 3: FibonRose Trust Metrics
    print("\n[3] FibonRose Trust Metrics")
    print("-" * 40)
    
    # Add more votes for user_1 to build history
    voting.cast_vote("user_1", "test_456", VotableItemType.MODEL_TEST, VoteType.UPVOTE)
    voting.cast_vote("user_1", "test_789", VotableItemType.FEEDBACK, VoteType.APPROVE)
    voting.cast_vote("user_1", "proposal_1", VotableItemType.PROPOSAL, VoteType.APPROVE)
    
    # Get trust metrics
    metrics = voting.get_user_fibonrose_metrics("user_1")
    print(f"\n  User 1 Trust Metrics:")
    print(f"    Trust Score: {metrics['trust_score']:.1f}/100")
    print(f"    Consistency: {metrics['consistency_score']:.1f}%")
    print(f"    Participation: {metrics['participation_score']:.1f}%")
    print(f"    Total Votes: {metrics['total_votes']}")
    print(f"    Vote Distribution: {metrics['vote_distribution']}")
    
    # Example 4: IoT Device Notifications
    print("\n[4] IoT Device Notifications with Vibration")
    print("-" * 40)
    
    # Subscribe IoT device
    iot_device = pubsub.subscribe(
        subscriber_id="iot_device_1",
        topics=["iot.alerts"],
        iot_enabled=True,
        vibration_enabled=True
    )
    print(f"  ✓ IoT device subscribed: {iot_device.id}")
    print(f"    Vibration enabled: {iot_device.vibration_enabled}")
    
    # Send urgent alert to IoT devices
    await pubsub.publish(
        topic="iot.alerts",
        event_type=EventType.IOT_ALERT,
        data={
            "alert_type": "test_completed",
            "message": "Model test finished with high accuracy"
        },
        priority=NotificationPriority.URGENT
    )
    print("  📳 Vibration alert sent to IoT device")
    
    # Example 5: Privacy Protection
    print("\n[5] Privacy Protection Verification")
    print("-" * 40)
    
    # Public summary doesn't expose user info
    public_summary = voting.get_vote_summary(test_id)
    print(f"  Public Summary (no user info):")
    print(f"    Keys: {list(public_summary.keys())}")
    print(f"    ✓ No 'user_id' field exposed")
    
    # User can check their own vote status
    user_status = voting.get_user_voting_status("user_1", test_id)
    print(f"\n  User 1's Private Status:")
    print(f"    {user_status}")
    
    # Example 6: Top Voted Items
    print("\n[6] Top Voted Items")
    print("-" * 40)
    
    top_items = voting.get_top_voted_items(
        item_type=VotableItemType.MODEL_TEST,
        limit=5
    )
    
    print(f"  Top {len(top_items)} Model Tests:")
    for i, item in enumerate(top_items, 1):
        print(f"    {i}. {item['item_id']}: Score {item['score']:.1f} ({item['total_votes']} votes)")
    
    # Example 7: Event History
    print("\n[7] Event History")
    print("-" * 40)
    
    history = pubsub.get_history(limit=5)
    print(f"  Last {len(history)} events:")
    for event in history:
        print(f"    - {event.event_type.value} at {event.timestamp.strftime('%H:%M:%S')}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully! ✨")
    print("=" * 60)


if __name__ == "__main__":
    # Run the async example
    asyncio.run(main())
