#!/usr/bin/env python3
"""
Add missing columns to subscription_features table - Direct MySQL approach
"""

import mysql.connector
from datetime import datetime
import sys

def add_missing_columns():
    """Add missing columns to subscription_features table"""
    try:
        # Database connection
        connection = mysql.connector.connect(
            host='localhost',
            database='jobhunter_fresh',
            user='root',
            password='Naresh123'
        )
        
        cursor = connection.cursor()
        
        print("🔍 Checking current table structure...")
        
        # Check current table structure
        cursor.execute("DESCRIBE subscription_features")
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"Current columns: {existing_columns}")
        
        # Define missing columns with their SQL definitions
        missing_columns = {
            'display_order': "ALTER TABLE subscription_features ADD COLUMN display_order INT DEFAULT 0",
            'is_active': "ALTER TABLE subscription_features ADD COLUMN is_active TINYINT(1) DEFAULT 1",
            'created_at': "ALTER TABLE subscription_features ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            'updated_at': "ALTER TABLE subscription_features ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        }
        
        columns_added = []
        
        for column_name, alter_sql in missing_columns.items():
            if column_name not in existing_columns:
                print(f"➕ Adding column: {column_name}")
                try:
                    cursor.execute(alter_sql)
                    columns_added.append(column_name)
                    print(f"✅ Successfully added column: {column_name}")
                except mysql.connector.Error as e:
                    print(f"❌ Error adding column {column_name}: {e}")
            else:
                print(f"⏭️ Column {column_name} already exists")
        
        if columns_added:
            # Update existing records with proper values
            print("\n🔄 Updating existing records...")
            
            # Set display_order based on id (simple ordering)
            if 'display_order' in columns_added:
                cursor.execute("""
                    UPDATE subscription_features 
                    SET display_order = id 
                    WHERE display_order = 0 OR display_order IS NULL
                """)
                rows_updated = cursor.rowcount
                print(f"✅ Updated display_order for {rows_updated} records")
            
            # Ensure is_active is set to 1 for all existing records
            if 'is_active' in columns_added:
                cursor.execute("""
                    UPDATE subscription_features 
                    SET is_active = 1 
                    WHERE is_active IS NULL
                """)
                rows_updated = cursor.rowcount
                print(f"✅ Updated is_active for {rows_updated} records")
        
        # Commit all changes
        connection.commit()
        
        print("\n🔍 Final table structure:")
        cursor.execute("DESCRIBE subscription_features")
        final_columns = cursor.fetchall()
        for column in final_columns:
            print(f"  {column[0]} - {column[1]} - {column[2]} - {column[3]} - {column[4]} - {column[5]}")
        
        print(f"\n✅ Successfully added {len(columns_added)} missing columns to subscription_features table")
        
        # Count total records
        cursor.execute("SELECT COUNT(*) FROM subscription_features")
        total_records = cursor.fetchone()[0]
        print(f"📊 Total subscription features: {total_records}")
        
    except mysql.connector.Error as error:
        print(f"❌ Database error: {error}")
        return False
    
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Database connection closed")
    
    return True

if __name__ == "__main__":
    print("🚀 Adding missing columns to subscription_features table...")
    print("=" * 60)
    
    success = add_missing_columns()
    
    if success:
        print("\n🎉 Column addition completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Column addition failed!")
        sys.exit(1)