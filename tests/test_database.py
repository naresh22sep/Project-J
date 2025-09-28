"""
Database Connection Tests
Tests the database connectivity and basic operations
"""

import os
import sys
import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import pymysql

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, UserSession
from config.config import config

class TestDatabaseConnection(unittest.TestCase):
    """Test database connectivity and configuration"""
    
    def setUp(self):
        """Set up test environment"""
        # Load environment variables from .env file if it exists
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        """Clean up test environment"""
        self.app_context.pop()
    
    def test_database_config_loaded(self):
        """Test that database configuration is properly loaded"""
        config_obj = config['testing']
        
        # Test that database URL is configured
        self.assertIsNotNone(config_obj.SQLALCHEMY_DATABASE_URI)
        self.assertIn('mysql+pymysql', config_obj.SQLALCHEMY_DATABASE_URI)
        self.assertIn('jobhunter_fresh', config_obj.SQLALCHEMY_DATABASE_URI)
        
        print(f"✅ Database URI configured: {config_obj.SQLALCHEMY_DATABASE_URI}")
    
    def test_raw_mysql_connection(self):
        """Test raw MySQL connection using pymysql"""
        try:
            # Get database configuration
            host = os.environ.get('DB_HOST', 'localhost')
            port = int(os.environ.get('DB_PORT', '3306'))
            username = os.environ.get('DB_USERNAME', 'root')
            password = os.environ.get('DB_PASSWORD', 'Naresh123')
            database = os.environ.get('DB_NAME', 'jobhunter_fresh')
            
            # Test connection
            connection = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database,
                charset='utf8mb4'
            )
            
            # Test basic query
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"✅ MySQL Version: {version[0]}")
                
                cursor.execute("SELECT DATABASE()")
                current_db = cursor.fetchone()
                print(f"✅ Current Database: {current_db[0]}")
            
            connection.close()
            print("✅ Raw MySQL connection successful!")
            
        except Exception as e:
            self.fail(f"Raw MySQL connection failed: {str(e)}")
    
    def test_sqlalchemy_engine_connection(self):
        """Test SQLAlchemy engine connection"""
        try:
            engine = create_engine(self.app.config['SQLALCHEMY_DATABASE_URI'])
            
            # Test connection
            with engine.connect() as connection:
                result = connection.execute(text("SELECT VERSION()"))
                version = result.fetchone()
                print(f"✅ SQLAlchemy MySQL Version: {version[0]}")
                
                result = connection.execute(text("SELECT DATABASE()"))
                current_db = result.fetchone()
                print(f"✅ SQLAlchemy Current Database: {current_db[0]}")
            
            print("✅ SQLAlchemy engine connection successful!")
            
        except Exception as e:
            self.fail(f"SQLAlchemy connection failed: {str(e)}")
    
    def test_flask_sqlalchemy_connection(self):
        """Test Flask-SQLAlchemy connection"""
        try:
            # Test if we can connect to the database
            with self.app.app_context():
                # This will test if the database connection works
                db.engine.execute(text("SELECT 1"))
                print("✅ Flask-SQLAlchemy connection successful!")
                
        except Exception as e:
            self.fail(f"Flask-SQLAlchemy connection failed: {str(e)}")
    
    def test_database_tables_creation(self):
        """Test creating database tables"""
        try:
            with self.app.app_context():
                # Create all tables
                db.create_all()
                
                # Check if tables were created
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                
                expected_tables = ['users', 'user_sessions']
                for table in expected_tables:
                    self.assertIn(table, tables)
                    print(f"✅ Table '{table}' created successfully")
                
                print("✅ All database tables created successfully!")
                
        except Exception as e:
            self.fail(f"Table creation failed: {str(e)}")
    
    def test_database_crud_operations(self):
        """Test basic CRUD operations"""
        try:
            with self.app.app_context():
                # Create tables
                db.create_all()
                
                # Test CREATE
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    first_name='Test',
                    last_name='User'
                )
                test_user.set_password('testpassword123')
                
                db.session.add(test_user)
                db.session.commit()
                print("✅ User created successfully")
                
                # Test READ
                found_user = User.query.filter_by(username='testuser').first()
                self.assertIsNotNone(found_user)
                self.assertEqual(found_user.email, 'test@example.com')
                print("✅ User read successfully")
                
                # Test UPDATE
                found_user.first_name = 'Updated'
                db.session.commit()
                
                updated_user = User.query.filter_by(username='testuser').first()
                self.assertEqual(updated_user.first_name, 'Updated')
                print("✅ User updated successfully")
                
                # Test DELETE
                db.session.delete(found_user)
                db.session.commit()
                
                deleted_user = User.query.filter_by(username='testuser').first()
                self.assertIsNone(deleted_user)
                print("✅ User deleted successfully")
                
                print("✅ All CRUD operations successful!")
                
        except Exception as e:
            db.session.rollback()
            self.fail(f"CRUD operations failed: {str(e)}")
        finally:
            # Clean up
            with self.app.app_context():
                db.drop_all()


class TestDatabasePerformance(unittest.TestCase):
    """Test database performance and optimization"""
    
    def setUp(self):
        """Set up test environment"""
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            from dotenv import load_dotenv
            load_dotenv(env_path)
            
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up test environment"""
        db.drop_all()
        self.app_context.pop()
    
    def test_bulk_insert_performance(self):
        """Test bulk insert performance"""
        import time
        
        try:
            start_time = time.time()
            
            # Create multiple users
            users = []
            for i in range(100):
                user = User(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    first_name=f'User{i}',
                    last_name='Test'
                )
                user.set_password('password123')
                users.append(user)
            
            # Bulk insert
            db.session.add_all(users)
            db.session.commit()
            
            end_time = time.time()
            insert_time = end_time - start_time
            
            # Verify count
            user_count = User.query.count()
            self.assertEqual(user_count, 100)
            
            print(f"✅ Bulk insert of 100 users completed in {insert_time:.3f} seconds")
            
        except Exception as e:
            db.session.rollback()
            self.fail(f"Bulk insert test failed: {str(e)}")
    
    def test_query_performance(self):
        """Test query performance"""
        import time
        
        try:
            # Create test data
            for i in range(50):
                user = User(
                    username=f'queryuser{i}',
                    email=f'queryuser{i}@example.com',
                    first_name=f'Query{i}',
                    last_name='User'
                )
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            
            # Test different query types
            start_time = time.time()
            
            # Simple query
            users = User.query.all()
            simple_time = time.time() - start_time
            
            # Filtered query
            start_time = time.time()
            filtered_users = User.query.filter(User.username.like('queryuser%')).all()
            filter_time = time.time() - start_time
            
            # Paginated query
            start_time = time.time()
            paginated = User.query.paginate(page=1, per_page=20, error_out=False)
            pagination_time = time.time() - start_time
            
            print(f"✅ Simple query: {simple_time:.3f}s, Filtered: {filter_time:.3f}s, Paginated: {pagination_time:.3f}s")
            
        except Exception as e:
            db.session.rollback()
            self.fail(f"Query performance test failed: {str(e)}")


if __name__ == '__main__':
    print("🧪 Starting Database Connection Tests...\n")
    
    # Check if python-dotenv is available
    try:
        import dotenv
    except ImportError:
        print("⚠️  Warning: python-dotenv not found. Environment variables from .env file will not be loaded.")
        print("   Install with: pip install python-dotenv\n")
    
    # Run tests with verbose output
    unittest.main(verbosity=2, exit=False)
    
    print("\n🎉 Database tests completed!")