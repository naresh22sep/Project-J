"""
SuperAdmin Routes - ACL and Subscription Management
Minimalist admin interface with comprehensive controls
"""

from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, g
from app.services.auth_service import (
    JWTAuthService, SecurityService, AuthorizationService,
    jwt_required, require_role, require_permission, csrf_protect
)
from app.middleware.security_middleware import AuthMiddleware
from app.auth.auth_models import (
    AuthUser, Role, Permission, SubscriptionPlan, UserSubscription, SubscriptionFeature,
    SecurityLog, SecurityEventType, SubscriptionStatus, UserRole, JobPortal, UserPortalAccess
)
from app.models import (
    IndustryType, Skill, Experience, JobRole, CompanyType, JobType, Country, State, City
)
from app import db
from datetime import datetime, timedelta
import json

# Create blueprint
superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')

# Apply superadmin middleware to all routes
@superadmin_bp.before_request
def require_superadmin():
    """Require superadmin role for all routes in this blueprint"""
    result = AuthMiddleware.superadmin_only()
    if result:
        return result

# Dashboard Routes
@superadmin_bp.route('/')
@superadmin_bp.route('/dashboard')
def dashboard():
    """SuperAdmin dashboard with key metrics"""
    try:
        # Get key statistics
        stats = {
            'total_users': AuthUser.query.count(),
            'active_users': AuthUser.query.filter_by(is_active=True).count(),
            'total_subscriptions': UserSubscription.query.count(),
            'active_subscriptions': UserSubscription.query.filter_by(
                status=SubscriptionStatus.ACTIVE.value
            ).count(),
            'security_events_today': SecurityLog.query.filter(
                SecurityLog.created_at >= datetime.utcnow().date()
            ).count(),
            'high_severity_events': SecurityLog.query.filter_by(severity='high').count()
        }
        
        # Recent security events
        recent_events = SecurityLog.query.order_by(
            SecurityLog.created_at.desc()
        ).limit(10).all()
        
        # Subscription breakdown
        subscription_stats = db.session.query(
            SubscriptionPlan.name,
            db.func.count(UserSubscription.id).label('count')
        ).join(UserSubscription).group_by(SubscriptionPlan.name).all()
        
        return render_template('superadmin/dashboard.html', 
                             stats=stats, 
                             recent_events=recent_events,
                             subscription_stats=subscription_stats)
    
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('superadmin/dashboard.html', 
                             stats={}, recent_events=[], subscription_stats=[])

