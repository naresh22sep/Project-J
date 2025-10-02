"""
Admin Module Routes - Enhanced with API endpoints
"""

from flask import Blueprint, jsonify, render_template, session, g
from datetime import datetime, timedelta

admin = Blueprint("admin", __name__)

@admin.route("/")
def dashboard():
    """Admin dashboard"""
    try:
        # Mock data for dashboard (in real app, fetch from database)
        dashboard_data = {
            'days': 30,
            'total_users': 156,
            'new_users_today': 8,
            'total_jobs': 234,
            'active_jobs': 189,
            'total_applications': 567,
            'pending_applications': 89,
            'accepted_applications': 145,
            'applications_today': 12,
            'user_trend': [
                {'date': '2024-01-01', 'count': 5},
                {'date': '2024-01-02', 'count': 8},
                {'date': '2024-01-03', 'count': 12},
                {'date': '2024-01-04', 'count': 7},
                {'date': '2024-01-05', 'count': 15},
                {'date': '2024-01-06', 'count': 9},
                {'date': '2024-01-07', 'count': 11}
            ],
            'top_categories': [
                {'category': 'Software Engineering', 'job_count': 45},
                {'category': 'Marketing', 'job_count': 32},
                {'category': 'Sales', 'job_count': 28},
                {'category': 'Design', 'job_count': 18},
                {'category': 'Finance', 'job_count': 15}
            ],
            'recent_users': [],  # Would be fetched from database
            'recent_jobs': []    # Would be fetched from database
        }
        
        # Add current user info to context (mock for now)
        dashboard_data['current_user'] = {
            'first_name': session.get('first_name', 'Admin'),
            'last_name': session.get('last_name', 'User'),
            'email': session.get('email', 'admin@example.com')
        }
        
        return render_template('admin/dashboard.html', **dashboard_data)
        
    except Exception as e:
        print(f"Error rendering admin dashboard: {e}")
        return f"<h1>Admin Dashboard</h1><p>Error: {e}</p><p><b>Path:</b> /admin/</p>"

@admin.route("/users")
def users():
    """User management page"""
    try:
        return render_template('admin/users.html', 
                             title='User Management',
                             users=[])  # Would fetch from database
    except Exception as e:
        return f"<h1>Admin Users</h1><p>Error: {e}</p><p><b>Path:</b> /admin/users</p>"

@admin.route("/users/<int:user_id>")
def user_detail(user_id):
    """User detail page"""
    return f"<h1>Admin User Detail</h1><p><b>Route:</b> user_detail</p><p><b>Path:</b> /admin/users/{user_id}</p><p><b>User ID:</b> {user_id}</p>"

@admin.route("/jobs")
def jobs():
    """Job management page"""
    try:
        return render_template('admin/jobs.html', 
                             title='Job Management',
                             jobs=[])  # Would fetch from database
    except Exception as e:
        return f"<h1>Admin Jobs</h1><p>Error: {e}</p><p><b>Path:</b> /admin/jobs</p>"

@admin.route("/applications")
def applications():
    """Applications management page"""
    try:
        return render_template('admin/applications.html', 
                             title='Application Management',
                             applications=[])  # Would fetch from database
    except Exception as e:
        return f"<h1>Admin Applications</h1><p>Error: {e}</p><p><b>Path:</b> /admin/applications</p>"

@admin.route("/jobs/<int:job_id>")
def job_detail(job_id):
    """Job detail page"""
    return f"<h1>Admin Job Detail</h1><p><b>Route:</b> job_detail</p><p><b>Path:</b> /admin/jobs/{job_id}</p><p><b>Job ID:</b> {job_id}</p>"

@admin.route("/companies")
def companies():
    """Company management page"""
    return f"<h1>Admin Companies</h1><p><b>Route:</b> companies</p><p><b>Path:</b> /admin/companies</p>"

@admin.route("/reports")
def reports():
    """Reports page"""
    return f"<h1>Admin Reports</h1><p><b>Route:</b> reports</p><p><b>Path:</b> /admin/reports</p>"

@admin.route("/settings")
def settings():
    """Settings page"""
    return f"<h1>Admin Settings</h1><p><b>Route:</b> settings</p><p><b>Path:</b> /admin/settings</p>"

# API Endpoints
@admin.route("/api/dashboard-stats")
def dashboard_stats():
    """Get dashboard statistics for admin panel"""
    try:
        # Basic stats for admin dashboard
        # Note: In a real implementation, these would come from actual database queries
        stats = {
            'total_users': 42,
            'active_users': 38,
            'total_jobs': 156,
            'active_jobs': 89,
            'total_companies': 23,
            'active_companies': 21,
            'applications_today': 12,
            'jobs_posted_today': 5,
            'new_users_today': 3,
            'revenue_today': 1245.50,
            'system_status': 'operational',
            'last_updated': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': stats,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@admin.route("/api/recent-activity")
def recent_activity():
    """Get recent activity for admin dashboard"""
    try:
        # Mock recent activity data
        activities = [
            {
                'id': 1,
                'type': 'user_registration',
                'message': 'New user John Doe registered',
                'timestamp': (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
                'severity': 'info'
            },
            {
                'id': 2,
                'type': 'job_posted',
                'message': 'New job posted: Software Engineer at TechCorp',
                'timestamp': (datetime.utcnow() - timedelta(minutes=15)).isoformat(),
                'severity': 'info'
            },
            {
                'id': 3,
                'type': 'application_submitted',
                'message': 'Application submitted for Marketing Manager position',
                'timestamp': (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
                'severity': 'info'
            },
            {
                'id': 4,
                'type': 'company_verified',
                'message': 'Company InnovateLabs verification completed',
                'timestamp': (datetime.utcnow() - timedelta(hours=1)).isoformat(),
                'severity': 'success'
            },
            {
                'id': 5,
                'type': 'system_maintenance',
                'message': 'Scheduled database backup completed',
                'timestamp': (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                'severity': 'info'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': activities,
            'count': len(activities),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@admin.route("/api/system-health")
def system_health():
    """Get system health status for admin dashboard"""
    try:
        health_data = {
            'database': {
                'status': 'healthy',
                'response_time': '2ms',
                'last_check': datetime.utcnow().isoformat()
            },
            'api': {
                'status': 'healthy',
                'response_time': '15ms',
                'last_check': datetime.utcnow().isoformat()
            },
            'storage': {
                'status': 'healthy',
                'usage': '45%',
                'available': '550GB',
                'last_check': datetime.utcnow().isoformat()
            },
            'cache': {
                'status': 'healthy',
                'hit_rate': '94%',
                'memory_usage': '32%',
                'last_check': datetime.utcnow().isoformat()
            },
            'overall_status': 'healthy',
            'uptime': '99.8%',
            'last_incident': None
        }
        
        return jsonify({
            'success': True,
            'data': health_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
