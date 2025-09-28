"""
Enhanced Configuration with Prompt Tracking Settings
"""

import os
from datetime import timedelta

class Config:
    """Base configuration with prompt tracking settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Database configuration from environment variables
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Naresh123')
    DB_NAME = os.environ.get('DB_NAME', 'jobhunter_fresh')
    
    # ===== PROMPT TRACKING CONFIGURATION =====
    
    # Basic Settings
    PROMPT_TRACKING_ENABLED = os.environ.get('PROMPT_TRACKING_ENABLED', 'True').lower() == 'true'
    PROMPT_MAX_LENGTH = int(os.environ.get('PROMPT_MAX_LENGTH', '10000'))
    PROMPT_SAVE_TIMEOUT = int(os.environ.get('PROMPT_SAVE_TIMEOUT', '30'))
    
    # Data Retention
    PROMPT_RETENTION_DAYS = int(os.environ.get('PROMPT_RETENTION_DAYS', '365'))
    
    # Rate Limiting
    PROMPT_RATE_LIMIT_PER_HOUR = int(os.environ.get('PROMPT_RATE_LIMIT_PER_HOUR', '100'))
    
    # Feature Toggles
    PROMPT_TRACKING_DEBUG = os.environ.get('PROMPT_TRACKING_DEBUG', 'False').lower() == 'true'
    PROMPT_TRACK_GIT_COMMITS = os.environ.get('PROMPT_TRACK_GIT_COMMITS', 'True').lower() == 'true'
    PROMPT_TRACK_FILE_OPERATIONS = os.environ.get('PROMPT_TRACK_FILE_OPERATIONS', 'True').lower() == 'true'
    PROMPT_TRACK_COMMANDS = os.environ.get('PROMPT_TRACK_COMMANDS', 'True').lower() == 'true'
    
    # Filter Settings
    PROMPT_MIN_COMPLEXITY = os.environ.get('PROMPT_MIN_COMPLEXITY', None)
    PROMPT_IGNORE_CATEGORIES = os.environ.get('PROMPT_IGNORE_CATEGORIES', '').split(',') if os.environ.get('PROMPT_IGNORE_CATEGORIES') else []
    
    # Export Settings
    PROMPT_EXPORT_MAX_RECORDS = int(os.environ.get('PROMPT_EXPORT_MAX_RECORDS', '10000'))
    
    # Privacy Settings
    PROMPT_ANONYMIZE_DATA = os.environ.get('PROMPT_ANONYMIZE_DATA', 'False').lower() == 'true'
    PROMPT_ENCRYPT_CONTENT = os.environ.get('PROMPT_ENCRYPT_CONTENT', 'False').lower() == 'true'
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        f'mysql+pymysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
    
    # Development-specific prompt settings
    PROMPT_TRACKING_DEBUG = True
    PROMPT_RATE_LIMIT_PER_HOUR = 1000  # Higher limit for development
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
    
    # Production-specific prompt settings
    PROMPT_TRACKING_DEBUG = False
    PROMPT_ANONYMIZE_DATA = True  # Enable privacy protection in production
    PROMPT_RETENTION_DAYS = 90   # Shorter retention in production
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        f'mysql+pymysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/test_{Config.DB_NAME}'
    
    # Testing-specific prompt settings
    PROMPT_TRACKING_ENABLED = False  # Disable in tests unless specifically testing prompts
    PROMPT_RETENTION_DAYS = 1       # Clean up quickly in tests

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}