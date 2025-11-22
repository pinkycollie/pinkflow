"""
Tests for User model and database operations.
"""
import pytest
from app.models import User, TokenBlacklist
from app.extensions import db
from datetime import datetime, timedelta


def test_user_creation(app):
    """Test creating a new user."""
    with app.app_context():
        user = User(
            email='test@example.com',
            username='testuser',
            preferred_sign_language='ASL'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.email == 'test@example.com'
        assert user.check_password('password123')


def test_user_password_hashing(app):
    """Test password hashing and verification."""
    with app.app_context():
        user = User(email='test@example.com', username='test')
        user.set_password('mypassword')
        
        assert user.password_hash != 'mypassword'
        assert user.check_password('mypassword')
        assert not user.check_password('wrongpassword')


def test_user_accessibility_preferences(app):
    """Test user accessibility preferences."""
    with app.app_context():
        user = User(
            email='test@example.com',
            username='test',
            preferred_sign_language='BSL',
            visual_density=4,
            reading_level=2,
            motion_sensitivity=True,
            color_contrast='high'
        )
        
        prefs = user.accessibility_preferences
        assert prefs['preferred_sign_language'] == 'BSL'
        assert prefs['visual_density'] == 4
        assert prefs['reading_level'] == 2
        assert prefs['motion_sensitivity'] == True
        assert prefs['color_contrast'] == 'high'


def test_user_authorized_modules(app):
    """Test user authorized modules property."""
    with app.app_context():
        user = User(email='test@example.com', username='test')
        
        # Set authorized modules
        user.authorized_modules = ['auth', 'video', 'document']
        db.session.add(user)
        db.session.commit()
        
        # Retrieve and check
        retrieved_user = User.query.filter_by(email='test@example.com').first()
        assert 'auth' in retrieved_user.authorized_modules
        assert 'video' in retrieved_user.authorized_modules
        assert 'document' in retrieved_user.authorized_modules


def test_user_has_module_access(app):
    """Test checking user module access."""
    with app.app_context():
        user = User(email='test@example.com', username='test')
        user.authorized_modules = ['auth', 'video']
        
        assert user.has_module_access('auth')
        assert user.has_module_access('video')
        assert not user.has_module_access('admin')


def test_get_by_module_access(app):
    """Test querying users by module access."""
    with app.app_context():
        user1 = User(email='user1@example.com', username='user1')
        user1.authorized_modules = ['video', 'auth']
        
        user2 = User(email='user2@example.com', username='user2')
        user2.authorized_modules = ['auth']
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        video_users = User.get_by_module_access('video').all()
        assert len(video_users) == 1
        assert video_users[0].email == 'user1@example.com'


def test_token_blacklist(app):
    """Test token blacklist functionality."""
    with app.app_context():
        user = User(email='test@example.com', username='test')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        # Add token to blacklist
        jti = 'test-jti-123'
        TokenBlacklist.revoke_token(
            jti=jti,
            token_type='access',
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        
        # Check if token is revoked
        assert TokenBlacklist.is_token_revoked(jti)
        assert not TokenBlacklist.is_token_revoked('non-existent-jti')
