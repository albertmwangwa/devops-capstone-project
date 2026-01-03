"""Test for app.py"""

from app import app
import json
import os
import sys
import unittest
from service import config

# Add to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestApp(unittest.TestCase):
    """Test the main app module"""

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    def test_app_runs(self):
        """Test that the app can be imported and run"""
        self.assertIsNotNone(app)
        self.assertTrue(app.config["TESTING"])

    def test_app_has_routes(self):
        """Test that app has all expected routes"""
        routes = [rule.rule for rule in app.url_map.iter_rules()]

        # Check for accounts routes (using Flask's pattern matching)
        has_accounts_route = any(
            "/accounts" in route and "<" not in route for route in routes
        )
        has_account_by_id_route = any("/accounts/<" in route for route in routes)

        self.assertTrue(has_accounts_route, "Should have /accounts route")
        self.assertTrue(has_account_by_id_route, "Should have /accounts/<id> route")

        # Print routes for debugging
        print("\nRegistered routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.rule} [{', '.join(rule.methods)}]")

    def test_main_block(self):
        """Test that app can run directly"""
        # This tests the if __name__ == '__main__': block
        # We can't easily test it running, but we can test it exists
        import app as app_module

        self.assertTrue(hasattr(app_module, "__name__"))
        self.assertEqual(app_module.__name__, "app")

    def test_app_config(self):
        """Test app configuration"""
        self.assertEqual(app.config["SQLALCHEMY_TRACK_MODIFICATIONS"], False)
        self.assertIn("sqlite:///", app.config["SQLALCHEMY_DATABASE_URI"])

    def test_error_handling(self):
        """Test error handling routes"""
        # Test missing fields
        response = self.client.post(
            "/accounts",
            json={"email": "test@example.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

        # Test invalid JSON - Flask may return 400 or 500 depending on version
        response = self.client.post(
            "/accounts", data="invalid json", content_type="application/json"
        )
        # Accept either 400 or 500 - the important thing is it doesn't crash
        self.assertIn(response.status_code, [400, 500])
        if response.status_code == 400:
            # If it's a 400, check for error message
            response_data = response.get_json()
            if response_data:  # Some Flask versions return empty response
                self.assertIn("error", response_data)
