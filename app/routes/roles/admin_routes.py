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

print("🚀 ADMIN ROUTES BLUEPRINT LOADED SUCCESSFULLY!")
print(f"🚀 Blueprint name: {admin_routes_bp.name}")
print(f"🚀 Blueprint url_prefix: {admin_routes_bp.url_prefix}")

def get_admin_layout():
    """Determine which layout to use based on user role"""
    print(f"DEBUG get_admin_layout: hasattr(g, 'current_user') = {hasattr(g, 'current_user')}")
    if hasattr(g, 'current_user') and g.current_user:
        print(f"DEBUG get_admin_layout: current_user exists")
        print(f"DEBUG get_admin_layout: user roles = {g.current_user.get_roles()}")
        if g.current_user.has_role('superadmin'):
            print(f"DEBUG get_admin_layout: returning admin_layout.html for superadmin")
            return 'layouts/admin_layout.html'
        elif g.current_user.has_role('admin'):
            print(f"DEBUG get_admin_layout: returning admin_child.html for admin")
            return 'layouts/admin_child.html'
    print(f"DEBUG get_admin_layout: returning default admin_layout.html")
    return 'layouts/admin_layout.html'  # Default fallback

@admin_routes_bp.before_request
def require_admin_auth():
    """Require admin authentication and load permissions"""
    print(f"🔐 BEFORE_REQUEST DEBUG: request.endpoint = {request.endpoint}")
    print(f"🔐 BEFORE_REQUEST DEBUG: request.path = {request.path}")
    print(f"🔐 BEFORE_REQUEST DEBUG: request.url = {request.url}")
    
    # Skip auth check for login page
    if request.endpoint and 'login' in request.endpoint:
        print("🔐 BEFORE_REQUEST: Skipping auth for login page")
        return
    
    # Check if user is authenticated
    print(f"🔐 BEFORE_REQUEST: hasattr(g, 'current_user') = {hasattr(g, 'current_user')}")
    if hasattr(g, 'current_user') and g.current_user:
        print(f"🔐 BEFORE_REQUEST: current_user exists = {g.current_user}")
        print(f"🔐 BEFORE_REQUEST: user roles = {g.current_user.get_roles()}")
    
    if not hasattr(g, 'current_user') or not g.current_user:
        # No user is logged in, redirect to admin login
        print("🔐 BEFORE_REQUEST: No user logged in, redirecting to login")
        return redirect('/admin/auth/login')
    
    # Check if user has admin or superadmin role  
    if not (g.current_user.has_role('admin') or g.current_user.has_role('superadmin')):
        print("🔐 BEFORE_REQUEST: User lacks admin privileges, redirecting to login")
        flash('Access denied. Admin privileges required.', 'error')
        return redirect('/admin/auth/login')
    
    print("🔐 BEFORE_REQUEST: Authentication successful")
    # Load user permissions for menu generation
    g.user_permissions = g.current_user.get_permissions()
    g.admin_menu = generate_admin_menu(g.current_user)
    print("🔐 BEFORE_REQUEST: Permissions and menu loaded")

