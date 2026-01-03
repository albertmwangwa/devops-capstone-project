"""Flask application for the account service"""

from flask import Flask, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def create_app():
    """Create Flask application"""
    app = Flask(__name__)

    # Default configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask-Talisman for security headers
    Talisman(
        app,
        content_security_policy={
            'default-src': ['\'self\''],
            'style-src': ['\'self\'', '\'unsafe-inline\''],
            'script-src': ['\'self\'', '\'unsafe-inline\'']
        },
        content_security_policy_nonce_in=['script-src'],
        force_https=False,  # Set to True in production
        force_https_permanent=False,
        session_cookie_secure=True,
        session_cookie_http_only=True,
        session_cookie_samesite='Lax'
    )

    # Initialize Flask-CORS
    CORS(app,
         resources={r"/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
         expose_headers=["Content-Type", "Authorization"],
         max_age=600)

    # Initialize database - use relative import
    try:
        from .models import db
        db.init_app(app)

        # Create tables
        with app.app_context():
            db.create_all()
    except ImportError:
        print("Warning: Could not initialize database models")

    # Register blueprints - use relative import
    try:
        from .routes import accounts_bp
        app.register_blueprint(accounts_bp)
    except ImportError as e:
        print(f"Warning: Could not register routes: {e}")

    # Add health check endpoint
    @app.route('/')
    def index():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "Account Service",
            "version": "1.0.0",
            "security": "enabled"
        }), 200

    # Add a CORS test endpoint
    @app.route('/test-cors')
    def test_cors():
        """Test CORS endpoint"""
        return jsonify({
            "message": "CORS test successful",
            "cors_enabled": True
        }), 200

    return app


# Only create app if this file is run directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    app = create_app()