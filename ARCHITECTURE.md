# Flask Platform Architecture Documentation

## Overview

This Flask platform implements a production-ready, deaf-first accessible web application with comprehensive security, performance optimizations, and resilience features.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  (React/HTMX Frontend with Accessibility Support)                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP/REST API
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Flask Application Layer                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │         Application Factory (app/__init__.py)          │     │
│  │  - Extension initialization                            │     │
│  │  - Blueprint registration                              │     │
│  │  - Error handlers                                      │     │
│  │  - Event listeners                                     │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │   Extensions    │  │    Blueprints    │  │ Core Services│   │
│  │                 │  │                  │  │              │   │
│  │ - SQLAlchemy   │  │ - Auth Module    │  │ - Auth       │   │
│  │ - Flask-Migrate│  │ - Video Module   │  │ - Video      │   │
│  │ - Flask-Caching│  │ - Document       │  │ - Cache      │   │
│  │ - Flask-Limiter│  │   Module         │  │ - EventBus   │   │
│  │ - Flask-CORS   │  │ - Custom Modules │  │ - HTMX       │   │
│  │                 │  │                  │  │ - Monitoring │   │
│  └─────────────────┘  └──────────────────┘  └──────────────┘   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  PostgreSQL │ │    Redis    │ │   Celery    │
│             │ │             │ │   Workers   │
│ - Users     │ │ - Cache     │ │             │
│ - Tokens    │ │ - Sessions  │ │ - Video     │
│ - Metadata  │ │ - Rate Limit│ │   Processing│
└─────────────┘ └─────────────┘ └─────────────┘
```

## Core Components

### 1. Application Factory Pattern

**File**: `app/__init__.py`

The application uses the factory pattern for flexibility and testability:

```python
def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Register modules
    register_modules(app)
    
    return app
```

**Benefits**:
- Multiple instances for different environments
- Easier testing with different configurations
- Delayed extension initialization

### 2. Modular Blueprint System

**Directory**: `app/modules/`

Each feature is a self-contained blueprint:

```
app/modules/
├── auth/           # Authentication & user management
│   └── __init__.py # Blueprint with routes
├── video/          # Video processing (can be added)
└── document/       # Document handling (can be added)
```

**Adding a New Module**:
1. Create directory in `app/modules/`
2. Define `blueprint` in `__init__.py`
3. Application factory auto-discovers and registers it

### 3. Core Services Layer

**Directory**: `app/core/`

Shared services used across modules:

#### Authentication Service (`app/core/auth/`)
- JWT token generation (access + refresh)
- Token verification and validation
- Token revocation with blacklist
- User login/logout

#### Video Service (`app/core/video/`)
- Async video processing with Celery
- Video validation (type, size)
- Sign language processing
- Circuit breaker protection

#### Caching Service (`app/core/cache/`)
- User preference-aware caching
- Smart cache key generation
- Cache invalidation strategies

#### Event Bus (`app/core/event_bus/`)
- Pub/sub pattern for loose coupling
- Standard event definitions
- Cross-module communication

#### HTMX Renderer (`app/core/frontend/`)
- Accessibility-aware template selection
- Visual density variants
- HTMX request detection

#### Monitoring (`app/core/monitoring/`)
- Accessibility metrics tracking
- Performance monitoring
- Video load time tracking
- Sign language accuracy metrics

### 4. Database Layer

**File**: `app/models.py`

#### User Model
```python
class User(db.Model):
    # Identity
    id, email, username, password_hash
    
    # Accessibility Preferences
    preferred_sign_language      # ASL, BSL, etc.
    visual_density              # 1-5 scale
    reading_level               # 1-5 scale
    motion_sensitivity          # Boolean
    color_contrast              # normal, high
    
    # Authorization
    authorized_modules          # JSON list
    module_preferences          # JSON object
```

**Optimizations**:
- Indexes on frequently queried fields
- Deferred loading for large JSON fields
- Connection pooling configuration
- Query optimization methods

#### Token Blacklist Model
```python
class TokenBlacklist(db.Model):
    jti                 # JWT ID
    token_type          # access or refresh
    user_id             # Foreign key
    revoked_at          # Timestamp
    expires_at          # Token expiration
```

### 5. Security Features

#### Circuit Breaker (`app/core/circuit_breaker.py`)
Prevents cascading failures:

```python
@CircuitBreaker(failure_threshold=5, recovery_timeout=60)
def external_api_call():
    # Protected operation
    pass
