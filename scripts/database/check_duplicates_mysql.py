#!/usr/bin/env python
"""
Check for duplicate subscription plans directly via MySQL
"""

import mysql.connector
from datetime import datetime

def connect_to_db():
    """Connect to MySQL database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Naresh123',
            database='jobhunter_fresh'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def check_duplicates():
    """Check for duplicate subscription plans"""
    conn = connect_to_db()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get all subscription plans
        cursor.execute("""
            SELECT id, name, display_name, plan_type, price_monthly, created_at,
                   (SELECT COUNT(*) FROM user_subscriptions us WHERE us.plan_id = sp.id) as user_count
            FROM subscription_plans sp 
            ORDER BY plan_type, name, created_at
        """)
        
        plans = cursor.fetchall()
        
        print(f"🔍 Total subscription plans: {len(plans)}")
        print("\nAll Plans:")
        print("-" * 100)
        
        # Group by name to find duplicates
        name_groups = {}
        for plan in plans:
            name = plan['name']
            if name not in name_groups:
                name_groups[name] = []
            name_groups[name].append(plan)
        
        duplicates_found = False
        
        for name, group in name_groups.items():
            if len(group) > 1:
                duplicates_found = True
                print(f"\n🚨 DUPLICATE PLANS for '{name}' ({len(group)} instances):")
                for i, plan in enumerate(group, 1):
                    print(f"  {i}. ID: {plan['id']:2d} | Display: {plan['display_name']:20s} | Type: {plan['plan_type']:12s} | "
                          f"Price: ${plan['price_monthly']:6.2f} | Users: {plan['user_count']:2d} | Created: {plan['created_at']}")
            else:
                plan = group[0]
                print(f"✅ {plan['name']:20s} | ID: {plan['id']:2d} | Display: {plan['display_name']:20s} | "
                      f"Type: {plan['plan_type']:12s} | Price: ${plan['price_monthly']:6.2f} | Users: {plan['user_count']:2d}")
        
        if not duplicates_found:
            print("\n✅ No duplicate plans found!")
        else:
            print(f"\n🗑️  Would you like to remove duplicate plans? (Plans with 0 users will be removed)")
            
            # Show which duplicates can be safely removed
            removable_plans = []
            for name, group in name_groups.items():
                if len(group) > 1:
                    # Keep the first one (oldest), remove others that have no users
                    for plan in group[1:]:  # Skip first plan
                        if plan['user_count'] == 0:
                            removable_plans.append(plan)
            
            if removable_plans:
                print(f"\nPLANS TO REMOVE ({len(removable_plans)}):")
                for plan in removable_plans:
                    print(f"  - ID {plan['id']:2d}: {plan['display_name']} (no users)")
                
                response = input(f"\nRemove these {len(removable_plans)} duplicate plans? (y/N): ")
                if response.lower() == 'y':
                    for plan in removable_plans:
                        # Remove associated features first
                        cursor.execute("DELETE FROM subscription_features WHERE plan_id = %s", (plan['id'],))
                        print(f"  ✅ Removed features for plan ID {plan['id']}")
                        
                        # Remove the plan
                        cursor.execute("DELETE FROM subscription_plans WHERE id = %s", (plan['id'],))
                        print(f"  ✅ Removed plan ID {plan['id']}: {plan['display_name']}")
                    
                    conn.commit()
                    print(f"\n🎉 Successfully removed {len(removable_plans)} duplicate plans!")
                else:
                    print("\n❌ Operation cancelled")
            else:
                print("\n⚠️  All duplicate plans have active users - cannot remove safely")
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    check_duplicates()