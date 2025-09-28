"""
Authentication Routes - Login, Registration, JWT Management
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from app.services.auth_service import (
    JWTAuthService, SecurityService, AuthorizationService,
    jwt_required, csrf_protect, sanitize_inputs
)
from app.auth.auth_models import (
    AuthUser, Role, UserSubscription, SubscriptionPlan, 
    SecurityLog, SecurityEventType, SubscriptionStatus
)
from app import db
from datetime import datetime
import re

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
@csrf_protect
@sanitize_inputs(['username', 'password'])
def login():
    """User login endpoint"""
    if request.method == 'GET':
        # Return login form or page
        return render_template('auth/login.html')
    
    try:
        # Get sanitized data
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '')
        remember_me = data.get('remember_me', False)
        
        # Validation
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        # Authenticate user
        user, message = JWTAuthService.authenticate_user(
            username, password, ip_address, user_agent
        )
        
        if not user:
            return jsonify({
                'success': False,
                'message': message
            }), 401
        
        # Generate tokens
        tokens = JWTAuthService.generate_tokens(user)
        
        if not tokens:
            return jsonify({
                'success': False,
                'message': 'Failed to generate authentication tokens'
            }), 500
        
        # Generate CSRF token for session
        csrf_token = SecurityService.generate_csrf_token(user.id)
        
        # Store session info
        session['user_id'] = user.id
        session['csrf_token'] = csrf_token
        
        response_data = {
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': [role.name for role in user.roles],
                'subscription': {
                    'plan': user.get_active_subscription().plan.name if user.get_active_subscription() else None,
                    'status': user.get_active_subscription().status if user.get_active_subscription() else None
                }
            },
            'tokens': {
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'expires_in': tokens['expires_in'],
                'token_type': tokens['token_type']
            },
            'csrf_token': csrf_token
        }
        
        # For web forms, redirect to dashboard
        if not request.is_json:
            flash('Login successful!', 'success')
            
            # Redirect based on user role
            if user.has_role('superadmin'):
                return redirect(url_for('superadmin.dashboard'))
            elif user.has_role('admin'):
                return redirect('/admin/dashboard')
            elif user.has_role('consultancy'):
                return redirect('/consultancy/dashboard')
            else:
                return redirect('/jobseeker/dashboard')
        
        return jsonify(response_data), 200
    
    except Exception as e:
        SecurityLog.log_security_event(
            SecurityEventType.SYSTEM_ERROR,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'endpoint': 'login', 'error': str(e)},
            severity='high'
        )
        
        return jsonify({
            'success': False,
            'message': 'An error occurred during login'
        }), 500

@auth_bp.route('/register', methods=['GET', 'POST'])
@csrf_protect
@sanitize_inputs(['username', 'email', 'first_name', 'last_name', 'password'])
def register():
    """User registration endpoint"""
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Get sanitized data
        username = data.get('username', '').strip().lower()
        email = data.get('email', '').strip().lower()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        user_type = data.get('user_type', 'jobseeker')  # Default role
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores')
        
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('Valid email address is required')
        
        if not first_name:
            errors.append('First name is required')
        
        if not last_name:
            errors.append('Last name is required')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        elif password != confirm_password:
            errors.append('Passwords do not match')
        
        # Password strength check
        if not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            errors.append('Password must contain at least one lowercase letter')
        if not re.search(r'\d', password):
            errors.append('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Password must contain at least one special character')
        
        if user_type not in ['jobseeker', 'consultancy']:
            errors.append('Invalid user type')
        
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Check if username or email already exists
        existing_user = AuthUser.query.filter(
            (AuthUser.username == username) | (AuthUser.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                error_msg = 'Username already exists'
            else:
                error_msg = 'Email already registered'
            
            return jsonify({
                'success': False,
                'message': error_msg
            }), 409
        
        # Create user
        user = AuthUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        # Assign role
        role = Role.query.filter_by(name=user_type).first()
        if not role:
            # Create default role if doesn't exist
            role = Role(name=user_type, description=f'Default {user_type} role')
            db.session.add(role)
            db.session.flush()  # Get role ID
        
        user.roles.append(role)
        
        db.session.add(user)
        db.session.commit()
        
        # Assign default subscription (Starter plan)
        starter_plan = SubscriptionPlan.query.filter_by(name='Starter').first()
        if starter_plan:
            subscription = UserSubscription(
                user_id=user.id,
                plan_id=starter_plan.id,
                status=SubscriptionStatus.ACTIVE.value,
                starts_at=datetime.utcnow(),
                expires_at=None  # Free plan doesn't expire
            )
            db.session.add(subscription)
            db.session.commit()
        
        # Log registration
        SecurityLog.log_security_event(
            SecurityEventType.USER_REGISTERED,
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={
                'username': username,
                'email': email,
                'user_type': user_type
            },
            severity='low'
        )
        
        # Auto-login after registration
        tokens = JWTAuthService.generate_tokens(user)
        csrf_token = SecurityService.generate_csrf_token(user.id)
        
        session['user_id'] = user.id
        session['csrf_token'] = csrf_token
        
        response_data = {
            'success': True,
            'message': 'Registration successful! Welcome to JobHunter!',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': [role.name for role in user.roles]
            },
            'tokens': tokens if tokens else None,
            'csrf_token': csrf_token
        }
        
        if not request.is_json:
            flash('Registration successful! Welcome to JobHunter!', 'success')
            
            # Redirect based on user type
            if user_type == 'consultancy':
                return redirect('/consultancy/dashboard')
            else:
                return redirect('/jobseeker/dashboard')
        
        return jsonify(response_data), 201
    
    except Exception as e:
        db.session.rollback()
        
        SecurityLog.log_security_event(
            SecurityEventType.SYSTEM_ERROR,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'endpoint': 'register', 'error': str(e)},
            severity='high'
        )
        
        return jsonify({
            'success': False,
            'message': 'An error occurred during registration'
        }), 500

@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    """User logout endpoint"""
    try:
        # Get token from header or form
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        user_id = session.get('user_id')
        
        # Logout user (blacklist token)
        if token:
            success, message = JWTAuthService.logout_user(token, user_id)
        
        # Clear session
        session.clear()
        
        if not request.is_json:
            flash('You have been logged out successfully', 'info')
            return redirect(url_for('auth.login'))
        
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during logout'
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh JWT token"""
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({
                'success': False,
                'message': 'Refresh token is required'
            }), 400
        
        tokens, message = JWTAuthService.refresh_token(refresh_token)
        
        if not tokens:
            return jsonify({
                'success': False,
                'message': message
            }), 401
        
        return jsonify({
            'success': True,
            'message': 'Token refreshed successfully',
            'tokens': tokens
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while refreshing token'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile():
    """Get current user profile"""
    try:
        user = request.current_user
        subscription = user.get_active_subscription()
        
        profile_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_activity': user.last_activity.isoformat() if user.last_activity else None,
            'roles': [{'id': role.id, 'name': role.name, 'description': role.description} for role in user.roles],
            'subscription': {
                'plan': subscription.plan.name if subscription else None,
                'status': subscription.status if subscription else None,
                'expires_at': subscription.expires_at.isoformat() if subscription and subscription.expires_at else None,
                'features': [
                    {
                        'key': feature.feature_key,
                        'value': feature.feature_value,
                        'is_boolean': feature.is_boolean
                    } for feature in subscription.plan.features
                ] if subscription else []
            }
        }
        
        return jsonify({
            'success': True,
            'user': profile_data
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error retrieving profile'
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required
@csrf_protect
@sanitize_inputs(['first_name', 'last_name', 'email'])
def update_profile():
    """Update user profile"""
    try:
        user = request.current_user
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        
        if 'email' in data:
            new_email = data['email'].strip().lower()
            
            # Check if email is already taken
            existing_user = AuthUser.query.filter(
                AuthUser.email == new_email,
                AuthUser.id != user.id
            ).first()
            
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email already in use'
                }), 409
            
            user.email = new_email
        
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.PROFILE_UPDATED,
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'updated_fields': list(data.keys())},
            severity='low'
        )
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error updating profile'
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required
@csrf_protect
def change_password():
    """Change user password"""
    try:
        user = request.current_user
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Validation
        if not current_password or not new_password or not confirm_password:
            return jsonify({
                'success': False,
                'message': 'All password fields are required'
            }), 400
        
        if not user.check_password(current_password):
            SecurityLog.log_security_event(
                SecurityEventType.PASSWORD_CHANGE_FAILED,
                user_id=user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={'reason': 'incorrect_current_password'},
                severity='medium'
            )
            
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 400
        
        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'New passwords do not match'
            }), 400
        
        if len(new_password) < 8:
            return jsonify({
                'success': False,
                'message': 'New password must be at least 8 characters long'
            }), 400
        
        # Set new password
        user.set_password(new_password)
        db.session.commit()
        
        SecurityLog.log_security_event(
            SecurityEventType.PASSWORD_CHANGED,
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            severity='medium'
        )
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error changing password'
        }), 500

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token validity"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({
                'valid': False,
                'message': 'Token is required'
            }), 400
        
        user, message = JWTAuthService.verify_token(token)
        
        if user:
            return jsonify({
                'valid': True,
                'user_id': user.id,
                'username': user.username,
                'roles': [role.name for role in user.roles]
            }), 200
        else:
            return jsonify({
                'valid': False,
                'message': message
            }), 401
    
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': 'Error verifying token'
        }), 500

# Health check endpoint
@auth_bp.route('/health')
def health_check():
    """Authentication service health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'authentication',
        'timestamp': datetime.utcnow().isoformat()
    }), 200