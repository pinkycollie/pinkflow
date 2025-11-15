"""
PinkFlow Sign Language Feedback - Example Usage

This module demonstrates how to use the sign language feedback system
with the workflow orchestrator.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.feedback_workflow import (
    FeedbackWorkflowOrchestrator,
    VideoValidator,
    FeedbackMetadata,
    FeedbackStatus,
    EXAMPLE_AWS_S3_CONFIG,
    EXAMPLE_FIREBASE_CONFIG,
    EXAMPLE_PUBSUB_CONFIG
)


def example_basic_upload():
    """
    Example 1: Basic feedback upload workflow
    """
    print("=" * 80)
    print("Example 1: Basic Feedback Upload")
    print("=" * 80)
    
    # Initialize orchestrator
    storage_config = {
        'provider': 'local',
        'base_url': 'https://storage.pinkflow.dev'
    }
    
    pubsub_config = {
        'enabled': True,
        'type': 'mock'
    }
    
    orchestrator = FeedbackWorkflowOrchestrator(storage_config, pubsub_config)
    
    # Simulate file upload
    file_path = "/tmp/sign_language_feedback.mp4"
    filename = "my_feedback.mp4"
    file_size = 15 * 1024 * 1024  # 15 MB
    user_id = "user123"
    description = "Feedback about the new accessibility features"
    tags = ["accessibility", "feature-request", "ui"]
    
    print(f"\nUploading feedback:")
    print(f"  File: {filename}")
    print(f"  Size: {file_size / (1024*1024):.2f} MB")
    print(f"  User: {user_id}")
    print(f"  Description: {description}")
    print(f"  Tags: {', '.join(tags)}")
    
    # Process upload
    result = orchestrator.process_upload(
        file_path=file_path,
        filename=filename,
        file_size=file_size,
        user_id=user_id,
        description=description,
        tags=tags
    )
    
    print(f"\nResult:")
    print(f"  Success: {result['success']}")
    if result['success']:
        print(f"  Feedback ID: {result['feedback_id']}")
        print(f"  Video URL: {result['metadata']['video_url']}")
        print(f"  Thumbnail URL: {result['metadata']['thumbnail_url']}")
        print(f"  Status: {result['metadata']['status']}")
    else:
        print(f"  Errors: {', '.join(result['errors'])}")
    
    print()


def example_validation():
    """
    Example 2: File validation
    """
    print("=" * 80)
    print("Example 2: File Validation")
    print("=" * 80)
    
    validator = VideoValidator()
    
    # Test cases
    test_cases = [
        {
            'name': 'Valid MP4',
            'filename': 'feedback.mp4',
            'file_size': 20 * 1024 * 1024,
            'duration': 45.0
        },
        {
            'name': 'File too large',
            'filename': 'feedback.mp4',
            'file_size': 150 * 1024 * 1024,
            'duration': 30.0
        },
        {
            'name': 'Invalid format',
            'filename': 'feedback.avi',
            'file_size': 10 * 1024 * 1024,
            'duration': 30.0
        },
        {
            'name': 'Video too long',
            'filename': 'feedback.mp4',
            'file_size': 50 * 1024 * 1024,
            'duration': 400.0
        },
        {
            'name': 'Video too short',
            'filename': 'feedback.mov',
            'file_size': 1 * 1024 * 1024,
            'duration': 0.5
        }
    ]
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"  File: {test['filename']}")
        print(f"  Size: {test['file_size'] / (1024*1024):.2f} MB")
        print(f"  Duration: {test['duration']}s")
        
        is_valid, errors = validator.validate_all(
            test['filename'],
            test['file_size'],
            test['duration']
        )
        
        print(f"  Valid: {is_valid}")
        if not is_valid:
            print(f"  Errors:")
            for error in errors:
                print(f"    - {error}")
    
    print()


def example_failed_upload():
    """
    Example 3: Failed upload due to validation errors
    """
    print("=" * 80)
    print("Example 3: Failed Upload (Validation Errors)")
    print("=" * 80)
    
    orchestrator = FeedbackWorkflowOrchestrator(
        {'provider': 'local', 'base_url': 'https://storage.pinkflow.dev'},
        {'enabled': True, 'type': 'mock'}
    )
    
    # Try to upload invalid file
    result = orchestrator.process_upload(
        file_path="/tmp/invalid_file.avi",
        filename="feedback.avi",
        file_size=150 * 1024 * 1024,  # Too large
        user_id="user456",
        description="This upload should fail"
    )
    
    print(f"\nUpload attempt result:")
    print(f"  Success: {result['success']}")
    print(f"  Errors:")
    for error in result['errors']:
        print(f"    - {error}")
    print(f"  Status: {result['metadata']['status']}")
    
    print()


def example_feedback_deletion():
    """
    Example 4: Deleting feedback
    """
    print("=" * 80)
    print("Example 4: Feedback Deletion")
    print("=" * 80)
    
    orchestrator = FeedbackWorkflowOrchestrator(
        {'provider': 'local', 'base_url': 'https://storage.pinkflow.dev'},
        {'enabled': True, 'type': 'mock'}
    )
    
    # Simulate deletion
    feedback_id = "feedback_user123_1699564800"
    video_url = "https://storage.pinkflow.dev/feedback/feedback_user123_1699564800/video.mp4"
    deleted_by = "admin_user"
    
    print(f"\nDeleting feedback:")
    print(f"  Feedback ID: {feedback_id}")
    print(f"  Video URL: {video_url}")
    print(f"  Deleted by: {deleted_by}")
    
    result = orchestrator.delete_feedback(feedback_id, video_url, deleted_by)
    
    print(f"\nDeletion result:")
    print(f"  Success: {result['success']}")
    if result['success']:
        print(f"  Deleted at: {result['deleted_at']}")
    else:
        print(f"  Error: {result.get('error')}")
    
    print()


def example_with_aws_s3():
    """
    Example 5: Using AWS S3 configuration (conceptual)
    """
    print("=" * 80)
    print("Example 5: AWS S3 Configuration (Conceptual)")
    print("=" * 80)
    
    print("\nAWS S3 Configuration Example:")
    print("```python")
    print("storage_config = {")
    print("    'provider': 'aws_s3',")
    print("    'bucket': 'pinkflow-feedback',")
    print("    'region': 'us-east-1',")
    print("    'access_key_id': 'YOUR_ACCESS_KEY',")
    print("    'secret_access_key': 'YOUR_SECRET_KEY',")
    print("    'base_url': 'https://pinkflow-feedback.s3.amazonaws.com'")
    print("}")
    print("```")
    
    print("\nNote: In production, you would:")
    print("  1. Install boto3 for AWS S3 integration")
    print("  2. Set up IAM roles with appropriate permissions")
    print("  3. Configure CORS settings on the S3 bucket")
    print("  4. Implement proper error handling and retries")
    print("  5. Use CloudFront for CDN distribution")
    
    print()


def example_with_firebase():
    """
    Example 6: Using Firebase Storage configuration (conceptual)
    """
    print("=" * 80)
    print("Example 6: Firebase Storage Configuration (Conceptual)")
    print("=" * 80)
    
    print("\nFirebase Storage Configuration Example:")
    print("```python")
    print("storage_config = {")
    print("    'provider': 'firebase',")
    print("    'bucket': 'pinkflow-feedback.appspot.com',")
    print("    'credentials_path': '/path/to/firebase-credentials.json',")
    print("    'base_url': 'https://firebasestorage.googleapis.com'")
    print("}")
    print("```")
    
    print("\nNote: In production, you would:")
    print("  1. Install firebase-admin SDK")
    print("  2. Set up Firebase project and storage rules")
    print("  3. Configure authentication and authorization")
    print("  4. Implement security rules for video access")
    print("  5. Use Firebase Cloud Functions for processing")
    
    print()


def example_deaf_first_considerations():
    """
    Example 7: Deaf-First design considerations
    """
    print("=" * 80)
    print("Example 7: Deaf-First Design Considerations")
    print("=" * 80)
    
    print("\nDeaf-First Design Principles for Feedback System:")
    print()
    print("1. Visual Communication Priority")
    print("   - Sign language videos are the PRIMARY form of feedback")
    print("   - Text descriptions are OPTIONAL and supplementary")
    print("   - Video player must have accessible controls")
    print()
    print("2. Accessibility Features")
    print("   - High-contrast video player controls")
    print("   - Keyboard navigation support")
    print("   - Clear visual indicators for upload progress")
    print("   - Error messages with visual icons")
    print()
    print("3. Technical Considerations")
    print("   - High-quality video encoding (preserve sign details)")
    print("   - Fast loading times (minimize buffering)")
    print("   - Multiple resolution options")
    print("   - Thumbnail selection showing clear hand positions")
    print()
    print("4. User Experience")
    print("   - Simple, visual upload interface")
    print("   - Preview before upload")
    print("   - Clear feedback on upload status")
    print("   - Easy retake/re-record option")
    print()
    print("5. Admin Dashboard")
    print("   - Video preview without auto-play (user control)")
    print("   - Visual tags and categorization")
    print("   - Batch processing capabilities")
    print("   - Response system supporting sign language replies")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "PinkFlow Sign Language Feedback System" + " " * 20 + "║")
    print("║" + " " * 30 + "Example Usage" + " " * 35 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Run all examples
    example_basic_upload()
    example_validation()
    example_failed_upload()
    example_feedback_deletion()
    example_with_aws_s3()
    example_with_firebase()
    example_deaf_first_considerations()
    
    print("=" * 80)
    print("All examples completed!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Integrate with actual cloud storage (AWS S3, Firebase, etc.)")
    print("  2. Connect to database for persistence")
    print("  3. Implement Phoenix PubSub for real-time notifications")
    print("  4. Add video processing pipeline (transcoding, thumbnails)")
    print("  5. Build frontend UI with React/Next.js")
    print("  6. Add authentication and authorization")
    print("  7. Implement admin dashboard")
    print("  8. Add analytics and monitoring")
    print()


if __name__ == "__main__":
    main()
