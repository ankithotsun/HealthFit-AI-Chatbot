"""
HealthFit AI Chatbot — Application Entry Point

Uses the Flask Application Factory pattern to create and
configure the application instance. This enables:
- Different configurations for dev/test/prod environments.
- Easy unit testing with isolated app instances.
- Clean blueprint registration without circular imports.

Usage
-----
Development server:
    $ flask run
    or
    $ python app.py

Testing:
    app = create_app('testing')  # in-memory SQLite

Production:
    $ export FLASK_ENV=production
    $ flask run

Functions
---------
create_app(config_name)
    Factory function that builds a configured Flask app.
"""

import os
import logging

from flask import Flask

from config import config_by_name
from routes import register_blueprints
from utils.db_manager import init_db


def create_app(config_name: str = None) -> Flask:
    """Create and configure the Flask application.

    Parameters
    ----------
    config_name : str, optional
        The configuration environment to use. Must be one
        of 'development', 'testing', or 'production'.
        If not provided, reads from the FLASK_ENV environment
        variable, defaulting to 'development'.

    Returns
    -------
    Flask
        A fully configured Flask application instance with
        blueprints registered and database initialized.
    """
    # Determine configuration environment
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # Create the Flask application instance
    app = Flask(
        __name__,
        instance_relative_config=True
    )

    # --------------------------------------------------------
    # Load Configuration
    # --------------------------------------------------------
    config_class = config_by_name.get(config_name)
    if config_class is None:
        raise ValueError(
            f"Unknown configuration: '{config_name}'. "
            f"Must be one of: {list(config_by_name.keys())}"
        )
    app.config.from_object(config_class)

    # Warn if production secret key is not set
    if config_name == "production" and not app.config.get("SECRET_KEY"):
        app.logger.warning(
            "SECRET_KEY is not set! Set it via the .env file "
            "before deploying to production."
        )

    # --------------------------------------------------------
    # Configure Logging
    # --------------------------------------------------------
    log_level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] %(levelname)s in %(module)s: "
               "%(message)s"
    )

    # --------------------------------------------------------
    # Register Blueprints (Routes)
    # --------------------------------------------------------
    register_blueprints(app)

    # --------------------------------------------------------
    # Initialize Database
    # --------------------------------------------------------
    db_path = app.config["DATABASE_PATH"]
    init_db(db_path)
    app.logger.info("Database initialized at: %s", db_path)

    # --------------------------------------------------------
    # Log Startup Information
    # --------------------------------------------------------
    app.logger.info(
        "HealthFit AI Chatbot v%s started in '%s' mode.",
        app.config.get("APP_VERSION", "1.0.0"),
        config_name
    )

    return app


# =============================================================
# Direct Execution
# =============================================================

if __name__ == "__main__":
    application = create_app()
    application.run(
        host="127.0.0.1",
        port=5000,
        debug=application.debug
    )