# User Management
@superadmin_bp.route('/users')
def users():
    """List all users with management options"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    
    query = AuthUser.query
    
    # Apply search filter
    if search:
        query = query.filter(
            (AuthUser.username.contains(search)) |
            (AuthUser.email.contains(search)) |
            (AuthUser.first_name.contains(search)) |
            (AuthUser.last_name.contains(search))
        )
    
    # Apply role filter
    if role_filter:
        query = query.join(AuthUser.roles).filter(Role.name == role_filter)
    
    users = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get all roles for filter dropdown
    roles = Role.query.all()
    
    return render_template('superadmin/users.html', 
                         users=users, roles=roles, 
                         search=search, role_filter=role_filter)

@superadmin_bp.route('/users/add', methods=['GET', 'POST'])
# @csrf_protect  # Temporarily disabled for testing
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        try:
            # Validate required fields
            username = SecurityService.sanitize_input(request.form.get('username', ''))
            email = SecurityService.sanitize_input(request.form.get('email', ''))
            first_name = SecurityService.sanitize_input(request.form.get('first_name', ''))
            last_name = SecurityService.sanitize_input(request.form.get('last_name', ''))
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validation
            if not all([username, email, first_name, last_name, password]):
                flash('All required fields must be filled', 'error')
                return render_template('superadmin/add_user.html', roles=Role.query.all())
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('superadmin/add_user.html', roles=Role.query.all())
            
            if len(password) < 8:
                flash('Password must be at least 8 characters long', 'error')
                return render_template('superadmin/add_user.html', roles=Role.query.all())
            
            # Check if username or email already exists
            existing_user = AuthUser.query.filter(
                (AuthUser.username == username) | (AuthUser.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    flash('Username already exists', 'error')
                else:
                    flash('Email already exists', 'error')
                return render_template('superadmin/add_user.html', roles=Role.query.all())
            
            # Create new user
            user = AuthUser(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=SecurityService.sanitize_input(request.form.get('phone', '')),
                is_active='is_active' in request.form,
                email_verified='email_verified' in request.form,
                two_factor_enabled='two_factor_enabled' in request.form
            )
            
            # Set password
            user.set_password(password)
            
            # Generate UUID
            import uuid as uuid_module
            user.uuid = str(uuid_module.uuid4())
            
            db.session.add(user)
            db.session.flush()  # Get the user ID
            
            # Assign roles
            selected_role_ids = request.form.getlist('roles')
            if selected_role_ids:
                for role_id in selected_role_ids:
                    role = Role.query.get(role_id)
                    if role:
                        user_role = UserRole(user_id=user.id, role_id=role.id, is_active=True)
                        db.session.add(user_role)
            else:
                # Assign default jobseeker role if no roles selected
                default_role = Role.query.filter_by(name='jobseeker').first()
                if default_role:
                    user_role = UserRole(user_id=user.id, role_id=default_role.id, is_active=True)
                    db.session.add(user_role)
            
            db.session.commit()
            
            # Log the creation
            SecurityLog.log_security_event(
                SecurityEventType.USER_REGISTERED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'created_user_id': user.id,
                    'created_username': user.username,
                    'created_email': user.email,
                    'assigned_roles': selected_role_ids,
                    'created_by_admin': True
                },
                severity='medium'
            )
            
            flash(f'User {username} created successfully', 'success')
            return redirect(url_for('superadmin.user_detail', user_id=user.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
    
    roles = Role.query.all()
    return render_template('superadmin/add_user.html', roles=roles)

@superadmin_bp.route('/users/<int:user_id>')
def user_detail(user_id):
    """View user details and permissions"""
    user = AuthUser.query.get_or_404(user_id)
    
    # Get user's subscription
    subscription = user.get_active_subscription()
    
    # Get user's recent activity
    recent_activity = SecurityLog.query.filter_by(user_id=user_id).order_by(
        SecurityLog.created_at.desc()
    ).limit(20).all()
    
    # Get user statistics (mock data for now)
    user_stats = {
        'jobs_posted': 0,  # Would be calculated from database
        'applications_submitted': 0,  # Would be calculated from database
        'profile_views': 0,  # Would be calculated from database
        'total_logins': SecurityLog.query.filter_by(
            user_id=user_id, 
            event_type=SecurityEventType.LOGIN_SUCCESS.value
        ).count()
    }
    
    return render_template('superadmin/user_detail.html', 
                         user=user, subscription=subscription, 
                         recent_activity=recent_activity,
                         user_stats=user_stats)

@superadmin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@csrf_protect
def edit_user(user_id):
    """Edit user details and roles"""
    user = AuthUser.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            # Update basic info
            user.username = SecurityService.sanitize_input(request.form.get('username', ''))
            user.first_name = SecurityService.sanitize_input(request.form.get('first_name', ''))
            user.last_name = SecurityService.sanitize_input(request.form.get('last_name', ''))
            user.email = SecurityService.sanitize_input(request.form.get('email', ''))
            user.phone = SecurityService.sanitize_input(request.form.get('phone', ''))
            user.is_active = 'is_active' in request.form
            user.email_verified = 'email_verified' in request.form
            user.two_factor_enabled = 'two_factor_enabled' in request.form
            
            # Update login attempts
            login_attempts = request.form.get('login_attempts', type=int)
            if login_attempts is not None:
                user.login_attempts = max(0, min(10, login_attempts))
            
            # Handle password update
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if new_password:
                if new_password != confirm_password:
                    flash('Passwords do not match', 'error')
                    return render_template('superadmin/edit_user.html', user=user, roles=Role.query.all())
                
                if len(new_password) < 8:
                    flash('Password must be at least 8 characters long', 'error')
                    return render_template('superadmin/edit_user.html', user=user, roles=Role.query.all())
                
                user.set_password(new_password)
                
                # Clear reset token if requested
                if 'clear_reset_token' in request.form:
                    user.password_reset_token = None
                    user.password_reset_expires = None
            
            # Update roles
            selected_role_ids = request.form.getlist('roles')
            if selected_role_ids:
                # Clear existing roles
                existing_user_roles = user.user_roles.all()
                for user_role in existing_user_roles:
                    db.session.delete(user_role)
                
                # Add new roles
                for role_id in selected_role_ids:
                    role = Role.query.get(role_id)
                    if role:
                        user_role = UserRole(user_id=user.id, role_id=role.id, is_active=True)
                        db.session.add(user_role)
            else:
                flash('Please select at least one role for the user', 'error')
                return render_template('superadmin/edit_user.html', user=user, roles=Role.query.all())
            
            # Handle account unlock
            if user.login_attempts == 0:
                user.account_locked_until = None
            
            db.session.commit()
            
            # Log the change
            SecurityLog.log_security_event(
                SecurityEventType.USER_MODIFIED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'modified_user_id': user_id,
                    'changes': {
                        'roles': selected_role_ids,
                        'is_active': user.is_active,
                        'email_verified': user.email_verified,
                        'password_changed': bool(new_password)
                    }
                },
                severity='medium'
            )
            
            flash('User updated successfully', 'success')
            return redirect(url_for('superadmin.user_detail', user_id=user_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    roles = Role.query.all()
    return render_template('superadmin/edit_user.html', user=user, roles=roles)

# Role and Permission Management
@superadmin_bp.route('/roles')
def roles():
    """List all roles and permissions"""
    roles = Role.query.all()
    permissions = Permission.query.all()
    
    return render_template('superadmin/roles.html', roles=roles, permissions=permissions)

@superadmin_bp.route('/roles/create', methods=['GET', 'POST'])
@csrf_protect
def create_role():
    """Create a new role"""
    if request.method == 'POST':
        try:
            name = SecurityService.sanitize_input(request.form.get('name', ''))
            description = SecurityService.sanitize_input(request.form.get('description', ''))
            
            if not name:
                flash('Role name is required', 'error')
                return render_template('superadmin/create_role.html')
            
            # Check if role exists
            if Role.query.filter_by(name=name).first():
                flash('Role already exists', 'error')
                return render_template('superadmin/create_role.html')
            
            # Create role
            role = Role(name=name, description=description)
            
            # Add permissions
            selected_permissions = request.form.getlist('permissions')
            for perm_id in selected_permissions:
                permission = Permission.query.get(perm_id)
                if permission:
                    role.permissions.append(permission)
            
            db.session.add(role)
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.ROLE_CREATED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={'role_name': name, 'permissions': selected_permissions},
                severity='medium'
            )
            
            flash('Role created successfully', 'success')
            return redirect(url_for('superadmin.roles'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating role: {str(e)}', 'error')
    
    permissions = Permission.query.all()
    return render_template('superadmin/create_role.html', permissions=permissions)

@superadmin_bp.route('/roles/<int:role_id>')
def view_role(role_id):
    """View role details as JSON"""
    try:
        role = Role.query.get_or_404(role_id)
        
        # Get role statistics (handle lazy relationships)
        user_count = role.get_users_count()
        permission_count = role.permissions.count() if hasattr(role, 'permissions') else 0
        
        # Get permissions list
        permissions_list = []
        if hasattr(role, 'permissions'):
            for perm in role.permissions.all():
                permissions_list.append({
                    'id': perm.id,
                    'name': perm.name,
                    'display_name': perm.display_name,
                    'description': perm.description,
                    'resource': perm.resource,
                    'action': perm.action
                })
        
        role_data = {
            'id': role.id,
            'name': role.name,
            'display_name': role.display_name,
            'description': role.description,
            'level': role.level,
            'is_system_role': role.is_system_role,
            'user_count': user_count,
            'permission_count': permission_count,
            'created_at': role.created_at.isoformat() if role.created_at else None,
            'updated_at': role.updated_at.isoformat() if role.updated_at else None,
            'permissions': permissions_list
        }
        
        return jsonify({'success': True, 'role': role_data})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/roles/<int:role_id>/edit', methods=['GET', 'POST'])
def edit_role(role_id):
    """Edit role details"""
    role = Role.query.get_or_404(role_id)
    
    # Prevent editing system roles
    if role.is_system_role:
        flash('System roles cannot be edited', 'error')
        return redirect(url_for('superadmin.roles'))
    
    # Prevent editing roles with active users
    user_count = role.get_users_count()
    if user_count > 0:
        flash(f'Cannot edit role "{role.display_name}" - it has {user_count} active users assigned. Remove users first.', 'error')
        return redirect(url_for('superadmin.roles'))
    
    if request.method == 'POST':
        try:
            display_name = SecurityService.sanitize_input(request.form.get('display_name', ''))
            description = SecurityService.sanitize_input(request.form.get('description', ''))
            level = request.form.get('level', type=int)
            
            # Update role details
            if display_name:
                role.display_name = display_name
            if description:
                role.description = description
            if level is not None:
                role.level = level
            
            # Update permissions
            selected_permissions = request.form.getlist('permissions')
            role.permissions = []
            for perm_id in selected_permissions:
                permission = Permission.query.get(perm_id)
                if permission:
                    role.permissions.append(permission)
            
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.ROLE_MODIFIED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={'role_id': role.id, 'role_name': role.name, 'permissions': selected_permissions},
                severity='medium'
            )
            
            flash('Role updated successfully', 'success')
            return redirect(url_for('superadmin.roles'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating role: {str(e)}', 'error')
    
    permissions = Permission.query.all()
    return render_template('superadmin/edit_role.html', role=role, permissions=permissions)

@superadmin_bp.route('/roles/<int:role_id>/delete', methods=['DELETE'])
# @csrf_protect  # Temporarily disabled for testing
def delete_role(role_id):
    """Delete a role"""
    try:
        role = Role.query.get_or_404(role_id)
        
        # Prevent deleting system roles
        if role.is_system_role:
            return jsonify({'success': False, 'message': 'System roles cannot be deleted'}), 400
        
        # Check if role has users
        user_count = role.get_users_count()
        if user_count > 0:
            return jsonify({'success': False, 'message': f'Cannot delete role with {user_count} active users'}), 400
        
        role_name = role.name
        
        # Remove role-permission relationships
        role.permissions = []
        
        # Delete the role
        db.session.delete(role)
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,  # Using USER_MODIFIED since there's no ROLE_DELETED
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'action': 'role_deleted', 'role_name': role_name, 'role_id': role_id},
            severity='high'
        )
        
        return jsonify({'success': True, 'message': f'Role "{role_name}" deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Permission Management Routes
@superadmin_bp.route('/permissions')
def permissions():
    """List all permissions"""
    permissions = Permission.query.order_by(Permission.resource, Permission.action).all()
    return render_template('superadmin/permissions.html', permissions=permissions)

@superadmin_bp.route('/permissions/<int:permission_id>')
def view_permission(permission_id):
    """View permission details"""
    permission = Permission.query.get_or_404(permission_id)
    
    # Get roles that have this permission
    roles_with_permission = permission.roles.all() if hasattr(permission, 'roles') else []
    
    return render_template('superadmin/permission_detail.html', 
                         permission=permission, 
                         roles_with_permission=roles_with_permission)

@superadmin_bp.route('/permissions/add', methods=['GET', 'POST'])
def add_permission():
    """Add a new permission"""
    if request.method == 'POST':
        try:
            name = SecurityService.sanitize_input(request.form.get('name', ''))
            display_name = SecurityService.sanitize_input(request.form.get('display_name', ''))
            description = SecurityService.sanitize_input(request.form.get('description', ''))
            resource = SecurityService.sanitize_input(request.form.get('resource', ''))
            action = SecurityService.sanitize_input(request.form.get('action', ''))
            
            if not all([name, resource, action]):
                flash('Name, Resource, and Action are required', 'error')
                return render_template('superadmin/add_permission.html')
            
            # Check if permission exists
            if Permission.query.filter_by(name=name).first():
                flash('Permission with this name already exists', 'error')
                return render_template('superadmin/add_permission.html')
            
            permission = Permission(
                name=name,
                display_name=display_name,
                description=description,
                resource=resource,
                action=action,
                is_system_permission=False
            )
            
            db.session.add(permission)
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.USER_MODIFIED,  # Using available event type
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'action': 'permission_created',
                    'permission_name': name,
                    'resource': resource,
                    'action_type': action
                },
                severity='medium'
            )
            
            flash('Permission created successfully', 'success')
            return redirect(url_for('superadmin.permissions'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating permission: {str(e)}', 'error')
            return render_template('superadmin/add_permission.html')
    
    return render_template('superadmin/add_permission.html')

@superadmin_bp.route('/permissions/<int:permission_id>/edit', methods=['GET', 'POST'])
def edit_permission(permission_id):
    """Edit permission details"""
    permission = Permission.query.get_or_404(permission_id)
    
    # Prevent editing system permissions
    if permission.is_system_permission:
        flash('System permissions cannot be edited', 'error')
        return redirect(url_for('superadmin.permissions'))
    
    if request.method == 'POST':
        try:
            display_name = SecurityService.sanitize_input(request.form.get('display_name', ''))
            description = SecurityService.sanitize_input(request.form.get('description', ''))
            
            # Update permission details (name, resource, action should not be changed)
            if display_name:
                permission.display_name = display_name
            if description:
                permission.description = description
            
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.USER_MODIFIED,  # Using available event type
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'action': 'permission_modified',
                    'permission_id': permission.id,
                    'permission_name': permission.name
                },
                severity='medium'
            )
            
            flash('Permission updated successfully', 'success')
            return redirect(url_for('superadmin.permissions'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating permission: {str(e)}', 'error')
    
    return render_template('superadmin/edit_permission.html', permission=permission)

@superadmin_bp.route('/permissions/<int:permission_id>/delete', methods=['DELETE'])
def delete_permission(permission_id):
    """Delete a permission"""
    try:
        permission = Permission.query.get_or_404(permission_id)
        
        # Prevent deleting system permissions
        if permission.is_system_permission:
            return jsonify({'success': False, 'message': 'System permissions cannot be deleted'}), 400
        
        # Check if permission is assigned to any roles
        roles_count = permission.roles.count() if hasattr(permission, 'roles') else 0
        if roles_count > 0:
            return jsonify({'success': False, 'message': f'Cannot delete permission assigned to {roles_count} roles'}), 400
        
        permission_name = permission.name
        
        # Delete the permission
        db.session.delete(permission)
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,  # Using available event type
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'action': 'permission_deleted',
                'permission_name': permission_name
            },
            severity='high'
        )
        
        return jsonify({'success': True, 'message': f'Permission "{permission_name}" deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/permissions/create', methods=['GET', 'POST'])
@csrf_protect
def create_permission():
    """Create a new permission"""
    if request.method == 'POST':
        try:
            name = SecurityService.sanitize_input(request.form.get('name', ''))
            description = SecurityService.sanitize_input(request.form.get('description', ''))
            resource = SecurityService.sanitize_input(request.form.get('resource', ''))
            action = SecurityService.sanitize_input(request.form.get('action', ''))
            
            if not all([name, resource, action]):
                flash('All fields are required', 'error')
                return render_template('superadmin/create_permission.html')
            
            # Check if permission exists
            if Permission.query.filter_by(name=name).first():
                flash('Permission already exists', 'error')
                return render_template('superadmin/create_permission.html')
            
            permission = Permission(
                name=name,
                description=description,
                resource=resource,
                action=action
            )
            
            db.session.add(permission)
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.PERMISSION_CREATED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'permission_name': name,
                    'resource': resource,
                    'action': action
                },
                severity='medium'
            )
            
            flash('Permission created successfully', 'success')
            return redirect(url_for('superadmin.roles'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating permission: {str(e)}', 'error')
    
    return render_template('superadmin/create_permission.html')

# Subscription Management
@superadmin_bp.route('/subscriptions')
def subscriptions():
    """List all subscriptions"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    status_filter = request.args.get('status', '')
    plan_filter = request.args.get('plan', '')
    plan_type_filter = request.args.get('plan_type', '')
    
    query = UserSubscription.query.join(AuthUser).join(SubscriptionPlan)
    
    if status_filter:
        query = query.filter(UserSubscription.status == status_filter)
    
    if plan_filter:
        query = query.filter(SubscriptionPlan.name == plan_filter)
    
    if plan_type_filter:
        query = query.filter(SubscriptionPlan.plan_type == plan_type_filter)
    
    subscriptions = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get plans grouped by type
    consultancy_plans = SubscriptionPlan.query.filter_by(plan_type='consultancy').all()
    jobseeker_plans = SubscriptionPlan.query.filter_by(plan_type='jobseeker').all()
    all_plans = SubscriptionPlan.query.all()
    
    statuses = [status.value for status in SubscriptionStatus]
    
    return render_template('superadmin/subscriptions.html',
                         subscriptions=subscriptions, 
                         consultancy_plans=consultancy_plans,
                         jobseeker_plans=jobseeker_plans,
                         all_plans=all_plans,
                         statuses=statuses, 
                         status_filter=status_filter,
                         plan_filter=plan_filter,
                         plan_type_filter=plan_type_filter)

