"""
Jobseeker Routes - Role-based functionality for job seekers
Handles user table (not auth_users)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.middleware.security_middleware import AuthMiddleware
from app.models import User, UserSession  # Using User model for jobseekers
from app import db

# Create blueprint
jobseeker_routes_bp = Blueprint('jobseeker_routes', __name__, url_prefix='/jobseeker')

@jobseeker_routes_bp.before_request
def require_jobseeker_auth():
    """Require jobseeker authentication for all routes"""
    # Skip auth check for login page
    if request.endpoint and 'login' in request.endpoint:
        return
    
    # Check if user is logged in and has jobseeker role
    if not session.get('user_id') or session.get('role') != 'jobseeker':
        return redirect('/jobseeker/login')

@jobseeker_routes_bp.route('/dashboard')
def dashboard():
    """Jobseeker dashboard with job search focus"""
    try:
        # Get current user from session
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        
        if not user:
            flash('Session expired. Please login again.', 'warning')
            return redirect('/jobseeker/login')
        
        # Dashboard statistics for job seeker
        dashboard_data = {
            'user': user,
            'stats': {
                'applications_submitted': 0,  # Would fetch from database
                'jobs_viewed': 0,
                'profile_views': 0,
                'interviews_scheduled': 0
            },
            'recent_jobs': [],  # Would fetch recent job postings
            'recent_applications': [],  # Would fetch user's applications
            'recommended_jobs': []  # Would fetch AI-recommended jobs
        }
        
        return render_template('jobseeker/dashboard.html', **dashboard_data)
        
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('jobseeker/dashboard.html', 
                             stats={}, recent_jobs=[], recent_applications=[])

@jobseeker_routes_bp.route('/jobs')
def jobs():
    """Job search and browse page"""
    try:
        user_id = session.get('user_id')
        
        # Get search parameters
        search_query = request.args.get('q', '')
        location = request.args.get('location', '')
        category = request.args.get('category', '')
        job_type = request.args.get('type', '')
        
        # Mock job data (would come from database in real app)
        jobs_data = {
            'jobs': [],  # Would fetch from jobs table
            'total_count': 0,
            'filters': {
                'categories': [],  # Would fetch from database
                'locations': [],
                'job_types': ['full-time', 'part-time', 'contract', 'remote']
            },
            'search_params': {
                'query': search_query,
                'location': location,
                'category': category,
                'type': job_type
            }
        }
        
        return render_template('jobseeker/jobs.html', **jobs_data)
        
    except Exception as e:
        flash(f'Error loading jobs: {str(e)}', 'error')
        return render_template('jobseeker/jobs.html', jobs=[], total_count=0)

@jobseeker_routes_bp.route('/applications')
def applications():
    """View job applications history"""
    try:
        user_id = session.get('user_id')
        
        applications_data = {
            'applications': [],  # Would fetch user's applications
            'stats': {
                'total': 0,
                'pending': 0,
                'accepted': 0,
                'rejected': 0
            }
        }
        
        return render_template('jobseeker/applications.html', **applications_data)
        
    except Exception as e:
        flash(f'Error loading applications: {str(e)}', 'error')
        return render_template('jobseeker/applications.html', applications=[], stats={})

@jobseeker_routes_bp.route('/resume')
def resume():
    """Resume builder and management"""
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        resume_data = {
            'user': user,
            'resume_sections': {
                'personal_info': {},
                'experience': [],
                'education': [],
                'skills': [],
                'projects': []
            }
        }
        
        return render_template('jobseeker/resume.html', **resume_data)
        
    except Exception as e:
        flash(f'Error loading resume: {str(e)}', 'error')
        return render_template('jobseeker/resume.html', user=None, resume_sections={})

@jobseeker_routes_bp.route('/profile')
def profile():
    """User profile management"""
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            flash('User not found', 'error')
            return redirect('/jobseeker/dashboard')
        
        profile_data = {
            'user': user,
            'profile_completeness': 75,  # Would calculate based on filled fields
            'verification_status': 'pending'
        }
        
        return render_template('jobseeker/profile.html', **profile_data)
        
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        return redirect('/jobseeker/dashboard')

@jobseeker_routes_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Edit user profile"""
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            flash('User not found', 'error')
            return redirect('/jobseeker/dashboard')
        
        if request.method == 'POST':
            # Update user profile
            user.first_name = request.form.get('first_name', user.first_name)
            user.last_name = request.form.get('last_name', user.last_name)
            user.phone = request.form.get('phone', user.phone)
            
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect('/jobseeker/profile')
        
        return render_template('jobseeker/edit_profile.html', user=user)
        
    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'error')
        return redirect('/jobseeker/profile')