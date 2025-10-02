# 🧪 Route Testing Guide

This guide explains how to test all routes/links in your 4-module Flask application.

## 🚀 Quick Start

### Option 1: Automated Testing
```bash
# Run all route tests
python tests/test_routes.py

# Or use the batch file
test_routes.bat
```

### Option 2: Manual Testing
```bash
# First, start your Flask app
python run.py

# Then in another terminal
python test_routes_manual.py
```

### Option 3: Using cURL
```bash
# Generate cURL commands
python test_routes_manual.py curl

# Then copy and run the commands
```

## 📋 Route Categories

### 🏠 Main Routes
- `/` - Landing page
- `/health` - Health check
- `/about` - About page  
- `/contact` - Contact page
- `/pricing` - Pricing page

**Expected Status:** 200 (OK)

### 👤 JobSeeker Routes (`/jobseeker/`)
- `/jobseeker/` - JobSeeker homepage
- `/jobseeker/jobs` - Job listings
- `/jobseeker/jobs/<id>` - Job details
- `/jobseeker/dashboard` - Dashboard (requires auth)
- `/jobseeker/profile` - Profile (requires auth)
- `/jobseeker/applications` - Applications (requires auth)

**Expected Status:** 
- Public routes: 200 (OK)
- Protected routes: 302 (Redirect to login) or 401 (Unauthorized)

### 🏢 Consultancy Routes (`/consultancy/`)
- `/consultancy/` - Consultancy homepage
- `/consultancy/dashboard` - Dashboard (requires auth)
- `/consultancy/jobs` - Job management (requires auth)
- `/consultancy/jobs/new` - Create job (requires auth)
- `/consultancy/applications` - View applications (requires auth)
- `/consultancy/analytics` - Analytics (requires auth)

**Expected Status:**
- Public routes: 200 (OK)
- Protected routes: 302 (Redirect) or 401 (Unauthorized)

### 👮 Admin Routes (`/admin/`)
- `/admin/` - Admin dashboard (requires admin auth)
- `/admin/users` - User management (requires admin auth)
- `/admin/jobs` - Job moderation (requires admin auth)
- `/admin/applications` - Application oversight (requires admin auth)
- `/admin/analytics` - System analytics (requires admin auth)
- `/admin/reports` - Reports (requires admin auth)

**Expected Status:** 302 (Redirect) or 403 (Forbidden) without admin auth

### 👑 SuperAdmin Routes (`/superadmin/`)
- `/superadmin/` - SuperAdmin dashboard
- `/superadmin/admin-management` - Admin management
- `/superadmin/system-settings` - System configuration
- `/superadmin/advanced-analytics` - Advanced analytics
- `/superadmin/system-monitoring` - System monitoring

**Expected Status:** 302 (Redirect) or 403 (Forbidden) without superadmin auth

### 🔌 API Routes
- `/admin/api/dashboard-stats` - Admin dashboard stats
- `/superadmin/api/system-stats` - System statistics
- `/jobseeker/api/jobs/search` - Job search API

**Expected Status:** 200 (JSON response) or 401/403 for auth-required endpoints

## 🔧 Manual Testing Methods

### Method 1: Browser Testing
1. Start your Flask app: `python run.py`
2. Open browser and visit: `http://localhost:5051`
3. Navigate through the routes manually

### Method 2: cURL Testing
```bash
# Test main page
curl -X GET "http://localhost:5051/"

# Test health endpoint
curl -X GET "http://localhost:5051/health"

# Test job search API
curl -X POST "http://localhost:5051/jobseeker/api/jobs/search" \
  -H "Content-Type: application/json" \
  -d '{"search": "python", "location": "remote"}'

# Test with headers
curl -X GET "http://localhost:5051/admin/" -i
```

### Method 3: Python Requests
```python
import requests

# Test a route
response = requests.get('http://localhost:5051/')
print(f"Status: {response.status_code}")
print(f"Content: {response.text[:100]}...")
```

