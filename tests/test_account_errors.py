"""Additional tests for Account model error handling"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from service import create_app
from service.models import Account

class TestAccountErrorHandling(unittest.TestCase):
    """Test error handling in Account model"""
    
    def setUp(self):
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
        self.app = create_app(test_config)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from service import db
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            from service import db
            db.session.remove()
            db.drop_all()
    
    def test_deserialize_missing_name(self):
        """Test deserialize raises error when name is missing"""
        account = Account()
        data = {'email': 'test@example.com'}  # Missing name
        
        with self.assertRaises(ValueError) as context:
            account.deserialize(data)
        
        self.assertIn('Missing required field', str(context.exception))
        self.assertIn('name', str(context.exception))
    
    def test_deserialize_missing_email(self):
        """Test deserialize raises error when email is missing"""
        account = Account()
        data = {'name': 'Test User'}  # Missing email
        
        with self.assertRaises(ValueError) as context:
            account.deserialize(data)
        
        self.assertIn('Missing required field', str(context.exception))
        self.assertIn('email', str(context.exception))
    
    def test_create_account_missing_fields(self):
        """Test API returns error when required fields are missing"""
        # Missing name - should return 400, not raise ValueError
        response = self.client.post('/accounts', 
                                   json={'email': 'test@example.com'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertIn('Missing required field', response_data['error'])
        
        # Missing email
        response = self.client.post('/accounts',
                                   json={'name': 'Test User'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertIn('Missing required field', response_data['error'])
    
    def test_duplicate_email_error(self):
        """Test that duplicate emails return error"""
        # Create first account
        data1 = {'name': 'User1', 'email': 'same@example.com'}
        response1 = self.client.post('/accounts', json=data1)
        self.assertEqual(response1.status_code, 201)
        
        # Try to create second account with same email
        data2 = {'name': 'User2', 'email': 'same@example.com'}
        response2 = self.client.post('/accounts', json=data2)
        self.assertEqual(response2.status_code, 400)
        self.assertIn('already exists', response2.get_json()['error'].lower())
