#!/usr/bin/env python3
"""
Check database status for subscription system
"""
import pymysql

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
            # Check subscription plans
            cursor.execute('SELECT COUNT(*) FROM subscription_plans')
            plans_count = cursor.fetchone()[0]
            print(f'📋 Subscription Plans: {plans_count}')
            
            # Check user subscriptions
            cursor.execute('SELECT COUNT(*) FROM user_subscriptions')
            subs_count = cursor.fetchone()[0]
            print(f'👥 User Subscriptions: {subs_count}')
            
            # Check users
            cursor.execute('SELECT COUNT(*) FROM auth_users')
            users_count = cursor.fetchone()[0]
            print(f'🔐 Total Users: {users_count}')
            
            # Show subscription plans
            cursor.execute('SELECT name, display_name, plan_type, price_monthly FROM subscription_plans ORDER BY plan_type, sort_order')
            plans = cursor.fetchall()
            print(f'\n📋 Available Plans:')
            for plan in plans:
                print(f'   {plan[1]} ({plan[2]}): ${plan[3]}/month')
            
            # Show users
            cursor.execute('SELECT username, email, first_name, last_name FROM auth_users')
            users = cursor.fetchall()
            print(f'\n👥 Users in system:')
            for user in users:
                print(f'   {user[0]} - {user[2]} {user[3]} ({user[1]})')
                
    finally:
        connection.close()

if __name__ == '__main__':
    main()