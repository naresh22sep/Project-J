"""
Authentication and Security Middleware
"""

from flask import request, session, g, current_app, jsonify, has_request_context
from functools import wraps
import time
import uuid
from datetime import datetime, timedelta
from app.services.auth_service import (
    JWTAuthService, SecurityService, AuthorizationService
)
from app.auth.auth_models import SecurityLog, SecurityEventType
import json

def get_safe_request_info():
    """Safely get request information when in request context"""
    if has_request_context():
        return {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'endpoint': request.endpoint,
            'method': request.method,
            'url': request.url
        }
    return {
        'ip_address': None,
        'user_agent': None,
        'endpoint': None,
        'method': None,
        'url': None
    }

class SecurityMiddleware:
    """Global security middleware for the application"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the middleware with the Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_appcontext(self.teardown)
    
    def before_request(self):
        """Run before each request"""
        # Set request start time for performance monitoring
        g.start_time = time.time()
        
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        # Set CSRF token for forms if needed
        if not session.get('csrf_token') and request.endpoint and \
           not request.endpoint.startswith('static'):
            user_id = None
            if hasattr(g, 'current_user') and g.current_user:
                user_id = g.current_user.id
            
            csrf_token = SecurityService.generate_csrf_token(user_id)
            session['csrf_token'] = csrf_token
            g.csrf_token = csrf_token
        else:
            g.csrf_token = session.get('csrf_token')
        
        # Check for JWT token and authenticate user
        self._authenticate_request()
        
        # Basic rate limiting check
        self._check_rate_limiting()
        
        # Log suspicious activity
        self._check_suspicious_activity()
    
    def after_request(self, response):
        """Run after each request"""
        # Add security headers
        response = self._add_security_headers(response)
        
        # Log request details
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            self._log_request(response.status_code, duration)
        
        return response
    
    def teardown(self, exception):
        """Cleanup after request"""
        # Log any unhandled exceptions
        if exception:
            user_id = None
            if hasattr(g, 'current_user') and g.current_user:
                user_id = g.current_user.id
            
            request_info = get_safe_request_info()
            SecurityLog.log_security_event(
                SecurityEventType.SYSTEM_ERROR,
                user_id=user_id,
                ip_address=request_info['ip_address'],
                user_agent=request_info['user_agent'],
                details={
                    'endpoint': request_info['endpoint'],
                    'method': request_info['method'],
                    'error': str(exception)
                },
                severity='high'
            )
    
    def _authenticate_request(self):
        """Authenticate the current request"""
        g.current_user = None
        
        # Skip authentication for static files and health checks
        if request.endpoint in ['static', 'health']:
            return
        
        # Check for JWT token
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]
            except (IndexError, AttributeError):
                pass
        
        # Try to authenticate with token
        if token:
            user, message = JWTAuthService.verify_token(token)
            if user:
                g.current_user = user
                # Update last activity
                user.update_last_activity()
            else:
                # Log failed token verification
                request_info = get_safe_request_info()
                SecurityLog.log_security_event(
                    SecurityEventType.INVALID_TOKEN,
                    ip_address=request_info['ip_address'],
                    user_agent=request_info['user_agent'],
                    details={'reason': message, 'token_preview': token[:10] + '...'},
                    severity='medium'
                )
    
    def _check_rate_limiting(self):
        """Basic rate limiting check"""
        # Simple IP-based rate limiting
        request_info = get_safe_request_info()
        ip_address = request_info['ip_address'] or 'unknown'
        
        if not SecurityService.check_rate_limit(f"ip:{ip_address}", limit=100, window=300):
            # Rate limit exceeded
            return jsonify({'error': 'Rate limit exceeded'}), 429
    
    def _check_suspicious_activity(self):
        """Check for suspicious activity patterns"""
        request_info = get_safe_request_info()
        user_agent = request_info['user_agent'] or ''
        ip_address = request_info['ip_address'] or 'unknown'
        
        # Check for common bot patterns
        suspicious_agents = [
            'scanner', 'crawler', 'bot', 'spider',
            'hack', 'exploit', 'sql', 'script'
        ]
        
        if any(agent in user_agent.lower() for agent in suspicious_agents):
            SecurityLog.log_security_event(
                SecurityEventType.SUSPICIOUS_ACTIVITY,
                user_id=getattr(g.current_user, 'id', None),
                ip_address=ip_address,
                user_agent=user_agent,
                details={
                    'type': 'suspicious_user_agent',
                    'endpoint': request.endpoint,
                    'method': request.method
                },
                severity='medium'
            )
        
        # Check for SQL injection patterns in query parameters
        sql_patterns = [
            'union select', 'drop table', 'insert into',
            '1=1', '1\' or \'1', 'script>', '<script'
        ]
        
        query_string = request.query_string.decode('utf-8').lower()
        for pattern in sql_patterns:
            if pattern in query_string:
                SecurityLog.log_security_event(
                    SecurityEventType.SQL_INJECTION_ATTEMPT,
                    user_id=getattr(g.current_user, 'id', None),
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={
                        'pattern': pattern,
                        'query_string': request.query_string.decode('utf-8')[:200],
                        'endpoint': request.endpoint
                    },
                    severity='high'
                )
                break
    
    def _add_security_headers(self, response):
        """Add security headers to response"""
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers['Content-Security-Policy'] = csp
        
        # Other security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove server header
        response.headers.pop('Server', None)
        
        return response
    
    def _log_request(self, status_code, duration):
        """Log request details for monitoring"""
        # Only log if it took too long or returned an error
        if duration > 2.0 or status_code >= 400:
            user_id = getattr(g.current_user, 'id', None)
            
            request_info = get_safe_request_info()
            SecurityLog.log_security_event(
                SecurityEventType.SLOW_REQUEST if duration > 2.0 else SecurityEventType.ERROR_RESPONSE,
                user_id=user_id,
                ip_address=request_info['ip_address'],
                user_agent=request_info['user_agent'],
                details={
                    'endpoint': request_info['endpoint'],
                    'method': request_info['method'],
                    'status_code': status_code,
                    'duration': round(duration, 3),
                    'url': request.url
                },
                severity='low' if duration > 2.0 else 'medium'
            )

class AuthMiddleware:
    """Authentication-specific middleware"""
    
    @staticmethod
    def require_auth():
        """Middleware to require authentication"""
        if not hasattr(g, 'current_user') or not g.current_user:
            # For browser requests, redirect to login
            if request.content_type != 'application/json' and 'application/json' not in request.headers.get('Accept', ''):
                from flask import redirect, url_for
                return redirect(url_for('auth.login'))
            
            # For API requests, return JSON
            return jsonify({
                'error': 'Authentication required',
                'message': 'You must be logged in to access this resource'
            }), 401
        
        return None
    
    @staticmethod
    def require_role(required_role):
        """Middleware to require specific role"""
        auth_result = AuthMiddleware.require_auth()
        if auth_result:
            return auth_result
        
        if not g.current_user.has_role(required_role):
            request_info = get_safe_request_info()
            SecurityLog.log_security_event(
                SecurityEventType.UNAUTHORIZED_ACCESS,
                user_id=g.current_user.id,
                ip_address=request_info['ip_address'],
                user_agent=request_info['user_agent'],
                details={
                    'required_role': required_role,
                    'user_roles': [role.name for role in g.current_user.roles],
                    'endpoint': request.endpoint
                },
                severity='medium'
            )
            
            # For browser requests, redirect to login
            if request.content_type != 'application/json' and 'application/json' not in request.headers.get('Accept', ''):
                from flask import redirect, url_for
                return redirect(url_for('auth.login'))
                
            return jsonify({
                'error': 'Insufficient privileges',
                'message': f'Role "{required_role}" is required'
            }), 403
        
        return None
    
    @staticmethod
    def require_permission(required_permission):
        """Middleware to require specific permission"""
        auth_result = AuthMiddleware.require_auth()
        if auth_result:
            return auth_result
        
        if not g.current_user.has_permission(required_permission):
            request_info = get_safe_request_info()
            SecurityLog.log_security_event(
                SecurityEventType.UNAUTHORIZED_ACCESS,
                user_id=g.current_user.id,
                ip_address=request_info['ip_address'],
                user_agent=request_info['user_agent'],
                details={
                    'required_permission': required_permission,
                    'endpoint': request.endpoint
                },
                severity='medium'
            )
            
            return jsonify({
                'error': 'Permission denied',
                'message': f'Permission "{required_permission}" is required'
            }), 403
        
        return None
    
    @staticmethod
    def superadmin_only():
        """Middleware for superadmin-only endpoints"""
        return AuthMiddleware.require_role('superadmin')

class CSRFMiddleware:
    """CSRF protection middleware"""
    
    @staticmethod
    def validate_csrf():
        """Validate CSRF token for state-changing requests"""
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            # Skip CSRF for API endpoints with JWT (already authenticated)
            if request.path.startswith('/api/') and hasattr(g, 'current_user') and g.current_user:
                return None
            
            csrf_token = (
                request.form.get('csrf_token') or 
                request.headers.get('X-CSRF-Token') or
                request.headers.get('X-CSRFToken')
            )
            
            user_id = getattr(g.current_user, 'id', None)
            
            if not SecurityService.validate_csrf_token(csrf_token, user_id):
                return jsonify({
                    'error': 'CSRF protection',
                    'message': 'Invalid or missing CSRF token'
                }), 403
        
        return None

# Utility function to create middleware stack
def create_middleware_stack(app):
    """Create and configure all middleware"""
    # Initialize security middleware
    security_middleware = SecurityMiddleware(app)
    
    # Register middleware functions
    @app.context_processor
    def inject_csrf_token():
        """Inject CSRF token into template context"""
        return dict(csrf_token=getattr(g, 'csrf_token', ''))
    
    @app.context_processor
    def inject_current_user():
        """Inject current user into template context"""
        return dict(current_user=getattr(g, 'current_user', None))
    
    # Error handlers for security-related errors
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'Insufficient privileges'
        }), 403
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    return security_middleware