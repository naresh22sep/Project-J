"""
Consultancy Module Routes - Simplified for Testing
"""

from flask import Blueprint

consultancy = Blueprint("consultancy", __name__)

@consultancy.route("/")
def dashboard():
    """Consultancy dashboard"""
    return f"<h1>Consultancy Dashboard</h1><p><b>Route:</b> dashboard</p><p><b>Path:</b> /consultancy/</p>"

@consultancy.route("/jobs")
def jobs():
    """Job postings page"""
    return f"<h1>Consultancy Jobs</h1><p><b>Route:</b> jobs</p><p><b>Path:</b> /consultancy/jobs</p>"

@consultancy.route("/jobs/create")
def create_job():
    """Create job page"""
    return f"<h1>Consultancy Create Job</h1><p><b>Route:</b> create_job</p><p><b>Path:</b> /consultancy/jobs/create</p>"

@consultancy.route("/jobs/<int:job_id>")
def job_detail(job_id):
    """Job detail page"""
    return f"<h1>Consultancy Job Detail</h1><p><b>Route:</b> job_detail</p><p><b>Path:</b> /consultancy/jobs/{job_id}</p><p><b>Job ID:</b> {job_id}</p>"

@consultancy.route("/candidates")
def candidates():
    """Candidates page"""
    return f"<h1>Consultancy Candidates</h1><p><b>Route:</b> candidates</p><p><b>Path:</b> /consultancy/candidates</p>"

@consultancy.route("/candidates/<int:candidate_id>")
def candidate_detail(candidate_id):
    """Candidate detail page"""
    return f"<h1>Consultancy Candidate Detail</h1><p><b>Route:</b> candidate_detail</p><p><b>Path:</b> /consultancy/candidates/{candidate_id}</p><p><b>Candidate ID:</b> {candidate_id}</p>"

@consultancy.route("/company")
def company():
    """Company profile page"""
    return f"<h1>Consultancy Company</h1><p><b>Route:</b> company</p><p><b>Path:</b> /consultancy/company</p>"

@consultancy.route("/reports")
def reports():
    """Reports page"""
    return f"<h1>Consultancy Reports</h1><p><b>Route:</b> reports</p><p><b>Path:</b> /consultancy/reports</p>"

@consultancy.route("/billing")
def billing():
    """Billing page"""
    return f"<h1>Consultancy Billing</h1><p><b>Route:</b> billing</p><p><b>Path:</b> /consultancy/billing</p>"