def generate_admin_menu(admin_user):
    """Generate admin menu based on user permissions"""
    menu_items = []
    
    # Dashboard is always available for admin users
    menu_items.append({
        'label': 'Dashboard',
        'icon': 'fas fa-chart-pie',
        'route': 'admin_routes.dashboard',
        'active': True,
        'has_permission': True
    })
    
    # Users menu - check for user management permissions
    if admin_user.has_permission('user.read') or admin_user.has_permission('user.list'):
        menu_items.append({
            'label': 'Manage Users',
            'icon': 'fas fa-user-shield',
            'route': 'admin_routes.users',
            'active': True,
            'has_permission': True
        })
    else:
        menu_items.append({
            'label': 'Manage Users',
            'icon': 'fas fa-user-shield',
            'route': 'admin_routes.users',
            'active': False,
            'has_permission': False,
            'disabled_reason': 'You do not have permission to manage users'
        })
    
    # Roles & Permissions dropdown
    roles_submenu = []
    
    # Roles
    if admin_user.has_permission('role.read'):
        roles_submenu.append({
            'label': 'Manage Roles',
            'icon': 'fas fa-shield-alt',
            'route': 'admin_routes.roles',
            'active': True,
            'has_permission': True
        })
    else:
        roles_submenu.append({
            'label': 'Manage Roles',
            'icon': 'fas fa-shield-alt',
            'route': 'admin_routes.roles',
            'active': False,
            'has_permission': False,
            'disabled_reason': 'You do not have permission to manage roles'
        })
    
    # Permissions
    if admin_user.has_permission('permission.read'):
        roles_submenu.append({
            'label': 'Manage Permissions',
            'icon': 'fas fa-key',
            'route': 'admin_routes.permissions',
            'active': True,
            'has_permission': True
        })
    else:
        roles_submenu.append({
            'label': 'Manage Permissions',
            'icon': 'fas fa-key',
            'route': 'admin_routes.permissions',
            'active': False,
            'has_permission': False,
            'disabled_reason': 'You do not have permission to manage permissions'
        })
    
    menu_items.append({
        'label': 'Roles & Permissions',
        'icon': 'fas fa-user-tag',
        'dropdown': True,
        'submenu': roles_submenu,
        'dropdown_id': 'rolesDropdown'
    })
    
    # Jobs menu
    if admin_user.has_permission('job.list') or admin_user.has_permission('job.read'):
        menu_items.append({
            'label': 'Job Management',
            'icon': 'fas fa-briefcase',
            'route': 'admin_routes.jobs',
            'active': True,
            'has_permission': True
        })
    else:
        menu_items.append({
            'label': 'Job Management',
            'icon': 'fas fa-briefcase',
            'route': 'admin_routes.jobs',
            'active': False,
            'has_permission': False,
            'disabled_reason': 'You do not have permission to manage jobs'
        })
    
    # Security Logs
    if admin_user.has_permission('security.read'):
        menu_items.append({
            'label': 'Security Logs',
            'icon': 'fas fa-shield-alt',
            'route': 'admin_routes.security',
            'active': True,
            'has_permission': True
        })
    else:
        menu_items.append({
            'label': 'Security Logs',
            'icon': 'fas fa-shield-alt',
            'route': 'admin_routes.security',
            'active': False,
            'has_permission': False,
            'disabled_reason': 'You do not have permission to view security logs'
        })
    
    # Subscription Management - Add this for admin users with subscription.read permission
    if admin_user.has_permission('subscription.read'):
        menu_items.append({
            'label': 'Subscriptions',
            'icon': 'fas fa-credit-card',
            'route': 'admin_routes.subscriptions',
            'active': True,
            'has_permission': True
        })
    else:
        menu_items.append({
            'label': 'Subscriptions',
            'icon': 'fas fa-credit-card',
            'route': 'admin_routes.subscriptions',
            'active': False,
            'has_permission': False,
            'disabled_reason': 'You do not have permission to view subscriptions'
        })
    
    # Analytics menu removed - not required for admin role
    # Previously was showing analytics for all admin users
    
    return menu_items

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
        else:
            stats['total_users'] = 0
            stats['active_users'] = 0
        
        if admin_user.has_permission('job.read'):
            stats['total_jobs'] = 0  # Would fetch from jobs table
            stats['active_jobs'] = 0
        else:
            stats['total_jobs'] = 0
            stats['active_jobs'] = 0
        
        if admin_user.has_permission('subscription.read'):
            stats['total_subscriptions'] = 0  # Would fetch from subscriptions
            stats['active_subscriptions'] = 0
        else:
            stats['total_subscriptions'] = 0
            stats['active_subscriptions'] = 0
        
        if admin_user.has_permission('security.read'):
            stats['security_events_today'] = 0  # Would fetch from security logs
        else:
            stats['security_events_today'] = 0
        
        # Provide default data for template
        dashboard_data = {
            'admin_user': admin_user,
            'stats': stats,
            'recent_activities': [],  # Would fetch based on permissions
            'recent_users': [],  # Recent users if permitted
            'recent_jobs': [],   # Recent jobs if permitted
            'user_trend': [],    # User registration trend data
            'top_categories': [], # Top job categories
            'admin_menu': g.admin_menu,
            'user_permissions': [perm.name for perm in g.user_permissions],
            'layout_template': get_admin_layout()
        }
        
        print(f"DEBUG Dashboard: layout_template = {dashboard_data['layout_template']}")
        return render_template('admin/dashboard.html', **dashboard_data)
        
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        # Provide minimal data to prevent template errors
        return render_template('admin/dashboard.html', 
                             stats={}, 
                             recent_activities=[], 
                             recent_users=[],
                             recent_jobs=[],
                             user_trend=[],
                             top_categories=[],
                             admin_menu=getattr(g, 'admin_menu', []),
                             user_permissions=[])

