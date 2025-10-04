"""
Consultancy Routes - Role-based functionality for recruitment companies
Handles user table (not auth_users)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.middleware.security_middleware import AuthMiddleware
from app.models import User, UserSession  # Using User model for consultancies
from app import db

# Create blueprint
consultancy_routes_bp = Blueprint('consultancy_routes', __name__, url_prefix='/consultancy')

@consultancy_routes_bp.before_request
def require_consultancy_auth():
    """Require consultancy authentication for all routes"""
    # Skip auth check for login page
    if request.endpoint and 'login' in request.endpoint:
        return
    
    # Check if user is logged in and has consultancy role
    if not session.get('user_id') or session.get('role') != 'consultancy':
        return redirect('/consultancy/login')

@consultancy_routes_bp.route('/dashboard')
def dashboard():
    """Consultancy dashboard with recruitment focus"""
    try:
        # Get current user from session
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        
        if not user:
            flash('Session expired. Please login again.', 'warning')
            return redirect('/consultancy/login')
        
        # Dashboard statistics for consultancy
        dashboard_data = {
            'user': user,
            'stats': {
                'active_jobs': 0,  # Would fetch from database
                'total_applications': 0,
                'interviews_scheduled': 0,
                'positions_filled': 0,
                'candidate_views': 0
            },
            'recent_jobs': [],  # Would fetch company's job postings
            'recent_applications': [],  # Would fetch recent applications
            'top_candidates': [],  # Would fetch recommended candidates
            'hiring_metrics': {
                'this_month': {
                    'jobs_posted': 0,
                    'applications_received': 0,
                    'interviews_conducted': 0,
                    'hires_made': 0
                }
            }
        }
        
        return render_template('consultancy/dashboard.html', **dashboard_data)
        
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('consultancy/dashboard.html', 
                             stats={}, recent_jobs=[], recent_applications=[])

@consultancy_routes_bp.route('/jobs')
def jobs():
    """Manage job postings"""
    try:
        user_id = session.get('user_id')
        
        # Get filter parameters
        status = request.args.get('status', 'all')
        category = request.args.get('category', '')
        
        jobs_data = {
            'jobs': [],  # Would fetch company's job postings
            'stats': {
                'active': 0,
                'draft': 0,
                'closed': 0,
                'expired': 0
            },
            'filters': {
                'status': status,
                'category': category
            }
        }
        
        return render_template('consultancy/jobs.html', **jobs_data)
        
    except Exception as e:
        flash(f'Error loading jobs: {str(e)}', 'error')
        return render_template('consultancy/jobs.html', jobs=[], stats={})

@consultancy_routes_bp.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    """Create new job posting"""
    try:
        if request.method == 'POST':
            # Process job creation
            job_data = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'requirements': request.form.get('requirements'),
                'location': request.form.get('location'),
                'salary_min': request.form.get('salary_min'),
                'salary_max': request.form.get('salary_max'),
                'job_type': request.form.get('job_type'),
                'category': request.form.get('category')
            }
            
            # Would save to database
            flash('Job posting created successfully', 'success')
            return redirect('/consultancy/jobs')
        
        # GET request - show form
        form_data = {
            'categories': [],  # Would fetch from database
            'job_types': ['full-time', 'part-time', 'contract', 'remote'],
            'locations': []  # Would fetch from database
        }
        
        return render_template('consultancy/create_job.html', **form_data)
        
    except Exception as e:
        flash(f'Error creating job: {str(e)}', 'error')
        return redirect('/consultancy/jobs')

@consultancy_routes_bp.route('/applications')
def applications():
    """View and manage job applications"""
    try:
        user_id = session.get('user_id')
        
        # Get filter parameters
        job_id = request.args.get('job_id')
        status = request.args.get('status', 'all')
        
        applications_data = {
            'applications': [],  # Would fetch applications for company's jobs
            'jobs': [],  # Would fetch company's jobs for filtering
            'stats': {
                'total': 0,
                'new': 0,
                'reviewed': 0,
                'interviewed': 0,
                'hired': 0,
                'rejected': 0
            },
            'filters': {
                'job_id': job_id,
                'status': status
            }
        }
        
        return render_template('consultancy/applications.html', **applications_data)
        
    except Exception as e:
        flash(f'Error loading applications: {str(e)}', 'error')
        return render_template('consultancy/applications.html', applications=[], stats={})

@consultancy_routes_bp.route('/candidates')
def candidates():
    """Browse and search candidates"""
    try:
        user_id = session.get('user_id')
        
        # Get search parameters
        search_query = request.args.get('q', '')
        skills = request.args.get('skills', '')
        experience = request.args.get('experience', '')
        location = request.args.get('location', '')
        
        candidates_data = {
            'candidates': [],  # Would fetch from jobseeker profiles
            'total_count': 0,
            'filters': {
                'skills': [],  # Would fetch from database
                'experience_levels': [],
                'locations': []
            },
            'search_params': {
                'query': search_query,
                'skills': skills,
                'experience': experience,
                'location': location
            }
        }
        
        return render_template('consultancy/candidates.html', **candidates_data)
        
    except Exception as e:
        flash(f'Error loading candidates: {str(e)}', 'error')
        return render_template('consultancy/candidates.html', candidates=[], total_count=0)

@consultancy_routes_bp.route('/company')
def company_profile():
    """Company profile management"""
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            flash('User not found', 'error')
            return redirect('/consultancy/dashboard')
        
        company_data = {
            'user': user,
            'company': {
                'name': 'Sample Company',  # Would fetch from company profile
                'industry': 'Technology',
                'size': '50-100 employees',
                'location': 'New York, NY',
                'website': 'https://example.com',
                'description': 'Leading technology company...'
            },
            'subscription': {
                'plan': 'Professional',
                'status': 'active',
                'jobs_remaining': 25,
                'expires_at': '2024-12-31'
            }
        }
        
        return render_template('consultancy/company.html', **company_data)
        
    except Exception as e:
        flash(f'Error loading company profile: {str(e)}', 'error')
        return redirect('/consultancy/dashboard')

@consultancy_routes_bp.route('/company/edit', methods=['GET', 'POST'])
def edit_company():
    """Edit company profile"""
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            flash('User not found', 'error')
            return redirect('/consultancy/dashboard')
        
        if request.method == 'POST':
            # Update company profile
            # Would update company table in database
            flash('Company profile updated successfully', 'success')
            return redirect('/consultancy/company')
        
        company_data = {
            'user': user,
            'company': {
                'name': 'Sample Company',
                'industry': 'Technology',
                'size': '50-100 employees',
                'location': 'New York, NY',
                'website': 'https://example.com',
                'description': 'Leading technology company...'
            }
        }
        
        return render_template('consultancy/edit_company.html', **company_data)
        
    except Exception as e:
        flash(f'Error updating company profile: {str(e)}', 'error')
        return redirect('/consultancy/company')

@consultancy_routes_bp.route('/analytics')
def analytics():
    """Recruitment analytics and reports"""
    try:
        user_id = session.get('user_id')
        
        analytics_data = {
            'hiring_funnel': {
                'applications': 156,
                'reviewed': 89,
                'interviewed': 34,
                'offered': 12,
                'hired': 8
            },
            'time_to_hire': {
                'average_days': 18,
                'median_days': 15,
                'fastest': 7,
                'slowest': 35
            },
            'source_performance': [
                {'source': 'JobMilgaya', 'applications': 78, 'hires': 5},
                {'source': 'LinkedIn', 'applications': 45, 'hires': 2},
                {'source': 'Direct', 'applications': 33, 'hires': 1}
            ],
            'monthly_trends': []  # Would fetch time-series data
        }
        
        return render_template('consultancy/analytics.html', **analytics_data)
        
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return render_template('consultancy/analytics.html', hiring_funnel={}, time_to_hire={})