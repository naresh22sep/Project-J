#!/usr/bin/env python3
"""
Test script to authenticate as admin user and check layout selection
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:5051"
LOGIN_URL = f"{BASE_URL}/admin/auth/login"
USERS_URL = f"{BASE_URL}/admin/users"

# Admin credentials
USERNAME = "admin_user"
PASSWORD = "AdminUser@2024"

def test_admin_layout():
    """Test admin user layout selection"""
    
    # Create a session
    session = requests.Session()
    
    print("🔑 Testing Admin Layout Selection...")
    print("="*50)
    
    # Step 1: Get login page to get CSRF token
    print("1. Getting login page...")
    login_page = session.get(LOGIN_URL)
    if login_page.status_code != 200:
        print(f"❌ Failed to get login page: {login_page.status_code}")
        return
    
    print(f"✅ Login page loaded: {login_page.status_code}")
    
    # Extract CSRF token from page
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = None
    
    # Look for CSRF token in meta tag
    csrf_meta = soup.find('meta', {'name': 'csrf-token'})
    if csrf_meta:
        csrf_token = csrf_meta.get('content')
    
    # Look for CSRF token in hidden input
    if not csrf_token:
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
    
    print(f"🔒 CSRF Token: {csrf_token[:20]}..." if csrf_token else "❌ No CSRF token found")
    
    # Step 2: Login as admin user
    print("\n2. Logging in as admin user...")
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    
    if csrf_token:
        login_data['csrf_token'] = csrf_token
    
    login_response = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
    print(f"📊 Login response status: {login_response.status_code}")
    print(f"📊 Login response headers: {dict(login_response.headers)}")
    
    # Check if login was successful
    if login_response.status_code in [302, 200]:
        print("✅ Login appears successful")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response text: {login_response.text[:500]}")
        return
    
    # Step 3: Access admin users page
    print("\n3. Accessing admin users page...")
    users_response = session.get(USERS_URL)
    print(f"📊 Users page status: {users_response.status_code}")
    print(f"📊 Content length: {len(users_response.text)} bytes")
    
    # Check which layout is being used
    if "admin_layout.html" in users_response.text:
        print("🚨 ISSUE: Page is using admin_layout.html (superadmin layout)")
    elif "admin_child.html" in users_response.text:
        print("✅ CORRECT: Page is using admin_child.html (admin layout)")
    else:
        print("❓ Unknown layout being used")
    
    # Look for our debugging output or specific layout indicators
    soup = BeautifulSoup(users_response.text, 'html.parser')
    
    # Check for images that indicate which layout
    admin_layout_img = soup.find('img', src='/static/admin_layout/images/default-avatar.png')
    admin_child_img = soup.find('img', src='/static/admin_child/images/default-avatar.png')
    
    if admin_layout_img:
        print("🚨 CONFIRMED: Using admin_layout.html (superadmin template)")
    elif admin_child_img:
        print("✅ CONFIRMED: Using admin_child.html (admin template)")
    
    # Look for menu differences
    dashboard_link = soup.find('a', href='/admin/dashboard')
    if dashboard_link:
        print(f"📋 Dashboard link found: {dashboard_link.get_text().strip()}")
    
    print("\n" + "="*50)
    print("🔍 Layout Analysis Complete")

if __name__ == "__main__":
    try:
        test_admin_layout()
    except ImportError:
        print("❌ BeautifulSoup4 not available. Installing...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
        print("✅ BeautifulSoup4 installed. Re-run the script.")
    except Exception as e:
        print(f"❌ Error: {e}")