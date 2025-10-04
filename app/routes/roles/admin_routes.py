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
    """Generate simple text-only menu based on user's actual permissions"""
    print(f"🔍 MENU DEBUG: Starting permission-based menu generation for {admin_user.username}")
    
    # Get all user permissions
    permissions = admin_user.get_permissions()
    permission_names = [perm.name for perm in permissions]
    print(f"🔍 MENU DEBUG: User has {len(permission_names)} permissions")
    
    menu_items = []
    
    # Dashboard (always present)
    menu_items.append({
        'text': 'Dashboard',
        'url': url_for('admin_routes.dashboard'),
        'active': request.endpoint == 'admin_routes.dashboard'
    })
    
    # User Management Section
    user_menu = []
    if 'user.read' in permission_names or 'user.list' in permission_names:
        user_menu.append({'text': 'View Users', 'url': url_for('admin_routes.users')})
    if 'user.create' in permission_names:
        user_menu.append({'text': 'Add User', 'url': '#'})  # Placeholder
    
    if user_menu:
        menu_items.append({
            'text': 'User Management',
            'submenu': user_menu
        })
    
    # Roles & Permissions Section
    role_menu = []
    if 'permission.read' in permission_names or 'permission.list' in permission_names:
        role_menu.append({'text': 'View Permissions', 'url': url_for('admin_routes.permissions')})
    if 'permission.create' in permission_names:
        role_menu.append({'text': 'Add Permission', 'url': '#'})  # Placeholder
    
    if role_menu:
        menu_items.append({
            'text': 'Roles & Permissions',
            'submenu': role_menu
        })
    
    # Job Management Section
    job_menu = []
    if 'job.read' in permission_names or 'job.list' in permission_names:
        job_menu.append({'text': 'View Jobs', 'url': url_for('admin_routes.jobs')})
    if 'job.create' in permission_names:
        job_menu.append({'text': 'Add Job', 'url': '#'})  # Placeholder
    
    if job_menu:
        menu_items.append({
            'text': 'Job Management',
            'submenu': job_menu
        })
    
    # Subscription Management Section
    subscription_menu = []
    if 'subscription.read' in permission_names or 'subscription.list' in permission_names:
        subscription_menu.append({'text': 'View Subscriptions', 'url': url_for('admin_routes.subscriptions')})
    if 'subscription.create' in permission_names:
        subscription_menu.append({'text': 'Add Subscription', 'url': '#'})  # Placeholder
    
    if subscription_menu:
        menu_items.append({
            'text': 'Subscription Management',
            'submenu': subscription_menu
        })
    
    # Master Data Section
    master_menu = []
    if 'industry.read' in permission_names or 'industry.list' in permission_names:
        master_menu.append({'text': 'Industries', 'url': '#'})  # Placeholder
    if 'skill.read' in permission_names or 'skill.list' in permission_names:
        master_menu.append({'text': 'Skills', 'url': '#'})  # Placeholder
    if 'country.read' in permission_names or 'country.list' in permission_names:
        master_menu.append({'text': 'Countries', 'url': '#'})  # Placeholder
    if 'city.read' in permission_names or 'city.list' in permission_names:
        master_menu.append({'text': 'Cities', 'url': '#'})  # Placeholder
    if 'job_role.read' in permission_names or 'job_role.list' in permission_names:
        master_menu.append({'text': 'Job Roles', 'url': '#'})  # Placeholder
    if 'company_type.read' in permission_names or 'company_type.list' in permission_names:
        master_menu.append({'text': 'Company Types', 'url': '#'})  # Placeholder
    if 'job_type.read' in permission_names or 'job_type.list' in permission_names:
        master_menu.append({'text': 'Job Types', 'url': '#'})  # Placeholder
    if 'experience.read' in permission_names or 'experience.list' in permission_names:
        master_menu.append({'text': 'Experience Levels', 'url': '#'})  # Placeholder
    if 'job_portal.read' in permission_names or 'job_portal.list' in permission_names:
        master_menu.append({'text': 'Job Portals', 'url': '#'})  # Placeholder
    
    if master_menu:
        menu_items.append({
            'text': 'Master Data',
            'submenu': master_menu
        })
    
    # System Section
    system_menu = []
    if 'system.maintenance' in permission_names:
        system_menu.append({'text': 'Maintenance', 'url': '#'})  # Placeholder
    if 'system.config' in permission_names:
        system_menu.append({'text': 'Configuration', 'url': '#'})  # Placeholder
    
    if system_menu:
        menu_items.append({
            'text': 'System',
            'submenu': system_menu
        })
    
    print(f"🔍 MENU DEBUG: Generated {len(menu_items)} menu sections")
    for item in menu_items:
        if 'submenu' in item:
            print(f"🔍 MENU DEBUG: - {item['text']} ({len(item['submenu'])} subitems)")
        else:
            print(f"🔍 MENU DEBUG: - {item['text']}")
    
    return menu_items
    
    # Skills - Admin has skill.read and skill.list permissions
    if admin_user.has_permission('skill.read') or admin_user.has_permission('skill.list'):
        master_data_submenu.append({
            'label': 'Skills',
            'icon': 'fas fa-cogs',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Skills management coming soon!")'
        })
    
    # Experience Levels - Admin has experience.read and experience.list permissions
    if admin_user.has_permission('experience.read') or admin_user.has_permission('experience.list'):
        master_data_submenu.append({
            'label': 'Experience Levels',
            'icon': 'fas fa-layer-group',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Experience Levels management coming soon!")'
        })
    
    # Job Roles - Admin has job_role.read and job_role.list permissions
    if admin_user.has_permission('job_role.read') or admin_user.has_permission('job_role.list'):
        master_data_submenu.append({
            'label': 'Job Roles',
            'icon': 'fas fa-user-tie',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Job Roles management coming soon!")'
        })
    
    # Company Types - Admin has company_type.read and company_type.list permissions
    if admin_user.has_permission('company_type.read') or admin_user.has_permission('company_type.list'):
        master_data_submenu.append({
            'label': 'Company Types',
            'icon': 'fas fa-building',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Company Types management coming soon!")'
        })
    
    # Job Types - Admin has job_type.read and job_type.list permissions
    if admin_user.has_permission('job_type.read') or admin_user.has_permission('job_type.list'):
        master_data_submenu.append({
            'label': 'Job Types',
            'icon': 'fas fa-briefcase',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Job Types management coming soon!")'
        })
    
    # Only add master data dropdown if user has access to at least one item
    if master_data_submenu:
        menu_items.append({
            'label': 'Master Data',
            'icon': 'fas fa-database',
            'dropdown': True,
            'submenu': master_data_submenu,
            'dropdown_id': 'masterDataDropdown'
        })
    
    # Location Management Section - Admin has these permissions
    location_submenu = []
    
    # Countries - Admin has country.read and country.list permissions
    if admin_user.has_permission('country.read') or admin_user.has_permission('country.list'):
        location_submenu.append({
            'label': 'Countries',
            'icon': 'fas fa-globe',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Countries management coming soon!")'
        })
    
    # Cities - Admin has city.read and city.list permissions
    if admin_user.has_permission('city.read') or admin_user.has_permission('city.list'):
        location_submenu.append({
            'label': 'Cities',
            'icon': 'fas fa-city',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Cities management coming soon!")'
        })
    
    # Only add location dropdown if user has access to at least one item
    if location_submenu:
        menu_items.append({
            'label': 'Locations',
            'icon': 'fas fa-map-marker-alt',
            'dropdown': True,
            'submenu': location_submenu,
            'dropdown_id': 'locationDropdown'
        })
    
    # Job Portals Management - Admin has job_portal.read and job_portal.list permissions
    if admin_user.has_permission('job_portal.read') or admin_user.has_permission('job_portal.list'):
        menu_items.append({
            'label': 'Job Portals',
            'icon': 'fas fa-external-link-alt',
            'route': '#',  # Placeholder until route is created
            'active': True,
            'has_permission': True,
            'onclick': 'alert("Job Portals management coming soon!")'
        })
    
    # Subscription Management
    if admin_user.has_permission('subscription.read'):
        menu_items.append({
            'label': 'Subscriptions',
            'icon': 'fas fa-credit-card',
            'route': 'admin_routes.subscriptions',
            'active': True,
            'has_permission': True
        })
    
    # System Management Section
    system_submenu = []
    
    # Security Logs
    if admin_user.has_permission('security.read'):
        system_submenu.append({
            'label': 'Security Logs',
            'icon': 'fas fa-shield-alt',
            'route': 'admin_routes.security',
            'active': True,
            'has_permission': True
        })
    
    # NOTE: These routes don't exist yet - commenting out to prevent errors
    # TODO: Create these routes in the future
    
    # # System Config (if needed)
    # if admin_user.has_permission('system.config'):
    #     system_submenu.append({
    #         'label': 'System Config',
    #         'icon': 'fas fa-cog',
    #         'route': 'admin_routes.system_config',
    #         'active': True,
    #         'has_permission': True
    #     })
    
    # # System Maintenance (if needed)
    # if admin_user.has_permission('system.maintenance'):
    #     system_submenu.append({
    #         'label': 'System Maintenance',
    #         'icon': 'fas fa-tools',
    #         'route': 'admin_routes.system_maintenance',
    #         'active': True,
    #         'has_permission': True
    #     })
    
    # Only add system dropdown if user has access to at least one item
    if system_submenu:
        menu_items.append({
            'label': 'System',
            'icon': 'fas fa-server',
            'dropdown': True,
            'submenu': system_submenu,
            'dropdown_id': 'systemDropdown'
        })
    
    print(f"🔍 MENU DEBUG: Final menu has {len(menu_items)} items:")
    for i, item in enumerate(menu_items):
        if 'dropdown' in item and item['dropdown']:
            print(f"🔍 MENU DEBUG:   {i+1}. {item['label']} (dropdown with {len(item.get('submenu', []))} items)")
        else:
            print(f"🔍 MENU DEBUG:   {i+1}. {item['label']} -> {item.get('route', 'no route')}")
    return menu_items

