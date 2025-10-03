"""
Main Application Factory with Complete Authentication System
"""

from flask import Flask, g, request, session
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os

# Import db from app module to avoid duplicate instances
from app import db, migrate

def create_app(config_name=None):
    """Create and configure the Flask application"""
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config, apply_security_config
    app.config.from_object(config[config_name])
    
    # Apply security configuration
    security_config = apply_security_config(app, config_name)
    
    # Add context processors for templates
    @app.context_processor
    def inject_csrf_token():
        def csrf_token():
            try:
                # Try to get/create a session-based CSRF token
                if 'csrf_token' not in session:
                    import secrets
                    session['csrf_token'] = secrets.token_urlsafe(32)
                return session['csrf_token']
            except Exception as e:
                # Fallback: generate a temporary token
                import secrets
                return secrets.token_urlsafe(32)
        return {'csrf_token': csrf_token}
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize middleware
    from app.middleware.security_middleware import create_middleware_stack
    create_middleware_stack(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Initialize database and default data
    database_initialized = False
    try:
        with app.app_context():
            initialize_database()
            database_initialized = True
    except Exception as e:
        # Ensure session is properly cleaned up
        try:
            db.session.rollback()
            db.session.close()
        except:
            pass
        
        error_str = str(e)
        app.logger.error(f"Database initialization failed: {error_str}")
        print(f"⚠️ Database initialization failed: {error_str}")
        
        # If it's a MySQL connection error, try switching to SQLite temporarily
        if "Access denied" in error_str or "Can't connect" in error_str:
            print("🔄 MySQL connection failed. Trying SQLite fallback...")
            try:
                # Temporarily switch to SQLite
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp_jobhunter.db'
                db.init_app(app)  # Re-initialize with new config
                
                with app.app_context():
                    initialize_database()
                    database_initialized = True
                print("✅ Successfully initialized with SQLite fallback database")
            except Exception as sqlite_error:
                print(f"❌ SQLite fallback also failed: {str(sqlite_error)}")
        
        if not database_initialized:
            print("🔧 You may need to:")
            print("   1. Ensure MySQL is running")
            print("   2. Create the database: CREATE DATABASE jobhunter_auth_dev;")
            print("   3. Check MySQL authentication settings")
            print("   4. The app will still start without database initialization")
    
    # Configure logging
    configure_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_blueprints(app):
    """Register all blueprints"""
    
    # Register role-specific authentication routes
    try:
        from app.routes.auth_routes import (
            auth_bp, superadmin_auth_bp, admin_auth_bp, 
            jobseeker_auth_bp, consultancy_auth_bp
        )
        # Register all role-specific auth blueprints
        app.register_blueprint(superadmin_auth_bp)
        app.register_blueprint(admin_auth_bp)
        app.register_blueprint(jobseeker_auth_bp)
        app.register_blueprint(consultancy_auth_bp)
        # Register legacy auth blueprint for compatibility
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
    except ImportError as e:
        print(f"Warning: Could not register auth routes: {e}")
    
    # SuperAdmin routes (if they exist)
    try:
        from app.routes.superadmin_routes import superadmin_bp
        app.register_blueprint(superadmin_bp, url_prefix='/superadmin')
    except ImportError:
        print("Note: SuperAdmin routes not found, using auth routes only")
    
    # Admin routes (if they exist)
    try:
        from app.modules.admin.routes import admin
        app.register_blueprint(admin, url_prefix='/admin')
        print("✅ Admin blueprint registered successfully")
    except ImportError:
        print("Note: Admin routes not found")
    
    # Register modular role-based routes (new approach)
    try:
        from app.routes.roles.jobseeker_routes import jobseeker_routes_bp
        from app.routes.roles.consultancy_routes import consultancy_routes_bp
        from app.routes.roles.admin_routes import admin_routes_bp
        
        app.register_blueprint(jobseeker_routes_bp)
        app.register_blueprint(consultancy_routes_bp)
        app.register_blueprint(admin_routes_bp)
        print("✅ Modular role-based routes registered successfully")
    except ImportError as e:
        print(f"Note: Modular role routes not found: {e}")
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {
            'status': 'healthy',
            'service': 'JobHunter Authentication System',
            'version': '1.0.0'
        }
    
    # Root redirect - Show public homepage
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('public/homepage.html')
        
    # Logout redirect for legacy URLs
    @app.route('/logout')
    def logout_redirect():
        from flask import redirect
        # Redirect to proper auth logout route
        return redirect('/auth/logout')

def initialize_database():
    """Initialize database with default data"""
    try:
        # Create all tables
        db.create_all()
        
        # Import models
        from app.auth.auth_models import (
            Role, Permission, AuthUser, SubscriptionPlan, 
            SubscriptionFeature, SecurityEventType, JobPortal, UserPortalAccess
        )
        
        # Create default roles if they don't exist
        default_roles = [
            {'name': 'superadmin', 'description': 'Super Administrator with full system access'},
            {'name': 'admin', 'description': 'Administrator with limited system access'},
            {'name': 'consultancy', 'description': 'Consultancy user with hiring capabilities'},
            {'name': 'jobseeker', 'description': 'Job seeker with application capabilities'}
        ]
        
        for role_data in default_roles:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)
        
        # Create default permissions
        default_permissions = [
            # User management permissions
            {'name': 'user.create', 'display_name': 'Create Users', 'description': 'Create new users', 'resource': 'user', 'action': 'create'},
            {'name': 'user.read', 'display_name': 'View Users', 'description': 'View user details', 'resource': 'user', 'action': 'read'},
            {'name': 'user.update', 'display_name': 'Update Users', 'description': 'Update user information', 'resource': 'user', 'action': 'update'},
            {'name': 'user.delete', 'display_name': 'Delete Users', 'description': 'Delete users', 'resource': 'user', 'action': 'delete'},
            {'name': 'user.list', 'display_name': 'List Users', 'description': 'List all users', 'resource': 'user', 'action': 'list'},
            
            # Role and permission management
            {'name': 'role.create', 'display_name': 'Create Roles', 'description': 'Create new roles', 'resource': 'role', 'action': 'create'},
            {'name': 'role.read', 'display_name': 'View Roles', 'description': 'View role details', 'resource': 'role', 'action': 'read'},
            {'name': 'role.update', 'display_name': 'Update Roles', 'description': 'Update roles', 'resource': 'role', 'action': 'update'},
            {'name': 'role.delete', 'display_name': 'Delete Roles', 'description': 'Delete roles', 'resource': 'role', 'action': 'delete'},
            {'name': 'role.assign', 'display_name': 'Assign Roles', 'description': 'Assign roles to users', 'resource': 'role', 'action': 'assign'},
            
            {'name': 'permission.create', 'display_name': 'Create Permissions', 'description': 'Create permissions', 'resource': 'permission', 'action': 'create'},
            {'name': 'permission.read', 'display_name': 'View Permissions', 'description': 'View permissions', 'resource': 'permission', 'action': 'read'},
            {'name': 'permission.update', 'display_name': 'Update Permissions', 'description': 'Update permissions', 'resource': 'permission', 'action': 'update'},
            {'name': 'permission.delete', 'display_name': 'Delete Permissions', 'description': 'Delete permissions', 'resource': 'permission', 'action': 'delete'},
            
            # Subscription management
            {'name': 'subscription.create', 'display_name': 'Create Subscriptions', 'description': 'Create subscriptions', 'resource': 'subscription', 'action': 'create'},
            {'name': 'subscription.read', 'display_name': 'View Subscriptions', 'description': 'View subscriptions', 'resource': 'subscription', 'action': 'read'},
            {'name': 'subscription.update', 'display_name': 'Update Subscriptions', 'description': 'Update subscriptions', 'resource': 'subscription', 'action': 'update'},
            {'name': 'subscription.delete', 'display_name': 'Delete Subscriptions', 'description': 'Delete subscriptions', 'resource': 'subscription', 'action': 'delete'},
            
            # Security monitoring
            {'name': 'security.read', 'display_name': 'View Security', 'description': 'View security logs', 'resource': 'security', 'action': 'read'},
            {'name': 'security.export', 'display_name': 'Export Security', 'description': 'Export security data', 'resource': 'security', 'action': 'export'},
            
            # System administration
            {'name': 'system.maintenance', 'display_name': 'System Maintenance', 'description': 'Perform system maintenance', 'resource': 'system', 'action': 'maintenance'},
            {'name': 'system.config', 'display_name': 'System Config', 'description': 'Manage system configuration', 'resource': 'system', 'action': 'config'},
            
            # Job-related permissions
            {'name': 'job.create', 'display_name': 'Create Jobs', 'description': 'Create job postings', 'resource': 'job', 'action': 'create'},
            {'name': 'job.read', 'display_name': 'View Jobs', 'description': 'View job postings', 'resource': 'job', 'action': 'read'},
            {'name': 'job.update', 'display_name': 'Update Jobs', 'description': 'Update job postings', 'resource': 'job', 'action': 'update'},
            {'name': 'job.delete', 'display_name': 'Delete Jobs', 'description': 'Delete job postings', 'resource': 'job', 'action': 'delete'},
            {'name': 'job.apply', 'display_name': 'Apply to Jobs', 'description': 'Apply to jobs', 'resource': 'job', 'action': 'apply'},
        ]
        
        for perm_data in default_permissions:
            permission = Permission.query.filter_by(name=perm_data['name']).first()
            if not permission:
                permission = Permission(**perm_data)
                db.session.add(permission)
        
        # Commit roles and permissions first
        db.session.commit()
        
        # Assign permissions to roles
        superadmin_role = Role.query.filter_by(name='superadmin').first()
        admin_role = Role.query.filter_by(name='admin').first()
        consultancy_role = Role.query.filter_by(name='consultancy').first()
        jobseeker_role = Role.query.filter_by(name='jobseeker').first()
        
        # SuperAdmin gets all permissions
        if superadmin_role:
            all_permissions = Permission.query.all()
            superadmin_role.permissions = all_permissions
        
        # Admin gets user and role management permissions
        if admin_role:
            admin_permissions = Permission.query.filter(
                Permission.name.in_([
                    'user.read', 'user.update', 'user.list',
                    'role.read', 'subscription.read'
                ])
            ).all()
            admin_role.permissions = admin_permissions
        
        # Consultancy gets job management permissions
        if consultancy_role:
            consultancy_permissions = Permission.query.filter(
                Permission.name.in_([
                    'job.create', 'job.read', 'job.update', 'job.delete'
                ])
            ).all()
            consultancy_role.permissions = consultancy_permissions
        
        # Job seeker gets basic job permissions
        if jobseeker_role:
            jobseeker_permissions = Permission.query.filter(
                Permission.name.in_(['job.read', 'job.apply'])
            ).all()
            jobseeker_role.permissions = jobseeker_permissions
        
        # Create subscription plans
        from config import Config
        
        for plan_key, plan_config in Config.SUBSCRIPTION_PLANS.items():
            plan = SubscriptionPlan.query.filter_by(name=plan_config['name']).first()
            if not plan:
                plan = SubscriptionPlan(
                    name=plan_config['name'],
                    display_name=plan_config['name'],
                    description=f"{plan_config['name']} subscription plan",
                    plan_type=plan_config.get('plan_type', 'consultancy'),
                    price_monthly=plan_config.get('price', 0.00),
                    price_yearly=plan_config.get('yearly_price', plan_config.get('price', 0.00) * 10),
                    max_job_portals=plan_config['features'].get('portal_access_count', 0),
                    is_active=True
                )
                db.session.add(plan)
                db.session.flush()  # Get the plan ID
                
                # Add plan features
                for feature_key, feature_value in plan_config['features'].items():
                    if isinstance(feature_value, bool):
                        value_str = 'true' if feature_value else 'false'
                        is_boolean = True
                    elif isinstance(feature_value, int):
                        value_str = str(feature_value)
                        is_boolean = False
                    else:
                        value_str = str(feature_value)
                        is_boolean = False
                    
                    # Create a user-friendly feature name from the key
                    feature_name = feature_key.replace('_', ' ').title()
                    
                    feature = SubscriptionFeature(
                        plan_id=plan.id,
                        feature_key=feature_key,
                        feature_name=feature_name,
                        feature_value=value_str,
                        is_boolean=is_boolean
                    )
                    db.session.add(feature)
        
        # Create default superadmin user
        superadmin = AuthUser.query.filter_by(username='superadmin').first()
        if not superadmin:
            superadmin = AuthUser(
                username='superadmin',
                email='admin@jobhunter.com',
                first_name='Super',
                last_name='Admin',
                is_active=True
            )
            superadmin.set_password('SuperAdmin@2024')  # Change this in production
            
            db.session.add(superadmin)
            db.session.flush()  # Get user ID
            
            if superadmin_role:
                # Create UserRole relationship
                from app.auth.auth_models import UserRole
                user_role = UserRole(user_id=superadmin.id, role_id=superadmin_role.id)
                db.session.add(user_role)
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Database initialized successfully with default data")
        
    except Exception as e:
        # Ensure proper session cleanup
        try:
            db.session.rollback()
        except:
            # If rollback fails, close the session completely
            try:
                db.session.close()
            except:
                pass
        print(f"❌ Error initializing database: {str(e)}")
        raise

