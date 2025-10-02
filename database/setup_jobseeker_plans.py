#!/usr/bin/env python3
"""
Script to add job seeker subscription plans and job portals
"""

import pymysql
import os

def main():
    # Read the SQL script
    with open('database/jobseeker_subscription_update.sql', 'r') as f:
        sql_content = f.read()

    # Split SQL commands (handle multiline statements properly)
    commands = []
    current_command = ''
    lines = sql_content.split('\n')

    for line in lines:
        line = line.strip()
        if line and not line.startswith('--'):
            current_command += line + ' '
            if line.endswith(';'):
                commands.append(current_command.strip())
                current_command = ''

    # Connect to database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Naresh123',
        database='jobhunter_fresh',
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            for i, command in enumerate(commands):
                if command and command != ';':
                    try:
                        print(f'Executing command {i+1}/{len(commands)}: {command[:60]}...')
                        cursor.execute(command)
                        if command.lower().startswith('select'):
                            results = cursor.fetchall()
                            if results:
                                print(f'Results: {results}')
                    except Exception as e:
                        print(f'Error executing command {i+1}: {e}')
                        if 'Duplicate column name' not in str(e) and 'already exists' not in str(e):
                            raise
                        else:
                            print('Ignoring duplicate column/table error')
            
            connection.commit()
            print('\n✅ Job seeker subscription plans added successfully!')
            
            # Test query to show results
            cursor.execute('SELECT name, display_name, price_monthly, plan_type FROM subscription_plans WHERE plan_type = %s ORDER BY sort_order', ('jobseeker',))
            plans = cursor.fetchall()
            print(f'\n📋 Added {len(plans)} job seeker plans:')
            for plan in plans:
                print(f'   {plan[1]}: ${plan[2]}/month')
                
    finally:
        connection.close()

if __name__ == '__main__':
    main()