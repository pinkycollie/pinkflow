# Flask Platform - Production-Ready Implementation

A Flask-based platform with production-ready enhancements including:
- Circuit breaker pattern for resilience
- Enhanced JWT authentication with refresh tokens
- Smart caching with user preference awareness
- Async video processing
- Event-driven architecture
- HTMX integration with accessibility support
- Comprehensive accessibility features for deaf-first design

## Features

### Security
- ✅ JWT tokens with access and refresh token pattern
- ✅ Token blacklisting/revocation
- ✅ Rate limiting per endpoint
- ✅ CSRF protection
- ✅ Password hashing with bcrypt
- ✅ Secure configuration management

### Performance
- ✅ Database connection pooling
- ✅ Redis caching with user preference awareness
- ✅ Database indexes for optimized queries
- ✅ Async video processing with Celery

### Resilience
- ✅ Circuit breaker pattern for external services
- ✅ Graceful error handling
- ✅ Event-driven architecture for loose coupling

### Accessibility
- ✅ User model with comprehensive accessibility preferences
- ✅ Visual density levels (1-5)
- ✅ Sign language preference support
- ✅ Motion sensitivity settings
- ✅ Color contrast options
- ✅ Reading level preferences
- ✅ HTMX renderer with accessibility-aware template variants

### Architecture
- ✅ Modular blueprint system
- ✅ Application factory pattern
- ✅ Shared service layer
- ✅ Event bus for cross-module communication

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- (Optional) Celery for async processing

### Installation

1. Clone the repository:
```bash
git clone https://github.com/pinkycollie/pinkflow.git
cd pinkflow
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from example:
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
- Set `SECRET_KEY` and `REFRESH_SECRET_KEY`
- Configure database URL
- Configure Redis URL

6. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

7. Run the application:
```bash
python run.py
```

## Configuration

Environment variables can be set in `.env` file:

- `FLASK_ENV`: Application environment (development, testing, production)
- `SECRET_KEY`: Secret key for JWT access tokens
- `REFRESH_SECRET_KEY`: Secret key for JWT refresh tokens
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `CELERY_BROKER_URL`: Celery broker URL
- `VIDEO_UPLOAD_FOLDER`: Directory for video uploads

## API Endpoints

### Authentication (`/api/auth`)

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and receive tokens
- `POST /api/auth/logout` - Logout and revoke tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/user` - Get current user info
- `PUT /api/auth/user/preferences` - Update accessibility preferences

### Example Requests

#### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "securepassword",
    "preferred_sign_language": "ASL"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

#### Get User Info
```bash
curl -X GET http://localhost:5000/api/auth/user \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing

Run tests with pytest:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Architecture

### Directory Structure
```
pinkflow/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models.py             # Database models
│   ├── extensions.py         # Flask extensions
│   ├── core/                 # Core services
│   │   ├── auth/            # Authentication service
│   │   ├── video/           # Video processing service
│   │   ├── cache/           # Smart caching service
│   │   ├── frontend/        # HTMX renderer
│   │   ├── event_bus/       # Event-driven architecture
│   │   ├── monitoring/      # Metrics and monitoring
│   │   └── circuit_breaker.py
│   ├── modules/             # Feature modules (blueprints)
│   │   └── auth/           # Auth module
│   ├── static/             # Static files
│   └── templates/          # HTML templates
├── config/
│   └── config.py           # Configuration
├── tests/                  # Test suite
├── requirements.txt        # Dependencies
└── run.py                 # Application entry point
```

### Core Components

**Circuit Breaker**: Prevents cascading failures by monitoring service health
**Enhanced Auth Service**: JWT with access/refresh tokens and revocation
**Smart Cache**: User preference-aware caching
**Event Bus**: Pub/sub pattern for module communication
**HTMX Renderer**: Accessibility-aware template rendering

## Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY` and `REFRESH_SECRET_KEY`
- [ ] Use production database (PostgreSQL)
- [ ] Configure Redis for caching and rate limiting
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up monitoring and logging
- [ ] Configure Celery workers for video processing
- [ ] Set up database backups
- [ ] Configure CDN for video content (optional)

### Recommended Stack
- **Web Server**: Gunicorn or uWSGI
- **Reverse Proxy**: Nginx
- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis
- **Task Queue**: Celery with Redis broker
- **Deployment**: Docker or Cloud Run

## License

See LICENSE file for details.

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.
