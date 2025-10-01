#!/usr/bin/env python3
"""Test script to verify superadmin login functionality"""

import requests
import sys

def test_superadmin_login():
    """Test SuperAdmin login flow"""
    base_url = "http://localhost:5051"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("🧪 Testing SuperAdmin Login Flow...")
    print("=" * 50)
    
    # Step 1: Get the login page
    print("Step 1: Accessing login page...")
    try:
        login_response = session.get(f"{base_url}/superadmin/auth/login")
        print(f"✅ Login page status: {login_response.status_code}")
        if login_response.status_code != 200:
            print(f"❌ Failed to access login page: {login_response.text}")
            return False
    except Exception as e:
        print(f"❌ Error accessing login page: {str(e)}")
        return False
    
    # Step 2: Submit login credentials
    print("\nStep 2: Submitting login credentials...")
    login_data = {
        'username': 'superadmin',
        'password': 'SuperAdmin@2024'
    }
    
    try:
        # Submit login form
        auth_response = session.post(f"{base_url}/superadmin/auth/login", data=login_data, allow_redirects=False)
        print(f"✅ Login submission status: {auth_response.status_code}")
        
        if auth_response.status_code == 302:
            redirect_location = auth_response.headers.get('Location', '')
            print(f"✅ Redirect to: {redirect_location}")
            
            if 'dashboard' in redirect_location:
                print("✅ Successfully redirected to dashboard!")
            else:
                print(f"⚠️ Unexpected redirect: {redirect_location}")
                return False
        else:
            print(f"❌ Unexpected login response: {auth_response.status_code}")
            print(f"Response text: {auth_response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Error during login: {str(e)}")
        return False
    
    # Step 3: Access dashboard
    print("\nStep 3: Accessing dashboard...")
    try:
        dashboard_response = session.get(f"{base_url}/superadmin/dashboard", allow_redirects=False)
        print(f"✅ Dashboard access status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✅ Successfully accessed dashboard!")
            if "SuperAdmin Dashboard" in dashboard_response.text:
                print("✅ Dashboard content verified!")
                return True
            else:
                print("⚠️ Dashboard content not as expected")
                print(f"Content preview: {dashboard_response.text[:200]}")
                
        elif dashboard_response.status_code == 302:
            redirect_location = dashboard_response.headers.get('Location', '')
            print(f"❌ Dashboard redirected to: {redirect_location}")
            print("This indicates authentication failed")
            return False
        else:
            print(f"❌ Unexpected dashboard response: {dashboard_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing dashboard: {str(e)}")
        return False
    
    return False

if __name__ == "__main__":
    success = test_superadmin_login()
    if success:
        print("\n🎉 SuperAdmin login test PASSED!")
        sys.exit(0)
    else:
        print("\n❌ SuperAdmin login test FAILED!")
        sys.exit(1)