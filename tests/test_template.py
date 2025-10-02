#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import render_template

# Create Flask app
app = create_app()

with app.app_context():
    try:
        print("Testing template rendering...")
        # Test direct template rendering
        result = render_template('auth/login.html', role='superadmin')
        print(f"Template rendered successfully! Length: {len(result)} chars")
        print("First 200 characters:")
        print(result[:200])
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()