#!/usr/bin/env python
"""
Simple script to remove duplicate subscription plans
"""

import mysql.connector

def cleanup_duplicates():
    # Connect to database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Naresh123',
        database='jobhunter_fresh'
    )

    cursor = conn.cursor(dictionary=True)

    try:
        # Get all plans grouped by display name and price
        cursor.execute("""
            SELECT id, name, display_name, plan_type, price_monthly, created_at,
                   (SELECT COUNT(*) FROM user_subscriptions us WHERE us.plan_id = sp.id) as user_count
            FROM subscription_plans sp 
            ORDER BY display_name, price_monthly, created_at
        """)

        plans = cursor.fetchall()

        # Group by display_name + price
        display_groups = {}
        for plan in plans:
            key = f"{plan['display_name']}_{plan['price_monthly']}"
            if key not in display_groups:
                display_groups[key] = []
            display_groups[key].append(plan)

        # Find removable duplicates (keep oldest, remove newer ones with no users)
        removable_plans = []
        for key, group in display_groups.items():
            if len(group) > 1:
                # Sort by creation date to keep the oldest (handle None dates)
                from datetime import datetime
                group.sort(key=lambda x: x['created_at'] if x['created_at'] else datetime(1900, 1, 1))
                # Remove newer duplicates that have no users
                for plan in group[1:]:
                    if plan['user_count'] == 0:
                        removable_plans.append(plan)

        print(f'🔍 Found {len(removable_plans)} duplicate plans to remove:')
        for plan in removable_plans:
            print(f'  - ID {plan["id"]:2d}: {plan["name"]:20s} ({plan["display_name"]})')

        if removable_plans:
            # Remove duplicates
            removed_count = 0
            for plan in removable_plans:
                # Remove features first
                cursor.execute("DELETE FROM subscription_features WHERE plan_id = %s", (plan['id'],))
                features_removed = cursor.rowcount
                
                # Remove plan
                cursor.execute("DELETE FROM subscription_plans WHERE id = %s", (plan['id'],))
                if cursor.rowcount > 0:
                    removed_count += 1
                    print(f'✅ Removed plan ID {plan["id"]}: {plan["name"]} ({features_removed} features)')

            conn.commit()
            print(f'\n🎉 Successfully removed {removed_count} duplicate plans!')
            
            # Show final count
            cursor.execute("SELECT COUNT(*) as count FROM subscription_plans")
            final_count = cursor.fetchone()['count']
            print(f'📊 Final plan count: {final_count}')
        else:
            print('✅ No removable duplicates found!')

    except Exception as e:
        print(f'❌ Error: {e}')
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    cleanup_duplicates()