@superadmin_bp.route('/subscriptions/<int:subscription_id>/manage', methods=['GET', 'POST'])
@csrf_protect
def manage_subscription(subscription_id):
    """Manage subscription status and plan"""
    subscription = UserSubscription.query.get_or_404(subscription_id)
    
    if request.method == 'POST':
        try:
            old_status = subscription.status
            old_plan_id = subscription.plan_id
            
            subscription.status = request.form.get('status')
            subscription.plan_id = request.form.get('plan_id', type=int)
            
            # Update expiry if extending
            if request.form.get('extend_days'):
                days = int(request.form.get('extend_days', 0))
                if days > 0:
                    if subscription.expires_at:
                        subscription.expires_at = subscription.expires_at + timedelta(days=days)
                    else:
                        subscription.expires_at = datetime.utcnow() + timedelta(days=days)
            
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.SUBSCRIPTION_MODIFIED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'subscription_id': subscription_id,
                    'user_id': subscription.user_id,
                    'changes': {
                        'status': {'old': old_status, 'new': subscription.status},
                        'plan_id': {'old': old_plan_id, 'new': subscription.plan_id}
                    }
                },
                severity='medium'
            )
            
            flash('Subscription updated successfully', 'success')
            return redirect(url_for('superadmin.subscriptions'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating subscription: {str(e)}', 'error')
    
    plans = SubscriptionPlan.query.all()
    statuses = [status.value for status in SubscriptionStatus]
    
    return render_template('superadmin/manage_subscription.html',
                         subscription=subscription, plans=plans, statuses=statuses)

# Security Monitoring
@superadmin_bp.route('/security')
def security_logs():
    """View security logs and events"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    event_type = request.args.get('event_type', '')
    severity = request.args.get('severity', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = SecurityLog.query
    
    # Apply filters
    if event_type:
        query = query.filter(SecurityLog.event_type == event_type)
    
    if severity:
        query = query.filter(SecurityLog.severity == severity)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(SecurityLog.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(SecurityLog.created_at < date_to_obj)
        except ValueError:
            pass
    
    logs = query.order_by(SecurityLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get unique event types and severities for filters
    event_types = db.session.query(SecurityLog.event_type.distinct()).all()
    severities = db.session.query(SecurityLog.severity.distinct()).all()
    
    # Extract string values from enums
    event_type_values = [et[0].value if hasattr(et[0], 'value') else et[0] for et in event_types]
    severity_values = [s[0] for s in severities]
    
    # Calculate today's start for filtering today's events
    from datetime import datetime, timedelta
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Calculate today's events count
    today_events_count = len([log for log in logs.items if log.created_at and log.created_at >= today_start])

    return render_template('superadmin/security_logs.html',
                         logs=logs, event_types=event_type_values,
                         severities=severity_values,
                         today_start=today_start,
                         today_events_count=today_events_count,
                         filters={
                             'event_type': event_type,
                             'severity': severity,
                             'date_from': date_from,
                             'date_to': date_to
                         })# API Endpoints for AJAX operations
@superadmin_bp.route('/api/users/<int:user_id>/toggle-active', methods=['POST'])
@csrf_protect
def toggle_user_active(user_id):
    """Toggle user active status"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        user.is_active = not user.is_active
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'modified_user_id': user_id,
                'action': 'toggle_active',
                'new_status': user.is_active
            },
            severity='medium'
        )
        
        return jsonify({
            'success': True,
            'message': f'User {"activated" if user.is_active else "deactivated"}',
            'is_active': user.is_active
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
# @csrf_protect  # Temporarily disabled for testing
def activate_user(user_id):
    """Activate user"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        user.is_active = True
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'modified_user_id': user_id, 'action': 'activate'},
            severity='medium'
        )
        
        return jsonify({'success': True, 'message': 'User activated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
# @csrf_protect  # Temporarily disabled for testing
def deactivate_user(user_id):
    """Deactivate user"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        user.is_active = False
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'modified_user_id': user_id, 'action': 'deactivate'},
            severity='medium'
        )
        
        return jsonify({'success': True, 'message': 'User deactivated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/unlock', methods=['POST'])
# @csrf_protect  # Temporarily disabled for testing
def unlock_user(user_id):
    """Unlock user account"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        user.account_locked_until = None
        user.login_attempts = 0
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'modified_user_id': user_id, 'action': 'unlock'},
            severity='medium'
        )
        
        return jsonify({'success': True, 'message': 'User account unlocked successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/delete', methods=['DELETE'])
# @csrf_protect  # Temporarily disabled for testing
def delete_user(user_id):
    """Delete user account"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        
        # Prevent deleting the current user
        if user.id == g.current_user.id:
            return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
        
        # Prevent deleting superadmin users (safety measure)
        if user.has_role('superadmin') and not g.current_user.has_role('superadmin'):
            return jsonify({'success': False, 'message': 'Insufficient permissions to delete superadmin user'}), 403
        
        # Store user info for logging before deletion
        deleted_user_info = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': f"{user.first_name} {user.last_name}",
            'roles': [role.name for role in user.get_roles()]
        }
        
        # Delete user roles first (foreign key constraint)
        UserRole.query.filter_by(user_id=user.id).delete()
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        # Log the deletion
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'deleted_user': deleted_user_info,
                'deleted_by': g.current_user.username,
                'action': 'delete'
            },
            severity='high'
        )
        
        return jsonify({'success': True, 'message': f'User {deleted_user_info["username"]} deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@csrf_protect
def reset_user_password(user_id):
    """Reset user password"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        
        # Generate password reset token (mock implementation)
        import secrets
        reset_token = secrets.token_urlsafe(32)
        user.password_reset_token = reset_token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=24)
        
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.PASSWORD_RESET_REQUESTED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'target_user_id': user_id, 'action': 'admin_reset'},
            severity='medium'
        )
        
        # In a real implementation, send email with reset token
        # For now, just return success
        return jsonify({
            'success': True, 
            'message': 'Password reset initiated. Reset token generated.',
            'reset_token': reset_token  # Remove this in production
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/verify-email', methods=['POST'])
@csrf_protect
def verify_user_email(user_id):
    """Manually verify user email"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        user.email_verified = True
        user.email_verification_token = None
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'modified_user_id': user_id, 'action': 'verify_email'},
            severity='low'
        )
        
        return jsonify({'success': True, 'message': 'Email verified successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/send-verification', methods=['POST'])
@csrf_protect
def send_verification_email(user_id):
    """Send verification email to user"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        
        # Generate verification token (mock implementation)
        import secrets
        verification_token = secrets.token_urlsafe(32)
        user.email_verification_token = verification_token
        
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'target_user_id': user_id, 'action': 'send_verification'},
            severity='low'
        )
        
        # In a real implementation, send email with verification token
        # For now, just return success
        return jsonify({
            'success': True, 
            'message': 'Verification email sent successfully',
            'verification_token': verification_token  # Remove this in production
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@superadmin_bp.route('/users/<int:user_id>/activity')
def user_activity_log(user_id):
    """View user activity log"""
    user = AuthUser.query.get_or_404(user_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    activity_logs = SecurityLog.query.filter_by(user_id=user_id).order_by(
        SecurityLog.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('superadmin/user_activity.html', 
                         user=user, activity_logs=activity_logs)

@superadmin_bp.route('/users/<int:user_id>/update', methods=['POST'])
@csrf_protect
def update_user(user_id):
    """Update user information from modal form"""
    try:
        user = AuthUser.query.get_or_404(user_id)
        
        # Update basic info
        user.first_name = SecurityService.sanitize_input(request.form.get('first_name', ''))
        user.last_name = SecurityService.sanitize_input(request.form.get('last_name', ''))
        user.email = SecurityService.sanitize_input(request.form.get('email', ''))
        user.phone = SecurityService.sanitize_input(request.form.get('phone', ''))
        user.is_active = 'is_active' in request.form
        
        # Update user role if provided
        new_role_name = request.form.get('user_type')
        if new_role_name:
            # Remove existing roles
            existing_roles = user.user_roles.all()
            for user_role in existing_roles:
                db.session.delete(user_role)
            
            # Add new role
            new_role = Role.query.filter_by(name=new_role_name).first()
            if new_role:
                user_role = UserRole(user_id=user.id, role_id=new_role.id, is_active=True)
                db.session.add(user_role)
        
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'modified_user_id': user_id, 
                'action': 'update_profile',
                'new_role': new_role_name if new_role_name else None
            },
            severity='medium'
        )
        
        flash('User updated successfully', 'success')
        return redirect(url_for('superadmin.user_detail', user_id=user_id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user: {str(e)}', 'error')
        return redirect(url_for('superadmin.user_detail', user_id=user_id))

@superadmin_bp.route('/api/security-stats')
def security_stats():
    """Get security statistics for dashboard"""
    try:
        today = datetime.utcnow().date()
        last_week = today - timedelta(days=7)
        
        stats = {
            'events_today': SecurityLog.query.filter(
                SecurityLog.created_at >= today
            ).count(),
            'events_this_week': SecurityLog.query.filter(
                SecurityLog.created_at >= last_week
            ).count(),
            'high_severity_events': SecurityLog.query.filter_by(severity='high').count(),
            'failed_logins_today': SecurityLog.query.filter(
                SecurityLog.event_type == SecurityEventType.LOGIN_FAILED.value,
                SecurityLog.created_at >= today
            ).count()
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export/Import functionality
@superadmin_bp.route('/export/users')
def export_users():
    """Export users data as JSON"""
    try:
        users = AuthUser.query.all()
        
        export_data = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'roles': [role.name for role in user.roles],
                'subscription': {
                    'plan': user.get_active_subscription().plan.name if user.get_active_subscription() else None,
                    'status': user.get_active_subscription().status if user.get_active_subscription() else None
                }
            }
            export_data.append(user_data)
        
        SecurityLog.log_security_event(
            SecurityEventType.DATA_EXPORT,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'export_type': 'users', 'record_count': len(export_data)},
            severity='medium'
        )
        
        return jsonify({
            'success': True,
            'data': export_data,
            'exported_at': datetime.utcnow().isoformat(),
            'exported_by': g.current_user.username
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# System maintenance
@superadmin_bp.route('/maintenance/cleanup-logs', methods=['POST'])
@csrf_protect
def cleanup_old_logs():
    """Clean up old security logs"""
    try:
        days = request.form.get('days', 90, type=int)
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        deleted_count = SecurityLog.query.filter(
            SecurityLog.created_at < cutoff_date
        ).delete()
        
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.SYSTEM_MAINTENANCE,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'action': 'cleanup_logs',
                'days': days,
                'deleted_count': deleted_count
            },
            severity='low'
        )
        
        flash(f'Cleaned up {deleted_count} old log entries', 'success')
        return redirect(url_for('superadmin.security_logs'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error cleaning up logs: {str(e)}', 'error')
        return redirect(url_for('superadmin.security_logs'))

# Job Portal Management
@superadmin_bp.route('/job-portals')
def job_portals():
    """List all job portals"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    query = JobPortal.query
    
    if search:
        query = query.filter(JobPortal.name.contains(search) | 
                           JobPortal.display_name.contains(search))
    
    if status_filter:
        is_active = status_filter == 'active'
        query = query.filter(JobPortal.is_active == is_active)
    
    portals = query.order_by(JobPortal.sort_order, JobPortal.display_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('superadmin/job_portals.html', portals=portals)

@superadmin_bp.route('/job-portals/add', methods=['GET', 'POST'])
@csrf_protect
def add_job_portal():
    """Add new job portal"""
    if request.method == 'POST':
        try:
            portal = JobPortal(
                name=request.form['name'].lower().replace(' ', '_'),
                display_name=request.form['display_name'],
                website_url=request.form['website_url'],
                logo_url=request.form.get('logo_url', ''),
                description=request.form.get('description', ''),
                sort_order=int(request.form.get('sort_order', 0)),
                api_integration=bool(request.form.get('api_integration')),
                api_endpoint=request.form.get('api_endpoint', ''),
                is_active=True
            )
            
            db.session.add(portal)
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.USER_MODIFIED,  # Using available event type
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'action': 'job_portal_created',
                    'portal_name': portal.name,
                    'portal_id': portal.id
                },
                severity='low'
            )
            
            flash(f'Job portal "{portal.display_name}" created successfully!', 'success')
            return redirect(url_for('superadmin.job_portals'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating job portal: {str(e)}', 'error')
    
    return render_template('superadmin/add_job_portal.html')

@superadmin_bp.route('/job-portals/<int:id>/edit', methods=['GET', 'POST'])
@csrf_protect
def edit_job_portal(id):
    """Edit job portal"""
    portal = JobPortal.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            portal.display_name = request.form['display_name']
            portal.website_url = request.form['website_url']
            portal.logo_url = request.form.get('logo_url', '')
            portal.description = request.form.get('description', '')
            portal.sort_order = int(request.form.get('sort_order', 0))
            portal.api_integration = bool(request.form.get('api_integration'))
            portal.api_endpoint = request.form.get('api_endpoint', '')
            portal.is_active = bool(request.form.get('is_active'))
            
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.USER_MODIFIED,  # Using available event type
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'action': 'job_portal_updated',
                    'portal_name': portal.name,
                    'portal_id': portal.id
                },
                severity='low'
            )
            
            flash(f'Job portal "{portal.display_name}" updated successfully!', 'success')
            return redirect(url_for('superadmin.job_portals'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating job portal: {str(e)}', 'error')
    
    return render_template('superadmin/edit_job_portal.html', portal=portal)

@superadmin_bp.route('/job-portals/<int:id>/delete', methods=['POST'])
@csrf_protect
def delete_job_portal(id):
    """Delete job portal"""
    try:
        portal = JobPortal.query.get_or_404(id)
        
        # Check if portal is being used by any users
        user_count = UserPortalAccess.query.filter_by(portal_id=id, is_active=True).count()
        if user_count > 0:
            flash(f'Cannot delete "{portal.display_name}" - it is currently being used by {user_count} users.', 'error')
            return redirect(url_for('superadmin.job_portals'))
        
        portal_name = portal.display_name
        db.session.delete(portal)
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,  # Using available event type
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'action': 'job_portal_deleted',
                'portal_name': portal.name,
                'portal_id': id
            },
            severity='medium'
        )
        
        flash(f'Job portal "{portal_name}" deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting job portal: {str(e)}', 'error')
    
    return redirect(url_for('superadmin.job_portals'))