```

**States**:
- CLOSED: Normal operation
- OPEN: Failures exceeded, fail fast
- HALF_OPEN: Testing recovery

#### Enhanced JWT Authentication
- Short-lived access tokens (15 min)
- Long-lived refresh tokens (7 days)
- Token blacklisting for revocation
- Secure token generation with JTI

#### Rate Limiting
- Per-endpoint configuration
- Redis-backed storage
- User-specific and IP-based limiting

### 6. Event-Driven Architecture

**Event Flow**:
```
User Action → Module → Event Bus → Subscribers → Actions
```

**Example Events**:
- `user.login` → Log event, update metrics
- `video.uploaded` → Queue processing, notify user
- `preferences.updated` → Invalidate cache, re-render

**Benefits**:
- Loose coupling between modules
- Easy to add new features
- Auditing and logging
- Async processing triggers

## Data Flow Examples

### 1. User Registration Flow
```
POST /api/auth/register
    ↓
Auth Blueprint validates input
    ↓
Create User model
    ↓
Hash password with bcrypt
    ↓
Save to PostgreSQL
    ↓
Publish USER_CREATED event
    ↓
Return success response
```

### 2. Protected Resource Access
```
GET /api/auth/user
    ↓
@token_required decorator
    ↓
Verify JWT signature
    ↓
Check token not in blacklist
    ↓
Load user from g.user_id
    ↓
Return user data
```

### 3. Video Processing Flow
```
POST /api/video/upload
    ↓
Validate file (type, size)
    ↓
Save to storage
    ↓
Queue Celery task
    ↓
Publish VIDEO_PROCESSING_STARTED event
    ↓
Return job_id
    ↓
(Async) Celery worker processes
    ↓
Publish VIDEO_PROCESSING_COMPLETED event
```

## Configuration Management

**File**: `config/config.py`

Three environments:
- `DevelopmentConfig`: Debug enabled, SQLite ok
- `TestingConfig`: In-memory DB, no CSRF
- `ProductionConfig`: Strict security, pooling

**Environment Variables** (`.env`):
- `SECRET_KEY`, `REFRESH_SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`

## Testing Strategy

**Directory**: `tests/`

### Test Structure
```
tests/
├── conftest.py              # Fixtures
├── test_auth.py            # Auth endpoints
├── test_circuit_breaker.py # Resilience
└── test_models.py          # Database models
```

### Fixtures
- `app`: Test application instance
- `client`: Test client
- `deaf_user`: User with accessibility preferences
- `accessibility_client`: Authenticated client

### Running Tests
```bash
pytest                      # Run all tests
pytest --cov=app           # With coverage
pytest -v                  # Verbose output
```

## Deployment Architecture

### Development
```
python run.py
    ↓
Flask dev server (port 5000)
    ↓
SQLite database
```

### Production (Recommended)
```
Nginx (Reverse Proxy)
    ↓
Gunicorn (WSGI Server)
    ↓
Flask Application (multiple workers)
    ↓
PostgreSQL (Database)
    ↓
Redis (Cache + Rate Limiting)
    ↓
Celery Workers (Async Tasks)
```

## Scalability Considerations

### Horizontal Scaling
- Stateless application design
- JWT tokens (no server-side sessions)
- Redis for shared cache
- Database connection pooling

### Vertical Scaling
- Connection pool sizing
- Worker process configuration
- Cache hit optimization
- Database query optimization

### Performance Features
- Database indexes
- Query result caching
- Lazy loading relationships
- CDN for static/video content

## Accessibility Features

### Visual Density Levels (1-5)
1. **Minimal**: Essential content only
2. **Low**: Reduced visual elements
3. **Normal**: Standard design
4. **Rich**: Enhanced visuals
5. **Max**: Full experience

### Template Variants
```
templates/
├── page.html              # Normal (density 3)
├── page_minimal.html      # Density 1
├── page_low.html          # Density 2
├── page_rich.html         # Density 4
└── page_max.html          # Density 5
```

### Sign Language Support
- User preference stored
- Video processing adapts
- Avatar/video selection
- Subtitle generation

## Monitoring & Observability

### Metrics Tracked
- Video load times by type
- Sign language accuracy feedback
- Page load times with accessibility features
- Visual density usage patterns
- Reading level preferences

### Logging
- Security events (login, logout)
- Module loading/errors
- Circuit breaker state changes
- Video processing status

## Future Enhancements

1. **Two-Factor Authentication (2FA)**
2. **WebSocket Support** (PinkSync integration)
3. **GraphQL API** (alternative to REST)
4. **Machine Learning Integration** (sign language recognition)
5. **CDN Integration** (CloudFront/Cloudflare)
6. **Microservices Split** (separate video service)
7. **Kubernetes Deployment** (container orchestration)
8. **API Versioning** (v1, v2 endpoints)

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Security Guidelines](https://owasp.org/)
