#!/usr/bin/env python3
"""
Execute SQL scripts to populate the database with job data and location data
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

# Import the Flask app from app.py
from app import db
import app as app_module

def execute_sql_file(filename):
    """Execute SQL commands from a file"""
    print(f"🔄 Executing {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split SQL content into individual statements
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        # Create app instance
        app = app_module.create_app()
        
        with app.app_context():
            executed_count = 0
            for statement in statements:
                # Skip comments and empty statements
                if statement.startswith('--') or not statement.strip():
                    continue
                
                try:
                    db.session.execute(db.text(statement))
                    executed_count += 1
                except Exception as e:
                    print(f"⚠️  Warning executing statement: {str(e)}")
                    continue
            
            db.session.commit()
            print(f"✅ Successfully executed {executed_count} SQL statements from {filename}")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error executing {filename}: {str(e)}")
        return False
    
    return True

def main():
    """Main execution function"""
    print("🚀 Starting Database Population...")
    print("=" * 50)
    
    # Execute location data first (countries, states, cities)
    if execute_sql_file('location_data_usa_canada.sql'):
        print("✅ Location data populated successfully!")
    else:
        print("❌ Failed to populate location data")
        return
    
    print()
    
    # Execute job data second (industries, skills, roles, etc.)
    if execute_sql_file('job_data_it_ites.sql'):
        print("✅ Job data populated successfully!")
    else:
        print("❌ Failed to populate job data")
        return
    
    print()
    print("🎉 Database population completed successfully!")
    print("📊 You can now check the admin interface for populated data:")
    print("   • Countries & States: http://localhost:5051/superadmin/countries")
    print("   • Cities: http://localhost:5051/superadmin/cities")
    print("   • Industry Types: http://localhost:5051/superadmin/industry-types")
    print("   • Skills: http://localhost:5051/superadmin/skills")
    print("   • Job Roles: http://localhost:5051/superadmin/job-roles")
    print("   • Company Types: http://localhost:5051/superadmin/company-types")
    print("   • Job Types: http://localhost:5051/superadmin/job-types")

if __name__ == "__main__":
    main()