"""
Enhanced authentication service with secure JWT tokens.
Implements access and refresh token pattern with revocation support.
"""
import secrets
from datetime import datetime, timedelta
import jwt
from flask import current_app, g, request, jsonify
from functools import wraps
from app.models import User, TokenBlacklist
from app.extensions import db


class EnhancedAuthService:
    """Authentication service with enhanced security features."""
    
    @staticmethod
    def generate_secure_token(user):
        """
        Generate secure tokens with access and refresh token pattern.
        
        Args:
            user: User instance
            
        Returns:
            Dictionary with access_token, refresh_token, and expires_in
        """
        # Short-lived access token (15 minutes)
        access_payload = {
            'user_id': user.id,
            'type': 'access',
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)  # JWT ID for revocation
        }
        
        # Long-lived refresh token (7 days)
        refresh_payload = {
            'user_id': user.id,
            'type': 'refresh',
            'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)
        }
        
        access_token = jwt.encode(
            access_payload, 
            current_app.config['SECRET_KEY'], 
            algorithm=current_app.config['JWT_ALGORITHM']
        )
        
        refresh_token = jwt.encode(
            refresh_payload, 
            current_app.config['REFRESH_SECRET_KEY'], 
            algorithm=current_app.config['JWT_ALGORITHM']
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': 900  # 15 minutes in seconds
        }
    
    @staticmethod
    def verify_access_token(token):
        """
        Verify and decode an access token.
        
        Args:
            token: JWT access token string
            
        Returns:
            Decoded payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            
            # Check if token is revoked
            if TokenBlacklist.is_token_revoked(payload.get('jti')):
                return None
            
            # Verify token type
            if payload.get('type') != 'access':
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def verify_refresh_token(token):
        """
        Verify and decode a refresh token.
        
        Args:
            token: JWT refresh token string
            
        Returns:
            Decoded payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['REFRESH_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            
            # Check if token is revoked
            if TokenBlacklist.is_token_revoked(payload.get('jti')):
                return None
            
            # Verify token type
            if payload.get('type') != 'refresh':
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def refresh_access_token(refresh_token):
        """
        Generate a new access token using a refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token or None if refresh token is invalid
        """
        payload = EnhancedAuthService.verify_refresh_token(refresh_token)
        if not payload:
            return None
        
        user = User.query.get(payload['user_id'])
        if not user:
            return None
        
        # Generate new access token
        access_payload = {
            'user_id': user.id,
            'type': 'access',
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)
        }
        
        access_token = jwt.encode(
            access_payload,
            current_app.config['SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
        
        return {
            'access_token': access_token,
            'expires_in': 900
        }
    
    @staticmethod
    def revoke_token(token, token_type='access'):
        """
        Revoke a token by adding it to the blacklist.
        
        Args:
            token: Token to revoke
            token_type: Type of token ('access' or 'refresh')
        """
        secret_key = (
            current_app.config['SECRET_KEY'] if token_type == 'access'
            else current_app.config['REFRESH_SECRET_KEY']
        )
        
        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            
            TokenBlacklist.revoke_token(
                jti=payload['jti'],
                token_type=token_type,
                user_id=payload['user_id'],
                expires_at=datetime.fromtimestamp(payload['exp'])
            )
            
        except jwt.InvalidTokenError:
            pass  # Token is already invalid
    
    @staticmethod
    def login(email, password):
        """
        Authenticate a user and generate tokens.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with tokens and user info, or None if authentication fails
        """
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        tokens = EnhancedAuthService.generate_secure_token(user)
        
        return {
            **tokens,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'accessibility_preferences': user.accessibility_preferences
            }
        }


def token_required(f):
    """
    Decorator to require valid JWT token for route access.
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route():
            user_id = g.user_id
            return {'message': 'Protected data'}
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = EnhancedAuthService.verify_access_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Store user_id in Flask's g object for use in the route
        g.user_id = payload['user_id']
        
        return f(*args, **kwargs)
    
    return decorated
