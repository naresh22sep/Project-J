#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request
from app import create_app

# Create test Flask app
test_app = Flask(__name__)
test_app.secret_key = 'test-secret-key'

@test_app.route('/test-login')
def test_login():
    """Test route to verify template rendering"""
    try:
        return render_template('auth/login.html', role='superadmin')
    except Exception as e:
        return f"Template Error: {str(e)}"

@test_app.route('/test-basic')
def test_basic():
    """Basic test route"""
    return "Basic route working!"

if __name__ == '__main__':
    print("Starting test Flask app...")
    print("Test routes:")
    print("- http://localhost:5052/test-basic")
    print("- http://localhost:5052/test-login")
    test_app.run(debug=True, port=5052)