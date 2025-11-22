"""
Flask application factory.
Creates and configures the Flask application with all extensions and blueprints.
"""
import os
import importlib
import logging
from flask import Flask
from config import config
from app.extensions import init_extensions
from app.core.event_bus import event_bus, Events
from app.core.video import make_celery


def create_app(config_name=None):
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration environment name (development, testing, production)
        
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Configure Celery
    celery = make_celery(app)
    app.celery = celery
    
    # Register blueprints/modules
    register_modules(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Setup event listeners
    setup_event_listeners(app)
    
    # Create database tables
    with app.app_context():
        from app.extensions import db
        db.create_all()
    
    app.logger.info(f"Application created with {config_name} configuration")
    
    return app


def setup_logging(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    if not app.debug:
        # Production logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


def register_modules(app):
    """
    Dynamically register modules as blueprints.
    
    This implements the modular blueprint system mentioned in the review.
    Modules are loaded from app/modules directory.
    
    Args:
        app: Flask application instance
    """
    modules_path = os.path.join(os.path.dirname(__file__), 'modules')
    
    # Check if modules directory exists
    if not os.path.exists(modules_path):
        app.logger.warning(f"Modules directory not found: {modules_path}")
        return
    
    # Get list of module directories
    module_dirs = [
        d for d in os.listdir(modules_path)
        if os.path.isdir(os.path.join(modules_path, d))
        and not d.startswith('_')
    ]
    
    for module_name in module_dirs:
        try:
            # Import the module
            module = importlib.import_module(f"app.modules.{module_name}")
            
            # Register blueprint if it exists
            if hasattr(module, 'blueprint'):
                app.register_blueprint(module.blueprint)
                app.logger.info(f"Registered module: {module_name}")
                
                # Publish module loaded event
                event_bus.publish(Events.MODULE_LOADED, module_name=module_name)
            else:
                app.logger.warning(f"Module {module_name} has no blueprint attribute")
                
        except Exception as e:
            app.logger.error(f"Failed to register module {module_name}: {str(e)}")
            event_bus.publish(
                Events.MODULE_ERROR,
                module_name=module_name,
                error=str(e)
            )


def register_error_handlers(app):
    """
    Register error handlers for common HTTP errors.
    
    Args:
        app: Flask application instance
    """
    from flask import jsonify
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400


def setup_event_listeners(app):
    """
    Setup event listeners for application events.
    
    Args:
        app: Flask application instance
    """
    # Example: Log user login events
    def log_user_login(user_id):
        app.logger.info(f"User {user_id} logged in")
    
    event_bus.subscribe(Events.USER_LOGIN, log_user_login)
    
    # Example: Track video processing events
    def track_video_processing(video_id, user_id):
        app.logger.info(f"Video {video_id} processing started for user {user_id}")
    
    event_bus.subscribe(Events.VIDEO_PROCESSING_STARTED, track_video_processing)
