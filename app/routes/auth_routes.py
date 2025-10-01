"""
Authentication Routes - Login, Registration, JWT Management
"""

import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from app.services.auth_service import (
    JWTAuthService, SecurityService, AuthorizationService,
    jwt_required, csrf_protect, sanitize_inputs
)
from app.auth.auth_models import (
    AuthUser, Role, UserRole, UserSubscription, SubscriptionPlan, 
    SecurityLog, SecurityEventType, SubscriptionStatus
)
from app import db
from datetime import datetime
import re

# Configure authentication logger
auth_logger = logging.getLogger('auth_system')
auth_logger.setLevel(logging.DEBUG)

# Create file handler for authentication logs
log_handler = logging.FileHandler('app/logs/auth_debug.log')
log_handler.setLevel(logging.DEBUG)

# Create console handler for immediate feedback
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
)
log_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
if not auth_logger.handlers:
    auth_logger.addHandler(log_handler)
    auth_logger.addHandler(console_handler)

# Create blueprint for general auth (will be unused)
auth_bp = Blueprint('auth', __name__)

# Create role-specific auth blueprints
superadmin_auth_bp = Blueprint('superadmin_auth', __name__, url_prefix='/superadmin')
admin_auth_bp = Blueprint('admin_auth', __name__, url_prefix='/admin')
jobseeker_auth_bp = Blueprint('jobseeker_auth', __name__, url_prefix='/jobseeker')
consultancy_auth_bp = Blueprint('consultancy_auth', __name__, url_prefix='/consultancy')

