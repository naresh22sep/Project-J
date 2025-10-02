#!/usr/bin/env python
"""
Add missing display_order column to subscription_features table
"""

import mysql.connector
from datetime import datetime

def add_missing_columns():
    """Add missing columns to subscription_features table"""
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Naresh123',
            database='jobhunter_fresh'
        )
        
        cursor = conn.cursor()
        
        # Check current table structure
        cursor.execute("DESCRIBE subscription_features")
        columns = cursor.fetchall()
        existing_columns = [col[0] for col in columns]
        
        print("🔍 Current subscription_features table columns:")
        for col in existing_columns:
            print(f"  - {col}")
        
        # Check for missing columns
        required_columns = {
            'feature_category': 'VARCHAR(100) DEFAULT "general"',
            'display_order': 'INT DEFAULT 0',
            'is_active': 'TINYINT(1) DEFAULT 1',
            'created_at': 'DATETIME DEFAULT CURRENT_TIMESTAMP',
            'updated_at': 'DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        }
        
        missing_columns = []
        for col_name, col_def in required_columns.items():
            if col_name not in existing_columns:
                missing_columns.append((col_name, col_def))
        
        if not missing_columns:
            print("✅ All required columns already exist in subscription_features table")
            return
        
        print(f"\n🔧 Found {len(missing_columns)} missing columns:")
        for col_name, col_def in missing_columns:
            print(f"  - {col_name}: {col_def}")
        
        # Add missing columns
        for col_name, col_def in missing_columns:
            print(f"\n📝 Adding column '{col_name}'...")
            
            if col_name == 'display_order':
                # Add display_order after feature_category
                cursor.execute(f"""
                    ALTER TABLE subscription_features 
                    ADD COLUMN {col_name} {col_def} AFTER feature_category
                """)
            elif col_name == 'is_active':
                # Add is_active after display_order
                cursor.execute(f"""
                    ALTER TABLE subscription_features 
                    ADD COLUMN {col_name} {col_def} AFTER display_order
                """)
            elif col_name == 'created_at':
                # Add created_at after is_active
                cursor.execute(f"""
                    ALTER TABLE subscription_features 
                    ADD COLUMN {col_name} {col_def} AFTER is_active
                """)
            elif col_name == 'updated_at':
                # Add updated_at after created_at
                cursor.execute(f"""
                    ALTER TABLE subscription_features 
                    ADD COLUMN {col_name} {col_def} AFTER created_at
                """)
            else:
                # Add other columns at the end
                cursor.execute(f"""
                    ALTER TABLE subscription_features 
                    ADD COLUMN {col_name} {col_def}
                """)
            
            print(f"  ✅ Successfully added '{col_name}' column")
        
        conn.commit()
        print(f"\n🎉 Successfully added {len(missing_columns)} missing columns!")
        
        # Verify the final table structure
        cursor.execute("DESCRIBE subscription_features")
        final_columns = cursor.fetchall()
        
        print("\n📋 Final subscription_features table structure:")
        for i, column in enumerate(final_columns, 1):
            print(f"  {i:2d}. {column[0]} ({column[1]})")
        
        # Check current feature count
        cursor.execute("SELECT COUNT(*) FROM subscription_features")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total features in table: {count}")
        
        # Update existing records with default values for new columns
        if missing_columns:
            print("\n🔄 Updating existing records with default values...")
            
            updates = []
            if ('display_order', 'INT DEFAULT 0') in missing_columns:
                updates.append("display_order = 0")
            if ('is_active', 'TINYINT(1) DEFAULT 1') in missing_columns:
                updates.append("is_active = 1")
                
            if updates:
                update_sql = f"UPDATE subscription_features SET {', '.join(updates)} WHERE id > 0"
                cursor.execute(update_sql)
                updated_rows = cursor.rowcount
                conn.commit()
                print(f"  ✅ Updated {updated_rows} existing records")
        
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
    add_missing_columns()