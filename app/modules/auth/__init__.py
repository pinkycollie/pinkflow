"""
Authentication module blueprint.
Handles user authentication and token management endpoints.
"""
from flask import Blueprint, request, jsonify, g
from app.core.auth import EnhancedAuthService, token_required
from app.core.event_bus import event_bus, Events
from app.extensions import db, limiter
from app.models import User

# Create blueprint
blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')


@blueprint.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """
    Register a new user.
    
    POST /api/auth/register
    Body: {
        "email": "user@example.com",
        "password": "password123",
        "username": "username",
        "preferred_sign_language": "ASL" (optional)
    }
    """
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ['email', 'password', 'username']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    # Create new user
    user = User(
        email=data['email'],
        username=data['username'],
        preferred_sign_language=data.get('preferred_sign_language', 'ASL')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Publish user created event
    event_bus.publish(Events.USER_CREATED, user_id=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
    }), 201


@blueprint.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """
    Login and receive JWT tokens.
    
    POST /api/auth/login
    Body: {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing email or password'}), 400
    
    result = EnhancedAuthService.login(data['email'], data['password'])
    
    if not result:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Publish login event
    event_bus.publish(Events.USER_LOGIN, user_id=result['user']['id'])
    
    return jsonify(result), 200


@blueprint.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Logout and revoke tokens.
    
    POST /api/auth/logout
    Headers: Authorization: Bearer <access_token>
    Body: {
        "refresh_token": "<refresh_token>" (optional)
    }
    """
    # Get access token from header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1] if auth_header else None
    
    if access_token:
        EnhancedAuthService.revoke_token(access_token, 'access')
    
    # Revoke refresh token if provided
    data = request.get_json() or {}
    refresh_token = data.get('refresh_token')
    if refresh_token:
        EnhancedAuthService.revoke_token(refresh_token, 'refresh')
    
    # Publish logout event
    event_bus.publish(Events.USER_LOGOUT, user_id=g.user_id)
    
    return jsonify({'message': 'Logged out successfully'}), 200


@blueprint.route('/refresh', methods=['POST'])
@limiter.limit("20 per minute")
def refresh():
    """
    Refresh access token using refresh token.
    
    POST /api/auth/refresh
    Body: {
        "refresh_token": "<refresh_token>"
    }
    """
    data = request.get_json()
    
    if not data or 'refresh_token' not in data:
        return jsonify({'error': 'Missing refresh token'}), 400
    
    result = EnhancedAuthService.refresh_access_token(data['refresh_token'])
    
    if not result:
        return jsonify({'error': 'Invalid or expired refresh token'}), 401
    
    return jsonify(result), 200


@blueprint.route('/user', methods=['GET'])
@token_required
def get_user():
    """
    Get current user information.
    
    GET /api/auth/user
    Headers: Authorization: Bearer <access_token>
    """
    user = User.query.get(g.user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'accessibility_preferences': user.accessibility_preferences,
        'authorized_modules': user.authorized_modules,
        'last_login': user.last_login.isoformat() if user.last_login else None
    }), 200


@blueprint.route('/user/preferences', methods=['PUT'])
@token_required
def update_preferences():
    """
    Update user accessibility preferences.
    
    PUT /api/auth/user/preferences
    Headers: Authorization: Bearer <access_token>
    Body: {
        "preferred_sign_language": "ASL",
        "visual_density": 4,
        "reading_level": 3,
        "motion_sensitivity": false,
        "color_contrast": "high"
    }
    """
    user = User.query.get(g.user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update preferences
    if 'preferred_sign_language' in data:
        user.preferred_sign_language = data['preferred_sign_language']
    
    if 'visual_density' in data:
        user.visual_density = data['visual_density']
    
    if 'reading_level' in data:
        user.reading_level = data['reading_level']
    
    if 'motion_sensitivity' in data:
        user.motion_sensitivity = data['motion_sensitivity']
    
    if 'color_contrast' in data:
        user.color_contrast = data['color_contrast']
    
    db.session.commit()
    
    # Publish preferences updated event
    event_bus.publish(Events.PREFERENCES_UPDATED, user_id=user.id)
    
    return jsonify({
        'message': 'Preferences updated successfully',
        'accessibility_preferences': user.accessibility_preferences
    }), 200