def create_role_login_route(role_name, dashboard_url):
    """Factory function to create role-specific login routes with detailed logging"""
    
    def login():
        """Role-specific login endpoint with comprehensive logging"""
        
        # Log the request start
        auth_logger.info(f"=== {role_name.upper()} LOGIN REQUEST START ===")
        auth_logger.info(f"Request Method: {request.method}")
        auth_logger.info(f"Request URL: {request.url}")
        auth_logger.info(f"User Agent: {request.headers.get('User-Agent', 'Unknown')}")
        auth_logger.info(f"Remote Address: {request.remote_addr}")
        auth_logger.info(f"Role: {role_name}")
        auth_logger.info(f"Dashboard URL: {dashboard_url}")
        
        if request.method == 'GET':
            auth_logger.info("Processing GET request - Rendering login form")
            # Return role-specific login form
            try:
                result = render_template('auth/login.html', role=role_name)
                auth_logger.info("Template rendered successfully")
                auth_logger.info(f"=== {role_name.upper()} LOGIN GET REQUEST END ===")
                return result
            except Exception as template_error:
                auth_logger.error(f"Template rendering error: {str(template_error)}")
                raise template_error
        
        try:
            auth_logger.info("Processing POST request - Login attempt")
            
            # Get sanitized data
            auth_logger.debug("Extracting form data")
            data = request.get_json() if request.is_json else request.form
            auth_logger.debug(f"Request is JSON: {request.is_json}")
            auth_logger.debug(f"Form keys: {list(data.keys()) if data else 'No data'}")
            
            username = data.get('username', '').strip()
            password = data.get('password', '')
            remember_me = data.get('remember_me', False)
            
            auth_logger.info(f"Login attempt for username: '{username}'")
            auth_logger.debug(f"Password provided: {'Yes' if password else 'No'}")
            auth_logger.debug(f"Remember me: {remember_me}")
            
            # Validation
            auth_logger.info("Starting form validation")
            if not username or not password:
                auth_logger.warning("Validation failed: Missing username or password")
                flash('Username and password are required', 'error')
                return render_template('auth/login.html', role=role_name)
            
            auth_logger.info("Form validation passed")
            
            # Get client info
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            auth_logger.info(f"Client info - IP: {ip_address}, User-Agent: {user_agent[:50]}...")
            
            # Authenticate user
            auth_logger.info("Starting user authentication via JWTAuthService")
            try:
                user, message = JWTAuthService.authenticate_user(
                    username, password, ip_address, user_agent
                )
                auth_logger.info(f"Authentication result: User={'Found' if user else 'Not found'}, Message='{message}'")
            except Exception as auth_error:
                auth_logger.error(f"Authentication service error: {str(auth_error)}")
                flash('Authentication service error', 'error')
                return render_template('auth/login.html', role=role_name)
            
            if not user:
                auth_logger.warning(f"Authentication failed for user: {username}")
                flash(message, 'error')
                return render_template('auth/login.html', role=role_name)
            
            # Check if user has the required role for this login endpoint
            auth_logger.info("Checking user roles")
            try:
                user_roles = [role.name for role in user.get_roles()]
                auth_logger.info(f"User roles: {user_roles}")
            except Exception as role_error:
                auth_logger.error(f"Error getting user roles: {str(role_error)}")
                user_roles = []
            
            if role_name not in user_roles and role_name != 'general':
                auth_logger.warning(f"Access denied: User {username} does not have {role_name} role")
                flash(f'Access denied. You do not have {role_name} privileges.', 'error')
                return render_template('auth/login.html', role=role_name)
            
            # Generate tokens
            auth_logger.info("Generating JWT tokens")
            try:
                tokens = JWTAuthService.generate_tokens(user)
                auth_logger.info(f"Token generation result: {'Success' if tokens else 'Failed'}")
            except Exception as token_error:
                auth_logger.error(f"Token generation error: {str(token_error)}")
                tokens = None
            
            if not tokens:
                auth_logger.error("Failed to generate authentication tokens")
                flash('Failed to generate authentication tokens', 'error')
                return render_template('auth/login.html', role=role_name)
            
            # Store session info
            auth_logger.info("Storing session information")
            session['user_id'] = user.id
            session['role'] = role_name
            auth_logger.debug(f"Session user_id: {user.id}, role: {role_name}")
            
            flash('Login successful!', 'success')
            auth_logger.info(f"Login successful for user: {username}")
            
            # Redirect to role-specific dashboard
            auth_logger.info("Determining redirect destination")
            if role_name == 'superadmin':
                redirect_url = f'/superadmin/dashboard'
            elif role_name == 'admin':
                redirect_url = f'/admin/dashboard'
            elif role_name == 'consultancy':
                redirect_url = f'/consultancy/dashboard'
            elif role_name == 'jobseeker':
                redirect_url = f'/jobseeker/dashboard'
            else:
                # Fallback - redirect based on user's highest role
                auth_logger.info("Using fallback role-based redirect")
                if user.has_role('superadmin'):
                    redirect_url = '/superadmin/dashboard'
                elif user.has_role('admin'):
                    redirect_url = '/admin/dashboard'
                elif user.has_role('consultancy'):
                    redirect_url = '/consultancy/dashboard'
                else:
                    redirect_url = '/jobseeker/dashboard'
            
            auth_logger.info(f"Redirecting to: {redirect_url}")
            auth_logger.info(f"=== {role_name.upper()} LOGIN POST SUCCESS END ===")
            return redirect(redirect_url)
        
        except Exception as e:
            auth_logger.error(f"Unexpected error in {role_name}_login: {str(e)}")
            auth_logger.error(f"Error type: {type(e).__name__}")
            import traceback
            auth_logger.error(f"Traceback: {traceback.format_exc()}")
            
            SecurityLog.log_security_event(
                SecurityEventType.SYSTEM_ERROR,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                details={'endpoint': f'{role_name}_login', 'error': str(e)},
                severity='high'
            )
            
            flash('An error occurred during login', 'error')
            auth_logger.error(f"=== {role_name.upper()} LOGIN ERROR END ===")
            return render_template('auth/login.html', role=role_name)
    
    return login

