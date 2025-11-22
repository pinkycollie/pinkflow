"""
Database models for the application.
Includes User model with accessibility preferences and optimizations.
"""
from datetime import datetime
import json
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    User model with comprehensive accessibility preferences.
    Optimized with indexes for common queries.
    """
    __tablename__ = 'users'
    
    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    
    # Accessibility preferences
    preferred_sign_language = db.Column(db.String(10), default='ASL', index=True)
    visual_density = db.Column(db.Integer, default=3)  # 1-5 scale
    reading_level = db.Column(db.Integer, default=3)  # 1-5 scale
    motion_sensitivity = db.Column(db.Boolean, default=False)
    color_contrast = db.Column(db.String(20), default='normal')  # normal, high
    
    # Module authorization (JSON field)
    _authorized_modules = db.Column('authorized_modules', db.Text, default='[]')
    
    # User preferences (JSON field for complex preferences)
    _module_preferences = db.Column('module_preferences', db.Text, default='{}')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Add composite indexes for common queries
    __table_args__ = (
        db.Index('idx_user_email', 'email'),
        db.Index('idx_user_sign_language', 'preferred_sign_language'),
    )
    
    @property
    def authorized_modules(self):
        """Get authorized modules as a list."""
        try:
            return json.loads(self._authorized_modules)
        except (json.JSONDecodeError, TypeError):
            return []
    
    @authorized_modules.setter
    def authorized_modules(self, value):
        """Set authorized modules from a list."""
        self._authorized_modules = json.dumps(value) if value else '[]'
    
    @property
    def module_preferences(self):
        """Get module preferences as a dictionary."""
        try:
            return json.loads(self._module_preferences)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    @module_preferences.setter
    def module_preferences(self, value):
        """Set module preferences from a dictionary."""
        self._module_preferences = json.dumps(value) if value else '{}'
    
    @property
    def accessibility_preferences(self):
        """Get all accessibility preferences as a dictionary."""
        return {
            'preferred_sign_language': self.preferred_sign_language,
            'visual_density': self.visual_density,
            'reading_level': self.reading_level,
            'motion_sensitivity': self.motion_sensitivity,
            'color_contrast': self.color_contrast
        }
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_by_module_access(cls, module_name):
        """
        Optimized query for users with module access.
        
        Args:
            module_name: Name of the module to check access for
            
        Returns:
            Query object for users with access to the module
        """
        return cls.query.filter(
            cls._authorized_modules.contains(f'"{module_name}"')
        ).options(
            db.defer(cls._module_preferences)  # Don't load unless needed
        )
    
    def has_module_access(self, module_name):
        """
        Check if user has access to a specific module.
        
        Args:
            module_name: Name of the module to check
            
        Returns:
            Boolean indicating access
        """
        return module_name in self.authorized_modules
    
    def __repr__(self):
        return f'<User {self.username}>'


class TokenBlacklist(db.Model):
    """
    Token blacklist for JWT revocation.
    Stores revoked tokens to prevent reuse.
    """
    __tablename__ = 'token_blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), unique=True, nullable=False, index=True)
    token_type = db.Column(db.String(20), nullable=False)  # access or refresh
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref='revoked_tokens')
    
    @classmethod
    def is_token_revoked(cls, jti):
        """
        Check if a token has been revoked.
        
        Args:
            jti: JWT ID to check
            
        Returns:
            Boolean indicating if token is revoked
        """
        return cls.query.filter_by(jti=jti).first() is not None
    
    @classmethod
    def revoke_token(cls, jti, token_type, user_id, expires_at):
        """
        Revoke a token by adding it to the blacklist.
        
        Args:
            jti: JWT ID
            token_type: Type of token (access or refresh)
            user_id: User ID who owns the token
            expires_at: When the token expires
        """
        token = cls(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at
        )
        db.session.add(token)
        db.session.commit()
    
    def __repr__(self):
        return f'<TokenBlacklist {self.jti}>'
