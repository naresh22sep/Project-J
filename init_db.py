#!/usr/bin/env python
"""
Database Initialization Script
"""

from app import db, create_app
from app.auth.auth_models import (
    Role, Permission, AuthUser, SubscriptionPlan, 
    SecurityEventType, UserRole
)

def initialize_database():
    """Initialize database with default data"""
    try:
        # Create all tables
        db.create_all()
        
        # Create default roles if they don't exist
        default_roles = [
            {'name': 'superadmin', 'display_name': 'Super Administrator', 'description': 'Super Administrator with full system access'},
            {'name': 'admin', 'display_name': 'Administrator', 'description': 'Administrator with limited system access'},
            {'name': 'consultancy', 'display_name': 'Consultancy', 'description': 'Consultancy user with hiring capabilities'},
            {'name': 'jobseeker', 'display_name': 'Job Seeker', 'description': 'Job seeker with application capabilities'}
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
            
            # Role management permissions
            {'name': 'role.create', 'display_name': 'Create Roles', 'description': 'Create new roles', 'resource': 'role', 'action': 'create'},
            {'name': 'role.read', 'display_name': 'View Roles', 'description': 'View role details', 'resource': 'role', 'action': 'read'},
            {'name': 'role.update', 'display_name': 'Update Roles', 'description': 'Update role information', 'resource': 'role', 'action': 'update'},
            {'name': 'role.delete', 'display_name': 'Delete Roles', 'description': 'Delete roles', 'resource': 'role', 'action': 'delete'},
            
            # Subscription management permissions
            {'name': 'subscription.create', 'display_name': 'Create Subscriptions', 'description': 'Create subscriptions', 'resource': 'subscription', 'action': 'create'},
            {'name': 'subscription.read', 'display_name': 'View Subscriptions', 'description': 'View subscription details', 'resource': 'subscription', 'action': 'read'},
            {'name': 'subscription.update', 'display_name': 'Update Subscriptions', 'description': 'Update subscriptions', 'resource': 'subscription', 'action': 'update'},
            {'name': 'subscription.delete', 'display_name': 'Delete Subscriptions', 'description': 'Delete subscriptions', 'resource': 'subscription', 'action': 'delete'},
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
        if superadmin_role:
            all_permissions = Permission.query.all()
            superadmin_role.permissions = all_permissions

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
            db.session.commit()  # Commit to get user ID
            
            # Create user-role relationship
            if superadmin_role:
                user_role = UserRole(
                    user_id=superadmin.id,
                    role_id=superadmin_role.id,
                    is_active=True
                )
                db.session.add(user_role)

        # Commit all changes
        db.session.commit()
        
        print("Database initialized successfully with default data")
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        print("Initializing database...")
        initialize_database()
        
        # Verify initialization
        superadmin = AuthUser.query.filter_by(username='superadmin').first()
        if superadmin:
            print("SuperAdmin user created successfully")
            print(f"Username: {superadmin.username}")
            print(f"Email: {superadmin.email}")
            print("Password: SuperAdmin@2024")
        else:
            print("ERROR: SuperAdmin user not created")