# SuperAdmin Login
@superadmin_auth_bp.route('/auth/login', methods=['GET', 'POST'])
def superadmin_login():
    """SuperAdmin login endpoint with detailed logging"""
    
    # Log the request start
    auth_logger.info("=== SUPERADMIN LOGIN REQUEST START ===")
    auth_logger.info(f"Request Method: {request.method}")
    auth_logger.info(f"Request URL: {request.url}")
    auth_logger.info(f"User Agent: {request.headers.get('User-Agent', 'Unknown')}")
    auth_logger.info(f"Remote Address: {request.remote_addr}")
    auth_logger.info(f"Content Type: {request.content_type}")
    auth_logger.info(f"Request Headers: {dict(request.headers)}")
    
    try:
        role_name = 'superadmin'
        dashboard_url = '/superadmin/dashboard'
        
        auth_logger.debug(f"Role: {role_name}")
        auth_logger.debug(f"Dashboard URL: {dashboard_url}")
        
        if request.method == 'GET':
            auth_logger.info("Processing GET request - Rendering login form")
            auth_logger.debug("Attempting to render auth/login.html template")
            
            # Return role-specific login form
            try:
                result = render_template('auth/login.html', role=role_name)
                auth_logger.info("Template rendered successfully")
                auth_logger.info("=== SUPERADMIN LOGIN GET REQUEST END ===")
                return result
            except Exception as template_error:
                auth_logger.error(f"Template rendering error: {str(template_error)}")
                raise template_error
        
        # Handle POST request
        auth_logger.info("Processing POST request - Login attempt")
        
        # Extract form data
        auth_logger.debug("Extracting form data")
        data = request.get_json() if request.is_json else request.form
        auth_logger.debug(f"Request is JSON: {request.is_json}")
        auth_logger.debug(f"Form keys: {list(data.keys()) if data else 'No data'}")
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        auth_logger.info(f"Login attempt for username: '{username}'")
        auth_logger.debug(f"Password provided: {'Yes' if password else 'No'}")
        auth_logger.debug(f"Password length: {len(password) if password else 0}")
        
        # Basic validation
        auth_logger.info("Starting form validation")
        if not username or not password:
            auth_logger.warning("Validation failed: Missing username or password")
            auth_logger.debug(f"Username empty: {not username}")
            auth_logger.debug(f"Password empty: {not password}")
            flash('Username and password are required', 'error')
            return render_template('auth/login.html', role=role_name)
        
        auth_logger.info("Form validation passed")
        
        # Simple authentication check (hardcoded for demo/testing)
        auth_logger.info("Starting authentication check")
        auth_logger.debug(f"Checking credentials for user: {username}")
        auth_logger.debug("Using hardcoded credentials: superadmin / SuperAdmin@2024")
        
        if username == 'superadmin' and password == 'SuperAdmin@2024':
            auth_logger.info("Authentication successful - Credentials match")
            
            # Store session info
            auth_logger.info("Setting session data")
            session['user_id'] = 1
            session['role'] = role_name
            auth_logger.debug(f"Session user_id: {session.get('user_id')}")
            auth_logger.debug(f"Session role: {session.get('role')}")
            
            # Success flash message
            flash('Login successful!', 'success')
            auth_logger.info("Flash message set: Login successful!")
            
            # Redirect to dashboard
            auth_logger.info(f"Redirecting to dashboard: {dashboard_url}")
            auth_logger.info("=== SUPERADMIN LOGIN POST SUCCESS END ===")
            return redirect(dashboard_url)
            
        else:
            auth_logger.warning(f"Authentication failed for user: {username}")
            auth_logger.debug(f"Expected username: 'superadmin', got: '{username}'")
            auth_logger.debug(f"Password match: {password == 'SuperAdmin@2024'}")
            
            flash('Invalid credentials', 'error')
            auth_logger.info("Flash message set: Invalid credentials")
            auth_logger.info("=== SUPERADMIN LOGIN POST FAILED END ===")
            return render_template('auth/login.html', role=role_name)
            
    except Exception as e:
        auth_logger.error(f"Unexpected error in superadmin_login: {str(e)}")
        auth_logger.error(f"Error type: {type(e).__name__}")
        import traceback
        auth_logger.error(f"Traceback: {traceback.format_exc()}")
        
        flash(f'Login error: {str(e)}', 'error')
        auth_logger.info("Flash message set: Login error")
        auth_logger.error("=== SUPERADMIN LOGIN ERROR END ===")
        return render_template('auth/login.html', role='superadmin')

# Admin Login  
@admin_auth_bp.route('/auth/login', methods=['GET', 'POST'])
@sanitize_inputs(['username', 'password'])
def admin_login():
    return create_role_login_route('admin', '/admin/dashboard')()

# Jobseeker Login
@jobseeker_auth_bp.route('/login', methods=['GET', 'POST'])
@sanitize_inputs(['username', 'password'])
def jobseeker_login():
    return create_role_login_route('jobseeker', '/jobseeker/dashboard')()

# Consultancy Login
@consultancy_auth_bp.route('/login', methods=['GET', 'POST'])
@sanitize_inputs(['username', 'password'])
def consultancy_login():
    return create_role_login_route('consultancy', '/consultancy/dashboard')()

# Legacy login route (deprecated but kept for compatibility)
@auth_bp.route('/login', methods=['GET', 'POST'])
@sanitize_inputs(['username', 'password'])
def legacy_login():
    """Legacy login route - redirects to appropriate role-specific login"""
    if request.method == 'GET':
        # Redirect to superadmin login by default
        return redirect('/superadmin/auth/login')
    
    # For POST, try to authenticate and redirect to appropriate role login
    username = request.form.get('username', '').strip()
    
    if username:
        # Try to find user and redirect to their role-specific login
        user = AuthUser.query.filter(
            (AuthUser.username == username) | (AuthUser.email == username)
        ).first()
        
        if user:
            roles = user.get_roles()
            if any(role.name == 'superadmin' for role in roles):
                return redirect('/superadmin/auth/login')
            elif any(role.name == 'admin' for role in roles):
                return redirect('/admin/auth/login')
            elif any(role.name == 'consultancy' for role in roles):
                return redirect('/consultancy/login')
            else:
                return redirect('/jobseeker/login')
    
    # Default fallback
    return redirect('/superadmin/auth/login')

