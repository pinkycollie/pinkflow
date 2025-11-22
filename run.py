"""
Application entry point.
Run this file to start the Flask development server.

WARNING: Debug mode is enabled for development only.
For production, use a WSGI server like Gunicorn and set debug=False.
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug mode should NEVER be enabled in production
    # This is for development use only
    app.run(host='0.0.0.0', port=5000, debug=True)