@admin_routes_bp.route('/debug-template')
def debug_template():
    """Debug route to check template selection"""
    layout_template = get_admin_layout()
    user_roles = g.current_user.get_roles() if hasattr(g, 'current_user') and g.current_user else []
    role_names = [role.name for role in user_roles]
    
    debug_info = {
        'selected_template': layout_template,
        'user_exists': hasattr(g, 'current_user') and g.current_user is not None,
        'user_roles': role_names,
        'has_admin_role': g.current_user.has_role('admin') if hasattr(g, 'current_user') and g.current_user else False,
        'has_superadmin_role': g.current_user.has_role('superadmin') if hasattr(g, 'current_user') and g.current_user else False
    }
    
    return f"""
    <h1>Template Debug Info</h1>
    <pre>{debug_info}</pre>
    <p><strong>Selected Template:</strong> {layout_template}</p>
    <p><strong>User Roles:</strong> {role_names}</p>
    <p><strong>Expected Template:</strong> layouts/admin_child.html (for admin role)</p>
    """

@admin_routes_bp.route('/dashboard')
def dashboard():
    """Admin dashboard with role-based content"""
    try:
        print("🔍 DASHBOARD DEBUG: Starting dashboard generation")
        
        # Get admin user
        admin_user = g.current_user
        print(f"🔍 DASHBOARD DEBUG: admin_user = {admin_user}")
        print(f"🔍 DASHBOARD DEBUG: admin_user roles = {admin_user.get_roles() if admin_user else 'None'}")
        
        # Get layout template
        layout_template = get_admin_layout()
        print(f"🔍 DASHBOARD DEBUG: layout_template = {layout_template}")
        
        # Get admin menu
        admin_menu = generate_admin_menu(admin_user)
        print(f"🔍 DASHBOARD DEBUG: admin_menu generated with {len(admin_menu)} items")
        
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
            'admin_menu': admin_menu,
            'user_permissions': [perm.name for perm in admin_user.get_permissions()],
            'page_title': 'Dashboard'
        }
        
        print(f"🔍 DASHBOARD DEBUG: About to render template: {layout_template}")
        print(f"🔍 DASHBOARD DEBUG: dashboard_data keys: {list(dashboard_data.keys())}")
        return render_template(layout_template, **dashboard_data)
        
    except Exception as e:
        print(f"🔍 DASHBOARD ERROR: {str(e)}")
        flash(f'Error loading dashboard: {str(e)}', 'error')
        # Get layout template even in error case
        error_layout = get_admin_layout()
        # Provide minimal data to prevent template errors
        return render_template(error_layout, 
                             stats={}, 
                             recent_activities=[], 
                             recent_users=[],
                             recent_jobs=[],
                             user_trend=[],
                             top_categories=[],
                             admin_menu=[],
                             user_permissions=[],
                             page_title='Dashboard - Error')

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