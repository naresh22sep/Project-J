#!/usr/bin/env python3
"""
Test Automatic Prompt Tracking

This script demonstrates how to automatically track prompts without manual intervention.
"""

import sys
import os
import requests
import json
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_auto_capture():
    """Test the automatic prompt capture functionality"""
    
    # Your current prompt from this conversation
    current_prompt = "This is not the ideal process i want to track all my prompts in background not like stopping the code and running few scripts ??"
    
    print("🧪 Testing Automatic Prompt Capture")
    print("=" * 50)
    print(f"📝 Current prompt: {current_prompt}")
    print()
    
    # Test the auto-capture API endpoint
    try:
        url = "http://localhost:5051/prompts/track-current"
        
        # Try as form data first
        print("🔄 Sending prompt to auto-capture endpoint...")
        response = requests.post(url, data={'prompt': current_prompt}, timeout=10)
        
        if response.status_code == 201:
            result = response.json()
            print("✅ SUCCESS: Prompt tracked automatically!")
            print(f"   📋 Message: {result.get('message')}")
            print(f"   🆔 ID: {result.get('id')}")
            print(f"   📄 Preview: {result.get('prompt_preview')}")
        elif response.status_code == 200:
            result = response.json()
            print("ℹ️  INFO: Prompt already exists")
            print(f"   📋 Message: {result.get('message')}")
            print(f"   🆔 ID: {result.get('id')}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Flask server")
        print("   Make sure the server is running on http://localhost:5051")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    print("🔍 Checking database for new prompts...")
    
    # Check database directly
    try:
        from app import create_app
        from app.models import MyPrompts, db
        from sqlalchemy import text
        
        app = create_app()
        with app.app_context():
            # Get total count
            result = db.session.execute(text("SELECT COUNT(*) as count FROM myprompts")).fetchone()
            total_count = result[0]
            print(f"📊 Total prompts in database: {total_count}")
            
            # Check if our prompt exists
            prompt_exists = MyPrompts.query.filter_by(prompt_text=current_prompt).first()
            if prompt_exists:
                print(f"✅ Found current prompt in database!")
                print(f"   🆔 ID: {prompt_exists.id}")
                print(f"   📅 Created: {prompt_exists.created_at}")
                print(f"   🏷️ Category: {prompt_exists.prompt_category}")
                print(f"   ⭐ Rating: {prompt_exists.success_rating}")
            else:
                print("❌ Current prompt not found in database")
                
                # Show recent prompts
                print("\n🔍 Recent prompts:")
                recent_prompts = MyPrompts.query.order_by(MyPrompts.created_at.desc()).limit(3).all()
                for i, prompt in enumerate(recent_prompts, 1):
                    print(f"   {i}. [{prompt.created_at}] {prompt.prompt_text[:60]}...")
                    
    except Exception as e:
        print(f"❌ Database check failed: {e}")
    
    print()
    print("🌐 Next Steps:")
    print("   1. Visit: http://localhost:5051/prompts/list")
    print("   2. View stats: http://localhost:5051/prompts/stats") 
    print("   3. Manual test: http://localhost:5051/test-prompt")
    print()
    print("💡 How to use automatic tracking:")
    print("   - Send POST request to /prompts/track-current with 'prompt' field")
    print("   - Or use the conversation tracker service in your code")
    print("   - Prompts are automatically analyzed and categorized")


if __name__ == "__main__":
    test_auto_capture()