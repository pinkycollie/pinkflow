"""
Configuration management for Flask application.
Supports multiple environments with production-ready settings.
"""
import os
from datetime import timedelta


class Config:
    """Base configuration with common settings."""
    
    # App Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY', 'dev-refresh-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'postgresql://localhost/pinkflow_dev'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 30
    }
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_CONFIG = {
        'connection_pool_kwargs': {
            'max_connections': 100,
            'retry_on_timeout': True,
            'health_check_interval': 30
        },
        'decode_responses': True
    }
    
    # Cache Configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ALGORITHM = 'HS256'
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = "100/hour"
    
    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
    
    # Video Service
    VIDEO_UPLOAD_FOLDER = os.environ.get('VIDEO_UPLOAD_FOLDER', '/tmp/videos')
    VIDEO_MAX_SIZE_MB = 100
    VIDEO_ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm'}
    
    # CDN Configuration (optional)
    CDN_ENABLED = os.environ.get('CDN_ENABLED', 'false').lower() == 'true'
    CDN_BASE_URL = os.environ.get('CDN_BASE_URL', '')
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Accessibility Defaults
    DEFAULT_VISUAL_DENSITY = 3
    DEFAULT_SIGN_LANGUAGE = 'ASL'
    
    # Circuit Breaker Settings
    CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT = 60


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    
    # Enforce stronger security in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
