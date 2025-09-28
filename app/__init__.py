from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
import os
from config.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'index'  # Temporarily point to main page until auth is implemented
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register new module blueprints
    from app.modules.jobseeker.routes import jobseeker
    from app.modules.consultancy.routes import consultancy
    from app.modules.admin.routes import admin
    from app.modules.superadmin.routes import superadmin
    
    # Register legacy blueprints for backwards compatibility
    try:
        from app.modules.auth.routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
    except ImportError:
        pass  # Auth module will be created later
    
    try:
        from app.modules.users.routes import users_bp
        app.register_blueprint(users_bp, url_prefix='/users')
    except ImportError:
        pass  # Users module will be created later
    
    try:
        from app.modules.dashboard.routes import dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    except ImportError:
        pass  # Dashboard module will be created later
    
    # Register new modular blueprints
    app.register_blueprint(jobseeker, url_prefix='/jobseeker')
    app.register_blueprint(consultancy, url_prefix='/consultancy') 
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(superadmin, url_prefix='/superadmin')
    
    
    # Main application routes
    @app.route('/')
    def index():
        """Main landing page - route based on user type"""
        if current_user.is_authenticated:
            # Redirect authenticated users to their respective dashboards
            if current_user.user_type.value == 'job_seeker':
                return redirect(url_for('jobseeker.dashboard'))
            elif current_user.user_type.value == 'consultancy':
                return redirect(url_for('consultancy.dashboard'))
            elif current_user.user_type.value == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.user_type.value == 'super_admin':
                return redirect(url_for('superadmin.dashboard'))
        
        # Show main landing page for anonymous users
        return render_template('main/index.html')
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('main/about.html')
    
    @app.route('/contact')
    def contact():
        """Contact page"""
        return render_template('main/contact.html')
    
    @app.route('/pricing')
    def pricing():
        """Pricing page"""
        return render_template('main/pricing.html')
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'JobHunter Platform is running'}
    
    # Context processors for templates
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    return app