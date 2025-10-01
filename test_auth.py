#!/usr/bin/env python3
"""Test login functionality for role-based authentication"""

import requests
import time

def test_login_flow():
    print("Testing authentication flow with role-based URLs...")
    
    session = requests.Session()
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    # Test SuperAdmin login
    print("\n1. Testing SuperAdmin login...")
    
    # Get login page
    login_response = session.get('http://127.0.0.1:5051/superadmin/auth/login')
    print(f"   GET /superadmin/auth/login -> Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        # Try to login with superadmin credentials
        login_data = {
            'username': 'superadmin',
            'password': 'SuperAdmin@2024'
        }
        
        # Post login data
        post_response = session.post('http://127.0.0.1:5051/superadmin/auth/login', 
                                   data=login_data, allow_redirects=False)
        print(f"   POST login -> Status: {post_response.status_code}")
        
        if post_response.status_code == 302:
            location = post_response.headers.get('Location', '')
            print(f"   Redirects to: {location}")
            
            # Follow the redirect
            if location:
                final_response = session.get(f'http://127.0.0.1:5051{location}', allow_redirects=False)
                print(f"   Dashboard access -> Status: {final_response.status_code}")
        else:
            print(f"   Login response body: {post_response.text[:200]}...")
    
    # Test different role URLs
    print("\n2. Testing other role login pages...")
    test_urls = [
        '/admin/auth/login',
        '/jobseeker/login', 
        '/consultancy/login'
    ]
    
    for url in test_urls:
        response = session.get(f'http://127.0.0.1:5051{url}')
        role = url.split('/')[1]
        print(f"   {role.capitalize():12} login -> Status: {response.status_code}")
        
        if response.status_code == 200:
            # Check if the page contains role-specific content
            if role.lower() in response.text.lower():
                print(f"   {'':12}           -> Role-specific content detected ✓")
            else:
                print(f"   {'':12}           -> Generic login page")
    
    print("\nAuthentication flow testing complete!")

if __name__ == "__main__":
    test_login_flow()