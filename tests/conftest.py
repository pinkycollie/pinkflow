"""
Test configuration and fixtures.
Provides test fixtures for accessibility testing.
"""
import pytest
from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def deaf_user(app):
    """Create test user with deaf-specific preferences."""
    with app.app_context():
        user = User(
            email='test@deaf.example.com',
            username='deafuser',
            preferred_sign_language='ASL',
            visual_density=4,
            reading_level=2
        )
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        # Return user data for test usage
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'password': 'testpassword'
        }


@pytest.fixture
def regular_user(app):
    """Create a regular test user."""
    with app.app_context():
        user = User(
            email='test@example.com',
            username='regularuser',
            preferred_sign_language='ASL',
            visual_density=3,
            reading_level=3
        )
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'password': 'testpassword'
        }


@pytest.fixture
def accessibility_client(app, deaf_user):
    """Client configured for accessibility testing."""
    client = app.test_client()
    
    # Login and get token
    response = client.post('/api/auth/login', json={
        'email': deaf_user['email'],
        'password': deaf_user['password']
    })
    
    data = response.get_json()
    token = data.get('access_token')
    
    # Store token in client for authenticated requests
    client.token = token
    
    return client


def get_auth_header(token):
    """Helper function to create Authorization header."""
    return {'Authorization': f'Bearer {token}'}
