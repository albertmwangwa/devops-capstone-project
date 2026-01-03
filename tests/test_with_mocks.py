"""Test with mocks to achieve 100% coverage"""

from service import create_app
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestWithMocks(unittest.TestCase):
    """Use mocks to test error paths"""

    def setUp(self):
        test_config = {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
        self.app = create_app(test_config)
        self.client = self.app.test_client()

    @patch("service.routes.db.session.commit")
    @patch("service.routes.Account")
    def test_create_account_database_error(self, mock_account, mock_commit):
        """Test database error during account creation"""
        # Mock the account creation to raise an error on commit
        mock_commit.side_effect = Exception("Database error")

        # Mock account instance
        mock_instance = MagicMock()
        mock_instance.serialize.return_value = {
            "id": 1,
            "name": "Test",
            "email": "test@example.com",
        }
        mock_account.return_value = mock_instance

        # Mock query to return None (no duplicate)
        mock_account.query.filter_by.return_value.first.return_value = None

        response = self.client.post(
            "/accounts",
            json={"name": "Test", "email": "test@example.com"},
            content_type="application/json",
        )

        # Should get 500 error
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.get_json())

    @patch("service.routes.Account.find")
    @patch("service.routes.db.session.commit")
    def test_update_account_database_error(self, mock_commit, mock_find):
        """Test database error during account update"""
        # Mock finding an account
        mock_account = MagicMock()
        mock_account.deserialize = MagicMock()
        mock_find.return_value = mock_account

        # Mock commit to raise error
        mock_commit.side_effect = Exception("Database error")

        response = self.client.put(
            "/accounts/1",
            json={"name": "Updated", "email": "updated@example.com"},
            content_type="application/json",
        )

        # Should get 500 error
        self.assertEqual(response.status_code, 500)

    def test_route_import_statement(self):
        """Test that routes module imports correctly"""
        import service.routes

        self.assertIsNotNone(service.routes)
        self.assertTrue(hasattr(service.routes, "init_app"))
        self.assertTrue(callable(service.routes.init_app))


if __name__ == "__main__":
    unittest.main()
