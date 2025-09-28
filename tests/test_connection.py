"""
Simple Database Connection Test Script
Quick test to verify database connectivity
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_connection():
    """Simple database connection test"""
    print("🔍 Testing Database Connection...")
    print("=" * 50)
    
    # Test 1: Check environment variables
    print("1. Checking environment variables:")
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '3306')
    db_name = os.environ.get('DB_NAME', 'jobhunter_fresh')
    db_user = os.environ.get('DB_USERNAME', 'root')
    db_password = os.environ.get('DB_PASSWORD', 'Naresh123')
    
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   Database: {db_name}")
    print(f"   Username: {db_user}")
    print(f"   Password: {'*' * len(db_password)}")
    print()
    
    # Test 2: Raw MySQL connection
    print("2. Testing raw MySQL connection:")
    try:
        import pymysql
        connection = pymysql.connect(
            host=db_host,
            port=int(db_port),
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION(), DATABASE()")
            result = cursor.fetchone()
            print(f"   ✅ MySQL Version: {result[0]}")
            print(f"   ✅ Connected to database: {result[1]}")
        
        connection.close()
        print("   ✅ Raw connection successful!")
        
    except ImportError:
        print("   ❌ pymysql not installed. Install with: pip install pymysql")
        return False
    except Exception as e:
        print(f"   ❌ Raw connection failed: {e}")
        return False
    
    print()
    
    # Test 3: Flask app connection
    print("3. Testing Flask app connection:")
    try:
        from app import create_app, db
        
        app = create_app('development')
        with app.app_context():
            # Test connection using newer SQLAlchemy syntax
            from sqlalchemy import text
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT VERSION(), DATABASE()"))
                row = result.fetchone()
                print(f"   ✅ Flask-SQLAlchemy Version: {row[0]}")
                print(f"   ✅ Flask app connected to: {row[1]}")
            
        print("   ✅ Flask connection successful!")
        
    except Exception as e:
        print(f"   ❌ Flask connection failed: {e}")
        return False
    
    print()
    
    # Test 4: Table creation
    print("4. Testing table creation:")
    try:
        with app.app_context():
            db.create_all()
            
            # Check tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['users', 'user_sessions']
            for table in expected_tables:
                if table in tables:
                    print(f"   ✅ Table '{table}' exists")
                else:
                    print(f"   ⚠️  Table '{table}' not found")
            
            print("   ✅ Table creation test completed!")
            
    except Exception as e:
        print(f"   ❌ Table creation failed: {e}")
        return False
    
    print()
    print("🎉 All database tests passed!")
    return True

def check_requirements():
    """Check if required packages are installed"""
    print("📦 Checking required packages:")
    
    required_packages = [
        ('flask', 'flask'),
        ('flask-sqlalchemy', 'flask_sqlalchemy'),
        ('flask-migrate', 'flask_migrate'),
        ('pymysql', 'pymysql'),
        ('python-dotenv', 'dotenv')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - Not installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("   ✅ All required packages are installed!")
    return True

if __name__ == '__main__':
    print("🚀 Database Connection Checker")
    print("=" * 50)
    
    # Load .env file if exists
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
            print(f"📄 Loaded environment from: {env_path}")
        except ImportError:
            print("⚠️  python-dotenv not installed, using system environment variables")
    else:
        print(f"⚠️  No .env file found at: {env_path}")
        print("   Copy config/.env.example to .env and update with your settings")
    
    print()
    
    # Check requirements first
    if not check_requirements():
        print("\n❌ Please install missing packages before running tests")
        sys.exit(1)
    
    print()
    
    # Run connection test
    success = test_connection()
    
    if success:
        print("\n✅ Database is ready for use!")
        print("\nNext steps:")
        print("1. Run the application: python app.py")
        print("2. Run full tests: python -m pytest tests/")
        print("3. Initialize migrations: flask db init")
    else:
        print("\n❌ Database connection issues found")
        print("\nTroubleshooting:")
        print("1. Check if MySQL is running")
        print("2. Verify credentials in .env file")
        print("3. Make sure database 'jobhunter_fresh' exists")
        print("4. Check firewall settings")