"""
JWT Authentication Service with Security Features
"""

import jwt
import secrets
import hashlib
import bleach
from datetime import datetime, timedelta
from flask import request, current_app, session
from functools import wraps
from app.auth.auth_models import (
    AuthUser, JWTBlacklist, CSRFToken, SecurityLog, 
    SecurityEventType, SubscriptionStatus
)
from app import db
import re

class JWTAuthService:
    """JWT Authentication and Authorization Service"""
    
    @staticmethod
    def authenticate_user(username_or_email, password, ip_address=None, user_agent=None):
        """Authenticate user with enhanced security"""
        try:
            # Find user by username or email
            user = AuthUser.query.filter(
                (AuthUser.username == username_or_email) | 
                (AuthUser.email == username_or_email)
            ).first()
            
            if not user:
                SecurityLog.log_security_event(
                    SecurityEventType.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={'reason': 'user_not_found', 'attempted_login': username_or_email},
                    severity='medium'
                )
                return None, 'Invalid credentials'
            
            # Check if account is locked
            if user.is_account_locked():
                SecurityLog.log_security_event(
                    SecurityEventType.LOGIN_FAILED,
                    user_id=user.id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={'reason': 'account_locked'},
                    severity='high'
                )
                return None, 'Account is temporarily locked'
            
            # Check if account is active
            if not user.is_active:
                SecurityLog.log_security_event(
                    SecurityEventType.LOGIN_FAILED,
                    user_id=user.id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={'reason': 'account_inactive'},
                    severity='medium'
                )
                return None, 'Account is not active'
            
            # Verify password
            if not user.check_password(password):
                user.increment_login_attempts()
                SecurityLog.log_security_event(
                    SecurityEventType.LOGIN_FAILED,
                    user_id=user.id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={'reason': 'invalid_password', 'attempts': user.login_attempts},
                    severity='medium'
                )
                return None, 'Invalid credentials'
            
            # Successful authentication
            user.reset_login_attempts()
            SecurityLog.log_security_event(
                SecurityEventType.LOGIN_SUCCESS,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={'login_method': 'password'},
                severity='low'
            )
            
            return user, 'Authentication successful'
            
        except Exception as e:
            try:
                current_app.logger.error(f"Authentication error: {str(e)}")
            except RuntimeError:
                # Handle case where we're outside request context
                print(f"Authentication error: {str(e)}")
            return None, 'Authentication failed'
    
    @staticmethod
    def generate_tokens(user):
        """Generate access and refresh tokens"""
        try:
            access_token = user.generate_jwt_token('access', timedelta(hours=1))
            refresh_token = user.generate_jwt_token('refresh', timedelta(days=30))
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': 3600,  # 1 hour
                'user': user.to_dict()
            }
        except Exception as e:
            try:
                current_app.logger.error(f"Token generation error: {str(e)}")
            except RuntimeError:
                # Handle case where we're outside request context
                print(f"Token generation error: {str(e)}")
            return None
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'], 
                algorithms=['HS256'],
                audience='JobHunter-Users',
                issuer='JobHunter-Platform'
            )
            
            # Check if token is blacklisted
            jti = payload.get('jti')
            if jti and JWTBlacklist.query.filter_by(token_jti=jti).first():
                return None, 'Token is blacklisted'
            
            # Get user
            user_id = payload.get('user_id')
            user = AuthUser.query.get(user_id)
            
            if not user or not user.is_active:
                return None, 'User not found or inactive'
            
            return user, 'Token is valid'
            
        except jwt.ExpiredSignatureError:
            return None, 'Token has expired'
        except jwt.InvalidTokenError as e:
            return None, f'Invalid token: {str(e)}'
        except Exception as e:
            try:
                current_app.logger.error(f"Token verification error: {str(e)}")
            except RuntimeError:
                # Handle case where we're outside request context
                print(f"Token verification error: {str(e)}")
            return None, 'Token verification failed'
    
    @staticmethod
    def refresh_token(refresh_token):
        """Refresh access token"""
        try:
            user, message = JWTAuthService.verify_token(refresh_token)
            
            if not user:
                return None, message
            
            # Generate new tokens
            tokens = JWTAuthService.generate_tokens(user)
            
            if tokens:
                # Optionally blacklist old refresh token
                payload = jwt.decode(
                    refresh_token, 
                    current_app.config['SECRET_KEY'], 
                    algorithms=['HS256'],
                    options={"verify_exp": False}
                )
                
                if payload.get('jti'):
                    JWTAuthService.blacklist_token(
                        payload['jti'], 
                        user.id, 
                        payload.get('exp'),
                        'refresh',
                        'Token refreshed'
                    )
            
            return tokens, 'Token refreshed successfully'
            
        except Exception as e:
            try:
                current_app.logger.error(f"Token refresh error: {str(e)}")
            except RuntimeError:
                # Handle case where we're outside request context
                print(f"Token refresh error: {str(e)}")
            return None, 'Token refresh failed'
    
    @staticmethod
    def blacklist_token(jti, user_id, expires_at, token_type='access', reason='Logout'):
        """Add token to blacklist"""
        try:
            if isinstance(expires_at, (int, float)):
                expires_at = datetime.fromtimestamp(expires_at)
            
            blacklist_entry = JWTBlacklist(
                token_jti=jti,
                user_id=user_id,
                token_type=token_type,
                expires_at=expires_at,
                reason=reason
            )
            
            db.session.add(blacklist_entry)
            db.session.commit()
            
            return True
            
        except Exception as e:
            try:
                current_app.logger.error(f"Token blacklist error: {str(e)}")
            except RuntimeError:
                # Handle case where we're outside request context
                print(f"Token blacklist error: {str(e)}")
            return False
    
    @staticmethod
    def logout_user(token, user_id=None):
        """Logout user and blacklist token"""
        try:
            payload = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'], 
                algorithms=['HS256'],
                options={"verify_exp": False}
            )
            
            user_id = user_id or payload.get('user_id')
            jti = payload.get('jti')
            expires_at = payload.get('exp')
            
            if jti:
                JWTAuthService.blacklist_token(jti, user_id, expires_at, 'access', 'User logout')
            
            SecurityLog.log_security_event(
                SecurityEventType.LOGOUT,
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get('User-Agent') if request else None,
                severity='low'
            )
            
            return True, 'Logout successful'
            
        except Exception as e:
            try:
                current_app.logger.error(f"Logout error: {str(e)}")
            except RuntimeError:
                # Handle case where we're outside request context
                print(f"Logout error: {str(e)}")
            return False, 'Logout failed'