# =============================================================================
# SUBSCRIPTION PLAN MANAGEMENT ROUTES
# =============================================================================

@superadmin_bp.route('/subscription-plans')
def subscription_plans():
    """List all subscription plans with management options"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        plan_type = request.args.get('plan_type', '')
        
        query = SubscriptionPlan.query
        
        # Apply plan type filter
        if plan_type:
            query = query.filter(SubscriptionPlan.plan_type == plan_type)
        
        plans = query.order_by(SubscriptionPlan.plan_type, SubscriptionPlan.sort_order).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get usage statistics for each plan
        plan_usage = {}
        for plan in plans.items:
            usage_count = UserSubscription.query.filter_by(plan_id=plan.id).count()
            active_count = UserSubscription.query.filter_by(
                plan_id=plan.id, 
                status=SubscriptionStatus.ACTIVE.value
            ).count()
            plan_usage[plan.id] = {
                'total_users': usage_count,
                'active_users': active_count
            }
        
        # Get sidebar stats
        sidebar_stats = {
            'total_plans': SubscriptionPlan.query.count(),
            'active_plans': SubscriptionPlan.query.filter_by(is_active=True).count(),
            'jobseeker_count': SubscriptionPlan.query.filter_by(plan_type='jobseeker').count(),
            'consultancy_count': SubscriptionPlan.query.filter_by(plan_type='consultancy').count(),
            'total_subscribers': UserSubscription.query.count(),
            'active_subscribers': UserSubscription.query.filter_by(status=SubscriptionStatus.ACTIVE.value).count(),
            'portal_count': JobPortal.query.filter_by(is_active=True).count(),
            'monthly_revenue': db.session.query(
                db.func.sum(SubscriptionPlan.price_monthly)
            ).join(UserSubscription).filter(
                UserSubscription.status == SubscriptionStatus.ACTIVE.value
            ).scalar() or 0
        }
        
        return render_template('superadmin/subscription_plans.html', 
                             plans=plans, 
                             plan_usage=plan_usage,
                             current_plan_type=plan_type,
                             **sidebar_stats)
    
    except Exception as e:
        flash(f'Error loading subscription plans: {str(e)}', 'error')
        return render_template('superadmin/subscription_plans.html', 
                             plans=None, plan_usage={}, current_plan_type='')

@superadmin_bp.route('/subscription-plans/add', methods=['GET', 'POST'])
@csrf_protect
def add_subscription_plan():
    """Add new subscription plan"""
    if request.method == 'POST':
        try:
            # Basic plan details
            plan = SubscriptionPlan(
                name=request.form.get('name').strip(),
                display_name=request.form.get('display_name').strip(),
                description=request.form.get('description', '').strip(),
                plan_type=request.form.get('plan_type'),
                price_monthly=float(request.form.get('price_monthly', 0)),
                price_yearly=float(request.form.get('price_yearly', 0)),
                currency=request.form.get('currency', 'USD'),
                max_users=int(request.form.get('max_users', 1)),
                max_jobs=int(request.form.get('max_jobs', 0)),
                max_applications=int(request.form.get('max_applications', 0)),
                max_job_portals=int(request.form.get('max_job_portals', 0)),
                storage_limit_gb=int(request.form.get('storage_limit_gb', 1)),
                api_rate_limit=int(request.form.get('api_rate_limit', 100)),
                is_popular=bool(request.form.get('is_popular')),
                is_active=bool(request.form.get('is_active', True)),
                sort_order=int(request.form.get('sort_order', 0))
            )
            
            db.session.add(plan)
            db.session.flush()  # Get the plan ID
            
            # Add features
            feature_keys = request.form.getlist('feature_key[]')
            feature_names = request.form.getlist('feature_name[]')
            feature_values = request.form.getlist('feature_value[]')
            feature_types = request.form.getlist('feature_type[]')
            feature_categories = request.form.getlist('feature_category[]')
            
            for i, key in enumerate(feature_keys):
                if key and i < len(feature_names):
                    feature = SubscriptionFeature(
                        plan_id=plan.id,
                        feature_key=key.strip(),
                        feature_name=feature_names[i].strip(),
                        feature_value=feature_values[i].strip() if i < len(feature_values) else '',
                        is_boolean=feature_types[i] == 'boolean' if i < len(feature_types) else False,
                        is_numeric=feature_types[i] == 'numeric' if i < len(feature_types) else False,
                        is_unlimited=feature_types[i] == 'unlimited' if i < len(feature_types) else False,
                        feature_category=feature_categories[i] if i < len(feature_categories) else 'general',
                        display_order=i
                    )
                    db.session.add(feature)
            
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.USER_MODIFIED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'action': 'subscription_plan_created',
                    'plan_name': plan.name,
                    'plan_id': plan.id
                },
                severity='medium'
            )
            
            flash(f'Subscription plan "{plan.display_name}" created successfully!', 'success')
            return redirect(url_for('superadmin.subscription_plans'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating subscription plan: {str(e)}', 'error')
    
    return render_template('superadmin/add_subscription_plan.html')

@superadmin_bp.route('/subscription-plans/<int:id>/edit', methods=['GET', 'POST'])
@csrf_protect
def edit_subscription_plan(id):
    """Edit existing subscription plan"""
    plan = SubscriptionPlan.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Update basic plan details
            plan.name = request.form.get('name').strip()
            plan.display_name = request.form.get('display_name').strip()
            plan.description = request.form.get('description', '').strip()
            plan.plan_type = request.form.get('plan_type')
            plan.price_monthly = float(request.form.get('price_monthly', 0))
            plan.price_yearly = float(request.form.get('price_yearly', 0))
            plan.currency = request.form.get('currency', 'USD')
            plan.max_users = int(request.form.get('max_users', 1))
            plan.max_jobs = int(request.form.get('max_jobs', 0))
            plan.max_applications = int(request.form.get('max_applications', 0))
            plan.max_job_portals = int(request.form.get('max_job_portals', 0))
            plan.storage_limit_gb = int(request.form.get('storage_limit_gb', 1))
            plan.api_rate_limit = int(request.form.get('api_rate_limit', 100))
            plan.is_popular = bool(request.form.get('is_popular'))
            plan.is_active = bool(request.form.get('is_active'))
            plan.sort_order = int(request.form.get('sort_order', 0))
            plan.updated_at = datetime.utcnow()
            
            # Delete existing features and add new ones
            SubscriptionFeature.query.filter_by(plan_id=plan.id).delete()
            
            # Add updated features
            feature_keys = request.form.getlist('feature_key[]')
            feature_names = request.form.getlist('feature_name[]')
            feature_values = request.form.getlist('feature_value[]')
            feature_types = request.form.getlist('feature_type[]')
            feature_categories = request.form.getlist('feature_category[]')
            
            for i, key in enumerate(feature_keys):
                if key and i < len(feature_names):
                    feature = SubscriptionFeature(
                        plan_id=plan.id,
                        feature_key=key.strip(),
                        feature_name=feature_names[i].strip(),
                        feature_value=feature_values[i].strip() if i < len(feature_values) else '',
                        is_boolean=feature_types[i] == 'boolean' if i < len(feature_types) else False,
                        is_numeric=feature_types[i] == 'numeric' if i < len(feature_types) else False,
                        is_unlimited=feature_types[i] == 'unlimited' if i < len(feature_types) else False,
                        feature_category=feature_categories[i] if i < len(feature_categories) else 'general',
                        display_order=i
                    )
                    db.session.add(feature)
            
            db.session.commit()
            
            SecurityLog.log_security_event(
                SecurityEventType.USER_MODIFIED,
                user_id=g.current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={
                    'action': 'subscription_plan_updated',
                    'plan_name': plan.name,
                    'plan_id': plan.id
                },
                severity='medium'
            )
            
            flash(f'Subscription plan "{plan.display_name}" updated successfully!', 'success')
            return redirect(url_for('superadmin.subscription_plans'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating subscription plan: {str(e)}', 'error')
    
    # Get existing features
    features = SubscriptionFeature.query.filter_by(plan_id=plan.id).order_by(SubscriptionFeature.display_order).all()
    
    return render_template('superadmin/edit_subscription_plan.html', plan=plan, features=features)

@superadmin_bp.route('/subscription-plans/<int:id>/delete', methods=['POST'])
@csrf_protect
def delete_subscription_plan(id):
    """Delete subscription plan"""
    try:
        plan = SubscriptionPlan.query.get_or_404(id)
        
        # Check if plan is being used by any users
        user_count = UserSubscription.query.filter_by(plan_id=id).count()
        if user_count > 0:
            flash(f'Cannot delete "{plan.display_name}" - it is currently being used by {user_count} users.', 'error')
            return redirect(url_for('superadmin.subscription_plans'))
        
        plan_name = plan.display_name
        
        # Delete features first (cascade should handle this, but being explicit)
        SubscriptionFeature.query.filter_by(plan_id=id).delete()
        
        db.session.delete(plan)
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'action': 'subscription_plan_deleted',
                'plan_name': plan.name,
                'plan_id': id
            },
            severity='high'
        )
        
        flash(f'Subscription plan "{plan_name}" deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting subscription plan: {str(e)}', 'error')
    
    return redirect(url_for('superadmin.subscription_plans'))

@superadmin_bp.route('/subscription-plans/<int:id>/toggle-status', methods=['POST'])
@csrf_protect
def toggle_plan_status(id):
    """Toggle subscription plan active status"""
    try:
        plan = SubscriptionPlan.query.get_or_404(id)
        plan.is_active = not plan.is_active
        plan.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        status = "activated" if plan.is_active else "deactivated"
        flash(f'Subscription plan "{plan.display_name}" {status} successfully!', 'success')
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'action': 'subscription_plan_status_changed',
                'plan_name': plan.name,
                'plan_id': plan.id,
                'new_status': plan.is_active
            },
            severity='low'
        )
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating plan status: {str(e)}', 'error')
    
    return redirect(url_for('superadmin.subscription_plans'))

@superadmin_bp.route('/subscription-plans/<int:id>/duplicate', methods=['POST'])
@csrf_protect
def duplicate_subscription_plan(id):
    """Duplicate existing subscription plan"""
    try:
        original_plan = SubscriptionPlan.query.get_or_404(id)
        
        # Create new plan with copied data
        new_plan = SubscriptionPlan(
            name=f"{original_plan.name}_copy",
            display_name=f"{original_plan.display_name} (Copy)",
            description=original_plan.description,
            plan_type=original_plan.plan_type,
            price_monthly=original_plan.price_monthly,
            price_yearly=original_plan.price_yearly,
            currency=original_plan.currency,
            max_users=original_plan.max_users,
            max_jobs=original_plan.max_jobs,
            max_applications=original_plan.max_applications,
            max_job_portals=original_plan.max_job_portals,
            storage_limit_gb=original_plan.storage_limit_gb,
            api_rate_limit=original_plan.api_rate_limit,
            is_popular=False,  # New plan shouldn't be popular by default
            is_active=False,   # New plan should be inactive by default
            sort_order=original_plan.sort_order + 1
        )
        
        db.session.add(new_plan)
        db.session.flush()  # Get the new plan ID
        
        # Copy features
        original_features = SubscriptionFeature.query.filter_by(plan_id=original_plan.id).all()
        for feature in original_features:
            new_feature = SubscriptionFeature(
                plan_id=new_plan.id,
                feature_key=feature.feature_key,
                feature_name=feature.feature_name,
                feature_value=feature.feature_value,
                is_boolean=feature.is_boolean,
                is_numeric=feature.is_numeric,
                is_unlimited=feature.is_unlimited,
                feature_category=feature.feature_category,
                display_order=feature.display_order
            )
            db.session.add(new_feature)
        
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.USER_MODIFIED,
            user_id=g.current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'action': 'subscription_plan_duplicated',
                'original_plan_name': original_plan.name,
                'new_plan_name': new_plan.name,
                'new_plan_id': new_plan.id
            },
            severity='low'
        )
        
        flash(f'Subscription plan duplicated successfully! New plan: "{new_plan.display_name}"', 'success')
        return redirect(url_for('superadmin.edit_subscription_plan', id=new_plan.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error duplicating subscription plan: {str(e)}', 'error')
    
    return redirect(url_for('superadmin.subscription_plans'))

# =============================================================================
# SUBSCRIPTION DASHBOARD AND FEATURE MANAGEMENT
# =============================================================================

@superadmin_bp.route('/subscription-dashboard')
def subscription_dashboard():
    """Subscription management dashboard with overview and analytics"""
    try:
        # Basic statistics
        total_plans = SubscriptionPlan.query.count()
        active_plans = SubscriptionPlan.query.filter_by(is_active=True).count()
        jobseeker_count = SubscriptionPlan.query.filter_by(plan_type='jobseeker').count()
        consultancy_count = SubscriptionPlan.query.filter_by(plan_type='consultancy').count()
        
        # User subscription statistics
        total_subscribers = UserSubscription.query.count()
        active_subscribers = UserSubscription.query.filter_by(status=SubscriptionStatus.ACTIVE.value).count()
        
        # Feature statistics
        total_features = SubscriptionFeature.query.count()
        
        # Revenue calculation (active subscriptions)
        monthly_revenue = db.session.query(
            db.func.sum(SubscriptionPlan.price_monthly)
        ).join(UserSubscription, SubscriptionPlan.id == UserSubscription.plan_id).filter(
            UserSubscription.status == SubscriptionStatus.ACTIVE.value
        ).scalar() or 0
        
        # Portal count
        portal_count = JobPortal.query.filter_by(is_active=True).count()
        
        # Recent activity
        recent_plans = SubscriptionPlan.query.order_by(SubscriptionPlan.created_at.desc()).limit(5).all()
        recent_subscriptions = UserSubscription.query.join(AuthUser).join(SubscriptionPlan).order_by(
            UserSubscription.created_at.desc()
        ).limit(5).all()
        
        # Plan popularity (by user count)
        plan_popularity = db.session.query(
            SubscriptionPlan.display_name,
            SubscriptionPlan.plan_type,
            db.func.count(UserSubscription.id).label('user_count')
        ).outerjoin(UserSubscription).group_by(
            SubscriptionPlan.id, SubscriptionPlan.display_name, SubscriptionPlan.plan_type
        ).order_by(db.desc('user_count')).all()
        
        # Sidebar data
        sidebar_data = {
            'total_plans': total_plans,
            'active_plans': active_plans,
            'jobseeker_count': jobseeker_count,
            'consultancy_count': consultancy_count,
            'total_subscribers': total_subscribers,
            'active_subscribers': active_subscribers,
            'total_features': total_features,
            'monthly_revenue': f"{monthly_revenue:.2f}",
            'portal_count': portal_count
        }
        
        return render_template('superadmin/subscription_dashboard.html',
                             sidebar_data=sidebar_data,
                             recent_plans=recent_plans,
                             recent_subscriptions=recent_subscriptions,
                             plan_popularity=plan_popularity)
    
    except Exception as e:
        flash(f'Error loading subscription dashboard: {str(e)}', 'error')
        return render_template('superadmin/subscription_dashboard.html',
                             sidebar_data={}, recent_plans=[], recent_subscriptions=[], plan_popularity=[])

# ===========================
# JOB DATA MANAGEMENT ROUTES
# ===========================

# Industry Types Management
@superadmin_bp.route('/industry-types')
def industry_types():
    """List all industry types"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    search = request.args.get('search', '')
    
    query = IndustryType.query
    if search:
        query = query.filter(IndustryType.display_name.ilike(f'%{search}%'))
    
    industries = query.order_by(IndustryType.sort_order, IndustryType.display_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('superadmin/industry_types.html', industries=industries, search=search)

@superadmin_bp.route('/industry-types/create', methods=['GET', 'POST'])
def create_industry_type():
    """Create new industry type"""
    if request.method == 'POST':
        try:
            industry = IndustryType(
                name=request.form['name'],
                display_name=request.form['display_name'],
                description=request.form.get('description'),
                icon=request.form.get('icon'),
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(industry)
            db.session.commit()
            flash('Industry type created successfully', 'success')
            return redirect(url_for('superadmin.industry_types'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating industry type: {str(e)}', 'error')
    
    return render_template('superadmin/industry_type_form.html', industry=None)

@superadmin_bp.route('/industry-types/<int:id>/edit', methods=['GET', 'POST'])
def edit_industry_type(id):
    """Edit industry type"""
    industry = IndustryType.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            industry.name = request.form['name']
            industry.display_name = request.form['display_name']
            industry.description = request.form.get('description')
            industry.icon = request.form.get('icon')
            industry.sort_order = int(request.form.get('sort_order', 0))
            industry.is_active = 'is_active' in request.form
            
            db.session.commit()
            flash('Industry type updated successfully', 'success')
            return redirect(url_for('superadmin.industry_types'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating industry type: {str(e)}', 'error')
    
    return render_template('superadmin/industry_type_form.html', industry=industry)

@superadmin_bp.route('/industry-types/<int:id>/delete', methods=['POST'])
def delete_industry_type(id):
    """Delete industry type"""
    try:
        industry = IndustryType.query.get_or_404(id)
        db.session.delete(industry)
        db.session.commit()
        flash('Industry type deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting industry type: {str(e)}', 'error')
    
    return redirect(url_for('superadmin.industry_types'))

# Skills Management
@superadmin_bp.route('/skills')
def skills():
    """List all skills"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Skill.query
    if search:
        query = query.filter(Skill.display_name.ilike(f'%{search}%'))
    if category:
        query = query.filter(Skill.category == category)
    
    skills = query.order_by(Skill.sort_order, Skill.display_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    categories = db.session.query(Skill.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('superadmin/skills.html', skills=skills, search=search, 
                         category=category, categories=categories)

@superadmin_bp.route('/skills/create', methods=['GET', 'POST'])
def create_skill():
    """Create new skill"""
    if request.method == 'POST':
        try:
            skill = Skill(
                name=request.form['name'],
                display_name=request.form['display_name'],
                description=request.form.get('description'),
                category=request.form.get('category'),
                industry_id=int(request.form['industry_id']) if request.form.get('industry_id') else None,
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(skill)
            db.session.commit()
            flash('Skill created successfully', 'success')
            return redirect(url_for('superadmin.skills'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating skill: {str(e)}', 'error')
    
    industries = IndustryType.query.filter_by(is_active=True).order_by(IndustryType.display_name).all()
    return render_template('superadmin/skill_form.html', skill=None, industries=industries)

# Experience Levels Management
@superadmin_bp.route('/experience-levels')
def experience_levels():
    """List all experience levels"""
    experiences = Experience.query.order_by(Experience.sort_order, Experience.display_name).all()
    return render_template('superadmin/experience_levels.html', experiences=experiences)

@superadmin_bp.route('/experience-levels/create', methods=['GET', 'POST'])
def create_experience_level():
    """Create new experience level"""
    if request.method == 'POST':
        try:
            experience = Experience(
                name=request.form['name'],
                display_name=request.form['display_name'],
                description=request.form.get('description'),
                min_years=int(request.form['min_years']) if request.form.get('min_years') else None,
                max_years=int(request.form['max_years']) if request.form.get('max_years') else None,
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(experience)
            db.session.commit()
            flash('Experience level created successfully', 'success')
            return redirect(url_for('superadmin.experience_levels'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating experience level: {str(e)}', 'error')
    
    return render_template('superadmin/experience_form.html', experience=None)

# Job Roles Management
@superadmin_bp.route('/job-roles')
def job_roles():
    """List all job roles"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = JobRole.query
    if search:
        query = query.filter(JobRole.display_name.ilike(f'%{search}%'))
    if category:
        query = query.filter(JobRole.category == category)
    
    job_roles = query.order_by(JobRole.sort_order, JobRole.display_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    categories = db.session.query(JobRole.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('superadmin/job_roles.html', job_roles=job_roles, search=search,
                         category=category, categories=categories)

@superadmin_bp.route('/job-roles/create', methods=['GET', 'POST'])
def create_job_role():
    """Create new job role"""
    if request.method == 'POST':
        try:
            job_role = JobRole(
                name=request.form['name'],
                display_name=request.form['display_name'],
                description=request.form.get('description'),
                category=request.form.get('category'),
                industry_id=int(request.form['industry_id']) if request.form.get('industry_id') else None,
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(job_role)
            db.session.commit()
            flash('Job role created successfully', 'success')
            return redirect(url_for('superadmin.job_roles'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating job role: {str(e)}', 'error')
    
    industries = IndustryType.query.filter_by(is_active=True).order_by(IndustryType.display_name).all()
    return render_template('superadmin/job_role_form.html', job_role=None, industries=industries)

# Company Types Management
@superadmin_bp.route('/company-types')
def company_types():
    """List all company types"""
    company_types = CompanyType.query.order_by(CompanyType.sort_order, CompanyType.display_name).all()
    return render_template('superadmin/company_types.html', company_types=company_types)

@superadmin_bp.route('/company-types/create', methods=['GET', 'POST'])
def create_company_type():
    """Create new company type"""
    if request.method == 'POST':
        try:
            company_type = CompanyType(
                name=request.form['name'],
                display_name=request.form['display_name'],
                description=request.form.get('description'),
                employee_range_min=int(request.form['employee_range_min']) if request.form.get('employee_range_min') else None,
                employee_range_max=int(request.form['employee_range_max']) if request.form.get('employee_range_max') else None,
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(company_type)
            db.session.commit()
            flash('Company type created successfully', 'success')
            return redirect(url_for('superadmin.company_types'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating company type: {str(e)}', 'error')
    
    return render_template('superadmin/company_type_form.html', company_type=None)

# Job Types Management
@superadmin_bp.route('/job-types')
def job_types():
    """List all job types"""
    job_types = JobType.query.order_by(JobType.sort_order, JobType.display_name).all()
    return render_template('superadmin/job_types.html', job_types=job_types)

@superadmin_bp.route('/job-types/create', methods=['GET', 'POST'])
def create_job_type():
    """Create new job type"""
    if request.method == 'POST':
        try:
            job_type = JobType(
                name=request.form['name'],
                display_name=request.form['display_name'],
                description=request.form.get('description'),
                category=request.form.get('category'),
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(job_type)
            db.session.commit()
            flash('Job type created successfully', 'success')
            return redirect(url_for('superadmin.job_types'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating job type: {str(e)}', 'error')
    
    return render_template('superadmin/job_type_form.html', job_type=None)

# Location Management - Countries
@superadmin_bp.route('/countries')
def countries():
    """List all countries"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    search = request.args.get('search', '')
    
    query = Country.query
    if search:
        query = query.filter(Country.name.ilike(f'%{search}%'))
    
    countries = query.order_by(Country.sort_order, Country.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('superadmin/countries.html', countries=countries, search=search)

@superadmin_bp.route('/countries/create', methods=['GET', 'POST'])
def create_country():
    """Create new country"""
    if request.method == 'POST':
        try:
            country = Country(
                name=request.form['name'],
                code_alpha2=request.form['code_alpha2'].upper(),
                code_alpha3=request.form['code_alpha3'].upper(),
                numeric_code=request.form.get('numeric_code'),
                currency_code=request.form.get('currency_code'),
                phone_code=request.form.get('phone_code'),
                timezone_primary=request.form.get('timezone_primary'),
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(country)
            db.session.commit()
            flash('Country created successfully', 'success')
            return redirect(url_for('superadmin.countries'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating country: {str(e)}', 'error')
    
    return render_template('superadmin/country_form.html', country=None)

# Location Management - States
@superadmin_bp.route('/states')
def states():
    """List all states"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    search = request.args.get('search', '')
    country_id = request.args.get('country_id', type=int)
    
    query = State.query.join(Country)
    if search:
        query = query.filter(State.name.ilike(f'%{search}%'))
    if country_id:
        query = query.filter(State.country_id == country_id)
    
    states = query.order_by(Country.name, State.sort_order, State.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    countries = Country.query.filter_by(is_active=True).order_by(Country.name).all()
    
    return render_template('superadmin/states.html', states=states, search=search,
                         country_id=country_id, countries=countries)

@superadmin_bp.route('/states/create', methods=['GET', 'POST'])
def create_state():
    """Create new state"""
    if request.method == 'POST':
        try:
            state = State(
                name=request.form['name'],
                code=request.form.get('code'),
                country_id=int(request.form['country_id']),
                timezone_primary=request.form.get('timezone_primary'),
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(state)
            db.session.commit()
            flash('State created successfully', 'success')
            return redirect(url_for('superadmin.states'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating state: {str(e)}', 'error')
    
    countries = Country.query.filter_by(is_active=True).order_by(Country.name).all()
    return render_template('superadmin/state_form.html', state=None, countries=countries)

# Location Management - Cities
@superadmin_bp.route('/cities')
def cities():
    """List all cities"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    search = request.args.get('search', '')
    state_id = request.args.get('state_id', type=int)
    
    query = City.query.join(State).join(Country)
    if search:
        query = query.filter(City.name.ilike(f'%{search}%'))
    if state_id:
        query = query.filter(City.state_id == state_id)
    
    cities = query.order_by(Country.name, State.name, City.sort_order, City.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    states = State.query.join(Country).filter_by(is_active=True).order_by(Country.name, State.name).all()
    
    return render_template('superadmin/cities.html', cities=cities, search=search,
                         state_id=state_id, states=states)

@superadmin_bp.route('/cities/create', methods=['GET', 'POST'])
def create_city():
    """Create new city"""
    if request.method == 'POST':
        try:
            city = City(
                name=request.form['name'],
                state_id=int(request.form['state_id']),
                latitude=float(request.form['latitude']) if request.form.get('latitude') else None,
                longitude=float(request.form['longitude']) if request.form.get('longitude') else None,
                population=int(request.form['population']) if request.form.get('population') else None,
                timezone=request.form.get('timezone'),
                is_metro='is_metro' in request.form,
                sort_order=int(request.form.get('sort_order', 0))
            )
            db.session.add(city)
            db.session.commit()
            flash('City created successfully', 'success')
            return redirect(url_for('superadmin.cities'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating city: {str(e)}', 'error')
    
    states = State.query.join(Country).filter_by(is_active=True).order_by(Country.name, State.name).all()
    return render_template('superadmin/city_form.html', city=None, states=states)