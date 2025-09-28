"""
Manual Route Testing Script
Test routes manually using curl commands or browser
"""

import requests
import json
from datetime import datetime

class RouteTestor:
    def __init__(self, base_url="http://localhost:5051"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_route(self, endpoint, method="GET", data=None, headers=None):
        """Test a single route"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, data=data, headers=headers)
            elif method.upper() == "PUT":
                response = self.session.put(url, data=data, headers=headers)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            
            status = "✅" if response.status_code < 400 else "❌"
            print(f"{status} {method} {endpoint} - Status: {response.status_code}")
            
            return response
            
        except requests.exceptions.ConnectionError:
            print(f"❌ {method} {endpoint} - Connection Error (Server not running?)")
            return None
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {str(e)}")
            return None

def test_all_routes():
    """Test all routes systematically"""
    tester = RouteTestor()
    
    print("🧪 Manual Route Testing Started")
    print("Make sure your Flask app is running on http://localhost:5051")
    print("=" * 60)
    
    # Test main routes
    print("\n📍 Testing Main Routes:")
    main_routes = [
        "/",
        "/health", 
        "/about",
        "/contact",
        "/pricing"
    ]
    
    for route in main_routes:
        tester.test_route(route)
    
    # Test JobSeeker routes
    print("\n👤 Testing JobSeeker Routes:")
    jobseeker_routes = [
        "/jobseeker/",
        "/jobseeker/jobs",
        "/jobseeker/jobs?search=developer",
        "/jobseeker/jobs?location=remote", 
        "/jobseeker/dashboard",  # Should require auth
        "/jobseeker/profile",    # Should require auth
        "/jobseeker/applications"  # Should require auth
    ]
    
    for route in jobseeker_routes:
        tester.test_route(route)
    
    # Test Consultancy routes
    print("\n🏢 Testing Consultancy Routes:")
    consultancy_routes = [
        "/consultancy/",
        "/consultancy/dashboard",  # Should require auth
        "/consultancy/jobs",      # Should require auth
        "/consultancy/applications",  # Should require auth
        "/consultancy/profile",   # Should require auth
        "/consultancy/analytics"  # Should require auth
    ]
    
    for route in consultancy_routes:
        tester.test_route(route)
    
    # Test Admin routes  
    print("\n👮 Testing Admin Routes:")
    admin_routes = [
        "/admin/",           # Should require admin auth
        "/admin/users",      # Should require admin auth
        "/admin/jobs",       # Should require admin auth
        "/admin/applications",  # Should require admin auth
        "/admin/analytics",  # Should require admin auth
        "/admin/reports"     # Should require admin auth
    ]
    
    for route in admin_routes:
        tester.test_route(route)
    
    # Test SuperAdmin routes
    print("\n👑 Testing SuperAdmin Routes:")
    superadmin_routes = [
        "/superadmin/",              # Should require superadmin auth
        "/superadmin/admin-management",  # Should require superadmin auth
        "/superadmin/system-settings",  # Should require superadmin auth
        "/superadmin/advanced-analytics", # Should require superadmin auth
        "/superadmin/system-monitoring"  # Should require superadmin auth
    ]
    
    for route in superadmin_routes:
        tester.test_route(route)
    
    # Test API routes
    print("\n🔌 Testing API Routes:")
    api_routes = [
        "/admin/api/dashboard-stats",
        "/superadmin/api/system-stats",
        "/superadmin/api/user-analytics"
    ]
    
    for route in api_routes:
        tester.test_route(route)
    
    print("\n📊 Route Testing Complete!")
    print("\nNotes:")
    print("- Routes returning 302 (redirect) are normal for auth-required pages")
    print("- Routes returning 401/403 are normal for admin/auth-protected endpoints")
    print("- Routes returning 404 may indicate missing templates or route issues")
    print("- Routes returning 500 indicate server errors that need investigation")

def generate_curl_commands():
    """Generate curl commands for testing"""
    base_url = "http://localhost:5051"
    
    commands = [
        # Main routes
        f'curl -X GET "{base_url}/"',
        f'curl -X GET "{base_url}/health"',
        
        # JobSeeker routes
        f'curl -X GET "{base_url}/jobseeker/"',
        f'curl -X GET "{base_url}/jobseeker/jobs"',
        f'curl -X GET "{base_url}/jobseeker/jobs?search=developer&location=remote"',
        
        # API routes with JSON
        f'curl -X POST "{base_url}/jobseeker/api/jobs/search" -H "Content-Type: application/json" -d \'{{"search": "python", "location": "remote"}}\'',
        
        # Consultancy routes
        f'curl -X GET "{base_url}/consultancy/"',
        
        # Admin routes (will likely return 302/401 without auth)
        f'curl -X GET "{base_url}/admin/"',
        f'curl -X GET "{base_url}/admin/api/dashboard-stats"',
    ]
    
    print("🔧 cURL Commands for Manual Testing:")
    print("=" * 50)
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd}")
    
    print("\n💡 To save responses to files:")
    print(f'curl -X GET "{base_url}/health" -o health_response.json')
    
    print("\n💡 To include headers in response:")
    print(f'curl -X GET "{base_url}/" -i')

def test_with_authentication():
    """Example of testing with authentication"""
    print("\n🔐 Testing with Authentication:")
    print("To test authenticated routes, you would need to:")
    print("1. Create test users in your database")
    print("2. Login through your auth system")
    print("3. Use session cookies or tokens")
    
    # Example of how you might test with authentication
    tester = RouteTestor()
    
    # This would require implementing proper auth in your app
    login_data = {
        'email': 'admin@test.com',
        'password': 'password123'
    }
    
    print("\nExample login test:")
    response = tester.test_route('/auth/login', 'POST', data=login_data)
    
    if response and response.status_code == 200:
        print("Login successful, session cookie saved")
        # Now test protected routes
        tester.test_route('/admin/')
    else:
        print("Login failed or /auth/login not implemented")

if __name__ == "__main__":
    # Run different test types
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "curl":
            generate_curl_commands()
        elif sys.argv[1] == "auth":
            test_with_authentication()
        else:
            print("Usage: python test_routes_manual.py [curl|auth]")
    else:
        test_all_routes()