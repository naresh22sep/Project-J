#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import render_template

# Create Flask app
app = create_app()

with app.test_request_context('/superadmin/auth/login'):
    try:
        print("Testing template rendering with request context...")
        # Test direct template rendering
        result = render_template('auth/login.html', role='superadmin')
        print(f"Template rendered successfully! Length: {len(result)} chars")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()