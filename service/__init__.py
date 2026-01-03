"""Service Package"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app(test_config=None):
    """Create Flask Application"""
    app = Flask(__name__)

    # Default configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounts.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Override with test config if provided
    if test_config:
        app.config.update(test_config)

    # Initialize db with app
    db.init_app(app)

    # Import models to register them with SQLAlchemy
    with app.app_context():
        from service.models import Account

        db.create_all()

    # Import and register routes
    from service.routes import init_app

    init_app(app)

    return app
