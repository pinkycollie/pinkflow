# Voting and Broadcasting System Documentation

## Overview

This document describes the voting, feedback, and real-time broadcasting system integrated into PinkFlow. The system is designed with Deaf-First principles, emphasizing visual notifications, privacy protection, and IoT device support including the Vibration API.

## Architecture

### Components

1. **Voting Service** (`voting_service.py`)
   - Privacy-protected voting system
   - Vote count aggregation (public)
   - Individual voter identity protection (private)
   - FibonRose trust metrics integration

2. **PubSub Service** (`pubsub_service.py`)
   - Real-time event broadcasting
   - Topic-based subscriptions
   - Visual notification support
   - IoT device integration with Vibration API
   - Priority-based notification system

3. **Frontend Components**
   - `NotificationBanner.tsx` - Visual notification banners
   - `VoteWidget.tsx` - Voting interface and FibonRose metrics display

## Features

### Voting System

#### Privacy Protection
- Vote counts are publicly visible
- Individual voter identities remain private
- Only aggregated statistics are exposed via API

#### Vote Types
- **Upvote/Downvote**: For general approval/disapproval
- **Approve/Reject**: For formal decisions

#### Votable Items
- Model test results
- User feedback
- Proposals
- Contributions

#### API Endpoints

```
POST /api/vote
  - Cast or update a vote
  - Body: { item_id, item_type, vote_type }
  - Query param: user_id
  - Returns: Vote summary

GET /api/vote/{item_id}
  - Get vote summary (public, no user info)
  - Returns: { total_votes, upvotes, downvotes, score, ... }

DELETE /api/vote/{item_id}
  - Remove user's vote
  - Query param: user_id
  - Returns: Updated vote summary

GET /api/vote/{item_id}/status
  - Get user's vote status for an item
  - Query param: user_id
  - Returns: { has_voted, vote_type, timestamp }

GET /api/vote/top/{item_type}
  - Get top voted items by score
  - Query param: limit (default: 10)
  - Returns: List of vote summaries sorted by score
```

### FibonRose Trust Metrics

The voting system integrates with FibonRose to calculate trust scores based on voting history.

#### Metrics Calculation

```
Trust Score = (Consistency × 0.4) + (Participation × 0.3) + (Total Votes × 0.3)
```

Where:
- **Consistency Score**: Ratio of constructive to destructive votes (0-100%)
- **Participation Score**: Voting frequency over time (0-100%)
- **Total Votes**: Normalized vote count (0-100%)

#### API Endpoint

```
GET /api/fibonrose/metrics/{user_id}
  - Get user's trust metrics
  - Returns: {
      trust_score: float,
      consistency_score: float,
      participation_score: float,
      total_votes: int,
      vote_distribution: {...},
      activity_by_category: {...}
    }
```

### PubSub Broadcasting System

#### Event Types
- `test_started` - Model test initiated
- `test_progress` - Test progress update
- `test_completed` - Test finished successfully
- `test_failed` - Test encountered error
- `vote_cast` - Vote registered
- `vote_updated` - Vote count changed
- `feedback_submitted` - Feedback received
- `notification` - General notification
- `iot_alert` - IoT device alert

#### Notification Priorities
- **Low**: Informational, 3-second display
- **Normal**: Standard update, 5-second display
- **High**: Important, 10-second display
- **Urgent**: Critical, persistent until dismissed

#### Subscription Features
- Topic-based subscriptions
- Wildcard subscriptions (subscribe to all topics)
- IoT device support
- Vibration API integration
- Visual-only mode (Deaf-First default)

#### API Endpoints

```
POST /api/subscribe
  - Subscribe to topics
  - Body: {
      subscriber_id: string,
      topics: string[],
      iot_enabled: boolean,
      vibration_enabled: boolean
    }
  - Returns: Subscriber confirmation

DELETE /api/subscribe/{subscriber_id}
  - Unsubscribe from topics
  - Query param: topics (optional, removes all if not specified)
  - Returns: Unsubscribe confirmation

POST /api/broadcast
  - Broadcast notification
  - Body: {
      topic: string,
      event_type: string,
      data: object,
      priority: string
    }
  - Returns: Broadcast confirmation with subscriber count

GET /api/broadcast/history
  - Get event history
  - Query params: event_type, limit
  - Returns: List of historical events
```

## Deaf-First Design Principles

