from flask.cli import with_appcontext
from app import create_app, db
import click
import os

# Create the Flask application
app = create_app()

@app.cli.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')

@app.cli.command()
@with_appcontext
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    click.echo('Dropped all database tables.')

@app.cli.command()
@with_appcontext
def reset_db():
    """Drop and recreate all database tables."""
    db.drop_all()
    db.create_all()
    click.echo('Reset the database.')

if __name__ == '__main__':
    # Import all models to ensure they're registered with SQLAlchemy
    from app.models import (
        User, UserType, JobSeekerProfile, ConsultancyProfile, 
        Job, JobApplication, AuditLog
    )
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("✅ Database tables created successfully!")
        print("📊 Available tables:")
        for table in db.metadata.tables.keys():
            print(f"   - {table}")
    
    print("\n🚀 Starting JobHunter Platform...")
    print("📍 Available URLs:")
    print("   🏠 Main: http://localhost:5051/")
    print("   👤 JobSeeker: http://localhost:5051/jobseeker/")
    print("   🏢 Consultancy: http://localhost:5051/consultancy/")
    print("   👮 Admin: http://localhost:5051/admin/")
    print("   👑 SuperAdmin: http://localhost:5051/superadmin/")
    print("   🔍 Health: http://localhost:5051/health")
    
    # Run the application
    port = int(os.environ.get('PORT', 5051))
    app.run(host='0.0.0.0', port=port, debug=True)