"""
JobSeeker Module Routes - Simplified for Testing
"""

from flask import Blueprint

jobseeker = Blueprint("jobseeker", __name__)

@jobseeker.route("/")
def dashboard():
    """JobSeeker dashboard"""
    return f"<h1>JobSeeker Dashboard</h1><p><b>Route:</b> dashboard</p><p><b>Path:</b> /jobseeker/</p>"

@jobseeker.route("/jobs")
def jobs():
    """Job search page"""
    return f"<h1>JobSeeker Jobs</h1><p><b>Route:</b> jobs</p><p><b>Path:</b> /jobseeker/jobs</p>"

@jobseeker.route("/jobs/<int:job_id>")
def job_detail(job_id):
    """Job detail page"""
    return f"<h1>JobSeeker Job Detail</h1><p><b>Route:</b> job_detail</p><p><b>Path:</b> /jobseeker/jobs/{job_id}</p><p><b>Job ID:</b> {job_id}</p>"

@jobseeker.route("/apply/<int:job_id>")
def apply(job_id):
    """Apply for job page"""
    return f"<h1>JobSeeker Apply</h1><p><b>Route:</b> apply</p><p><b>Path:</b> /jobseeker/apply/{job_id}</p><p><b>Job ID:</b> {job_id}</p>"

@jobseeker.route("/profile")
def profile():
    """User profile page"""
    return f"<h1>JobSeeker Profile</h1><p><b>Route:</b> profile</p><p><b>Path:</b> /jobseeker/profile</p>"

@jobseeker.route("/applications")
def applications():
    """Job applications page"""
    return f"<h1>JobSeeker Applications</h1><p><b>Route:</b> applications</p><p><b>Path:</b> /jobseeker/applications</p>"

@jobseeker.route("/saved")
def saved():
    """Saved jobs page"""
    return f"<h1>JobSeeker Saved Jobs</h1><p><b>Route:</b> saved</p><p><b>Path:</b> /jobseeker/saved</p>"

@jobseeker.route("/alerts")
def alerts():
    """Job alerts page"""
    return f"<h1>JobSeeker Alerts</h1><p><b>Route:</b> alerts</p><p><b>Path:</b> /jobseeker/alerts</p>"
