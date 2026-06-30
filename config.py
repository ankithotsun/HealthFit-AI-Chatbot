"""
HealthFit AI Chatbot — Application Configuration

Provides environment-specific configuration classes using
inheritance. The factory function in app.py selects the
appropriate class based on the FLASK_ENV variable.

Classes
-------
BaseConfig
    Shared defaults for all environments.
DevelopmentConfig
    Debug mode enabled, verbose logging.
TestingConfig
    In-memory SQLite, testing flag enabled.
ProductionConfig
    Debug disabled, stricter security settings.
"""

import os

# Base directory of the project (where this file lives)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Shared configuration defaults for all environments."""

    # Application metadata
    APP_NAME = "HealthFit AI Chatbot"
    APP_VERSION = "1.0.0"

    # Flask secret key — override via .env in production
    SECRET_KEY = os.environ.get("SECRET_KEY", "healthfit-dev-secret-key")

    # SQLite database path (inside Flask's instance folder)
    DATABASE_PATH = os.path.join(BASE_DIR, "instance", "healthfit.db")

    # NLP confidence threshold: queries scoring below this
    # value are routed to the fallback intent
    CONFIDENCE_THRESHOLD = float(
        os.environ.get("CONFIDENCE_THRESHOLD", "0.45")
    )

    # Maximum number of chat messages returned by the
    # history endpoint in a single request
    MAX_HISTORY_LENGTH = int(
        os.environ.get("MAX_HISTORY_LENGTH", "50")
    )

    # Paths to trained ML model artefacts
    MODEL_DIR = os.path.join(BASE_DIR, "models_ml")
    CLASSIFIER_PATH = os.path.join(MODEL_DIR, "trained_model.pkl")
    VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

    # Paths to data files
    DATA_DIR = os.path.join(BASE_DIR, "data")
    INTENTS_PATH = os.path.join(DATA_DIR, "intents.json")
    KNOWLEDGE_PATH = os.path.join(DATA_DIR, "fitness_knowledge.json")

    # Debug mode (overridden per environment)
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development environment — debug mode enabled."""

    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing environment — in-memory database, testing flag on."""

    TESTING = True
    DEBUG = True

    # Use in-memory SQLite for isolated, fast tests
    DATABASE_PATH = ":memory:"


class ProductionConfig(BaseConfig):
    """Production environment — debug disabled, strict settings."""

    DEBUG = False

    # In production the SECRET_KEY must be set via .env
    # The fallback value here will trigger a warning in app.py
    SECRET_KEY = os.environ.get("SECRET_KEY", None)


# -----------------------------------------------------------------
# Configuration registry — maps environment names to config classes
# -----------------------------------------------------------------
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
