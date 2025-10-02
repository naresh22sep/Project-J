#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.auth.auth_models import CSRFToken

# Create Flask app
app = create_app()

with app.app_context():
    try:
        # Test CSRF token generation
        print("Testing CSRF token generation...")
        token = CSRFToken.generate_token(
            user_id=None,
            session_id="test_session",
            ip_address="127.0.0.1",
            user_agent="test"
        )
        print(f"Generated token: {token}")
        print(f"Token type: {type(token)}")
        print("CSRF token generation successful!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()