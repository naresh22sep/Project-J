"""
Admin Routes - Role-based functionality for admin users
Handles auth_users table with role-based permissions
Dynamic menu generation based on database permissions
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.middleware.security_middleware import AuthMiddleware
from app.auth.auth_models import AuthUser, Role, Permission  # Using AuthUser for admins
from app import db

# Create blueprint
admin_routes_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

@admin_routes_bp.before_request
def require_admin_auth():
    """Require admin authentication and load permissions"""
    # Skip auth check for login page
    if request.endpoint and 'login' in request.endpoint:
        return
    
    # Check if user is authenticated
    if not hasattr(g, 'current_user') or not g.current_user:
        # No user is logged in, redirect to admin login
        return redirect('/admin/auth/login')
    
    # Check if user has admin or superadmin role  
    if not (g.current_user.has_role('admin') or g.current_user.has_role('superadmin')):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect('/admin/auth/login')
    
    # Load user permissions for menu generation
    g.user_permissions = g.current_user.get_permissions()
    g.admin_menu = generate_admin_menu(g.user_permissions)

def generate_admin_menu(permissions):
    """Generate dynamic admin menu based on user permissions"""
    menu = []
    permission_names = [perm.name for perm in permissions]
    
    # Dashboard (always available)
    menu.append({
        'label': 'Dashboard',
        'icon': 'fas fa-tachometer-alt',
        'url': '/admin/dashboard',
        'active': request.endpoint == 'admin_routes.dashboard'
    })
    
    # User Management
    if any(perm in permission_names for perm in ['user.read', 'user.list', 'user.create']):
        user_submenu = []
        if 'user.list' in permission_names:
            user_submenu.append({'label': 'All Users', 'url': '/admin/users'})
        if 'user.create' in permission_names:
            user_submenu.append({'label': 'Add User', 'url': '/admin/users/create'})
        
        menu.append({
            'label': 'User Management',
            'icon': 'fas fa-users',
            'submenu': user_submenu,
            'has_access': True
        })
    
    # Role & Permission Management
    if any(perm in permission_names for perm in ['role.read', 'permission.read']):
        role_submenu = []
        if 'role.read' in permission_names:
            role_submenu.append({'label': 'Roles', 'url': '/admin/roles'})
        if 'permission.read' in permission_names:
            role_submenu.append({'label': 'Permissions', 'url': '/admin/permissions'})
        
        menu.append({
            'label': 'Access Control',
            'icon': 'fas fa-shield-alt',
            'submenu': role_submenu,
            'has_access': True
        })
    
    # Job Management
    if any(perm in permission_names for perm in ['job.read', 'job.list', 'job.create']):
        job_submenu = []
        if 'job.list' in permission_names:
            job_submenu.append({'label': 'All Jobs', 'url': '/admin/jobs'})
        if 'job.create' in permission_names:
            job_submenu.append({'label': 'Create Job', 'url': '/admin/jobs/create'})
        
        menu.append({
            'label': 'Job Management',
            'icon': 'fas fa-briefcase',
            'submenu': job_submenu,
            'has_access': True
        })
    
    # Company Management
    if any(perm in permission_names for perm in ['company.read', 'company.list']):
        menu.append({
            'label': 'Companies',
            'icon': 'fas fa-building',
            'url': '/admin/companies',
            'active': request.endpoint == 'admin_routes.companies'
        })
    
    # Subscription Management
    if any(perm in permission_names for perm in ['subscription.read', 'subscription.list']):
        menu.append({
            'label': 'Subscriptions',
            'icon': 'fas fa-credit-card',
            'url': '/admin/subscriptions',
            'active': request.endpoint == 'admin_routes.subscriptions'
        })
    
    # System Settings (for higher-level admins)
    if any(perm in permission_names for perm in ['system.config', 'system.maintenance']):
        system_submenu = []
        if 'system.config' in permission_names:
            system_submenu.append({'label': 'Configuration', 'url': '/admin/settings'})
        if 'system.maintenance' in permission_names:
            system_submenu.append({'label': 'Maintenance', 'url': '/admin/maintenance'})
        
        menu.append({
            'label': 'System',
            'icon': 'fas fa-cogs',
            'submenu': system_submenu,
            'has_access': True
        })
    
    # Reports & Analytics
    if any(perm in permission_names for perm in ['security.read', 'system.config']):
        reports_submenu = []
        if 'security.read' in permission_names:
            reports_submenu.append({'label': 'Security Logs', 'url': '/admin/security'})
        reports_submenu.append({'label': 'Analytics', 'url': '/admin/analytics'})
        
        menu.append({
            'label': 'Reports',
            'icon': 'fas fa-chart-bar',
            'submenu': reports_submenu,
            'has_access': True
        })
    
    return menu

@admin_routes_bp.route('/dashboard')
def dashboard():
    """Admin dashboard with role-based content"""
    try:
        # Get admin user
        admin_user = g.current_user
        
        # Get dashboard statistics based on permissions
        stats = {}
        
        # Only show stats the admin has permission to see
        if admin_user.has_permission('user.read'):
            stats['total_users'] = AuthUser.query.count()
            stats['active_users'] = AuthUser.query.filter_by(is_active=True).count()
        
        if admin_user.has_permission('job.read'):
            stats['total_jobs'] = 0  # Would fetch from jobs table
            stats['active_jobs'] = 0
        
        if admin_user.has_permission('subscription.read'):
            stats['total_subscriptions'] = 0  # Would fetch from subscriptions
            stats['active_subscriptions'] = 0
        
        if admin_user.has_permission('security.read'):
            stats['security_events_today'] = 0  # Would fetch from security logs
        
        dashboard_data = {
            'admin_user': admin_user,
            'stats': stats,
            'recent_activities': [],  # Would fetch based on permissions
            'admin_menu': g.admin_menu,
            'user_permissions': [perm.name for perm in g.user_permissions]
        }
        
        return render_template('admin/dashboard.html', **dashboard_data)
        
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('admin/dashboard.html', 
                             stats={}, recent_activities=[], admin_menu=[])

@admin_routes_bp.route('/users')
def users():
    """User management with permission checks"""
    try:
        if not g.current_user.has_permission('user.list'):
            flash('You do not have permission to view users', 'error')
            return redirect('/admin/dashboard')
        
        # Get users based on admin level
        if g.current_user.has_role('superadmin'):
            users = AuthUser.query.all()
        else:
            # Regular admin can only see non-admin users
            users = AuthUser.query.join(AuthUser.user_roles).join(Role).filter(
                Role.name.in_(['jobseeker', 'consultancy'])
            ).all()
        
        users_data = {
            'users': users,
            'can_create': g.current_user.has_permission('user.create'),
            'can_edit': g.current_user.has_permission('user.update'),
            'can_delete': g.current_user.has_permission('user.delete'),
            'admin_menu': g.admin_menu
        }
        
        return render_template('admin/users.html', **users_data)
        
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/roles')
def roles():
    """Role management with permission checks"""
    try:
        if not g.current_user.has_permission('role.read'):
            flash('You do not have permission to view roles', 'error')
            return redirect('/admin/dashboard')
        
        roles = Role.query.all()
        
        roles_data = {
            'roles': roles,
            'can_create': g.current_user.has_permission('role.create'),
            'can_edit': g.current_user.has_permission('role.update'),
            'can_delete': g.current_user.has_permission('role.delete'),
            'admin_menu': g.admin_menu
        }
        
        return render_template('admin/roles.html', **roles_data)
        
    except Exception as e:
        flash(f'Error loading roles: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/permissions')
def permissions():
    """Permission management"""
    try:
        if not g.current_user.has_permission('permission.read'):
            flash('You do not have permission to view permissions', 'error')
            return redirect('/admin/dashboard')
        
        permissions = Permission.query.all()
        
        permissions_data = {
            'permissions': permissions,
            'can_create': g.current_user.has_permission('permission.create'),
            'can_edit': g.current_user.has_permission('permission.update'),
            'can_delete': g.current_user.has_permission('permission.delete'),
            'admin_menu': g.admin_menu
        }
        
        return render_template('admin/permissions.html', **permissions_data)
        
    except Exception as e:
        flash(f'Error loading permissions: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/jobs')
def jobs():
    """Job management (if permitted)"""
    try:
        if not g.current_user.has_permission('job.list'):
            flash('You do not have permission to view jobs', 'error')
            return redirect('/admin/dashboard')
        
        jobs_data = {
            'jobs': [],  # Would fetch from jobs table
            'stats': {
                'total': 0,
                'active': 0,
                'expired': 0
            },
            'can_create': g.current_user.has_permission('job.create'),
            'can_edit': g.current_user.has_permission('job.update'),
            'can_delete': g.current_user.has_permission('job.delete'),
            'admin_menu': g.admin_menu
        }
        
        return render_template('admin/jobs.html', **jobs_data)
        
    except Exception as e:
        flash(f'Error loading jobs: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/security')
def security():
    """Security logs (if permitted)"""
    try:
        if not g.current_user.has_permission('security.read'):
            flash('You do not have permission to view security logs', 'error')
            return redirect('/admin/dashboard')
        
        from app.auth.auth_models import SecurityLog
        
        # Get recent security events
        security_logs = SecurityLog.query.order_by(
            SecurityLog.created_at.desc()
        ).limit(100).all()
        
        security_data = {
            'security_logs': security_logs,
            'stats': {
                'total_events': SecurityLog.query.count(),
                'high_severity': SecurityLog.query.filter_by(severity='high').count(),
                'today_events': SecurityLog.query.filter(
                    SecurityLog.created_at >= db.func.current_date()
                ).count()
            },
            'admin_menu': g.admin_menu
        }
        
        return render_template('admin/security.html', **security_data)
        
    except Exception as e:
        flash(f'Error loading security logs: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/analytics')
def analytics():
    """System analytics"""
    try:
        analytics_data = {
            'user_growth': [],  # Would fetch time-series data
            'job_stats': {},
            'popular_categories': [],
            'admin_menu': g.admin_menu
        }
        
        return render_template('admin/analytics.html', **analytics_data)
        
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return redirect('/admin/dashboard')