@auth_bp.route('/register', methods=['GET', 'POST'])
@csrf_protect
@sanitize_inputs(['username', 'email', 'first_name', 'last_name', 'password'])
def register():
    """User registration endpoint with detailed logging"""
    
    # Log the request start
    auth_logger.info("=== USER REGISTRATION REQUEST START ===")
    auth_logger.info(f"Request Method: {request.method}")
    auth_logger.info(f"Request URL: {request.url}")
    auth_logger.info(f"User Agent: {request.headers.get('User-Agent', 'Unknown')}")
    auth_logger.info(f"Remote Address: {request.remote_addr}")
    
    if request.method == 'GET':
        auth_logger.info("Processing GET request - Rendering registration form")
        try:
            result = render_template('auth/register.html')
            auth_logger.info("Registration template rendered successfully")
            auth_logger.info("=== USER REGISTRATION GET REQUEST END ===")
            return result
        except Exception as template_error:
            auth_logger.error(f"Template rendering error: {str(template_error)}")
            raise template_error
    
    try:
        auth_logger.info("Processing POST request - Registration attempt")
        
        data = request.get_json() if request.is_json else request.form
        auth_logger.debug(f"Request is JSON: {request.is_json}")
        auth_logger.debug(f"Form keys: {list(data.keys()) if data else 'No data'}")
        
        # Get sanitized data
        username = data.get('username', '').strip().lower()
        email = data.get('email', '').strip().lower()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        user_type = data.get('user_type', 'jobseeker')  # Default role
        
        auth_logger.info(f"Registration attempt for username: '{username}', email: '{email}'")
        auth_logger.debug(f"First name: '{first_name}', Last name: '{last_name}'")
        auth_logger.debug(f"User type: '{user_type}'")
        auth_logger.debug(f"Password provided: {'Yes' if password else 'No'}")
        auth_logger.debug(f"Confirm password provided: {'Yes' if confirm_password else 'No'}")
        
        # Validation
        auth_logger.info("Starting registration validation")
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
        
        auth_logger.debug(f"Validation errors count: {len(errors)}")
        if errors:
            auth_logger.warning(f"Registration validation failed: {errors}")
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        auth_logger.info("Registration validation passed")
        
        # Check if username or email already exists
        auth_logger.info("Checking for existing users")
        existing_user = AuthUser.query.filter(
            (AuthUser.username == username) | (AuthUser.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                error_msg = 'Username already exists'
                auth_logger.warning(f"Registration failed: Username '{username}' already exists")
            else:
                error_msg = 'Email already registered'
                auth_logger.warning(f"Registration failed: Email '{email}' already registered")
            
            return jsonify({
                'success': False,
                'message': error_msg
            }), 409
        
        auth_logger.info("No existing user conflicts found")
        
        # Create user
        auth_logger.info("Creating new user")
        user = AuthUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        auth_logger.debug(f"User object created with ID: {user.id}")
        
        # Assign role
        auth_logger.info(f"Assigning role: {user_type}")
        role = Role.query.filter_by(name=user_type).first()
        if not role:
            auth_logger.info(f"Role '{user_type}' not found, creating new role")
            # Create default role if doesn't exist
            role = Role(name=user_type, description=f'Default {user_type} role')
            db.session.add(role)
            db.session.flush()  # Get role ID
            auth_logger.debug(f"Created new role with ID: {role.id}")
        
        user.user_roles.append(UserRole(user_id=user.id, role_id=role.id))
        auth_logger.debug(f"Role '{user_type}' assigned to user")
        
        db.session.add(user)
        db.session.commit()
        auth_logger.info(f"User '{username}' successfully created and saved to database")
        
        # Assign default subscription (Starter plan)
        auth_logger.info("Assigning default subscription")
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
            auth_logger.info("Default subscription assigned successfully")
        else:
            auth_logger.warning("Starter plan not found, skipping subscription assignment")
        
        # Log registration
        auth_logger.info("Logging registration event")
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
        auth_logger.info("Performing auto-login after registration")
        try:
            tokens = JWTAuthService.generate_tokens(user)
            csrf_token = SecurityService.generate_csrf_token(user.id)
            auth_logger.info("Auto-login tokens generated successfully")
        except Exception as token_error:
            auth_logger.error(f"Auto-login token generation error: {str(token_error)}")
            tokens = None
            csrf_token = None
        
        session['user_id'] = user.id
        session['csrf_token'] = csrf_token
        auth_logger.debug(f"Session data set - user_id: {user.id}")
        
        response_data = {
            'success': True,
            'message': 'Registration successful! Welcome to JobHunter!',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': [role.name for role in user.get_roles()]
            },
            'tokens': tokens if tokens else None,
            'csrf_token': csrf_token
        }
        
        if not request.is_json:
            flash('Registration successful! Welcome to JobHunter!', 'success')
            auth_logger.info("Flash message set for HTML response")
            
            # Redirect based on user type
            if user_type == 'consultancy':
                redirect_url = '/consultancy/dashboard'
            else:
                redirect_url = '/jobseeker/dashboard'
            
            auth_logger.info(f"Redirecting to: {redirect_url}")
            auth_logger.info("=== USER REGISTRATION POST SUCCESS END ===")
            return redirect(redirect_url)
        
        auth_logger.info("Returning JSON response")
        auth_logger.info("=== USER REGISTRATION POST SUCCESS END ===")
        return jsonify(response_data), 201
    
    except Exception as e:
        auth_logger.error(f"Unexpected error in registration: {str(e)}")
        auth_logger.error(f"Error type: {type(e).__name__}")
        import traceback
        auth_logger.error(f"Traceback: {traceback.format_exc()}")
        
        db.session.rollback()
        
        SecurityLog.log_security_event(
            SecurityEventType.SYSTEM_ERROR,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details={'endpoint': 'register', 'error': str(e)},
            severity='high'
        )
        
        auth_logger.error("=== USER REGISTRATION ERROR END ===")
        return jsonify({
            'success': False,
            'message': 'An error occurred during registration'
        }), 500

@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    """User logout endpoint with detailed logging"""
    
    # Log the request start
    auth_logger.info("=== USER LOGOUT REQUEST START ===")
    auth_logger.info(f"Request Method: {request.method}")
    auth_logger.info(f"Request URL: {request.url}")
    auth_logger.info(f"User Agent: {request.headers.get('User-Agent', 'Unknown')}")
    auth_logger.info(f"Remote Address: {request.remote_addr}")
    
    try:
        # Get token from header or form
        auth_logger.info("Extracting authentication token")
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                auth_logger.debug("Token found in Authorization header")
            else:
                auth_logger.debug("Authorization header present but not Bearer format")
        else:
            auth_logger.debug("No Authorization header found")
        
        user_id = session.get('user_id')
        auth_logger.info(f"Session user_id: {user_id}")
        auth_logger.debug(f"Session keys: {list(session.keys())}")
        
        # Logout user (blacklist token)
        if token:
            auth_logger.info("Attempting to logout user via JWT service")
            try:
                success, message = JWTAuthService.logout_user(token, user_id)
                auth_logger.info(f"JWT logout result: Success={success}, Message='{message}'")
            except Exception as logout_error:
                auth_logger.error(f"JWT logout service error: {str(logout_error)}")
        else:
            auth_logger.info("No token to blacklist, proceeding with session logout only")
        
        # Clear session
        auth_logger.info("Clearing user session")
        session_keys_before = list(session.keys())
        auth_logger.debug(f"Session keys before clear: {session_keys_before}")
        session.clear()
        auth_logger.info("Session cleared successfully")
        
        if not request.is_json:
            auth_logger.info("Setting flash message for HTML response")
            flash('You have been logged out successfully', 'info')
            auth_logger.info("Redirecting to superadmin login page")
            auth_logger.info("=== USER LOGOUT SUCCESS END ===")
            return redirect('/superadmin/auth/login')
        
        auth_logger.info("Returning JSON logout response")
        auth_logger.info("=== USER LOGOUT SUCCESS END ===")
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
    
    except Exception as e:
        auth_logger.error(f"Unexpected error in logout: {str(e)}")
        auth_logger.error(f"Error type: {type(e).__name__}")
        import traceback
        auth_logger.error(f"Traceback: {traceback.format_exc()}")
        
        auth_logger.error("=== USER LOGOUT ERROR END ===")
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
            'roles': [{'id': role.id, 'name': role.name, 'description': role.description} for role in user.get_roles()],
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
                'roles': [role.name for role in user.get_roles()]
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