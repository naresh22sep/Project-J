#!/usr/bin/env python
"""
Check for duplicate subscription plans by display name and price
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

def check_display_duplicates():
    """Check for duplicate subscription plans by display name and price"""
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
            ORDER BY plan_type, display_name, created_at
        """)
        
        plans = cursor.fetchall()
        
        print(f"🔍 Total subscription plans: {len(plans)}")
        print("\nChecking for duplicates by display name and price...")
        print("-" * 100)
        
        # Group by display_name + price_monthly to find duplicates
        display_groups = {}
        for plan in plans:
            key = f"{plan['display_name']}_{plan['price_monthly']}"
            if key not in display_groups:
                display_groups[key] = []
            display_groups[key].append(plan)
        
        duplicates_found = False
        removable_plans = []
        
        for key, group in display_groups.items():
            if len(group) > 1:
                duplicates_found = True
                display_name = group[0]['display_name']
                price = group[0]['price_monthly']
                print(f"\n🚨 DUPLICATE PLANS for '{display_name}' at ${price} ({len(group)} instances):")
                
                # Sort by creation date to keep the oldest
                group.sort(key=lambda x: x['created_at'])
                
                for i, plan in enumerate(group, 1):
                    status = "KEEP (oldest)" if i == 1 else "REMOVE" if plan['user_count'] == 0 else "KEEP (has users)"
                    print(f"  {i}. ID: {plan['id']:2d} | Name: {plan['name']:20s} | Type: {plan['plan_type']:12s} | "
                          f"Users: {plan['user_count']:2d} | Created: {plan['created_at']} | {status}")
                    
                    # Add to removable list if not the first (oldest) and has no users
                    if i > 1 and plan['user_count'] == 0:
                        removable_plans.append(plan)
            else:
                plan = group[0]
                print(f"✅ {plan['display_name']:20s} | ID: {plan['id']:2d} | Name: {plan['name']:20s} | "
                      f"Type: {plan['plan_type']:12s} | Price: ${plan['price_monthly']:6.2f} | Users: {plan['user_count']:2d}")
        
        if not duplicates_found:
            print("\n✅ No duplicate plans by display name found!")
        else:
            print(f"\n📊 SUMMARY:")
            print(f"   - Total plans: {len(plans)}")
            print(f"   - Duplicate groups: {sum(1 for group in display_groups.values() if len(group) > 1)}")
            print(f"   - Plans that can be safely removed: {len(removable_plans)}")
            
            if removable_plans:
                print(f"\n🗑️  PLANS TO REMOVE ({len(removable_plans)}):")
                for plan in removable_plans:
                    print(f"  - ID {plan['id']:2d}: {plan['name']:20s} ({plan['display_name']}) - ${plan['price_monthly']} (no users)")
                
                response = input(f"\nRemove these {len(removable_plans)} duplicate plans? (y/N): ")
                if response.lower() == 'y':
                    removed_count = 0
                    for plan in removable_plans:
                        # Remove associated features first
                        cursor.execute("DELETE FROM subscription_features WHERE plan_id = %s", (plan['id'],))
                        features_removed = cursor.rowcount
                        
                        # Remove the plan
                        cursor.execute("DELETE FROM subscription_plans WHERE id = %s", (plan['id'],))
                        plan_removed = cursor.rowcount
                        
                        if plan_removed > 0:
                            removed_count += 1
                            print(f"  ✅ Removed plan ID {plan['id']}: {plan['name']} ({features_removed} features)")
                    
                    conn.commit()
                    print(f"\n🎉 Successfully removed {removed_count} duplicate plans!")
                    
                    # Show final count
                    cursor.execute("SELECT COUNT(*) as count FROM subscription_plans")
                    final_count = cursor.fetchone()['count']
                    print(f"📊 Final plan count: {final_count}")
                else:
                    print("\n❌ Operation cancelled")
            else:
                print("\n⚠️  All duplicate plans have active users - cannot remove safely")
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    check_display_duplicates()