# 🌐 Browser Testing URLs for 4-Module Flask App

**Base URL:** http://localhost:5051

## 🏠 Main Application URLs

### Public Pages (Should work for everyone)
```
http://localhost:5051/                    # Landing page
http://localhost:5051/health              # Health check (JSON response)
http://localhost:5051/about               # About page
http://localhost:5051/contact             # Contact page  
http://localhost:5051/pricing             # Pricing page
```

## 👤 JobSeeker Module URLs (`/jobseeker/`)

### Public JobSeeker Pages
```
http://localhost:5051/jobseeker/                           # JobSeeker homepage
http://localhost:5051/jobseeker/jobs                       # Job listings
http://localhost:5051/jobseeker/jobs?search=developer      # Job search with filter
http://localhost:5051/jobseeker/jobs?location=remote       # Job search by location
http://localhost:5051/jobseeker/jobs?category=technology   # Job search by category
http://localhost:5051/jobseeker/jobs/1                     # Job details (ID 1)
http://localhost:5051/jobseeker/jobs/2                     # Job details (ID 2)
```

### Protected JobSeeker Pages (Require Authentication)
```
http://localhost:5051/jobseeker/dashboard                  # JobSeeker dashboard
http://localhost:5051/jobseeker/profile                   # View profile
http://localhost:5051/jobseeker/profile/edit              # Edit profile
http://localhost:5051/jobseeker/applications              # View applications
http://localhost:5051/jobseeker/applications?status=pending # Filter applications
http://localhost:5051/jobseeker/applications/1            # Application details
http://localhost:5051/jobseeker/jobs/1/apply              # Apply to job form
```

## 🏢 Consultancy Module URLs (`/consultancy/`)

### Public Consultancy Pages
```
http://localhost:5051/consultancy/                         # Consultancy homepage
```

### Protected Consultancy Pages (Require Consultancy Authentication)
```
http://localhost:5051/consultancy/dashboard                # Company dashboard
http://localhost:5051/consultancy/profile                 # Company profile
http://localhost:5051/consultancy/profile/edit            # Edit company profile
http://localhost:5051/consultancy/jobs                    # Manage jobs
http://localhost:5051/consultancy/jobs?status=active      # Filter active jobs
http://localhost:5051/consultancy/jobs/new                # Create new job
http://localhost:5051/consultancy/jobs/1                  # Job details and applications
http://localhost:5051/consultancy/jobs/1/edit             # Edit job
http://localhost:5051/consultancy/applications            # View all applications
http://localhost:5051/consultancy/applications?status=pending # Filter applications
http://localhost:5051/consultancy/applications/1          # Application details
http://localhost:5051/consultancy/analytics               # Company analytics
http://localhost:5051/consultancy/analytics?days=30       # Analytics for 30 days
```

## 👮 Admin Module URLs (`/admin/`)

### All Admin Pages (Require Admin Authentication)
```
http://localhost:5051/admin/                               # Admin dashboard
http://localhost:5051/admin/?days=7                       # Dashboard for 7 days
http://localhost:5051/admin/?days=30                      # Dashboard for 30 days
http://localhost:5051/admin/users                         # User management
http://localhost:5051/admin/users?type=job_seeker         # Filter job seekers
http://localhost:5051/admin/users?type=consultancy        # Filter consultancies
http://localhost:5051/admin/users?status=active          # Filter active users
http://localhost:5051/admin/users?search=john             # Search users
http://localhost:5051/admin/users/1                       # User details
http://localhost:5051/admin/jobs                          # Job management
http://localhost:5051/admin/jobs?status=active            # Filter active jobs
http://localhost:5051/admin/jobs?category=technology      # Filter by category
http://localhost:5051/admin/jobs?search=developer         # Search jobs
http://localhost:5051/admin/jobs/1                        # Job details
http://localhost:5051/admin/applications                  # Application oversight
http://localhost:5051/admin/applications?status=pending   # Filter pending applications
http://localhost:5051/admin/applications/1                # Application details
http://localhost:5051/admin/analytics                     # System analytics
http://localhost:5051/admin/analytics?days=90             # Analytics for 90 days
http://localhost:5051/admin/reports                       # Reports page
http://localhost:5051/admin/settings                      # System settings
http://localhost:5051/admin/audit-logs                    # Audit logs
http://localhost:5051/admin/audit-logs?user_id=1          # Filter by user
```

## 👑 SuperAdmin Module URLs (`/superadmin/`)

### All SuperAdmin Pages (Require SuperAdmin Authentication)
```
http://localhost:5051/superadmin/                          # SuperAdmin dashboard
http://localhost:5051/superadmin/admin-management          # Admin management
http://localhost:5051/superadmin/admin-management?status=active # Filter active admins
http://localhost:5051/superadmin/admin-management/create   # Create new admin
http://localhost:5051/superadmin/system-settings           # System configuration
http://localhost:5051/superadmin/advanced-analytics        # Advanced analytics
http://localhost:5051/superadmin/advanced-analytics?days=30 # Analytics for 30 days
http://localhost:5051/superadmin/system-monitoring         # System monitoring
http://localhost:5051/superadmin/backup-restore            # Backup & restore
```

