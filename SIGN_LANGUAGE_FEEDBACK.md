# Sign Language Feedback System

## Overview

The PinkFlow Sign Language Feedback system enables users to submit feedback in sign language through video uploads. This feature prioritizes visual communication and adheres to Deaf-First design principles.

---

## Table of Contents

- [Features](#features)
- [API Routes](#api-routes)
- [Architecture](#architecture)
- [Storage Integration](#storage-integration)
- [Database Schema](#database-schema)
- [Real-time Notifications](#real-time-notifications)
- [Security Considerations](#security-considerations)
- [Deaf-First Design Principles](#deaf-first-design-principles)
- [Implementation Guide](#implementation-guide)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)

---

## Features

### Core Features

- ✅ **Video Upload**: Support for .mp4, .mov, and .webm formats
- ✅ **File Validation**: Size limits (100MB max), duration limits (1s-5min)
- ✅ **Cloud Storage**: Integration with AWS S3, Firebase Storage, or similar
- ✅ **Metadata Management**: User ID, description, tags, timestamps
- ✅ **Video Processing**: Automatic thumbnail generation, transcoding
- ✅ **Real-time Notifications**: Phoenix PubSub integration for admin alerts
- ✅ **Feedback Dashboard**: Admin view with video previews and management
- ✅ **Access Control**: User authentication and authorization
- ✅ **Analytics**: View counts, upload statistics

### Accessibility Features

- 🎯 **Deaf-First Design**: Sign language as primary communication method
- 🎯 **High Contrast UI**: Accessible video player controls
- 🎯 **Keyboard Navigation**: Full keyboard support
- 🎯 **Visual Feedback**: Clear indicators for all states
- 🎯 **Optional Text**: Text descriptions are supplementary, not required

---

## API Routes

### Primary Route

```
POST /feedback/sign-language
GET  /feedback/sign-language
GET  /feedback/sign-language/{id}
PATCH /feedback/sign-language/{id}
DELETE /feedback/sign-language/{id}
GET  /feedback/sign-language/stats
```

Also accessible via:
```
/api/feedback/sign-language/*
```

### Detailed Endpoints

See [API.md](API.md) for complete API documentation, including:
- Request/response formats
- Error codes
- Rate limiting
- Authentication requirements

---

## Architecture

### System Components

```
┌─────────────┐
│   Client    │ (React/Next.js Frontend)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   API       │ (FastAPI Backend)
│   Gateway   │
└──────┬──────┘
       │
       ├─────────────────┬────────────────┬──────────────┐
       ▼                 ▼                ▼              ▼
┌─────────────┐   ┌─────────────┐  ┌──────────┐  ┌──────────┐
│  Validation │   │   Storage   │  │ Database │  │  PubSub  │
│   Service   │   │   Service   │  │ (PostgreSQL)│ │ (Phoenix)│
└─────────────┘   └─────────────┘  └──────────┘  └──────────┘
                        │
                        ▼
                  ┌──────────┐
                  │  Cloud   │ (AWS S3 / Firebase)
                  │ Storage  │
                  └──────────┘
```

### Workflow

1. **Upload Request**
   - User selects video file
   - Frontend validates file format and size
   - POST request to `/api/feedback/sign-language`

2. **Server Validation**
   - Verify file format (.mp4, .mov, .webm)
   - Check file size (≤100MB)
   - Validate user authentication

3. **Storage**
   - Generate unique feedback ID
   - Upload video to cloud storage
   - Generate signed URL for access

4. **Processing**
   - Extract video metadata (duration, resolution)
   - Generate thumbnail
   - Transcode if necessary

5. **Database**
   - Store metadata in PostgreSQL
   - Link video URL to database entry

6. **Notification**
   - Publish to PubSub channel
   - Notify admins in real-time
   - Update dashboard

---

## Storage Integration

### Supported Storage Providers

#### AWS S3

```python
storage_config = {
    'provider': 'aws_s3',
    'bucket': 'pinkflow-feedback',
    'region': 'us-east-1',
    'access_key_id': 'YOUR_ACCESS_KEY',
    'secret_access_key': 'YOUR_SECRET_KEY',
    'base_url': 'https://pinkflow-feedback.s3.amazonaws.com'
}
```

**Setup Steps:**
1. Create S3 bucket
2. Configure CORS settings
3. Set up IAM role with permissions
4. Install boto3: `pip install boto3`
5. Configure CloudFront (optional, for CDN)

#### Firebase Storage

```python
storage_config = {
    'provider': 'firebase',
    'bucket': 'pinkflow-feedback.appspot.com',
    'credentials_path': '/path/to/firebase-credentials.json',
    'base_url': 'https://firebasestorage.googleapis.com'
}
```

**Setup Steps:**
1. Create Firebase project
2. Enable Firebase Storage
3. Download service account credentials
4. Install firebase-admin: `pip install firebase-admin`
5. Configure storage rules

#### Google Cloud Storage

```python
storage_config = {
    'provider': 'gcs',
    'bucket': 'pinkflow-feedback',
    'credentials_path': '/path/to/gcs-credentials.json',
    'base_url': 'https://storage.googleapis.com/pinkflow-feedback'
}
```

### File Organization

```
bucket-name/
├── feedback/
│   ├── {feedback-id}/
│   │   ├── video.mp4          # Original video
│   │   ├── video-720p.mp4     # Transcoded versions
│   │   ├── video-480p.mp4
│   │   ├── thumbnail.jpg      # Generated thumbnail
│   │   └── metadata.json      # Video metadata
```

---

## Database Schema

### sign_language_feedback Table

```sql
CREATE TABLE sign_language_feedback (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    video_url TEXT NOT NULL,
    thumbnail_url TEXT,
    description TEXT,
    tags TEXT[],
    status VARCHAR(50) NOT NULL DEFAULT 'processing',
    duration FLOAT DEFAULT 0,
    file_size BIGINT DEFAULT 0,
    resolution VARCHAR(50),
    codec VARCHAR(50),
    frame_rate INTEGER,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_tags (tags)
);
```

### feedback_views Table

```sql
CREATE TABLE feedback_views (
    id SERIAL PRIMARY KEY,
    feedback_id VARCHAR(255) NOT NULL,
    viewer_id VARCHAR(255),
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_feedback
        FOREIGN KEY(feedback_id)
        REFERENCES sign_language_feedback(id)
        ON DELETE CASCADE,
    
    INDEX idx_feedback_id (feedback_id),
    INDEX idx_viewer_id (viewer_id)
);
```

### Field Descriptions

- **id**: Unique identifier (format: `feedback_{user_id}_{timestamp}`)
- **user_id**: ID of user who submitted feedback
- **video_url**: URL to video in cloud storage
- **thumbnail_url**: URL to video thumbnail
- **description**: Optional text description
- **tags**: Array of categorization tags
- **status**: Processing status (`uploading`, `processing`, `ready`, `failed`)
- **duration**: Video length in seconds
- **file_size**: File size in bytes
- **resolution**: Video resolution (e.g., "1920x1080")
- **codec**: Video codec (e.g., "h264")
- **frame_rate**: Frames per second
- **views**: Number of times viewed

---

## Real-time Notifications

### Phoenix PubSub Integration

#### Configuration

```python
pubsub_config = {
    'enabled': True,
    'type': 'phoenix_pubsub',
    'channel': 'feedback:notifications',
    'admin_channel': 'admin:notifications',
    'redis_url': 'redis://localhost:6379'  # For scaling
}
```

#### Events

**1. feedback:uploaded**
```javascript
{
  event: 'feedback:uploaded',
  data: {
    feedbackId: 'feedback_user123_1699564800',
    userId: 'user123',
    userName: 'John Doe',
    timestamp: '2023-11-10T12:00:00Z',
    description: 'Feedback about accessibility',
    tags: ['accessibility', 'ui']
  }
}
```

**2. feedback:processed**
```javascript
{
  event: 'feedback:processed',
  data: {
    feedbackId: 'feedback_user123_1699564800',
    status: 'ready',
    videoUrl: 'https://storage.../video.mp4',
    thumbnailUrl: 'https://storage.../thumbnail.jpg',
    duration: 45.2
  }
}
```

**3. feedback:deleted**
```javascript
{
  event: 'feedback:deleted',
  data: {
    feedbackId: 'feedback_user123_1699564800',
    deletedBy: 'admin_user',
    timestamp: '2023-11-10T13:00:00Z'
  }
}
```

#### WebSocket Connection

```javascript
// Frontend connection
const socket = io('ws://localhost:3001', {
  auth: {
    token: userToken
  }
});

// Subscribe to feedback events (admin only)
socket.on('feedback:uploaded', (data) => {
  console.log('New feedback uploaded:', data);
  updateDashboard(data);
});

socket.on('feedback:processed', (data) => {
  console.log('Feedback processed:', data);
  showVideoPreview(data.videoUrl);
});
```

---

## Security Considerations

### Upload Security

1. **File Validation**
   - Whitelist allowed MIME types
   - Validate magic numbers (not just extension)
   - Scan for malware
   - Check file integrity

2. **Size Limits**
   - Maximum file size: 100MB
   - Rate limiting: 5 uploads per hour per user
   - Storage quota per user

3. **Authentication**
   - JWT token required for all operations
   - User must be logged in to upload
   - Admin role required for deletion

4. **Authorization**
   - Users can only delete their own feedback
   - Admins can delete any feedback
   - Moderators can hide feedback

### Access Control

```python
# Example authorization check
def can_delete_feedback(user_id, feedback_user_id, user_role):
    """Check if user can delete feedback."""
    return (
        user_id == feedback_user_id or  # Owner
        user_role in ['admin', 'moderator']  # Privileged users
    )
```

### Data Privacy

1. **Signed URLs**
   - Generate time-limited URLs for video access
   - Expiration: 1 hour (configurable)
   - Revocable on user deletion

2. **GDPR Compliance**
   - Users can delete their feedback
   - Data export functionality
   - Privacy policy acceptance

3. **Content Moderation**
   - Admin review queue
   - Report/flag system
   - Automatic content filtering

---

## Deaf-First Design Principles

### 1. Visual Communication Priority

**Sign language is the PRIMARY form of communication**

- Video upload is the main feature
- Text description is optional
- No audio required or expected
- High-quality video encoding preserves sign details

### 2. User Interface

**Clear, visual, and accessible**

- Large, high-contrast buttons
- Visual progress indicators
- Icon-based feedback
- No reliance on audio cues

### 3. Video Player

**Accessible and user-controlled**

```html
<video 
  controls
  preload="metadata"
  crossorigin="anonymous"
  aria-label="Sign language feedback video">
  <track kind="descriptions" src="descriptions.vtt">
</video>
```

Features:
- Keyboard navigation (Space to play/pause, Arrow keys to seek)
- Clear play/pause buttons
- Volume control (for hearing users)
- Playback speed control
- Fullscreen option

### 4. Upload Experience

**Simple and clear**

1. **Selection**: Visual file picker with drag-and-drop
2. **Preview**: Review video before upload
3. **Progress**: Clear visual progress bar
4. **Confirmation**: Success message with video preview

### 5. Error Handling

**Visual and clear**

❌ Bad:
```
Error: File size exceeds maximum allowed size
```

✅ Good:
```
[Icon: ⚠️] Your video is too large
Maximum size: 100 MB
Your file: 150 MB
```

### 6. Dashboard Design

**Admin dashboard considerations**

- Grid view of video thumbnails
- No auto-play (user control)
- Keyboard navigation
- Visual tags and categories
- Batch operations support

---

## Implementation Guide

### Frontend (React/Next.js)

#### 1. Upload Component

```typescript
// components/FeedbackUpload.tsx
import React, { useState } from 'react';

interface FeedbackUploadProps {
  onUploadComplete: (feedbackId: string) => void;
}

export const FeedbackUpload: React.FC<FeedbackUploadProps> = ({
  onUploadComplete
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      
      // Validate file
      if (!['video/mp4', 'video/quicktime', 'video/webm'].includes(selectedFile.type)) {
        alert('Please select a valid video file (.mp4, .mov, or .webm)');
        return;
      }
      
      if (selectedFile.size > 100 * 1024 * 1024) {
        alert('File size must be less than 100 MB');
        return;
      }
      
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    
    const formData = new FormData();
    formData.append('video', file);
    formData.append('description', description);
    formData.append('tags', JSON.stringify(tags));

    try {
      const response = await fetch('/api/feedback/sign-language', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${userToken}`
        },
        body: formData,
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted);
        }
      });

      const result = await response.json();
      
      if (result.success) {
        onUploadComplete(result.feedback_id);
      } else {
        alert('Upload failed: ' + result.errors.join(', '));
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div className="feedback-upload">
      <h2>Upload Sign Language Feedback</h2>
      
      {/* File input */}
      <input
        type="file"
        accept=".mp4,.mov,.webm"
        onChange={handleFileChange}
        disabled={uploading}
      />
      
      {/* Preview */}
      {file && (
        <video src={URL.createObjectURL(file)} controls width="400" />
      )}
      
      {/* Optional description */}
      <textarea
        placeholder="Optional: Add a text description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        disabled={uploading}
      />
      
      {/* Tags */}
      <input
        type="text"
        placeholder="Tags (comma-separated)"
        onChange={(e) => setTags(e.target.value.split(',').map(t => t.trim()))}
        disabled={uploading}
      />
      
      {/* Upload button */}
      <button
        onClick={handleUpload}
        disabled={!file || uploading}
      >
        {uploading ? `Uploading... ${progress}%` : 'Upload Feedback'}
      </button>
      
      {/* Progress bar */}
      {uploading && (
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
      )}
    </div>
  );
};
```

#### 2. Dashboard Component

```typescript
// components/FeedbackDashboard.tsx
import React, { useEffect, useState } from 'react';

interface Feedback {
  id: string;
  userName: string;
  videoUrl: string;
  thumbnailUrl: string;
  description: string;
  tags: string[];
  timestamp: string;
  views: number;
}

export const FeedbackDashboard: React.FC = () => {
  const [feedbackList, setFeedbackList] = useState<Feedback[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeedback();
    
    // Subscribe to real-time updates
    socket.on('feedback:uploaded', (data) => {
      // Add new feedback to list
      fetchFeedback();
    });
    
    return () => {
      socket.off('feedback:uploaded');
    };
  }, []);

  const fetchFeedback = async () => {
    try {
      const response = await fetch('/api/feedback/sign-language', {
        headers: {
          'Authorization': `Bearer ${userToken}`
        }
      });
      const data = await response.json();
      setFeedbackList(data.feedback);
    } catch (error) {
      console.error('Fetch error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feedback-dashboard">
      <h2>Sign Language Feedback</h2>
      
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="feedback-grid">
          {feedbackList.map((feedback) => (
            <div key={feedback.id} className="feedback-card">
              <video
                src={feedback.videoUrl}
                poster={feedback.thumbnailUrl}
                controls
                width="300"
              />
              <div className="feedback-info">
                <p><strong>{feedback.userName}</strong></p>
                <p>{feedback.description}</p>
                <div className="tags">
                  {feedback.tags.map(tag => (
                    <span key={tag} className="tag">{tag}</span>
                  ))}
                </div>
                <p className="timestamp">{feedback.timestamp}</p>
                <p className="views">👁️ {feedback.views} views</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

### Backend (FastAPI)

#### API Route Implementation

```python
# routes/feedback.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List
import shutil
from pathlib import Path

from core.feedback_workflow import (
    FeedbackWorkflowOrchestrator,
    VideoValidator
)
from auth import get_current_user

router = APIRouter()

# Initialize orchestrator
orchestrator = FeedbackWorkflowOrchestrator(
    storage_config={
        'provider': 'aws_s3',
        'bucket': 'pinkflow-feedback',
        # ... other config
    },
    pubsub_config={
        'enabled': True,
        'type': 'phoenix_pubsub'
    }
)

@router.post("/api/feedback/sign-language")
async def upload_feedback(
    video: UploadFile = File(...),
    description: Optional[str] = None,
    tags: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Upload sign language feedback video."""
    
    # Validate file
    validator = VideoValidator()
    is_valid, errors = validator.validate_all(
        video.filename,
        video.size
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=errors)
    
    # Save temporary file
    temp_path = f"/tmp/{video.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    
    # Process upload
    result = orchestrator.process_upload(
        file_path=temp_path,
        filename=video.filename,
        file_size=video.size,
        user_id=current_user.id,
        description=description,
        tags=tags.split(',') if tags else []
    )
    
    # Clean up temp file
    Path(temp_path).unlink()
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['errors'])
    
    return JSONResponse(
        status_code=201,
        content=result
    )

@router.get("/api/feedback/sign-language")
async def list_feedback(
    page: int = 1,
    limit: int = 20,
    status: str = "ready",
    current_user = Depends(get_current_user)
):
    """List sign language feedback."""
    
    # Query database
    # ... implementation
    
    return {
        'feedback': [],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': 0,
            'pages': 0
        }
    }

@router.delete("/api/feedback/sign-language/{feedback_id}")
async def delete_feedback(
    feedback_id: str,
    current_user = Depends(get_current_user)
):
    """Delete sign language feedback."""
    
    # Check permissions
    # ... implementation
    
    # Delete
    result = orchestrator.delete_feedback(
        feedback_id=feedback_id,
        video_url=video_url,
        deleted_by=current_user.id
    )
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result
```

---

## Testing

### Unit Tests

```python
# tests/test_feedback_workflow.py
import pytest
from core.feedback_workflow import VideoValidator, FeedbackWorkflowOrchestrator

def test_video_validator_valid_file():
    """Test validation of valid video file."""
    is_valid, errors = VideoValidator.validate_all(
        'feedback.mp4',
        20 * 1024 * 1024,  # 20 MB
        45.0  # 45 seconds
    )
    assert is_valid
    assert len(errors) == 0

def test_video_validator_file_too_large():
    """Test validation of oversized file."""
    is_valid, errors = VideoValidator.validate_all(
        'feedback.mp4',
        150 * 1024 * 1024  # 150 MB
    )
    assert not is_valid
    assert 'exceeds' in errors[0].lower()

def test_video_validator_invalid_format():
    """Test validation of invalid format."""
    is_valid, errors = VideoValidator.validate_all(
        'feedback.avi',
        20 * 1024 * 1024
    )
    assert not is_valid
    assert 'unsupported' in errors[0].lower()

def test_workflow_orchestrator_upload():
    """Test feedback upload workflow."""
    orchestrator = FeedbackWorkflowOrchestrator(
        storage_config={'provider': 'local'},
        pubsub_config={'enabled': False}
    )
    
    result = orchestrator.process_upload(
        file_path='/tmp/test.mp4',
        filename='test.mp4',
        file_size=20 * 1024 * 1024,
        user_id='test_user',
        description='Test feedback'
    )
    
    assert result['success']
    assert 'feedback_id' in result
```

### Integration Tests

```python
# tests/test_feedback_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_feedback_success():
    """Test successful feedback upload."""
    with open('test_video.mp4', 'rb') as video_file:
        response = client.post(
            '/api/feedback/sign-language',
            files={'video': video_file},
            data={
                'description': 'Test feedback',
                'tags': 'test,feedback'
            },
            headers={'Authorization': 'Bearer test_token'}
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data['success'] == True
    assert 'feedback_id' in data

def test_upload_feedback_invalid_format():
    """Test upload with invalid format."""
    with open('test_file.txt', 'rb') as file:
        response = client.post(
            '/api/feedback/sign-language',
            files={'video': file},
            headers={'Authorization': 'Bearer test_token'}
        )
    
    assert response.status_code == 400

def test_list_feedback():
    """Test listing feedback."""
    response = client.get(
        '/api/feedback/sign-language',
        headers={'Authorization': 'Bearer test_token'}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert 'feedback' in data
    assert 'pagination' in data
```

### Manual Testing

1. **Upload Test**
   - Upload valid .mp4 file (< 100MB)
   - Upload invalid format (should fail)
   - Upload oversized file (should fail)

2. **Dashboard Test**
   - View feedback list
   - Play videos
   - Check thumbnails
   - Verify real-time updates

3. **Accessibility Test**
   - Keyboard navigation
   - Screen reader compatibility
   - High contrast mode
   - Visual indicators

---

## Future Enhancements

### Phase 2

- [ ] Video editing (trim, crop) before upload
- [ ] Multiple video upload in single submission
- [ ] Sign language detection and tagging
- [ ] Automatic captioning (for hearing users)
- [ ] Video quality adjustment

### Phase 3

- [ ] Response system (sign language video replies)
- [ ] Discussion threads on feedback
- [ ] Voting/reaction system
- [ ] Translation services
- [ ] Analytics dashboard

### Phase 4

- [ ] Mobile app support
- [ ] Offline upload queue
- [ ] Live streaming feedback sessions
- [ ] AI-assisted categorization
- [ ] Community moderation tools

---

## Resources

### Documentation
- [API.md](API.md) - Complete API reference
- [SETUP.md](SETUP.md) - Setup instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

### External Resources
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Firebase Storage Documentation](https://firebase.google.com/docs/storage)
- [Phoenix PubSub](https://hexdocs.pm/phoenix_pubsub/)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Web Video Best Practices](https://web.dev/video/)

### Example Code
- [feedback_workflow.py](workflow-system/core/feedback_workflow.py) - Core implementation
- [feedback_example.py](workflow-system/examples/feedback_example.py) - Usage examples

---

## Support

For questions or issues:

- **GitHub Issues**: [Report a bug](https://github.com/pinkycollie/PinkFlow/issues)
- **Documentation**: Check this file and API.md
- **Community**: Join GitHub Discussions (when enabled)

---

**Last Updated**: 2025-11-15  
**Version**: 1.0.0  
**Status**: 🚧 In Development

---

**Built with ❤️ for the Deaf-First community**
