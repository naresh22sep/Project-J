"""
Authentication Models for JWT, ACL, and Subscription Management
"""

from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
import uuid
import secrets
import json
from enum import Enum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    SUSPENDED = "suspended"

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"
    PENDING = "pending"

class SecurityEventType(Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PASSWORD_RESET = "password_reset"
    PASSWORD_CHANGED = "password_changed"
    PASSWORD_CHANGE_FAILED = "password_change_failed"
    USER_REGISTERED = "user_registered"
    USER_MODIFIED = "user_modified"
    PROFILE_UPDATED = "profile_updated"
    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_REVOKED = "permission_revoked"
    ROLE_ASSIGNED = "role_assigned"
    ROLE_REMOVED = "role_removed"
    ROLE_CREATED = "role_created"
    ROLE_MODIFIED = "role_modified"
    PERMISSION_CREATED = "permission_created"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_UNLOCKED = "account_unlocked"
    SUBSCRIPTION_CHANGED = "subscription_changed"
    SUBSCRIPTION_MODIFIED = "subscription_modified"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    XSS_ATTEMPT = "xss_attempt"
    CSRF_VIOLATION = "csrf_violation"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    INVALID_TOKEN = "invalid_token"
    SQL_INJECTION_ATTEMPT = "sql_injection_attempt"
    SLOW_REQUEST = "slow_request"
    ERROR_RESPONSE = "error_response"
    DATA_EXPORT = "data_export"
    SYSTEM_ERROR = "system_error"
    SYSTEM_MAINTENANCE = "system_maintenance"

# Enhanced User Model
class AuthUser(UserMixin, db.Model):
    """Enhanced User model with authentication and authorization features"""
    __tablename__ = 'auth_users'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(500))
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(255))
    password_reset_token = db.Column(db.String(255))
    password_reset_expires = db.Column(db.DateTime)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(255))
    last_login = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_roles = db.relationship('UserRole', backref='user', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='UserRole.user_id')
    user_permissions = db.relationship('UserPermission', backref='user', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='UserPermission.user_id')
    subscriptions = db.relationship('UserSubscription', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    security_logs = db.relationship('SecurityLog', backref='user', lazy='dynamic')
    jwt_tokens = db.relationship('JWTBlacklist', backref='user', lazy='dynamic')
    csrf_tokens = db.relationship('CSRFToken', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def is_account_locked(self):
        """Check if account is locked"""
        if self.account_locked_until:
            return datetime.utcnow() < self.account_locked_until
        return False
    
    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration"""
        self.account_locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.login_attempts = 0
        db.session.commit()
    
    def unlock_account(self):
        """Unlock account"""
        self.account_locked_until = None
        self.login_attempts = 0
        db.session.commit()
    
    def increment_login_attempts(self):
        """Increment failed login attempts"""
        self.login_attempts = (self.login_attempts or 0) + 1
        if self.login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account()
        db.session.commit()
    
    def reset_login_attempts(self):
        """Reset login attempts on successful login"""
        self.login_attempts = 0
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def update_last_activity(self):
        """Update user's last activity timestamp"""
        self.updated_at = datetime.utcnow()
        try:
            db.session.commit()
        except Exception:
            # If commit fails, rollback to prevent session issues
            db.session.rollback()
    
    def has_role(self, role_name):
        """Check if user has specific role"""
        return self.user_roles.join(Role).filter(Role.name == role_name).first() is not None
    
    def has_permission(self, permission_name):
        """Check if user has specific permission (via role or direct assignment)"""
        # Check direct permissions first
        direct_perm = self.user_permissions.join(Permission).filter(
            Permission.name == permission_name,
            UserPermission.granted == True
        ).first()
        
        if direct_perm:
            return True
        
        # Check role-based permissions
        role_perm = db.session.query(Permission).join(RolePermission).join(Role).join(UserRole, Role.id == UserRole.role_id).filter(
            UserRole.user_id == self.id,
            UserRole.is_active == True,
            Permission.name == permission_name
        ).first()
        
        return role_perm is not None
    
    def get_roles(self):
        """Get all user roles"""
        return db.session.query(Role).join(UserRole, Role.id == UserRole.role_id).filter(
            UserRole.user_id == self.id,
            UserRole.is_active == True
        ).all()
    
    def get_permissions(self):
        """Get all user permissions"""
        # Get role-based permissions
        role_permissions = db.session.query(Permission).join(RolePermission).join(Role).join(UserRole, Role.id == UserRole.role_id).filter(
            UserRole.user_id == self.id,
            UserRole.is_active == True
        ).all()
        
        # Get direct permissions
        direct_permissions = db.session.query(Permission).join(UserPermission).filter(
            UserPermission.user_id == self.id,
            UserPermission.granted == True
        ).all()
        
        # Combine and deduplicate
        all_permissions = {perm.name: perm for perm in role_permissions + direct_permissions}
        return list(all_permissions.values())
    
    def get_active_subscription(self):
        """Get user's active subscription"""
        return self.subscriptions.filter(
            UserSubscription.status == SubscriptionStatus.ACTIVE.value
        ).first()
    
    def generate_jwt_token(self, token_type='access', expires_delta=None):
        """Generate JWT token"""
        if expires_delta is None:
            expires_delta = timedelta(hours=1) if token_type == 'access' else timedelta(days=30)
        
        payload = {
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': [role.name for role in self.get_roles()],
            'permissions': [perm.name for perm in self.get_permissions()],
            'type': token_type,
            'exp': datetime.utcnow() + expires_delta,
            'iat': datetime.utcnow(),
            'iss': 'JobHunter-Platform',
            'aud': 'JobHunter-Users',
            'jti': str(uuid.uuid4())
        }
        
        # Use app secret key safely
        try:
            from flask import current_app
            secret_key = current_app.config['SECRET_KEY']
        except RuntimeError:
            # Fallback if no request context (during initialization)
            secret_key = 'dev-secret-key-change-in-production-2024'  # This should match config
        
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'avatar_url': self.avatar_url,
            'email_verified': self.email_verified,
            'two_factor_enabled': self.two_factor_enabled,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'roles': [role.name for role in self.get_roles()],
            'permissions': [perm.name for perm in self.get_permissions()]
        }
        
        if include_sensitive:
            subscription = self.get_active_subscription()
            data.update({
                'login_attempts': self.login_attempts,
                'account_locked': self.is_account_locked(),
                'subscription': {
                    'plan': subscription.plan.name if subscription else 'starter',
                    'status': subscription.status if subscription else 'inactive',
                    'expires_at': subscription.expires_at.isoformat() if subscription and subscription.expires_at else None
                }
            })
        
        return data

class Role(db.Model):
    """Role model for RBAC"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    level = db.Column(db.Integer, default=0, nullable=False)
    is_system_role = db.Column(db.Boolean, default=False)
    permissions_json = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_roles = db.relationship('UserRole', backref='role', lazy='dynamic')
    role_permissions = db.relationship('RolePermission', backref='role', lazy='dynamic', cascade='all, delete-orphan')
    
    # Many-to-many relationship with Permission through RolePermission
    permissions = db.relationship(
        'Permission',
        secondary='role_permissions',
        backref=db.backref('roles', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def get_users(self):
        """Get all users assigned to this role"""
        from app.auth.auth_models import AuthUser
        return AuthUser.query.join(UserRole, UserRole.user_id == AuthUser.id).filter(
            UserRole.role_id == self.id, 
            UserRole.is_active == True
        ).all()
    
    def get_users_count(self):
        """Get count of users assigned to this role"""
        from app.auth.auth_models import AuthUser
        return AuthUser.query.join(UserRole, UserRole.user_id == AuthUser.id).filter(
            UserRole.role_id == self.id, 
            UserRole.is_active == True
        ).count()
    
    def is_locked(self):
        """Check if role is locked (has users or is system role)"""
        return self.is_system_role or self.get_users_count() > 0
    
    def can_be_deleted(self):
        """Check if role can be deleted"""
        return not self.is_system_role and self.get_users_count() == 0
    
    def can_be_edited(self):
        """Check if role can be edited (only system roles and roles with users are restricted)"""
        return not self.is_system_role and self.get_users_count() == 0

class UserRole(db.Model):
    """User-Role relationship"""
    __tablename__ = 'user_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('auth_users.id'))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assigner = db.relationship('AuthUser', foreign_keys=[assigned_by], backref='assigned_roles')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'role_id'),)

class Permission(db.Model):
    """Permission model"""
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    display_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    conditions_json = db.Column(db.JSON)
    is_system_permission = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    role_permissions = db.relationship('RolePermission', backref='permission', lazy='dynamic')
    user_permissions = db.relationship('UserPermission', backref='permission', lazy='dynamic')

class RolePermission(db.Model):
    """Role-Permission relationship"""
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    granted_by = db.Column(db.Integer, db.ForeignKey('auth_users.id'))
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    granter = db.relationship('AuthUser', foreign_keys=[granted_by], backref='granted_role_permissions')
    
    __table_args__ = (db.UniqueConstraint('role_id', 'permission_id'),)

class UserPermission(db.Model):
    """User-Permission relationship (direct assignments)"""
    __tablename__ = 'user_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    granted = db.Column(db.Boolean, default=True)
    granted_by = db.Column(db.Integer, db.ForeignKey('auth_users.id'))
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    reason = db.Column(db.Text)
    
    # Relationships
    granter = db.relationship('AuthUser', foreign_keys=[granted_by], backref='granted_permissions')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'permission_id'),)

class SubscriptionPlan(db.Model):
    """Subscription plan model"""
    __tablename__ = 'subscription_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    plan_type = db.Column(db.Enum('consultancy', 'jobseeker'), default='consultancy')  # New field to distinguish plan types
    price_monthly = db.Column(db.Numeric(10, 2), default=0.00)
    price_yearly = db.Column(db.Numeric(10, 2), default=0.00)
    currency = db.Column(db.String(3), default='USD')
    max_users = db.Column(db.Integer, default=1)
    max_jobs = db.Column(db.Integer, default=0)
    max_applications = db.Column(db.Integer, default=0)
    max_job_portals = db.Column(db.Integer, default=0)  # New field for job portal limits
    storage_limit_gb = db.Column(db.Integer, default=1)
    api_rate_limit = db.Column(db.Integer, default=100)
    features_json = db.Column(db.JSON)
    is_popular = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = db.relationship('UserSubscription', backref='plan', lazy='dynamic')
    features = db.relationship('SubscriptionFeature', backref='plan', lazy='dynamic', cascade='all, delete-orphan')

class UserSubscription(db.Model):
    """User subscription model"""
    __tablename__ = 'user_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False)
    status = db.Column(db.Enum(SubscriptionStatus), default=SubscriptionStatus.PENDING)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    billing_cycle = db.Column(db.Enum('monthly', 'yearly', 'lifetime'), default='monthly')
    payment_method = db.Column(db.String(50))
    payment_gateway = db.Column(db.String(50))
    gateway_subscription_id = db.Column(db.String(255))
    last_payment_date = db.Column(db.DateTime)
    next_payment_date = db.Column(db.DateTime)
    auto_renew = db.Column(db.Boolean, default=True)
    usage_stats_json = db.Column(db.JSON)
    metadata_json = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SubscriptionFeature(db.Model):
    """Subscription feature model"""
    __tablename__ = 'subscription_features'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False)
    feature_key = db.Column(db.String(150), nullable=False)  # e.g., 'max_jobs', 'job_portals', 'ai_assistance'
    feature_name = db.Column(db.String(200), nullable=False)  # e.g., 'Maximum Job Applications per Month'
    feature_value = db.Column(db.Text)  # String value for the feature
    is_boolean = db.Column(db.Boolean, default=False)  # True/False features
    is_numeric = db.Column(db.Boolean, default=False)  # Numeric features
    is_unlimited = db.Column(db.Boolean, default=False)  # Unlimited features
    feature_category = db.Column(db.String(100), default='general')  # Categories: limits, features, support
    display_order = db.Column(db.Integer, default=0)  # Order for displaying features
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('plan_id', 'feature_key'),)
    
    def get_formatted_value(self):
        """Get formatted value for display"""
        if self.is_unlimited:
            return "Unlimited"
        elif self.is_boolean:
            return "✓" if self.feature_value.lower() in ['true', '1', 'yes'] else "✗"
        elif self.is_numeric:
            return f"{self.feature_value:,}" if self.feature_value.isdigit() else self.feature_value
        else:
            return self.feature_value or "Not Available"
    
    def to_dict(self):
        """Convert feature to dictionary"""
        return {
            'id': self.id,
            'feature_key': self.feature_key,
            'feature_name': self.feature_name,
            'feature_value': self.feature_value,
            'formatted_value': self.get_formatted_value(),
            'is_boolean': self.is_boolean,
            'is_numeric': self.is_numeric,
            'is_unlimited': self.is_unlimited,
            'feature_category': self.feature_category,
            'display_order': self.display_order,
            'is_active': self.is_active
        }

class JobPortal(db.Model):
    """Job portal model for tracking different job websites"""
    __tablename__ = 'job_portals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    website_url = db.Column(db.String(255), nullable=False)
    logo_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    api_integration = db.Column(db.Boolean, default=False)
    api_endpoint = db.Column(db.String(255))
    job_categories = db.Column(db.JSON)  # List of supported job categories
    supported_countries = db.Column(db.JSON)  # List of supported countries
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_portal_access = db.relationship('UserPortalAccess', backref='portal', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<JobPortal {self.name}>'

class UserPortalAccess(db.Model):
    """User access to specific job portals based on subscription"""
    __tablename__ = 'user_portal_access'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'), nullable=False)
    portal_id = db.Column(db.Integer, db.ForeignKey('job_portals.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('user_subscriptions.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    jobs_posted_this_month = db.Column(db.Integer, default=0)
    last_job_posted = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'portal_id'),)
    
    def can_post_job(self, monthly_limit):
        """Check if user can post more jobs this month"""
        if monthly_limit == -1:  # Unlimited
            return True
        return self.jobs_posted_this_month < monthly_limit
    
    def reset_monthly_counter(self):
        """Reset monthly job counter (called by background job)"""
        self.jobs_posted_this_month = 0
        self.updated_at = datetime.utcnow()

class JWTBlacklist(db.Model):
    """JWT token blacklist"""
    __tablename__ = 'jwt_blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    token_jti = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'))
    token_type = db.Column(db.Enum('access', 'refresh'), default='access')
    expires_at = db.Column(db.DateTime, nullable=False)
    blacklisted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(255))

class CSRFToken(db.Model):
    """CSRF token model"""
    __tablename__ = 'csrf_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'))
    session_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    @staticmethod
    def generate_token(user_id=None, session_id=None, ip_address=None, user_agent=None):
        """Generate new CSRF token"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        csrf_token = CSRFToken(
            token=token,
            user_id=user_id,
            session_id=session_id,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.session.add(csrf_token)
        db.session.commit()
        
        return token
    
    @staticmethod
    def validate_token(token, user_id=None, session_id=None):
        """Validate CSRF token"""
        csrf_token = CSRFToken.query.filter_by(token=token).first()
        
        if not csrf_token:
            return False
        
        if csrf_token.expires_at < datetime.utcnow():
            return False
        
        if csrf_token.used_at:
            return False
        
        if user_id and csrf_token.user_id != user_id:
            return False
        
        if session_id and csrf_token.session_id != session_id:
            return False
        
        # Mark as used
        csrf_token.used_at = datetime.utcnow()
        db.session.commit()
        
        return True

class SecurityLog(db.Model):
    """Security audit log"""
    __tablename__ = 'security_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'))
    event_type = db.Column(db.Enum(SecurityEventType), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    details_json = db.Column(db.JSON)
    severity = db.Column(db.Enum('low', 'medium', 'high', 'critical'), default='medium')
    resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def log_security_event(event_type, user_id=None, ip_address=None, user_agent=None, details=None, severity='medium'):
        """Log security event"""
        log_entry = SecurityLog(
            user_id=user_id,
            event_type=event_type,
            ip_address=ip_address,
            user_agent=user_agent,
            details_json=details,
            severity=severity
        )
        
        db.session.add(log_entry)
        db.session.commit()
        
        return log_entry
