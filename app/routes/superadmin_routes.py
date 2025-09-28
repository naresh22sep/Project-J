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
    AuthUser, Role, Permission, SubscriptionPlan, UserSubscription, 
    SecurityLog, SecurityEventType, SubscriptionStatus
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
    
    return render_template('superadmin/user_detail.html', 
                         user=user, subscription=subscription, 
                         recent_activity=recent_activity)

@superadmin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@csrf_protect
def edit_user(user_id):
    """Edit user details and roles"""
    user = AuthUser.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            # Update basic info
            user.first_name = SecurityService.sanitize_input(request.form.get('first_name', ''))
            user.last_name = SecurityService.sanitize_input(request.form.get('last_name', ''))
            user.email = SecurityService.sanitize_input(request.form.get('email', ''))
            user.is_active = request.form.get('is_active') == 'true'
            
            # Update roles
            selected_roles = request.form.getlist('roles')
            user.roles = []  # Clear existing roles
            
            for role_id in selected_roles:
                role = Role.query.get(role_id)
                if role:
                    user.roles.append(role)
            
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
                        'roles': selected_roles,
                        'is_active': user.is_active
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
    
    query = UserSubscription.query.join(AuthUser).join(SubscriptionPlan)
    
    if status_filter:
        query = query.filter(UserSubscription.status == status_filter)
    
    if plan_filter:
        query = query.filter(SubscriptionPlan.name == plan_filter)
    
    subscriptions = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    plans = SubscriptionPlan.query.all()
    statuses = [status.value for status in SubscriptionStatus]
    
    return render_template('superadmin/subscriptions.html',
                         subscriptions=subscriptions, plans=plans,
                         statuses=statuses, status_filter=status_filter,
                         plan_filter=plan_filter)

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
    
    return render_template('superadmin/security_logs.html',
                         logs=logs, event_types=[et[0] for et in event_types],
                         severities=[s[0] for s in severities],
                         filters={
                             'event_type': event_type,
                             'severity': severity,
                             'date_from': date_from,
                             'date_to': date_to
                         })

# API Endpoints for AJAX operations
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