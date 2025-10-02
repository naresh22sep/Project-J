#!/usr/bin/env python3
"""
Create sample user subscriptions for testing
"""
import pymysql
from datetime import datetime, timedelta

def main():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Naresh123',
        database='jobhunter_fresh',
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            # Get user IDs
            cursor.execute('SELECT id, username FROM auth_users ORDER BY id')
            users = cursor.fetchall()
            print(f'👥 Found {len(users)} users')
            
            # Get plan IDs
            cursor.execute('SELECT id, name, display_name, plan_type FROM subscription_plans ORDER BY plan_type, sort_order')
            plans = cursor.fetchall()
            print(f'📋 Found {len(plans)} plans')
            
            # Create sample subscriptions
            subscriptions_to_create = [
                # SuperAdmin gets Enterprise consultancy plan
                {'user_id': 1, 'plan_name': 'Enterprise', 'status': 'ACTIVE'},
                # Naresh gets Basic Job Seeker plan
                {'user_id': 2, 'plan_name': 'jobseeker_basic', 'status': 'ACTIVE'},
            ]
            
            created_count = 0
            for sub_data in subscriptions_to_create:
                # Find the plan
                plan_id = None
                for plan in plans:
                    if plan[1] == sub_data['plan_name']:
                        plan_id = plan[0]
                        break
                
                if plan_id:
                    # Check if subscription already exists
                    cursor.execute('SELECT COUNT(*) FROM user_subscriptions WHERE user_id = %s', (sub_data['user_id'],))
                    exists = cursor.fetchone()[0]
                    
                    if exists == 0:
                        # Create subscription
                        started_at = datetime.utcnow()
                        expires_at = started_at + timedelta(days=30)  # 30 days from now
                        
                        cursor.execute('''
                            INSERT INTO user_subscriptions 
                            (user_id, plan_id, status, started_at, expires_at, billing_cycle, auto_renew, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''', (
                            sub_data['user_id'],
                            plan_id,
                            sub_data['status'],
                            started_at,
                            expires_at,
                            'monthly',
                            True,
                            started_at,
                            started_at
                        ))
                        created_count += 1
                        print(f'✅ Created subscription for user {sub_data["user_id"]} with plan {sub_data["plan_name"]}')
                    else:
                        print(f'⚠️ User {sub_data["user_id"]} already has a subscription')
                else:
                    print(f'❌ Plan {sub_data["plan_name"]} not found')
            
            connection.commit()
            print(f'\n🎉 Created {created_count} new subscriptions!')
            
            # Verify subscriptions were created
            cursor.execute('''
                SELECT us.id, au.username, sp.display_name, us.status, us.started_at, us.expires_at
                FROM user_subscriptions us
                JOIN auth_users au ON us.user_id = au.id
                JOIN subscription_plans sp ON us.plan_id = sp.id
                ORDER BY us.created_at DESC
            ''')
            
            subscriptions = cursor.fetchall()
            print(f'\n📋 Current Subscriptions ({len(subscriptions)}):')
            for sub in subscriptions:
                print(f'   {sub[1]} -> {sub[2]} ({sub[3]}) - Expires: {sub[5].strftime("%Y-%m-%d")}')
                
    except Exception as e:
        print(f'❌ Error: {e}')
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    main()