"""
Routes package for JobHunter Authentication System
"""

# Import all route blueprints for easy access
try:
    from .auth_routes import auth_bp
    from .superadmin_routes import superadmin_bp
except ImportError:
    # Handle import errors gracefully during development
    pass