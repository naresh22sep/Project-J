#!/usr/bin/env python3
"""
Test Dashboard Access
"""

from app import create_app

def test_dashboard():
    """Test if dashboard loads correctly"""
    app = create_app()
    
    with app.test_client() as client:
        print("Testing admin dashboard after login...")
        print("=" * 50)
        
        # First login as admin
        login_response = client.post('/admin/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=False)
        
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 302:
            print("✅ Login successful, redirected")
            
            # Now try to access dashboard
            dashboard_response = client.get('/admin/dashboard', follow_redirects=False)
            print(f"Dashboard Status: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                print("✅ Dashboard loads successfully!")
                content = dashboard_response.get_data(as_text=True)
                print(f"Content length: {len(content)} characters")
                if "TypeError" in content:
                    print("❌ TypeError still present in content")
                else:
                    print("✅ No TypeError found!")
            else:
                print(f"❌ Dashboard failed with status {dashboard_response.status_code}")
                
        else:
            print("❌ Login failed")

if __name__ == '__main__':
    test_dashboard()