## 🔌 API Endpoints (JSON Responses)

### JobSeeker API
```
# POST with JSON data
http://localhost:5051/jobseeker/api/jobs/search
# Body: {"search": "python", "location": "remote", "category": "technology"}

http://localhost:5051/jobseeker/api/profile/update
# POST with JSON profile data
```

### Consultancy API
```
http://localhost:5051/consultancy/api/jobs                 # GET - List company jobs
http://localhost:5051/consultancy/api/dashboard-stats      # GET - Dashboard stats
```

### Admin API
```
http://localhost:5051/admin/api/dashboard-stats            # GET - Admin dashboard stats
http://localhost:5051/admin/api/bulk-action               # POST - Bulk operations
```

### SuperAdmin API
```
http://localhost:5051/superadmin/api/system-stats          # GET - System statistics
http://localhost:5051/superadmin/api/user-analytics        # GET - User analytics
```

## 📄 File Download URLs

### Admin Reports
```
http://localhost:5051/admin/reports/users                  # Download users CSV
http://localhost:5051/admin/reports/jobs                   # Download jobs CSV
```

### SuperAdmin Reports
```
http://localhost:5051/superadmin/reports/comprehensive     # Download comprehensive JSON report
```

## ❌ Error Pages

### Test Error Handling
```
http://localhost:5051/nonexistent-page                     # Should show 404 error
http://localhost:5051/jobseeker/jobs/99999                 # Should show 404 for non-existent job
```

## 🔐 Authentication Test Flow

### Expected Behavior for Protected URLs:

1. **Without Authentication:**
   - Should redirect to login page (302)
   - Or show "Access denied" message (403)

2. **With Wrong User Type:**
   - JobSeeker trying to access `/admin/` → 403 Forbidden
   - Consultancy trying to access `/superadmin/` → 403 Forbidden

3. **With Correct Authentication:**
   - Should show the page content (200)

## 🧪 Browser Testing Checklist

### Step 1: Test Public Pages ✅
```
□ http://localhost:5051/
□ http://localhost:5051/jobseeker/
□ http://localhost:5051/jobseeker/jobs  
□ http://localhost:5051/consultancy/
□ http://localhost:5051/health
```

### Step 2: Test Authentication Required ✅
```
□ http://localhost:5051/jobseeker/dashboard    # Should redirect
□ http://localhost:5051/admin/                 # Should redirect
□ http://localhost:5051/superadmin/            # Should redirect
```

### Step 3: Test Search & Filters ✅
```
□ http://localhost:5051/jobseeker/jobs?search=python
□ http://localhost:5051/admin/users?type=job_seeker
□ http://localhost:5051/admin/jobs?status=active
```

### Step 4: Test API Endpoints ✅
```
□ http://localhost:5051/health                 # Should return JSON
□ http://localhost:5051/admin/api/dashboard-stats # Should require auth
```

### Step 5: Test Error Handling ✅
```
□ http://localhost:5051/invalid-page           # Should show 404
□ http://localhost:5051/jobseeker/jobs/99999   # Should handle gracefully
```

## 💡 Browser Testing Tips

### 1. Use Developer Tools
- **F12** → Network tab to see HTTP status codes
- **Console** tab to see JavaScript errors
- **Application** tab to check cookies/sessions

### 2. Test Different Browsers
- Chrome, Firefox, Safari, Edge
- Mobile browsers (responsive design)

### 3. Test Different Screen Sizes
- Desktop (1920x1080)
- Tablet (768x1024)  
- Mobile (375x667)

### 4. Bookmarks for Quick Testing
Save these as bookmarks for quick access:
- `http://localhost:5051/` (Home)
- `http://localhost:5051/jobseeker/jobs` (Jobs)
- `http://localhost:5051/admin/` (Admin)
- `http://localhost:5051/health` (Health)

### 5. Testing with Postman/Thunder Client
For API endpoints, use tools like:
- Postman
- Thunder Client (VS Code extension)
- curl commands

## 🚨 Common Issues to Watch For

1. **500 Errors** → Check server logs
2. **404 Errors** → Check route registration
3. **Blank pages** → Check template rendering
4. **JavaScript errors** → Check browser console
5. **CSS not loading** → Check static file paths
6. **Database errors** → Check model relationships

## 📊 Expected Results Summary

| URL Pattern | No Auth | JobSeeker Auth | Consultancy Auth | Admin Auth | SuperAdmin Auth |
|-------------|---------|----------------|------------------|------------|------------------|
| `/` | 200 | 200 | 200 | 200 | 200 |
| `/jobseeker/jobs` | 200 | 200 | 200 | 200 | 200 |
| `/jobseeker/dashboard` | 302 | 200 | 302 | 302 | 302 |
| `/consultancy/dashboard` | 302 | 302 | 200 | 302 | 302 |
| `/admin/` | 302 | 302 | 302 | 200 | 200 |
| `/superadmin/` | 302 | 302 | 302 | 302 | 200 |

Start with the public pages, then work your way through the protected routes! 🌐