"""
HealthFit AI Chatbot — Routes Package

Provides Flask Blueprints for all HTTP endpoints and a
helper function to register them with the application.

Blueprints
----------
main_bp
    Page routes and health check: GET /, GET /api/health
chat_bp
    Chat API: POST /api/chat, GET /api/history,
              DELETE /api/history
feedback_bp
    Feedback API: POST /api/feedback

Functions
---------
register_blueprints(app)
    Import and register all blueprints with a Flask app.
"""

from flask import Flask


def register_blueprints(app: Flask) -> None:
    """Register all route blueprints with the Flask app.

    This function is called by the application factory in
    app.py. It imports blueprints lazily to avoid circular
    imports.

    Parameters
    ----------
    app : Flask
        The Flask application instance.
    """
    from routes.main_routes import main_bp
    from routes.chat_routes import chat_bp
    from routes.feedback_routes import feedback_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(feedback_bp)
