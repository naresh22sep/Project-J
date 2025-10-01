#!/usr/bin/env python3
"""Test script for role-based authentication URLs"""

import requests
import time

def test_urls():
    print("Testing role-based authentication URLs...")
    session = requests.Session()
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    # Test endpoints
    endpoints = [
        ('Root URL', 'http://127.0.0.1:5051/'),
        ('SuperAdmin login', 'http://127.0.0.1:5051/superadmin/auth/login'),
        ('Admin login', 'http://127.0.0.1:5051/admin/auth/login'),
        ('Jobseeker login', 'http://127.0.0.1:5051/jobseeker/login'),
        ('Consultancy login', 'http://127.0.0.1:5051/consultancy/login'),
        ('Legacy login', 'http://127.0.0.1:5051/auth/login')
    ]
    
    for name, url in endpoints:
        try:
            response = session.get(url, allow_redirects=False, timeout=5)
            print(f"{name:18} -> Status: {response.status_code}")
            
            if response.status_code == 302:
                location = response.headers.get('Location', 'No location header')
                print(f"                   -> Redirects to: {location}")
            elif response.status_code == 200:
                # Check if it's the login page
                if 'login' in response.text.lower() and 'form' in response.text.lower():
                    print(f"                   -> Login page loaded successfully")
                else:
                    print(f"                   -> Page loaded (not login form)")
                    
        except requests.exceptions.RequestException as e:
            print(f"{name:18} -> Error: {e}")
    
    print("\nTesting complete!")

if __name__ == "__main__":
    test_urls()