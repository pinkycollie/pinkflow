"""
PinkFlow Voting and Feedback Service

Provides voting functionality with:
- Privacy-protected voting (vote counts visible, not individual voters)
- FibonRose integration for tracking voting history
- Trust metrics based on voting patterns
- Real-time vote count updates via PubSub
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid
from collections import defaultdict


class VoteType(Enum):
    """Types of votes"""
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"
    APPROVE = "approve"
    REJECT = "reject"


class VotableItemType(Enum):
    """Types of items that can be voted on"""
    MODEL_TEST = "model_test"
    FEEDBACK = "feedback"
    PROPOSAL = "proposal"
    CONTRIBUTION = "contribution"


@dataclass
class Vote:
    """Represents a single vote"""
    id: str
    user_id: str  # Stored but not exposed publicly
    item_id: str
    item_type: VotableItemType
    vote_type: VoteType
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_public_dict(self) -> Dict[str, Any]:
        """Convert to dictionary without exposing user_id"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_type': self.item_type.value,
            'vote_type': self.vote_type.value,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class VoteSummary:
    """Summary of votes for an item"""
    item_id: str
    item_type: VotableItemType
    upvotes: int = 0
    downvotes: int = 0
    approvals: int = 0
    rejections: int = 0
    total_votes: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'item_id': self.item_id,
            'item_type': self.item_type.value,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'approvals': self.approvals,
            'rejections': self.rejections,
            'total_votes': self.total_votes,
            'score': self.calculate_score(),
            'last_updated': self.last_updated.isoformat()
        }
    
    def calculate_score(self) -> float:
        """Calculate overall score"""
        positive = self.upvotes + self.approvals
        negative = self.downvotes + self.rejections
        total = positive + negative
        if total == 0:
            return 0.0
        return (positive - negative) / total * 100


@dataclass
class UserVotingHistory:
    """
    User's voting history for FibonRose trust metrics.
    This data is private and only used for trust calculations.
    """
    user_id: str
    total_votes: int = 0
    votes_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    votes_by_item_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    first_vote: Optional[datetime] = None
    last_vote: Optional[datetime] = None
    consistency_score: float = 0.0
    participation_score: float = 0.0
    
    def update_metrics(self):
        """Update FibonRose trust metrics"""
        # Consistency: ratio of constructive votes
        constructive = self.votes_by_type.get('upvote', 0) + self.votes_by_type.get('approve', 0)
        destructive = self.votes_by_type.get('downvote', 0) + self.votes_by_type.get('reject', 0)
        total = constructive + destructive
        
        if total > 0:
            self.consistency_score = (constructive / total) * 100
        
        # Participation: based on total votes and time span
        if self.first_vote and self.last_vote:
            days = (self.last_vote - self.first_vote).days + 1
            votes_per_day = self.total_votes / days
            # Normalize to 0-100 scale (assuming 5+ votes/day is max participation)
            self.participation_score = min((votes_per_day / 5.0) * 100, 100)
    
    def get_fibonrose_metrics(self) -> Dict[str, Any]:
        """
        Get FibonRose trust metrics derived from voting history.
        Uses Fibonacci-inspired weighting for recent activity.
        """
        self.update_metrics()
        
        # Calculate weighted trust score
        # Weight factors: consistency (40%), participation (30%), total votes (30%)
        trust_score = (
            self.consistency_score * 0.4 +
            self.participation_score * 0.3 +
            min((self.total_votes / 100) * 100, 100) * 0.3
        )
        
        return {
            'user_id': self.user_id,
            'trust_score': round(trust_score, 2),
            'consistency_score': round(self.consistency_score, 2),
            'participation_score': round(self.participation_score, 2),
            'total_votes': self.total_votes,
            'vote_distribution': dict(self.votes_by_type),
            'activity_by_category': dict(self.votes_by_item_type)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'total_votes': self.total_votes,
            'votes_by_type': dict(self.votes_by_type),
            'votes_by_item_type': dict(self.votes_by_item_type),
            'first_vote': self.first_vote.isoformat() if self.first_vote else None,
            'last_vote': self.last_vote.isoformat() if self.last_vote else None,
            'metrics': self.get_fibonrose_metrics()
        }


