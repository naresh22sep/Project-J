"""
Admin Module Routes - Simplified for Testing
"""

from flask import Blueprint

admin = Blueprint("admin", __name__)

@admin.route("/")
def dashboard():
    """Admin dashboard"""
    return f"<h1>Admin Dashboard</h1><p><b>Route:</b> dashboard</p><p><b>Path:</b> /admin/</p>"

@admin.route("/users")
def users():
    """User management page"""
    return f"<h1>Admin Users</h1><p><b>Route:</b> users</p><p><b>Path:</b> /admin/users</p>"

@admin.route("/users/<int:user_id>")
def user_detail(user_id):
    """User detail page"""
    return f"<h1>Admin User Detail</h1><p><b>Route:</b> user_detail</p><p><b>Path:</b> /admin/users/{user_id}</p><p><b>User ID:</b> {user_id}</p>"

@admin.route("/jobs")
def jobs():
    """Job management page"""
    return f"<h1>Admin Jobs</h1><p><b>Route:</b> jobs</p><p><b>Path:</b> /admin/jobs</p>"

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