class SecurityService:
    """Security service for XSS and CSRF protection"""
    
    @staticmethod
    def sanitize_input(text, allowed_tags=None):
        """Sanitize user input to prevent XSS"""
        if not text:
            return text
        
        if allowed_tags is None:
            allowed_tags = []
        
        # Clean HTML and potentially malicious content
        clean_text = bleach.clean(
            text,
            tags=allowed_tags,
            attributes={},
            strip=True
        )
        
        # Log potential XSS attempts
        if clean_text != text:
            SecurityLog.log_security_event(
                SecurityEventType.XSS_ATTEMPT,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get('User-Agent') if request else None,
                details={
                    'original': text[:200],  # First 200 chars
                    'sanitized': clean_text[:200]
                },
                severity='high'
            )
        
        return clean_text
    
    @staticmethod
    def validate_csrf_token(token, user_id=None):
        """Validate CSRF token"""
        if not token:
            SecurityLog.log_security_event(
                SecurityEventType.CSRF_VIOLATION,
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get('User-Agent') if request else None,
                details={'reason': 'missing_token'},
                severity='high'
            )
            return False
        
        session_id = session.get('session_id') if session else None
        
        if CSRFToken.validate_token(token, user_id, session_id):
            return True
        
        SecurityLog.log_security_event(
            SecurityEventType.CSRF_VIOLATION,
            user_id=user_id,
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent') if request else None,
            details={'token': token[:10] + '...', 'reason': 'invalid_token'},
            severity='high'
        )
        
        return False
    
    @staticmethod
    def generate_csrf_token(user_id=None):
        """Generate CSRF token"""
        session_id = session.get('session_id') if session else None
        ip_address = request.remote_addr if request else None
        user_agent = request.headers.get('User-Agent') if request else None
        
        return CSRFToken.generate_token(user_id, session_id, ip_address, user_agent)
    
    @staticmethod
    def check_rate_limit(identifier, limit=60, window=3600):
        """Simple rate limiting check"""
        # This is a basic implementation - in production, use Redis
        # For now, we'll just log excessive requests
        
        # In a real implementation, you would check request count per identifier per time window
        # Here we'll just demonstrate the concept
        
        try:
            # Placeholder for rate limiting logic
            # You would typically use Redis or similar for this
            current_requests = 1  # This would be the actual count
            
            if current_requests > limit:
                SecurityLog.log_security_event(
                    SecurityEventType.RATE_LIMIT_EXCEEDED,
                    ip_address=request.remote_addr if request else None,
                    user_agent=request.headers.get('User-Agent') if request else None,
                    details={
                        'identifier': identifier,
                        'limit': limit,
                        'window': window,
                        'requests': current_requests
                    },
                    severity='medium'
                )
                return False
            
            return True
            
        except Exception as e:
            try:
                current_app.logger.error(f"Rate limit check error: {str(e)}")
            except RuntimeError:
                # Handle case where we're outside request context
                print(f"Rate limit check error: {str(e)}")
            return True  # Allow request if check fails