### Visual Notifications
- No audio dependencies
- Clear, persistent banners for important events
- Color-coded priority levels (blue/green/orange/red)
- Large, readable text
- Icon-based visual cues

### Vibration API Support
Vibration patterns based on priority:
- Low: [100ms] - Single short
- Normal: [200ms, 100ms, 200ms] - Double pulse
- High: [300ms, 100ms, 300ms, 100ms, 300ms] - Triple pulse
- Urgent: [500ms, 200ms] × 4 - Intense pattern

### Accessibility Features
- ARIA labels for screen readers
- Keyboard navigation support
- High contrast visual design
- Persistent urgent notifications
- Dismissible non-urgent notifications

## Integration with Test Containers

When a model test runs, the system broadcasts events:

1. **Test Started**: Notifies subscribers that testing has begun
2. **Test Progress**: Optional progress updates during long-running tests
3. **Test Completed**: Final results with accuracy metrics
4. **Test Failed**: Error information if test encounters issues

Subscribers can receive notifications via:
- Visual banners in the web UI
- IoT devices with vibration alerts
- WebSocket connections (future)
- Email/SMS (future)

## Frontend Usage

### Voting Widget

```typescript
import VoteWidget, { FibonRoseMetrics } from './components/VoteWidget';

function TestResultPage() {
  return (
    <div>
      <h1>Test Result</h1>
      
      {/* Voting interface */}
      <VoteWidget
        itemId="test-123"
        itemType="model_test"
        userId="user-456"
        voteType="updown"
        showScore={true}
        showCounts={true}
      />
      
      {/* User's trust metrics */}
      <FibonRoseMetrics userId="user-456" />
    </div>
  );
}
```

### Notification Banner

```typescript
import NotificationBanner, { useNotifications } from './components/NotificationBanner';

function App() {
  const { notifications, addNotification, removeNotification } = useNotifications();

  const handleTestComplete = () => {
    addNotification({
      type: 'success',
      title: 'Test Completed',
      message: 'Model test finished with 95% accuracy',
      priority: 'high',
      duration: 5000,
      animation: 'bounce'
    });
  };

  return (
    <>
      <NotificationBanner 
        notifications={notifications}
        onDismiss={removeNotification}
        enableVibration={true}
      />
      <button onClick={handleTestComplete}>Run Test</button>
    </>
  );
}
```

## Backend Usage

### Broadcasting Events

```python
from backend.pubsub_service import get_pubsub_service, EventType, NotificationPriority

pubsub = get_pubsub_service()

# Broadcast test completion
await pubsub.publish(
    topic="test.model",
    event_type=EventType.TEST_COMPLETED,
    data={
        'test_id': test_id,
        'accuracy': 95.5,
        'passed': True
    },
    priority=NotificationPriority.HIGH
)
```

### Processing Votes

```python
from backend.voting_service import get_voting_service, VoteType, VotableItemType

voting = get_voting_service()

# Cast a vote
result = voting.cast_vote(
    user_id="user123",
    item_id="test456",
    item_type=VotableItemType.MODEL_TEST,
    vote_type=VoteType.UPVOTE
)

# Get FibonRose metrics
metrics = voting.get_user_fibonrose_metrics("user123")
print(f"Trust Score: {metrics['trust_score']}")
```

## Testing

Run the test suite:

```bash
cd webapp
python -m pytest tests/test_voting_pubsub.py -v
```

Tests cover:
- Vote casting and updating
- Vote privacy protection
- FibonRose metrics calculation
- PubSub event broadcasting
- Topic subscriptions
- Notification priorities
- IoT device support
- Integration scenarios

## Security Considerations

1. **Vote Privacy**: Individual votes are stored but never exposed publicly
2. **User Authentication**: All voting and subscription operations require user_id
3. **Rate Limiting**: Should be implemented in production to prevent abuse
4. **Data Validation**: All inputs validated via Pydantic models
5. **XSS Protection**: Frontend sanitizes all user-generated content

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Push notifications for mobile devices
- [ ] Email/SMS notification options
- [ ] Vote delegation for governance
- [ ] Advanced FibonRose metrics (temporal decay, weighted voting)
- [ ] Machine learning anomaly detection for voting patterns
- [ ] Blockchain integration for vote transparency
- [ ] Multi-language support for notifications

## References

- [Vibration API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API)
- [WCAG 2.1 Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [FibonRose Trust System](../../Fibonrose/)
- [PinkFlow Main Documentation](../../README.md)