@admin_routes_bp.route('/users')
def users():
    """User management with permission checks"""
    print("="*70)
    print("🔍 DEBUG ADMIN USERS ROUTE CALLED")
    print("="*70)
    print(f"DEBUG: hasattr(g, 'current_user') = {hasattr(g, 'current_user')}")
    if hasattr(g, 'current_user') and g.current_user:
        print(f"DEBUG: g.current_user exists = {g.current_user}")
        print(f"DEBUG: g.current_user.id = {g.current_user.id}")
        print(f"DEBUG: g.current_user.username = {g.current_user.username}")
        print(f"DEBUG: g.current_user.get_roles() = {g.current_user.get_roles()}")
        print(f"DEBUG: g.current_user.has_role('admin') = {g.current_user.has_role('admin')}")
        print(f"DEBUG: g.current_user.has_role('superadmin') = {g.current_user.has_role('superadmin')}")
    else:
        print("DEBUG: g.current_user is None or not set!")
    
    layout_template = get_admin_layout()
    print(f"DEBUG: get_admin_layout() returned = '{layout_template}'")
    print("="*70)
    
    try:
        # Check if user has permission to view users
        if not (g.current_user.has_permission('user.read') or g.current_user.has_permission('user.list')):
            flash('You do not have permission to view users', 'error')
            return redirect('/admin/dashboard')
        
        # Get users based on admin level
        if g.current_user.has_role('superadmin'):
            users = AuthUser.query.all()
        else:
            # Regular admin can only see non-admin users (jobseeker and consultancy roles)
            from app.auth.auth_models import UserRole
            try:
                users = AuthUser.query.join(
                    UserRole, AuthUser.id == UserRole.user_id
                ).join(
                    Role, UserRole.role_id == Role.id
                ).filter(
                    Role.name.in_(['jobseeker', 'consultancy']),
                    UserRole.is_active == True
                ).distinct().all()
            except Exception as query_error:
                users = []
        
        users_data = {
            'users': users,
            'can_create': g.current_user.has_permission('user.create'),
            'can_edit': g.current_user.has_permission('user.update'),
            'can_delete': g.current_user.has_permission('user.delete'),
            'admin_menu': g.admin_menu,
            'layout_template': layout_template  # Use the variable we already fetched
        }
        
        print(f"🚨 FINAL DEBUG Users: layout_template = '{users_data['layout_template']}'")
        print(f"🚨 FINAL DEBUG Users: current_user role = {g.current_user.get_roles() if g.current_user else 'No user'}")
        print("="*70)
        return render_template('admin/users.html', **users_data)
        
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/users/<int:user_id>')
def user_view(user_id):
    """View individual user details"""
    try:
        if not g.current_user.has_permission('user.read'):
            flash('You do not have permission to view user details', 'error')
            return redirect('/admin/users')
        
        user = AuthUser.query.get_or_404(user_id)
        
        # Check if admin can view this user
        if not g.current_user.has_role('superadmin'):
            # Regular admin can only view non-admin users
            user_roles = [role.name for role in user.get_roles()]
            if any(role in ['admin', 'superadmin'] for role in user_roles):
                flash('You do not have permission to view this user', 'error')
                return redirect('/admin/users')
        
        user_data = {
            'user': user,
            'user_roles': user.get_roles(),
            'user_permissions': user.get_permissions(),
            'can_edit': g.current_user.has_permission('user.update'),
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/user_detail.html', **user_data)
        
    except Exception as e:
        flash(f'Error loading user details: {str(e)}', 'error')
        return redirect('/admin/users')

@admin_routes_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    """Edit user details"""
    try:
        if not g.current_user.has_permission('user.update'):
            flash('You do not have permission to edit users', 'error')
            return redirect('/admin/users')
        
        user = AuthUser.query.get_or_404(user_id)
        
        # Check if admin can edit this user
        if not g.current_user.has_role('superadmin'):
            # Regular admin can only edit non-admin users
            user_roles = [role.name for role in user.get_roles()]
            if any(role in ['admin', 'superadmin'] for role in user_roles):
                flash('You do not have permission to edit this user', 'error')
                return redirect('/admin/users')
        
        if request.method == 'POST':
            # Handle form submission
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.email = request.form.get('email')
            user.phone = request.form.get('phone')
            user.is_active = bool(request.form.get('is_active'))
            
            try:
                db.session.commit()
                flash('User updated successfully', 'success')
                return redirect(url_for('admin_routes.user_view', user_id=user.id))
            except Exception as save_error:
                db.session.rollback()
                flash(f'Error updating user: {str(save_error)}', 'error')
        
        user_data = {
            'user': user,
            'user_roles': user.get_roles(),
            'available_roles': Role.query.filter(Role.name.in_(['jobseeker', 'consultancy'])).all() if not g.current_user.has_role('superadmin') else Role.query.all(),
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/user_edit.html', **user_data)
        
    except Exception as e:
        flash(f'Error editing user: {str(e)}', 'error')
        return redirect('/admin/users')

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
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/roles.html', **roles_data)
        
    except Exception as e:
        flash(f'Error loading roles: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/roles/<int:role_id>')
def role_view(role_id):
    """View individual role details"""
    try:
        if not g.current_user.has_permission('role.read'):
            flash('You do not have permission to view role details', 'error')
            return redirect('/admin/roles')
        
        role = Role.query.get_or_404(role_id)
        
        role_data = {
            'role': role,
            'role_permissions': role.get_permissions() if hasattr(role, 'get_permissions') else [],
            'can_edit': g.current_user.has_permission('role.update'),
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/role_detail.html', **role_data)
        
    except Exception as e:
        flash(f'Error loading role details: {str(e)}', 'error')
        return redirect('/admin/roles')

@admin_routes_bp.route('/roles/<int:role_id>/edit', methods=['GET', 'POST'])
def role_edit(role_id):
    """Edit role details"""
    try:
        if not g.current_user.has_permission('role.update'):
            flash('You do not have permission to edit roles', 'error')
            return redirect('/admin/roles')
        
        role = Role.query.get_or_404(role_id)
        
        # Prevent editing system roles
        if role.is_system_role:
            flash('System roles cannot be modified', 'error')
            return redirect(url_for('admin_routes.role_view', role_id=role.id))
        
        if request.method == 'POST':
            # Handle form submission
            role.display_name = request.form.get('display_name')
            role.description = request.form.get('description')
            
            try:
                db.session.commit()
                flash('Role updated successfully', 'success')
                return redirect(url_for('admin_routes.role_view', role_id=role.id))
            except Exception as save_error:
                db.session.rollback()
                flash(f'Error updating role: {str(save_error)}', 'error')
        
        role_data = {
            'role': role,
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/role_edit.html', **role_data)
        
    except Exception as e:
        flash(f'Error editing role: {str(e)}', 'error')
        return redirect('/admin/roles')

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
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
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
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
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
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/security.html', **security_data)
        
    except Exception as e:
        flash(f'Error loading security logs: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/subscriptions')
def subscriptions():
    """Subscription management"""
    try:
        if not g.current_user.has_permission('subscription.read'):
            flash('You do not have permission to view subscriptions', 'error')
            return redirect('/admin/dashboard')
        
        # Import subscription models
        try:
            from app.auth.auth_models import SubscriptionPlan
            from app.auth.auth_models import UserSubscription
            
            # Get subscription plans and user subscriptions
            subscription_plans = SubscriptionPlan.query.all()
            user_subscriptions = UserSubscription.query.all() if hasattr(UserSubscription, 'query') else []
            
            # Calculate statistics
            subscription_stats = {
                'total_plans': len(subscription_plans),
                'active_subscriptions': len([s for s in user_subscriptions if getattr(s, 'is_active', False)]),
                'total_revenue': sum([getattr(s, 'amount', 0) for s in user_subscriptions]),
                'most_popular_plan': 'Standard' if subscription_plans else 'None'
            }
            
        except ImportError:
            # Fallback if subscription models don't exist
            subscription_plans = []
            user_subscriptions = []
            subscription_stats = {
                'total_plans': 0,
                'active_subscriptions': 0,
                'total_revenue': 0,
                'most_popular_plan': 'None'
            }
        
        subscription_data = {
            'subscription_plans': subscription_plans,
            'user_subscriptions': user_subscriptions,
            'stats': subscription_stats,
            'can_create': g.current_user.has_permission('subscription.create'),
            'can_edit': g.current_user.has_permission('subscription.update'),
            'can_delete': g.current_user.has_permission('subscription.delete'),
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/subscriptions.html', **subscription_data)
        
    except Exception as e:
        flash(f'Error loading subscriptions: {str(e)}', 'error')
        return redirect('/admin/dashboard')

@admin_routes_bp.route('/analytics')
def analytics():
    """System analytics"""
    try:
        analytics_data = {
            'user_growth': [],  # Would fetch time-series data
            'job_stats': {},
            'popular_categories': [],
            'admin_menu': g.admin_menu,
            'layout_template': get_admin_layout()
        }
        
        return render_template('admin/analytics.html', **analytics_data)
        
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return redirect('/admin/dashboard')