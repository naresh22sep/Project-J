#!/usr/bin/env python
"""
Add missing feature_category column to subscription_features table
"""

import mysql.connector
from datetime import datetime

def add_missing_column():
    """Add the missing feature_category column to subscription_features table"""
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Naresh123',
            database='jobhunter_fresh'
        )
        
        cursor = conn.cursor()
        
        # Check if the column already exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'jobhunter_fresh' 
            AND TABLE_NAME = 'subscription_features' 
            AND COLUMN_NAME = 'feature_category'
        """)
        
        if cursor.fetchone():
            print("✅ Column 'feature_category' already exists in subscription_features table")
            return
        
        print("🔧 Adding missing 'feature_category' column to subscription_features table...")
        
        # Add the missing column
        cursor.execute("""
            ALTER TABLE subscription_features 
            ADD COLUMN feature_category VARCHAR(100) DEFAULT 'general' AFTER is_unlimited
        """)
        
        # Update existing records to have a default category
        cursor.execute("""
            UPDATE subscription_features 
            SET feature_category = 'general' 
            WHERE feature_category IS NULL
        """)
        
        conn.commit()
        print("✅ Successfully added 'feature_category' column to subscription_features table")
        
        # Verify the column was added
        cursor.execute("DESCRIBE subscription_features")
        columns = cursor.fetchall()
        
        print("\n📋 Current subscription_features table structure:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        # Check current feature count
        cursor.execute("SELECT COUNT(*) FROM subscription_features")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total features in table: {count}")
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    add_missing_column()