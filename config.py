"""
Application Configuration with Security Settings
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Basic Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2024'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///jobhunter_auth.db'
        # For MySQL use: 'mysql+pymysql://root:root@localhost:3306/jobhunter_auth'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    JWT_ISSUER = 'JobHunter-Platform'
    JWT_AUDIENCE = 'JobHunter-Users'
    
    # Security Configuration
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'security-salt-2024'
    SECURITY_CSRF_PROTECT_ALL = True
    SECURITY_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'jobhunter:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = 'memory://'  # Use Redis in production
    RATELIMIT_DEFAULT = '100 per hour'
    RATELIMIT_HEADERS_ENABLED = True
    
    # Email Configuration (for future password reset functionality)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@jobhunter.com'
    
    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Logging Configuration
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'false').lower() in ['true', 'on', '1']
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Security Headers
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
    }
    
    # Feature Flags
    ENABLE_REGISTRATION = os.environ.get('ENABLE_REGISTRATION', 'true').lower() in ['true', 'on', '1']
    ENABLE_PASSWORD_RESET = os.environ.get('ENABLE_PASSWORD_RESET', 'true').lower() in ['true', 'on', '1']
    ENABLE_EMAIL_VERIFICATION = os.environ.get('ENABLE_EMAIL_VERIFICATION', 'false').lower() in ['true', 'on', '1']
    
    # Subscription Plans Configuration
    SUBSCRIPTION_PLANS = {
        'starter': {
            'name': 'Starter',
            'price': 0.00,
            'features': {
                'job_applications_per_month': 10,
                'profile_views': 50,
                'basic_search': True,
                'advanced_search': False,
                'priority_support': False,
                'analytics': False
            }
        },
        'professional': {
            'name': 'Professional',
            'price': 29.99,
            'features': {
                'job_applications_per_month': 100,
                'profile_views': 500,
                'basic_search': True,
                'advanced_search': True,
                'priority_support': False,
                'analytics': True
            }
        },
        'business': {
            'name': 'Business',
            'price': 79.99,
            'features': {
                'job_applications_per_month': 500,
                'profile_views': 2000,
                'basic_search': True,
                'advanced_search': True,
                'priority_support': True,
                'analytics': True,
                'team_management': True,
                'bulk_operations': True
            }
        },
        'enterprise': {
            'name': 'Enterprise',
            'price': 199.99,
            'features': {
                'job_applications_per_month': -1,  # Unlimited
                'profile_views': -1,  # Unlimited
                'basic_search': True,
                'advanced_search': True,
                'priority_support': True,
                'analytics': True,
                'team_management': True,
                'bulk_operations': True,
                'custom_integrations': True,
                'dedicated_support': True
            }
        }
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'
    
    # Relaxed security for development
    SECURITY_CSRF_PROTECT_ALL = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    
    # Development database - using MySQL with credentials from .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        f'mysql+pymysql://{os.environ.get("DB_USERNAME", "root")}:{os.environ.get("DB_PASSWORD", "Naresh123")}@{os.environ.get("DB_HOST", "localhost")}:{os.environ.get("DB_PORT", "3306")}/{os.environ.get("DB_NAME", "jobhunter_fresh")}'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECURITY_CSRF_PROTECT_ALL = False
    
    # Shorter token expiry for faster testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Strong security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Production database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://username:password@localhost:3306/jobhunter_auth'
    
    # Use Redis for rate limiting in production
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    
    # Strict security headers for production
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
    }

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

# Security utilities
class SecurityConfig:
    """Security-specific configuration and utilities"""
    
    # Password policy
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SPECIAL = True
    PASSWORD_FORBIDDEN_SEQUENCES = ['123456', 'password', 'qwerty', 'admin']
    
    # Account lockout policy
    MAX_LOGIN_ATTEMPTS = 5
    ACCOUNT_LOCKOUT_DURATION = timedelta(minutes=30)
    
    # Session security
    SESSION_TIMEOUT = timedelta(hours=8)  # Auto-logout after 8 hours of inactivity
    CONCURRENT_SESSIONS_LIMIT = 3  # Max 3 active sessions per user
    
    # JWT security
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Rate limiting rules
    RATE_LIMITS = {
        'login': '10 per minute',
        'register': '5 per minute',
        'password_reset': '3 per hour',
        'api_calls': '1000 per hour',
        'file_upload': '50 per hour'
    }
    
    # Allowed origins for CORS (if needed)
    CORS_ORIGINS = [
        'http://localhost:3000',  # React dev server
        'http://localhost:8080',  # Vue dev server
        'https://yourdomain.com'  # Production frontend
    ]
    
    # File upload security
    UPLOAD_VIRUS_SCAN = False  # Enable in production with antivirus service
    UPLOAD_MAX_FILES = 10
    UPLOAD_ALLOWED_MIMETYPES = {
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'image/jpeg',
        'image/png',
        'image/gif'
    }

# Environment-specific security settings
def apply_security_config(app, config_name):
    """Apply security configuration to Flask app"""
    security_config = SecurityConfig()
    
    if config_name == 'production':
        # Production-specific security
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
        app.config['PREFERRED_URL_SCHEME'] = 'https'
        
    elif config_name == 'development':
        # Development-specific settings
        app.config['SESSION_COOKIE_SECURE'] = False
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        
    # Apply common security headers
    @app.after_request
    def apply_security_headers(response):
        for header, value in Config.SECURITY_HEADERS.items():
            response.headers[header] = value
        return response
    
    return security_config