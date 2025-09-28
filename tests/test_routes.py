"""
4-Module Route Testing
Tests all routes for JobSeeker, Consultancy, Admin, and SuperAdmin modules
"""

import os
import sys
import unittest
import json
from unittest.mock import patch

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, UserType, Job, JobSeekerProfile, ConsultancyProfile, JobApplication

class TestModuleRoutes(unittest.TestCase):
    """Test all module routes"""
    
    def setUp(self):
        """Set up test environment"""
        # Load environment variables
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
            except ImportError:
                pass
        
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create tables
        db.create_all()
        
        # Create test users
        self.create_test_users()
    
    def tearDown(self):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def create_test_users(self):
        """Create test users for different roles"""
        # Job Seeker
        self.job_seeker = User(
            email='jobseeker@test.com',
            first_name='John',
            last_name='Seeker',
            user_type=UserType.JOB_SEEKER,
            is_active=True
        )
        self.job_seeker.set_password('password123')
        
        # Consultancy
        self.consultancy = User(
            email='company@test.com',
            first_name='Tech Corp',
            user_type=UserType.CONSULTANCY,
            is_active=True
        )
        self.consultancy.set_password('password123')
        
        # Admin
        self.admin = User(
            email='admin@test.com',
            first_name='Admin',
            last_name='User',
            user_type=UserType.ADMIN,
            is_active=True
        )
        self.admin.set_password('password123')
        
        # SuperAdmin
        self.super_admin = User(
            email='superadmin@test.com',
            first_name='Super',
            last_name='Admin',
            user_type=UserType.SUPER_ADMIN,
            is_active=True
        )
        self.super_admin.set_password('password123')
        
        db.session.add_all([self.job_seeker, self.consultancy, self.admin, self.super_admin])
        db.session.commit()
        
        print("✅ Test users created")
    
    def login_as(self, user):
        """Helper to simulate login"""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True

