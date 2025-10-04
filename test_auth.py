#!/usr/bin/env python3
"""
Test Authentication for Admin Routes
"""

from app import create_app

def test_admin_authentication():
    """Test if admin routes are properly protected"""
    app = create_app()
    
    with app.test_client() as client:
        print("Testing admin/jobs authentication...")
        print("=" * 50)
        
        # Test without authentication
        response = client.get('/admin/jobs', follow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Location Header: {response.headers.get('Location', 'None')}")
        print(f"Is Redirect: {response.status_code in [301, 302, 303, 307, 308]}")
        
        if response.status_code == 302:
            print("✅ AUTHENTICATION WORKING - Route redirects when not logged in")
        elif response.status_code == 200:
            print("❌ AUTHENTICATION FAILED - Route accessible without login")
            print("Response content preview:")
            content = response.get_data(as_text=True)
            print(content[:200] + "..." if len(content) > 200 else content)
        else:
            print(f"⚠️  UNEXPECTED STATUS - Got status code {response.status_code}")
        
        print("\n" + "=" * 50)
        
        # Test other admin routes
        test_routes = ['/admin/users', '/admin/dashboard', '/admin/roles']
        
        for route in test_routes:
            response = client.get(route, follow_redirects=False)
            status = "✅ PROTECTED" if response.status_code == 302 else "❌ ACCESSIBLE"
            print(f"{route}: {response.status_code} - {status}")

if __name__ == '__main__':
    test_admin_authentication()