class VotingService:
    """
    Service for managing votes and feedback with privacy protection.
    
    Privacy Features:
    - Vote counts are public
    - Individual voter identities are private
    - Voting history used only for FibonRose trust metrics
    """
    
    def __init__(self):
        self.votes: Dict[str, Vote] = {}
        self.vote_summaries: Dict[str, VoteSummary] = {}
        self.user_histories: Dict[str, UserVotingHistory] = {}
        self.user_votes_by_item: Dict[str, Dict[str, str]] = defaultdict(dict)  # user_id -> item_id -> vote_id
    
    def cast_vote(
        self,
        user_id: str,
        item_id: str,
        item_type: VotableItemType,
        vote_type: VoteType
    ) -> Dict[str, Any]:
        """
        Cast or update a vote.
        
        Args:
            user_id: ID of the user voting (kept private)
            item_id: ID of the item being voted on
            item_type: Type of item
            vote_type: Type of vote
            
        Returns:
            Vote summary with updated counts
        """
        # Check if user already voted on this item
        existing_vote_id = self.user_votes_by_item[user_id].get(item_id)
        
        if existing_vote_id:
            # Update existing vote
            old_vote = self.votes[existing_vote_id]
            old_vote.vote_type = vote_type
            old_vote.timestamp = datetime.now()
            vote = old_vote
        else:
            # Create new vote
            vote_id = str(uuid.uuid4())
            vote = Vote(
                id=vote_id,
                user_id=user_id,
                item_id=item_id,
                item_type=item_type,
                vote_type=vote_type
            )
            self.votes[vote_id] = vote
            self.user_votes_by_item[user_id][item_id] = vote_id
        
        # Update vote summary
        self._update_vote_summary(item_id, item_type)
        
        # Update user voting history
        self._update_user_history(user_id, item_type, vote_type)
        
        # Return public summary (no user info)
        return self.get_vote_summary(item_id)
    
    def remove_vote(self, user_id: str, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Remove a user's vote from an item.
        
        Args:
            user_id: ID of the user
            item_id: ID of the item
            
        Returns:
            Updated vote summary or None if no vote existed
        """
        vote_id = self.user_votes_by_item[user_id].get(item_id)
        
        if not vote_id:
            return None
        
        vote = self.votes[vote_id]
        
        # Remove vote
        del self.votes[vote_id]
        del self.user_votes_by_item[user_id][item_id]
        
        # Update summary
        self._update_vote_summary(item_id, vote.item_type)
        
        return self.get_vote_summary(item_id)
    
    def get_vote_summary(self, item_id: str) -> Dict[str, Any]:
        """
        Get vote summary for an item (public, no user info).
        
        Args:
            item_id: ID of the item
            
        Returns:
            Vote summary dictionary
        """
        summary = self.vote_summaries.get(item_id)
        if summary:
            return summary.to_dict()
        return {
            'item_id': item_id,
            'total_votes': 0,
            'upvotes': 0,
            'downvotes': 0,
            'approvals': 0,
            'rejections': 0,
            'score': 0
        }
    
    def get_user_voting_status(self, user_id: str, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a user's vote status for a specific item.
        
        Args:
            user_id: ID of the user
            item_id: ID of the item
            
        Returns:
            User's vote information or None
        """
        vote_id = self.user_votes_by_item[user_id].get(item_id)
        if not vote_id:
            return None
        
        vote = self.votes[vote_id]
        return {
            'has_voted': True,
            'vote_type': vote.vote_type.value,
            'timestamp': vote.timestamp.isoformat()
        }
    
    def get_user_fibonrose_metrics(self, user_id: str) -> Dict[str, Any]:
        """
        Get FibonRose trust metrics for a user based on voting history.
        
        Args:
            user_id: ID of the user
            
        Returns:
            FibonRose metrics dictionary
        """
        history = self.user_histories.get(user_id)
        if not history:
            return {
                'user_id': user_id,
                'trust_score': 0,
                'total_votes': 0,
                'message': 'No voting history'
            }
        
        return history.get_fibonrose_metrics()
    
    def get_top_voted_items(
        self,
        item_type: Optional[VotableItemType] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get top voted items by score.
        
        Args:
            item_type: Filter by item type
            limit: Maximum number of items to return
            
        Returns:
            List of vote summaries sorted by score
        """
        summaries = list(self.vote_summaries.values())
        
        if item_type:
            summaries = [s for s in summaries if s.item_type == item_type]
        
        # Sort by score
        summaries.sort(key=lambda s: s.calculate_score(), reverse=True)
        
        return [s.to_dict() for s in summaries[:limit]]
    
    def _update_vote_summary(self, item_id: str, item_type: VotableItemType):
        """Update vote summary for an item"""
        # Count all votes for this item
        item_votes = [v for v in self.votes.values() if v.item_id == item_id]
        
        summary = VoteSummary(item_id=item_id, item_type=item_type)
        
        for vote in item_votes:
            if vote.vote_type == VoteType.UPVOTE:
                summary.upvotes += 1
            elif vote.vote_type == VoteType.DOWNVOTE:
                summary.downvotes += 1
            elif vote.vote_type == VoteType.APPROVE:
                summary.approvals += 1
            elif vote.vote_type == VoteType.REJECT:
                summary.rejections += 1
        
        summary.total_votes = len(item_votes)
        summary.last_updated = datetime.now()
        
        self.vote_summaries[item_id] = summary
    
    def _update_user_history(self, user_id: str, item_type: VotableItemType, vote_type: VoteType):
        """Update user's voting history for FibonRose metrics"""
        if user_id not in self.user_histories:
            self.user_histories[user_id] = UserVotingHistory(user_id=user_id)
        
        history = self.user_histories[user_id]
        history.total_votes += 1
        history.votes_by_type[vote_type.value] += 1
        history.votes_by_item_type[item_type.value] += 1
        
        if history.first_vote is None:
            history.first_vote = datetime.now()
        history.last_vote = datetime.now()
        
        history.update_metrics()


# Global instance
_voting_service: Optional[VotingService] = None


def get_voting_service() -> VotingService:
    """Get or create global voting service instance"""
    global _voting_service
    if _voting_service is None:
        _voting_service = VotingService()
    return _voting_service
