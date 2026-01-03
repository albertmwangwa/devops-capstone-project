"""Account Routes"""

from flask import abort, Blueprint, jsonify, request
from service import db
from service.models import Account

# Create a Blueprint
accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route("/accounts", methods=["POST"])
def create_account():
    """Create a new account"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Check if account with email already exists
        existing = Account.query.filter_by(email=data.get("email")).first()
        if existing:
            return jsonify({"error": "Account with this email already exists"}), 400

        account = Account()
        account.deserialize(data)
        db.session.add(account)
        db.session.commit()

        return jsonify(account.serialize()), 201

    except ValueError as e:
        # Handle validation errors from deserialize()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle any other errors
        from flask import current_app
        current_app.logger.error(f"Error creating account: {e}")
        return jsonify({"error": "Internal server error"}), 500

@accounts_bp.route("/accounts", methods=["GET"])
def list_accounts():
    """List all accounts"""
    accounts = Account.all()
    return jsonify([account.serialize() for account in accounts]), 200

@accounts_bp.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read an account by id"""
    account = Account.find(account_id)
    if not account:
        abort(404, description=f"Account with id {account_id} not found")
    return jsonify(account.serialize()), 200

@accounts_bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an existing account"""
    account = Account.find(account_id)
    if not account:
        abort(404, description=f"Account with id {account_id} not found")

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        account.deserialize(data)
        account.update()

        return jsonify(account.serialize()), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Error updating account: {e}")
        return jsonify({"error": "Internal server error"}), 500

@accounts_bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an account"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204


# Keep init_app for backward compatibility
def init_app(app):
    """Initialize routes with the app"""
    app.register_blueprint(accounts_bp)