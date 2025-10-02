#!/usr/bin/env python3
"""
Initialize Job Data - Simple version to just create tables and add basic sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def main():
    """Initialize job data tables"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 Creating Job Data Tables...")
            print("=" * 50)
            
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            
            # Commit the changes
            db.session.commit()
            
            print("\n" + "=" * 50)
            print("✅ Job data tables created successfully!")
            print("\n📊 You can now access the admin panel to add data:")
            print("  🏭 Industry Types")
            print("  ⚙️ Skills")
            print("  🎓 Experience Levels")
            print("  👔 Job Roles")
            print("  🏢 Company Types")
            print("  💼 Job Types")
            print("  🌍 Countries, States, Cities")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error during initialization: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)