"""
Tests for authentication module.
"""
import pytest
from app.models import User, TokenBlacklist


def test_user_registration(client):
    """Test user registration endpoint."""
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'username': 'newuser',
        'password': 'password123',
        'preferred_sign_language': 'BSL'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User registered successfully'
    assert data['user']['email'] == 'newuser@example.com'
    assert data['user']['username'] == 'newuser'


def test_duplicate_email_registration(client, regular_user):
    """Test that duplicate email registration fails."""
    response = client.post('/api/auth/register', json={
        'email': regular_user['email'],
        'username': 'different',
        'password': 'password123'
    })
    
    assert response.status_code == 409
    data = response.get_json()
    assert 'already registered' in data['error']


def test_login_success(client, regular_user):
    """Test successful login."""
    response = client.post('/api/auth/login', json={
        'email': regular_user['email'],
        'password': regular_user['password']
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'expires_in' in data
    assert data['user']['email'] == regular_user['email']


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'Invalid credentials' in data['error']


def test_get_user_info(accessibility_client):
    """Test getting user information with valid token."""
    response = accessibility_client.get(
        '/api/auth/user',
        headers={'Authorization': f'Bearer {accessibility_client.token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'email' in data
    assert 'accessibility_preferences' in data
    assert data['accessibility_preferences']['preferred_sign_language'] == 'ASL'


def test_get_user_without_token(client):
    """Test that accessing user info without token fails."""
    response = client.get('/api/auth/user')
    
    assert response.status_code == 401


def test_update_preferences(accessibility_client):
    """Test updating user accessibility preferences."""
    response = accessibility_client.put(
        '/api/auth/user/preferences',
        headers={'Authorization': f'Bearer {accessibility_client.token}'},
        json={
            'visual_density': 5,
            'color_contrast': 'high',
            'motion_sensitivity': True
        }
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['accessibility_preferences']['visual_density'] == 5
    assert data['accessibility_preferences']['color_contrast'] == 'high'
    assert data['accessibility_preferences']['motion_sensitivity'] == True


def test_refresh_token(client, regular_user):
    """Test refreshing access token."""
    # Login first
    login_response = client.post('/api/auth/login', json={
        'email': regular_user['email'],
        'password': regular_user['password']
    })
    
    login_data = login_response.get_json()
    refresh_token = login_data['refresh_token']
    
    # Use refresh token to get new access token
    response = client.post('/api/auth/refresh', json={
        'refresh_token': refresh_token
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'expires_in' in data


def test_logout(accessibility_client):
    """Test logout functionality."""
    response = accessibility_client.post(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {accessibility_client.token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'Logged out successfully' in data['message']
