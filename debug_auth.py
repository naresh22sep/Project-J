"""
Debug script to test authentication flow
"""

from app import create_app
from flask import g, session
import requests

def test_auth_debug():
    """Test the authentication flow"""
    app = create_app()
    
    with app.test_client() as client:
        # Test 1: Access /admin/jobs without authentication
        print("=== Test 1: Access /admin/jobs without authentication ===")
        response = client.get('/admin/jobs', follow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Location Header: {response.headers.get('Location', 'None')}")
        print(f"Content Length: {len(response.data)}")
        print(f"First 200 chars: {response.data[:200]}")
        print()
        
        # Test 2: Check if middleware is working
        print("=== Test 2: Check middleware setup ===")
        with app.test_request_context():
            print(f"App blueprints: {[bp.name for bp in app.blueprints.values()]}")
            print(f"URL map rules for /admin/jobs:")
            for rule in app.url_map.iter_rules():
                if rule.rule == '/admin/jobs':
                    print(f"  {rule} -> {rule.endpoint}")
        print()
        
        # Test 3: Check session data
        print("=== Test 3: Check session ===")
        with client.session_transaction() as sess:
            print(f"Session keys: {list(sess.keys())}")
            print(f"User ID in session: {sess.get('user_id', 'None')}")
        print()

if __name__ == '__main__':
    test_auth_debug()