/**
 * Voting Component
 * 
 * Features:
 * - Vote on test results, feedback, proposals
 * - Display vote counts (no user info)
 * - Real-time updates via PubSub
 * - Privacy-protected voting
 * - FibonRose trust metrics integration
 */

import React, { useState, useEffect } from 'react';

interface VoteSummary {
  item_id: string;
  total_votes: number;
  upvotes: number;
  downvotes: number;
  approvals: number;
  rejections: number;
  score: number;
}

interface VoteWidgetProps {
  itemId: string;
  itemType: 'model_test' | 'feedback' | 'proposal' | 'contribution';
  userId?: string;
  apiUrl?: string;
  showScore?: boolean;
  showCounts?: boolean;
  allowVoting?: boolean;
  voteType?: 'updown' | 'approvereject';
}

const VoteWidget: React.FC<VoteWidgetProps> = ({
  itemId,
  itemType,
  userId,
  apiUrl = 'http://localhost:8000',
  showScore = true,
  showCounts = true,
  allowVoting = true,
  voteType = 'updown'
}) => {
  const [voteSummary, setVoteSummary] = useState<VoteSummary | null>(null);
  const [userVote, setUserVote] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch vote summary
  useEffect(() => {
    fetchVoteSummary();
    if (userId) {
      fetchUserVoteStatus();
    }
  }, [itemId, userId]);

  const fetchVoteSummary = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/vote/${itemId}`);
      if (response.ok) {
        const data = await response.json();
        setVoteSummary(data);
      }
    } catch (err) {
      console.error('Failed to fetch vote summary:', err);
    }
  };

  const fetchUserVoteStatus = async () => {
    if (!userId) return;
    
    try {
      const response = await fetch(`${apiUrl}/api/vote/${itemId}/status?user_id=${userId}`);
      if (response.ok) {
        const data = await response.json();
        if (data.has_voted) {
          setUserVote(data.vote_type);
        }
      }
    } catch (err) {
      console.error('Failed to fetch user vote status:', err);
    }
  };

  const handleVote = async (voteTypeValue: string) => {
    if (!userId) {
      setError('You must be logged in to vote');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/api/vote?user_id=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          item_id: itemId,
          item_type: itemType,
          vote_type: voteTypeValue
        })
      });

      if (response.ok) {
        const data = await response.json();
        setVoteSummary(data);
        setUserVote(voteTypeValue);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to cast vote');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveVote = async () => {
    if (!userId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/api/vote/${itemId}?user_id=${userId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        const data = await response.json();
        setVoteSummary(data);
        setUserVote(null);
      } else {
        setError('Failed to remove vote');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getVoteButton = (type: string, label: string, icon: string) => {
    const isActive = userVote === type;
    const baseClasses = 'px-4 py-2 rounded-lg font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
    
    let colorClasses = '';
    if (type === 'upvote' || type === 'approve') {
      colorClasses = isActive 
        ? 'bg-green-500 text-white hover:bg-green-600 focus:ring-green-500' 
        : 'bg-gray-200 text-gray-700 hover:bg-gray-300 focus:ring-gray-500';
    } else {
      colorClasses = isActive 
        ? 'bg-red-500 text-white hover:bg-red-600 focus:ring-red-500' 
        : 'bg-gray-200 text-gray-700 hover:bg-gray-300 focus:ring-gray-500';
    }
    
    return (
      <button
        onClick={() => isActive ? handleRemoveVote() : handleVote(type)}
        disabled={loading || !allowVoting}
        className={`${baseClasses} ${colorClasses} ${loading || !allowVoting ? 'opacity-50 cursor-not-allowed' : ''}`}
        aria-label={`${label} ${isActive ? '(active)' : ''}`}
      >
        <span className="mr-2" aria-hidden="true">{icon}</span>
        {label}
      </button>
    );
  };

  if (!voteSummary) {
    return <div className="text-gray-500">Loading votes...</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4 border border-gray-200">
      {/* Vote Buttons */}
      {allowVoting && (
        <div className="flex gap-3 mb-4">
          {voteType === 'updown' ? (
            <>
              {getVoteButton('upvote', 'Upvote', '👍')}
              {getVoteButton('downvote', 'Downvote', '👎')}
            </>
          ) : (
            <>
              {getVoteButton('approve', 'Approve', '✅')}
              {getVoteButton('reject', 'Reject', '❌')}
            </>
          )}
        </div>
      )}

      {/* Vote Counts */}
      {showCounts && (
        <div className="grid grid-cols-2 gap-4 mb-3">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {voteType === 'updown' ? voteSummary.upvotes : voteSummary.approvals}
            </div>
            <div className="text-sm text-gray-600">
              {voteType === 'updown' ? 'Upvotes' : 'Approvals'}
            </div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">
              {voteType === 'updown' ? voteSummary.downvotes : voteSummary.rejections}
            </div>
            <div className="text-sm text-gray-600">
              {voteType === 'updown' ? 'Downvotes' : 'Rejections'}
            </div>
          </div>
        </div>
      )}

      {/* Score */}
      {showScore && (
        <div className="text-center border-t pt-3">
          <div className="text-3xl font-bold" style={{
            color: voteSummary.score > 0 ? '#10b981' : voteSummary.score < 0 ? '#ef4444' : '#6b7280'
          }}>
            {voteSummary.score > 0 ? '+' : ''}{voteSummary.score.toFixed(1)}
          </div>
          <div className="text-sm text-gray-600">Overall Score</div>
          <div className="text-xs text-gray-500 mt-1">
            {voteSummary.total_votes} total vote{voteSummary.total_votes !== 1 ? 's' : ''}
          </div>
        </div>
      )}

      {/* Privacy Notice */}
      <div className="mt-3 text-xs text-gray-500 italic text-center">
        🔒 Vote counts are public, voter identities are private
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-3 text-sm text-red-600 bg-red-50 p-2 rounded">
          {error}
        </div>
      )}

      {/* Screen reader announcement */}
      <div className="sr-only" role="status" aria-live="polite">
        {loading && 'Processing vote...'}
        {userVote && `You have ${userVote}d this item`}
      </div>
    </div>
  );
};

export default VoteWidget;

// FibonRose Metrics Display Component
interface FibonRoseMetricsProps {
  userId: string;
  apiUrl?: string;
}

export const FibonRoseMetrics: React.FC<FibonRoseMetricsProps> = ({
  userId,
  apiUrl = 'http://localhost:8000'
}) => {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, [userId]);

  const fetchMetrics = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/fibonrose/metrics/${userId}`);
      if (response.ok) {
        const data = await response.json();
        setMetrics(data);
      }
    } catch (err) {
      console.error('Failed to fetch FibonRose metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-gray-500">Loading trust metrics...</div>;
  }

  if (!metrics) {
    return null;
  }

  return (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md p-5 border border-purple-200">
      <h3 className="text-xl font-bold mb-4 text-purple-900">🌸 FibonRose Trust Score</h3>
      
      <div className="text-center mb-4">
        <div className="text-5xl font-bold text-purple-600">
          {metrics.trust_score.toFixed(1)}
        </div>
        <div className="text-sm text-gray-600">Trust Score (0-100)</div>
      </div>

      <div className="space-y-3">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-700">Consistency</span>
            <span className="font-semibold">{metrics.consistency_score.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-purple-500 h-2 rounded-full"
              style={{ width: `${metrics.consistency_score}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-700">Participation</span>
            <span className="font-semibold">{metrics.participation_score.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-pink-500 h-2 rounded-full"
              style={{ width: `${metrics.participation_score}%` }}
            />
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-purple-200">
        <div className="text-sm text-gray-600">
          <strong>{metrics.total_votes}</strong> total votes
        </div>
      </div>

      <div className="mt-3 text-xs text-gray-500 italic">
        Trust metrics based on voting history using Fibonacci-inspired weighting
      </div>
    </div>
  );
};

// Example usage:
/*
import VoteWidget, { FibonRoseMetrics } from './components/VoteWidget';

function TestResultPage() {
  const testId = 'test-123';
  const userId = 'user-456';

  return (
    <div>
      <h1>Test Result</h1>
      <VoteWidget
        itemId={testId}
        itemType="model_test"
        userId={userId}
        voteType="updown"
      />
      <FibonRoseMetrics userId={userId} />
    </div>
  );
}
*/
