#!/usr/bin/env python3
"""
Test script to validate authentication logging system
"""

import requests
import json
import time

def test_superadmin_login_get():
    """Test GET request to SuperAdmin login page"""
    print("=== Testing SuperAdmin Login GET Request ===")
    
    try:
        url = "http://localhost:5051/superadmin/auth/login"
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Length: {len(response.text)}")
        
        if response.status_code == 200:
            print("✅ GET request successful")
        else:
            print(f"❌ GET request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ GET request error: {str(e)}")

def test_superadmin_login_post():
    """Test POST request to SuperAdmin login"""
    print("\n=== Testing SuperAdmin Login POST Request ===")
    
    try:
        url = "http://localhost:5051/superadmin/auth/login"
        
        # Test with valid credentials
        print("\n--- Test 1: Valid Credentials ---")
        data = {
            'username': 'superadmin',
            'password': 'SuperAdmin@2024'
        }
        
        response = requests.post(url, data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Location Header: {response.headers.get('Location', 'None')}")
        
        if response.status_code == 302:
            print("✅ Valid credentials - redirect received")
        else:
            print(f"❌ Valid credentials failed with status {response.status_code}")
        
        # Test with invalid credentials
        print("\n--- Test 2: Invalid Credentials ---")
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        
        response = requests.post(url, data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Invalid credentials - form returned (expected)")
        else:
            print(f"❌ Invalid credentials unexpected status {response.status_code}")
        
        # Test with missing data
        print("\n--- Test 3: Missing Data ---")
        data = {
            'username': '',
            'password': ''
        }
        
        response = requests.post(url, data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Missing data - form returned (expected)")
        else:
            print(f"❌ Missing data unexpected status {response.status_code}")
            
    except Exception as e:
        print(f"❌ POST request error: {str(e)}")

def check_log_file():
    """Check if the authentication log file is being created and written to"""
    print("\n=== Checking Authentication Log File ===")
    
    try:
        log_file_path = "c:/Users/Pulipati/Desktop/FREE/ProjectJ/app/logs/auth_debug.log"
        
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"Log file exists: ✅")
        print(f"Log file size: {len(content)} characters")
        
        # Show last few lines
        lines = content.strip().split('\n')
        if len(lines) > 0:
            print(f"Total log lines: {len(lines)}")
            print("\n--- Last 10 log entries ---")
            for line in lines[-10:]:
                print(line)
        else:
            print("⚠️  Log file is empty")
            
    except FileNotFoundError:
        print("❌ Log file not found")
    except Exception as e:
        print(f"❌ Error reading log file: {str(e)}")

if __name__ == "__main__":
    print("🔍 Authentication Logging Test Script")
    print("=" * 50)
    
    # Give the server a moment to fully start
    time.sleep(2)
    
    # Run tests
    test_superadmin_login_get()
    test_superadmin_login_post()
    
    # Check logs
    time.sleep(1)  # Give logs a moment to write
    check_log_file()
    
    print("\n" + "=" * 50)
    print("🎯 Test completed! Check the log file for detailed authentication tracking.")