class TestJobSeekerRoutes(TestModuleRoutes):
    """Test JobSeeker module routes"""
    
    def test_jobseeker_index(self):
        """Test JobSeeker homepage"""
        response = self.client.get('/jobseeker/')
        self.assertEqual(response.status_code, 200)
        print("✅ JobSeeker index route working")
    
    def test_jobseeker_jobs_listing(self):
        """Test jobs listing page"""
        response = self.client.get('/jobseeker/jobs')
        self.assertEqual(response.status_code, 200)
        print("✅ JobSeeker jobs listing route working")
    
    def test_jobseeker_jobs_with_filters(self):
        """Test jobs with search filters"""
        response = self.client.get('/jobseeker/jobs?search=developer&location=New York')
        self.assertEqual(response.status_code, 200)
        print("✅ JobSeeker jobs with filters route working")
    
    def test_jobseeker_dashboard_unauthorized(self):
        """Test dashboard without login"""
        response = self.client.get('/jobseeker/dashboard')
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        print("✅ JobSeeker dashboard requires authentication")
    
    def test_jobseeker_dashboard_authorized(self):
        """Test dashboard with job seeker login"""
        self.login_as(self.job_seeker)
        response = self.client.get('/jobseeker/dashboard')
        self.assertEqual(response.status_code, 200)
        print("✅ JobSeeker dashboard works when authenticated")
    
    def test_jobseeker_profile_routes(self):
        """Test profile related routes"""
        self.login_as(self.job_seeker)
        
        routes = [
            '/jobseeker/profile',
            '/jobseeker/profile/edit',
            '/jobseeker/applications'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertIn(response.status_code, [200, 302])
            print(f"✅ JobSeeker route {route} - Status: {response.status_code}")
    
    def test_jobseeker_api_search(self):
        """Test job search API"""
        search_data = {
            'search': 'python',
            'location': 'remote',
            'category': 'technology'
        }
        
        response = self.client.post('/jobseeker/api/jobs/search',
                                  data=json.dumps(search_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✅ JobSeeker API search route working")

class TestConsultancyRoutes(TestModuleRoutes):
    """Test Consultancy module routes"""
    
    def test_consultancy_index(self):
        """Test Consultancy homepage"""
        response = self.client.get('/consultancy/')
        self.assertEqual(response.status_code, 200)
        print("✅ Consultancy index route working")
    
    def test_consultancy_dashboard_unauthorized(self):
        """Test dashboard without login"""
        response = self.client.get('/consultancy/dashboard')
        self.assertEqual(response.status_code, 302)
        print("✅ Consultancy dashboard requires authentication")
    
    def test_consultancy_dashboard_authorized(self):
        """Test dashboard with consultancy login"""
        self.login_as(self.consultancy)
        response = self.client.get('/consultancy/dashboard')
        self.assertEqual(response.status_code, 200)
        print("✅ Consultancy dashboard works when authenticated")
    
    def test_consultancy_job_management_routes(self):
        """Test job management routes"""
        self.login_as(self.consultancy)
        
        routes = [
            '/consultancy/jobs',
            '/consultancy/jobs/new',
            '/consultancy/applications',
            '/consultancy/analytics'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertIn(response.status_code, [200, 302])
            print(f"✅ Consultancy route {route} - Status: {response.status_code}")
    
    def test_consultancy_profile_routes(self):
        """Test profile routes"""
        self.login_as(self.consultancy)
        
        routes = [
            '/consultancy/profile',
            '/consultancy/profile/edit'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertIn(response.status_code, [200, 302])
            print(f"✅ Consultancy route {route} - Status: {response.status_code}")
    
    def test_consultancy_api_routes(self):
        """Test API routes"""
        self.login_as(self.consultancy)
        
        response = self.client.get('/consultancy/api/jobs')
        self.assertEqual(response.status_code, 200)
        print("✅ Consultancy API jobs route working")

class TestAdminRoutes(TestModuleRoutes):
    """Test Admin module routes"""
    
    def test_admin_dashboard_unauthorized(self):
        """Test admin dashboard without proper auth"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        print("✅ Admin dashboard requires authentication")
    
    def test_admin_dashboard_authorized(self):
        """Test admin dashboard with admin login"""
        self.login_as(self.admin)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        print("✅ Admin dashboard works when authenticated")
    
    def test_admin_user_management_routes(self):
        """Test user management routes"""
        self.login_as(self.admin)
        
        routes = [
            '/admin/users',
            '/admin/users?type=job_seeker',
            '/admin/users?status=active'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            print(f"✅ Admin route {route} - Status: {response.status_code}")
    
    def test_admin_job_management_routes(self):
        """Test job management routes"""
        self.login_as(self.admin)
        
        routes = [
            '/admin/jobs',
            '/admin/jobs?status=active',
            '/admin/applications'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            print(f"✅ Admin route {route} - Status: {response.status_code}")
    
    def test_admin_analytics_and_reports(self):
        """Test analytics and reporting routes"""
        self.login_as(self.admin)
        
        routes = [
            '/admin/analytics',
            '/admin/reports',
            '/admin/audit-logs'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            print(f"✅ Admin route {route} - Status: {response.status_code}")
    
    def test_admin_api_routes(self):
        """Test admin API routes"""
        self.login_as(self.admin)
        
        response = self.client.get('/admin/api/dashboard-stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_users', data)
        print("✅ Admin API dashboard stats route working")

class TestSuperAdminRoutes(TestModuleRoutes):
    """Test SuperAdmin module routes"""
    
    def test_superadmin_dashboard_unauthorized(self):
        """Test superadmin dashboard without proper auth"""
        response = self.client.get('/superadmin/')
        self.assertEqual(response.status_code, 302)
        print("✅ SuperAdmin dashboard requires authentication")
    
    def test_superadmin_dashboard_authorized(self):
        """Test superadmin dashboard with superadmin login"""
        self.login_as(self.super_admin)
        response = self.client.get('/superadmin/')
        self.assertEqual(response.status_code, 200)
        print("✅ SuperAdmin dashboard works when authenticated")
    
    def test_superadmin_management_routes(self):
        """Test admin management routes"""
        self.login_as(self.super_admin)
        
        routes = [
            '/superadmin/admin-management',
            '/superadmin/admin-management/create',
            '/superadmin/system-settings'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            print(f"✅ SuperAdmin route {route} - Status: {response.status_code}")
    
    def test_superadmin_analytics_routes(self):
        """Test advanced analytics routes"""
        self.login_as(self.super_admin)
        
        routes = [
            '/superadmin/advanced-analytics',
            '/superadmin/system-monitoring',
            '/superadmin/backup-restore'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            print(f"✅ SuperAdmin route {route} - Status: {response.status_code}")
    
    def test_superladmin_api_routes(self):
        """Test superadmin API routes"""
        self.login_as(self.super_admin)
        
        api_routes = [
            '/superadmin/api/system-stats',
            '/superadmin/api/user-analytics'
        ]
        
        for route in api_routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            print(f"✅ SuperAdmin API route {route} - Status: {response.status_code}")

class TestMainRoutes(TestModuleRoutes):
    """Test main application routes"""
    
    def test_main_routes(self):
        """Test main application routes"""
        routes = [
            '/',
            '/about',
            '/contact',
            '/pricing',
            '/health'
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertIn(response.status_code, [200, 302])
            print(f"✅ Main route {route} - Status: {response.status_code}")
    
    def test_error_routes(self):
        """Test error handling"""
        # Test 404
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        print("✅ 404 error handling working")

class TestJobOperations(TestModuleRoutes):
    """Test job-related operations across modules"""
    
    def test_job_lifecycle(self):
        """Test complete job lifecycle"""
        # 1. Consultancy creates job
        self.login_as(self.consultancy)
        
        job_data = {
            'title': 'Python Developer',
            'description': 'Looking for Python developer',
            'location': 'Remote',
            'job_type': 'full_time',
            'category': 'Technology',
            'skills_required': 'Python, Django, Flask',
            'salary_min': 80000,
            'salary_max': 120000
        }
        
        response = self.client.post('/consultancy/jobs/new', data=job_data)
        self.assertIn(response.status_code, [200, 302])
        print("✅ Job creation flow working")
        
        # 2. Create a job directly for testing
        job = Job(
            title='Test Job',
            description='Test Description',
            company_name='Test Company',
            location='Test Location',
            consultancy_id=self.consultancy.id,
            is_active=True
        )
        db.session.add(job)
        db.session.commit()
        
        # 3. JobSeeker views job
        response = self.client.get(f'/jobseeker/jobs/{job.id}')
        self.assertEqual(response.status_code, 200)
        print("✅ Job detail view working")
        
        # 4. JobSeeker applies to job
        self.login_as(self.job_seeker)
        
        application_data = {
            'cover_letter': 'I am interested in this position'
        }
        
        response = self.client.post(f'/jobseeker/jobs/{job.id}/apply', data=application_data)
        self.assertIn(response.status_code, [200, 302])
        print("✅ Job application flow working")

def run_route_tests():
    """Run all route tests"""
    print("🧪 Starting 4-Module Route Testing...\n")
    
    # Test suites
    test_classes = [
        TestJobSeekerRoutes,
        TestConsultancyRoutes, 
        TestAdminRoutes,
        TestSuperAdminRoutes,
        TestMainRoutes,
        TestJobOperations
    ]
    
    total_tests = 0
    total_failures = 0
    
    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}")
        print("-" * 50)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        result = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w')).run(suite)
        
        # Run tests manually to get our custom output
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for method_name in test_methods:
            try:
                test_instance.setUp()
                getattr(test_instance, method_name)()
                test_instance.tearDown()
                total_tests += 1
            except Exception as e:
                print(f"❌ {method_name} failed: {str(e)}")
                total_failures += 1
                total_tests += 1
    
    print(f"\n📊 Testing Summary:")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_tests - total_failures}")
    print(f"Failed: {total_failures}")
    
    if total_failures == 0:
        print("🎉 All routes are working correctly!")
    else:
        print(f"⚠️  {total_failures} routes need attention")

if __name__ == '__main__':
    run_route_tests()