def configure_logging(app):
    """Configure application logging"""
    if not app.debug and not app.testing:
        # Create logs directory
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configure file handler
        file_handler = RotatingFileHandler(
            'logs/jobhunter_auth.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('JobHunter Authentication System startup')

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {
            'error': 'Bad Request',
            'message': 'The request was invalid or malformed'
        }, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }, 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return {
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.'
        }, 429
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Server Error: {error}')
        return {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }, 500

# Create app instance
app = create_app()

if __name__ == '__main__':
    print("🚀 Starting JobHunter Authentication System...")
    print("=" * 50)
    print("🔐 Features enabled:")
    print("  • JWT Authentication with exp/iss/aud")
    print("  • XSS Protection")
    print("  • CSRF Token Protection") 
    print("  • Role-Based Access Control (RBAC)")
    print("  • Subscription Management")
    print("  • Security Event Logging")
    print("  • SuperAdmin Dashboard")
    print("=" * 50)
    print("👤 Default SuperAdmin Account:")
    print("   Username: superadmin")
    print("   Password: SuperAdmin@2024")
    print("   URL: http://localhost:5051/superadmin")
    print("=" * 50)
    print("🌟 Roles Available:")
    print("   • superadmin - Full system access")
    print("   • admin - Limited admin access")
    print("   • consultancy - Job posting management")  
    print("   • jobseeker - Job application access")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5051, debug=True)