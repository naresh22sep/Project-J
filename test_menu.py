#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.auth.auth_models import AuthUser

def test_admin_menu():
    """Test admin menu generation and access"""
    print("Testing admin menu with permission-based access...")
    print("=" * 50)
    
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            # Login as admin user
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            
            login_response = client.post('/admin/auth/login', data=login_data, follow_redirects=False)
            print(f"Login Status: {login_response.status_code}")
            if login_response.status_code == 302:
                print("✅ Login successful, redirected")
            else:
                print("❌ Login failed")
                return
            
            # Test Dashboard Access
            dashboard_response = client.get('/admin/dashboard', follow_redirects=False)
            print(f"Dashboard Status: {dashboard_response.status_code}")
            if dashboard_response.status_code == 200:
                print("✅ Dashboard accessible")
                # Check if content contains menu items
                content = dashboard_response.get_data(as_text=True)
                if 'Users' in content:
                    print("✅ Users menu item found")
                if 'Roles' in content:
                    print("✅ Roles menu item found")  
                if 'Subscriptions' in content:
                    print("✅ Subscriptions menu item found")
            else:
                print("❌ Dashboard not accessible")
                return
            
            # Test Users page (user.read permission)
            users_response = client.get('/admin/users', follow_redirects=False)
            print(f"Users page Status: {users_response.status_code}")
            if users_response.status_code == 200:
                print("✅ Users page accessible (user.read permission)")
            else:
                print("❌ Users page not accessible")
            
            # Test Roles page (role.read permission)
            roles_response = client.get('/admin/roles', follow_redirects=False)
            print(f"Roles page Status: {roles_response.status_code}")
            if roles_response.status_code == 200:
                print("✅ Roles page accessible (role.read permission)")
            else:
                print("❌ Roles page not accessible")
            
            # Test Analytics/Subscriptions page (subscription.read permission)
            analytics_response = client.get('/admin/analytics', follow_redirects=False)
            print(f"Analytics page Status: {analytics_response.status_code}")
            if analytics_response.status_code == 200:
                print("✅ Analytics page accessible (subscription.read permission)")
            else:
                print("❌ Analytics page not accessible")

if __name__ == '__main__':
    test_admin_menu()