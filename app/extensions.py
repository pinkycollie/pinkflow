"""
Flask extensions initialization.
Extensions are initialized here and configured in the application factory.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
cors = CORS()


def init_extensions(app):
    """
    Initialize Flask extensions with the app instance.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
