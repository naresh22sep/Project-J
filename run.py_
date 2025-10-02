#!/usr/bin/env python3
"""
JobHunter Platform - Main Application Runner
4-Module Flask Application (JobSeeker, Consultancy, Admin, SuperAdmin)
"""

import os
import sys
from app import create_app, db

def main():
    """Main application entry point"""
    
    # Create the Flask application
    app = create_app()
    
    # Import all models to ensure they're registered with SQLAlchemy
    from app.models import (
        User, UserType, JobSeekerProfile, ConsultancyProfile, 
        Job, JobApplication, AuditLog
    )
    
    with app.app_context():
        try:
            # Create all database tables
            db.create_all()
            print("✅ Database connection successful!")
            print("📊 Database tables created/verified:")
            
            tables = list(db.metadata.tables.keys())
            for table in sorted(tables):
                print(f"   - {table}")
                
        except Exception as e:
            print(f"❌ Database error: {str(e)}")
            print("💡 Make sure MySQL is running and database exists")
            return False
    
    # Print startup information
    print("\n🚀 Starting JobHunter Platform...")
    print("=" * 50)
    print("📍 Available Module URLs:")
    print("   🏠 Main Site:     http://localhost:5051/")
    print("   👤 JobSeeker:     http://localhost:5051/jobseeker/")
    print("   🏢 Consultancy:   http://localhost:5051/consultancy/")
    print("   👮 Admin:         http://localhost:5051/admin/")
    print("   👑 SuperAdmin:    http://localhost:5051/superadmin/")
    print("\n🔍 System URLs:")
    print("   ❤️ Health Check:  http://localhost:5051/health")
    print("   📋 About:         http://localhost:5051/about")
    print("   📞 Contact:       http://localhost:5051/contact")
    print("   💰 Pricing:       http://localhost:5051/pricing")
    print("\n" + "=" * 50)
    
    # Get port from environment or default to 5051
    port = int(os.environ.get('PORT', 5051))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    if debug_mode:
        print("🐛 Debug mode: ON")
    else:
        print("🔒 Production mode: ON")
        
    print(f"🌐 Server starting on: http://0.0.0.0:{port}")
    print("⏹️ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Run the application
        app.run(
            host='0.0.0.0', 
            port=port, 
            debug=debug_mode,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n⏹️ Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("🎯 JobHunter Platform - 4-Module Flask Application")
    print("📅 Starting application...")
    
    success = main()
    
    if not success:
        print("\n❌ Application failed to start")
        sys.exit(1)
    else:
        print("\n✅ Application stopped gracefully")
        sys.exit(0)