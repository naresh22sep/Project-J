#!/usr/bin/env python3
"""
Create Admin User Script
Creates an admin user for testing authentication
"""

from app import create_app, db
from app.auth.auth_models import AuthUser, Role, UserRole

def create_admin_user():
    """Create admin user if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        # Check if admin role exists
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("Creating admin role...")
            admin_role = Role(
                name='admin',
                display_name='Administrator',
                description='System administrator with full access',
                level=100,
                is_system_role=True
            )
            db.session.add(admin_role)
            db.session.commit()
            print("Admin role created successfully!")
        else:
            print("Admin role already exists.")
        
        # Check if admin user exists
        admin_user = AuthUser.query.filter_by(username='admin').first()
        if not admin_user:
            print("Creating admin user...")
            admin_user = AuthUser(
                username='admin',
                email='admin@jobmilgaya.com',
                first_name='System',
                last_name='Administrator',
                is_active=True
            )
            admin_user.set_password('admin123')  # Simple password for testing
            db.session.add(admin_user)
            db.session.flush()  # Get user ID
            
            # Assign admin role
            user_role = UserRole(
                user_id=admin_user.id,
                role_id=admin_role.id,
                is_active=True
            )
            db.session.add(user_role)
            db.session.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("Admin user already exists.")
            print("Username: admin")
            # Check if user has admin role
            has_admin_role = admin_user.has_role('admin')
            print(f"Has admin role: {has_admin_role}")
            
            if not has_admin_role:
                print("Assigning admin role to existing user...")
                user_role = UserRole(
                    user_id=admin_user.id,
                    role_id=admin_role.id,
                    is_active=True
                )
                db.session.add(user_role)
                db.session.commit()
                print("Admin role assigned!")

if __name__ == '__main__':
    create_admin_user()