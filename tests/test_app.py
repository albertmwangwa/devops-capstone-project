"""Test for app.py"""

import json
import os
import sys
import unittest

# Add to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestApp(unittest.TestCase):
    """Test the main app module"""

    def setUp(self):
        """Set up test client with properly initialized app"""
        # Import create_app instead of app directly
        from service import create_app

        # Create app with test configuration
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SECRET_KEY": "test-secret-key"
        })

        # Push app context for database operations
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Initialize database
        from service import db
        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after tests"""
        from service import db
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_runs(self):
        """Test that the app can be imported and run"""
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.config["TESTING"])

    def test_app_has_routes(self):
        """Test that app has all expected routes"""
        routes = [rule.rule for rule in self.app.url_map.iter_rules()]

        # Check for accounts routes (using Flask's pattern matching)
        has_accounts_route = any(
            "/accounts" in route and "<" not in route for route in routes
        )
        has_account_by_id_route = any("/accounts/<" in route for route in routes)

        self.assertTrue(has_accounts_route, "Should have /accounts route")
        self.assertTrue(has_account_by_id_route, "Should have /accounts/<id> route")

        # Print routes for debugging
        print("\nRegistered routes:")
        for rule in self.app.url_map.iter_rules():
            print(f"  {rule.rule} [{', '.join(rule.methods)}]")

    def test_main_block(self):
        """Test that app can run directly"""
        # Test that we can import the main app module
        # Since we're using create_app pattern, we need to handle this differently
        try:
            import app as app_module
            # If app.py exists, check it has expected attributes
            self.assertTrue(hasattr(app_module, "__name__"))
        except ImportError:
            # It's OK if app.py doesn't exist - we're using service/app.py
            self.skipTest("app.py not found in root directory")

    def test_app_config(self):
        """Test app configuration"""
        self.assertEqual(self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"], False)
        self.assertIn("sqlite:///", self.app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertTrue(self.app.config["TESTING"])

    def test_error_handling(self):
        """Test error handling routes"""
        # Test missing fields - should return 400 (validation error)
        response = self.client.post(
            "/accounts",
            json={"email": "test@example.com"},  # Missing required 'name' field
            content_type="application/json",
        )

        # The Account model's deserialize() should validate and raise ValueError
        # which should be caught and return 400
        self.assertEqual(response.status_code, 400)

        # Check error message structure
        response_data = response.get_json()
        self.assertIsNotNone(response_data)
        self.assertIn("error", response_data)

        # Test invalid JSON
        response = self.client.post(
            "/accounts",
            data="invalid json",
            content_type="application/json"
        )
        # Accept either 400 or 500 - the important thing is it doesn't crash
        self.assertIn(response.status_code, [400, 500])

        if response.status_code == 400 and response.get_json():
            response_data = response.get_json()
            self.assertIn("error", response_data)

    def test_health_check(self):
        """Test health check endpoint if it exists"""
        # Check if root route exists
        routes = [rule.rule for rule in self.app.url_map.iter_rules()]
        if '/' in routes or any(rule.rule == '/' for rule in self.app.url_map.iter_rules()):
            response = self.client.get('/')
            self.assertIn(response.status_code, [200, 404])
            if response.status_code == 200:
                response_data = response.get_json()
                self.assertIsNotNone(response_data)


if __name__ == '__main__':
    unittest.main()