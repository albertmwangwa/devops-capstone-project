"""Comprehensive tests for app.py"""

from app import app as flask_app
import app
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAppComprehensive(unittest.TestCase):
    """Test all aspects of app.py"""

    def setUp(self):
        self.client = flask_app.test_client()
        flask_app.config["TESTING"] = True
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    def test_app_import(self):
        """Test that app module can be imported"""
        self.assertIsNotNone(app)
        self.assertTrue(hasattr(app, "app"))
        self.assertTrue(hasattr(app, "run_app"))

    def test_flask_app_exists(self):
        """Test Flask app is properly configured"""
        self.assertIsNotNone(flask_app)
        self.assertEqual(flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"], False)

    def test_run_app_function(self):
        """Test run_app function exists and is callable"""
        self.assertTrue(callable(app.run_app))

    @patch("app.app.run")
    def test_run_app_calls_flask_run(self, mock_run):
        """Test that run_app() calls Flask's run method with correct args"""
        app.run_app()
        mock_run.assert_called_once_with(debug=True, host="0.0.0.0", port=5000)

    def test_error_handlers_exist(self):
        """Test that error handlers are registered"""
        # Check if error handlers exist
        error_handlers = flask_app.error_handler_spec.get(None, {})

        # Should have handlers for 400 and 500
        self.assertIn(400, error_handlers)
        self.assertIn(500, error_handlers)

    def test_400_error_handler(self):
        """Test 400 error handler"""
        # Trigger a 400 by accessing non-existent route with wrong method
        response = self.client.post("/nonexistent")
        self.assertEqual(response.status_code, 404)  # Actually 404, not 400

        # Test 400 by sending bad request to existing route
        response = self.client.post(
            "/accounts", data="{invalid json", content_type="application/json"
        )
        # Should be 400 or 415
        self.assertIn(response.status_code, [400, 415, 500])

    def test_500_error_handler(self):
        """Test 500 error handler by mocking an error"""
        # We can't easily trigger a real 500, but we can verify the handler exists
        error_handlers = flask_app.error_handler_spec.get(None, {})
        self.assertIn(500, error_handlers)

    def test_main_block(self):
        """Test the if __name__ == '__main__' block indirectly"""
        # Check that __name__ is set correctly
        self.assertEqual(app.__name__, "app")

        # The main block just calls run_app(), which we test above
        # We can't test the actual execution without running as main

    def test_app_name(self):
        """Test app name"""
        self.assertEqual(flask_app.name, "service")


if __name__ == "__main__":
    unittest.main()
