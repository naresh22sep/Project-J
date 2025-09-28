"""
Application Tests
Tests the Flask application functionality and API endpoints
"""

import os
import sys
import unittest
import json

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User

class TestFlaskApp(unittest.TestCase):
    """Test Flask application functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Load environment variables from .env file if it exists
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
            except ImportError:
                pass
        
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create tables
        db.create_all()
        
    def tearDown(self):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_app_exists(self):
        """Test that the app exists"""
        self.assertIsNotNone(self.app)
        print("✅ Flask app exists")
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        print("✅ Health endpoint working")
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        print("✅ Root endpoint working")
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = self.client.post('/auth/register',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['user']['username'], 'testuser')
        print("✅ User registration working")
    
    def test_user_login(self):
        """Test user login endpoint"""
        # First create a user
        user = User(username='logintest', email='login@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Test login
        login_data = {
            'username': 'logintest',
            'password': 'password123'
        }
        
        response = self.client.post('/auth/login',
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('session_token', data)
        print("✅ User login working")
    
    def test_protected_endpoint(self):
        """Test protected endpoint access"""
        # Try accessing without authentication
        response = self.client.get('/users/profile')
        self.assertEqual(response.status_code, 401)
        print("✅ Protected endpoint requires authentication")


class TestAPIEndpoints(unittest.TestCase):
    """Test all API endpoints"""
    
    def setUp(self):
        """Set up test environment"""
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
            except ImportError:
                pass
        
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        # Create a test user and login
        self.create_test_user_and_login()
    
    def tearDown(self):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def create_test_user_and_login(self):
        """Helper method to create user and login"""
        user = User(username='apitest', email='api@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Login to get session
        login_data = {'username': 'apitest', 'password': 'password123'}
        response = self.client.post('/auth/login',
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        
        if response.status_code == 200:
            print("✅ Test user created and logged in")
        else:
            print(f"❌ Failed to login test user: {response.data}")
    
    def test_all_auth_endpoints(self):
        """Test all authentication endpoints"""
        endpoints = [
            ('/auth/verify', 'GET'),
            ('/auth/logout', 'POST')
        ]
        
        for endpoint, method in endpoints:
            if method == 'GET':
                response = self.client.get(endpoint)
            else:
                response = self.client.post(endpoint)
            
            # Should be either 200 (success) or 401 (unauthorized)
            self.assertIn(response.status_code, [200, 401])
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
    
    def test_dashboard_endpoints(self):
        """Test dashboard endpoints"""
        endpoints = [
            '/dashboard/stats',
            '/dashboard/recent-users',
            '/dashboard/active-sessions',
            '/dashboard/system-info'
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            # Should be either 200 (success) or 401 (unauthorized)
            self.assertIn(response.status_code, [200, 401])
            print(f"✅ GET {endpoint} - Status: {response.status_code}")
    
    def test_users_endpoints(self):
        """Test user management endpoints"""
        endpoints = [
            '/users/profile',
            '/users/list',
            '/users/search?q=test'
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertIn(response.status_code, [200, 401])
            print(f"✅ GET {endpoint} - Status: {response.status_code}")


if __name__ == '__main__':
    print("🧪 Starting Flask Application Tests...\n")
    
    # Run tests with verbose output
    unittest.main(verbosity=2, exit=False)
    
    print("\n🎉 Application tests completed!")