## 🔐 Testing Authenticated Routes

### Create Test Users First
```python
# Run this in Flask shell or create a script
from app import create_app, db
from app.models import User, UserType

app = create_app()
with app.app_context():
    # Create job seeker
    job_seeker = User(
        email='jobseeker@test.com',
        first_name='John',
        user_type=UserType.JOB_SEEKER,
        is_active=True
    )
    job_seeker.set_password('password123')
    
    # Create admin
    admin = User(
        email='admin@test.com',
        first_name='Admin',
        user_type=UserType.ADMIN,
        is_active=True
    )
    admin.set_password('password123')
    
    db.session.add_all([job_seeker, admin])
    db.session.commit()
```

### Test Authentication Flow
```bash
# 1. Test login (implement /auth/login first)
curl -X POST "http://localhost:5051/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "password123"}' \
  -c cookies.txt

# 2. Use cookies for authenticated requests
curl -X GET "http://localhost:5051/admin/" -b cookies.txt
```

## 📊 Expected Response Codes

| Code | Meaning | When You'll See It |
|------|---------|-------------------|
| 200  | OK | Route works correctly |
| 302  | Redirect | Auth required, redirects to login |
| 401  | Unauthorized | Auth required but not provided |
| 403  | Forbidden | Wrong user type/permissions |
| 404  | Not Found | Route doesn't exist |
| 500  | Server Error | Bug in your code |

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "Connection Error" 
**Problem:** Flask app not running  
**Solution:** Start app with `python run.py`

#### 2. "404 Not Found"
**Problem:** Route not registered or typo in URL  
**Solution:** Check blueprint registration in `app/__init__.py`

#### 3. "500 Internal Server Error"
**Problem:** Bug in route handler  
**Solution:** Check Flask logs for error details

#### 4. "ImportError" in routes
**Problem:** Missing dependencies or import issues  
**Solution:** Check imports in route files

#### 5. Template not found errors
**Problem:** Template files missing  
**Solution:** Ensure templates exist in correct directories

### Debug Mode Testing
```bash
# Run app in debug mode for detailed errors
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python run.py
```

## 📈 Advanced Testing

### Load Testing
```bash
# Install Apache Bench
# Then test route performance
ab -n 100 -c 10 http://localhost:5051/
```

### API Testing with Postman
1. Import our routes into Postman
2. Set up environment variables
3. Create test collections
4. Run automated API tests

### Integration Testing
```python
# tests/test_integration.py
def test_complete_job_flow():
    # 1. Consultancy creates job
    # 2. JobSeeker searches and applies
    # 3. Admin moderates
    # 4. SuperAdmin monitors
    pass
```

## 🎯 Testing Checklist

- [ ] All main routes return 200
- [ ] Protected routes require authentication  
- [ ] Role-based access control works
- [ ] API endpoints return valid JSON
- [ ] Error pages display correctly
- [ ] Database operations don't cause errors
- [ ] File uploads work (if implemented)
- [ ] Search and filtering work
- [ ] Pagination works on list pages
- [ ] AJAX endpoints respond correctly

## 📝 Test Results Documentation

Keep track of your testing:

```markdown
## Test Results - [Date]

### ✅ Working Routes
- /jobseeker/ - 200 OK
- /consultancy/ - 200 OK
- /admin/ - 302 Redirect (correct)

### ❌ Issues Found  
- /superadmin/backup-restore - 500 Error (needs investigation)
- /jobseeker/jobs/999 - Should return 404 but returns 500

### 🔧 Next Steps
1. Fix backup-restore template
2. Add proper error handling for job detail route
3. Implement missing authentication routes
```

## 🚀 Production Testing

Before deploying:
1. Test all routes in production environment
2. Verify SSL certificates work
3. Test with real database data  
4. Check performance under load
5. Verify logging and monitoring work

Remember: Thorough testing now saves debugging time later! 🎯