class AuthorizationService:
    """Authorization service for role and permission management"""
    
    @staticmethod
    def has_permission(user, permission_name, resource_context=None):
        """Check if user has specific permission"""
        if not user:
            return False
        
        # SuperAdmin has all permissions
        if user.has_role('superadmin'):
            return True
        
        # Check specific permission
        has_perm = user.has_permission(permission_name)
        
        if not has_perm:
            SecurityLog.log_security_event(
                SecurityEventType.UNAUTHORIZED_ACCESS,
                user_id=user.id,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get('User-Agent') if request else None,
                details={
                    'permission': permission_name,
                    'resource_context': resource_context
                },
                severity='medium'
            )
        
        return has_perm
    
    @staticmethod
    def has_role(user, role_name):
        """Check if user has specific role"""
        if not user:
            return False
        
        return user.has_role(role_name)
    
    @staticmethod
    def check_subscription_feature(user, feature_key):
        """Check if user's subscription includes specific feature"""
        if not user:
            return False
        
        subscription = user.get_active_subscription()
        
        if not subscription or subscription.status != SubscriptionStatus.ACTIVE.value:
            return False
        
        # Check if subscription has expired
        if subscription.expires_at and subscription.expires_at < datetime.utcnow():
            return False
        
        # Check if plan includes the feature
        feature = subscription.plan.features.filter_by(feature_key=feature_key).first()
        
        if not feature:
            return False
        
        if feature.is_boolean:
            return feature.feature_value.lower() == 'true'
        
        return True

# Decorators for authentication and authorization
def jwt_required(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return {'error': 'Invalid token format'}, 401
        
        if not token:
            return {'error': 'Token is missing'}, 401
        
        user, message = JWTAuthService.verify_token(token)
        
        if not user:
            return {'error': message}, 401
        
        # Add user to request context
        request.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_permission(permission_name):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(request, 'current_user', None)
            
            if not user:
                return {'error': 'Authentication required'}, 401
            
            if not AuthorizationService.has_permission(user, permission_name):
                return {'error': f'Permission denied: {permission_name}'}, 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_role(role_name):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(request, 'current_user', None)
            
            if not user:
                return {'error': 'Authentication required'}, 401
            
            if not AuthorizationService.has_role(user, role_name):
                return {'error': f'Role required: {role_name}'}, 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_subscription_feature(feature_key):
    """Decorator to require subscription feature"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(request, 'current_user', None)
            
            if not user:
                return {'error': 'Authentication required'}, 401
            
            if not AuthorizationService.check_subscription_feature(user, feature_key):
                return {'error': f'Subscription upgrade required for feature: {feature_key}'}, 402
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def csrf_protect(f):
    """Decorator to protect against CSRF attacks"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            csrf_token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            
            # Get current user from Flask g object or request
            from flask import g
            user = getattr(g, 'current_user', None) or getattr(request, 'current_user', None)
            user_id = user.id if user else None
            
            # For session-based CSRF (when no user), validate against session token
            if not csrf_token:
                return {'error': 'CSRF token validation failed'}, 403
                
            # Session-based CSRF validation (fallback for when user_id is None)
            if not user_id:
                session_csrf = session.get('csrf_token')
                if csrf_token != session_csrf:
                    return {'error': 'CSRF token validation failed'}, 403
            else:
                # User-based CSRF validation
                if not SecurityService.validate_csrf_token(csrf_token, user_id):
                    return {'error': 'CSRF token validation failed'}, 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def sanitize_inputs(fields=None):
    """Decorator to sanitize form inputs"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.is_json:
                data = request.get_json()
                if data and isinstance(data, dict):
                    for key, value in data.items():
                        if fields is None or key in fields:
                            if isinstance(value, str):
                                data[key] = SecurityService.sanitize_input(value)
            
            elif request.form:
                # Create a mutable copy of form data
                sanitized_form = {}
                for key, value in request.form.items():
                    if fields is None or key in fields:
                        if isinstance(value, str):
                            sanitized_form[key] = SecurityService.sanitize_input(value)
                        else:
                            sanitized_form[key] = value
                    else:
                        sanitized_form[key] = value
                
                # Replace form data (this is a simplified approach)
                request.sanitized_form = sanitized_form
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator