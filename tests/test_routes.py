"""Test cases for Account Routes"""
import unittest
import json
import sys
import os

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import create_app function to create the Flask application
from service import create_app
from service.models import Account

class TestAccountRoutes(unittest.TestCase):
    """Test Cases for Account Routes"""
    
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        # Create the Flask app for testing with in-memory database
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
        cls.app = create_app(test_config)
    
    def setUp(self):
        """Run before each test"""
        # Create a test client
        self.client = self.app.test_client()
        
        # Create all tables
        with self.app.app_context():
            from service import db
            db.create_all()
    
    def tearDown(self):
        """Run after each test"""
        # Clean up database
        with self.app.app_context():
            from service import db
            db.session.remove()
            db.drop_all()
    
    # Test 1: Create Account
    def test_create_account(self):
        """Test creating a new account"""
        account_data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        response = self.client.post(
            '/accounts',
            data=json.dumps(account_data),
            content_type='application/json'
        )
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data[:100]}...")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'John Doe')
        self.assertIn('id', data)
        return data['id']
    
    # Test 2: Read Account
    def test_read_an_account(self):
        """Test reading an existing account"""
        # First create an account
        account_data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com'
        }
        create_response = self.client.post(
            '/accounts',
            data=json.dumps(account_data),
            content_type='application/json'
        )
        self.assertEqual(create_response.status_code, 201)
        created_account = json.loads(create_response.data)
        account_id = created_account['id']
        
        # Now read the account
        read_response = self.client.get(f'/accounts/{account_id}')
        self.assertEqual(read_response.status_code, 200)
        
        read_account = json.loads(read_response.data)
        self.assertEqual(read_account['id'], account_id)
        self.assertEqual(read_account['name'], 'Jane Smith')
        self.assertEqual(read_account['email'], 'jane@example.com')
    
    # Test 3: Account Not Found
    def test_account_not_found(self):
        """Test reading a non-existent account returns 404"""
        response = self.client.get('/accounts/0')
        self.assertEqual(response.status_code, 404)
    
    # Test 4: List All Accounts (Empty)
    def test_list_all_accounts_empty(self):
        """Test listing accounts when none exist"""
        response = self.client.get('/accounts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
    
    # Test 5: List All Accounts (With Data)
    def test_list_all_accounts_with_data(self):
        """Test listing all accounts"""
        # Create two accounts
        account1_data = {'name': 'Alice', 'email': 'alice@example.com'}
        account2_data = {'name': 'Bob', 'email': 'bob@example.com'}
        
        self.client.post('/accounts', data=json.dumps(account1_data), 
                        content_type='application/json')
        self.client.post('/accounts', data=json.dumps(account2_data), 
                        content_type='application/json')
        
        # List all accounts
        response = self.client.get('/accounts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 2)
        emails = [account['email'] for account in data]
        self.assertIn('alice@example.com', emails)
        self.assertIn('bob@example.com', emails)
    
    # Test 6: Update Account
    def test_update_account_success(self):
        """Test updating an existing account"""
        # Create account
        create_data = {'name': 'Original', 'email': 'original@example.com'}
        create_response = self.client.post('/accounts', 
                                          data=json.dumps(create_data),
                                          content_type='application/json')
        account_id = json.loads(create_response.data)['id']
        
        # Update account
        update_data = {'name': 'Updated', 'email': 'updated@example.com'}
        update_response = self.client.put(f'/accounts/{account_id}',
                                         data=json.dumps(update_data),
                                         content_type='application/json')
        self.assertEqual(update_response.status_code, 200)
        
        updated_account = json.loads(update_response.data)
        self.assertEqual(updated_account['name'], 'Updated')
        self.assertEqual(updated_account['email'], 'updated@example.com')
    
    # Test 7: Update Account Not Found
    def test_update_account_not_found(self):
        """Test updating non-existent account returns 404"""
        update_data = {'name': 'Test', 'email': 'test@example.com'}
        response = self.client.put('/accounts/999',
                                  data=json.dumps(update_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    # Test 8: Delete Account
    def test_delete_account_success(self):
        """Test deleting an existing account"""
        # Create account
        create_data = {'name': 'To Delete', 'email': 'delete@example.com'}
        create_response = self.client.post('/accounts',
                                          data=json.dumps(create_data),
                                          content_type='application/json')
        account_id = json.loads(create_response.data)['id']
        
        # Delete account
        delete_response = self.client.delete(f'/accounts/{account_id}')
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(delete_response.data, b'')
        
        # Verify account is deleted
        get_response = self.client.get(f'/accounts/{account_id}')
        self.assertEqual(get_response.status_code, 404)
    
    # Test 9: Delete Account Not Found
    def test_delete_account_not_found(self):
        """Test deleting non-existent account returns 204"""
        response = self.client.delete('/accounts/999')
        self.assertEqual(response.status_code, 204)
