#!/usr/bin/env python3
"""
Quick Test for Automatic Prompt Tracking
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_automatic_tracking():
    """Test the automatic prompt tracking with your test prompt"""
    
    test_prompt = "TEST PROMPT TO VERIFY THE AUTOMATIC PROMPT TRACKING"
    
    print("🧪 Testing Automatic Prompt Tracking")
    print("=" * 50)
    print(f"📝 Test prompt: {test_prompt}")
    print()
    
    try:
        # Import the auto tracker
        from auto_tracker import track_prompt
        
        print("🔄 Tracking prompt automatically...")
        
        # Track the prompt
        prompt_id = track_prompt(
            test_prompt, 
            category='testing', 
            complexity='simple', 
            rating=9
        )
        
        if prompt_id:
            print("✅ SUCCESS: Automatic tracking worked!")
            print(f"   🆔 Prompt ID: {prompt_id}")
            print(f"   🏷️ Category: testing")
            print(f"   ⚡ Complexity: simple")
            print(f"   ⭐ Rating: 9/10")
            
            # Verify in database
            from app import create_app
            from app.models import db
            from sqlalchemy import text
            
            app = create_app()
            with app.app_context():
                # Get the tracked prompt details
                result = db.session.execute(
                    text("SELECT id, created_at, prompt_category, prompt_complexity, success_rating FROM myprompts WHERE id = :id"),
                    {'id': prompt_id}
                ).fetchone()
                
                if result:
                    print("\n📊 Database Verification:")
                    print(f"   🆔 ID: {result[0]}")
                    print(f"   📅 Created: {result[1]}")
                    print(f"   🏷️ Category: {result[2]}")
                    print(f"   ⚡ Complexity: {result[3]}")
                    print(f"   ⭐ Rating: {result[4]}")
                    
                # Get total count
                count_result = db.session.execute(text("SELECT COUNT(*) FROM myprompts")).fetchone()
                total_count = count_result[0]
                print(f"\n📈 Total prompts in database: {total_count}")
                
        else:
            print("❌ FAILED: Could not track the prompt")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print(f"\n🌐 View your test prompt at:")
    print(f"   📋 All prompts: http://localhost:5051/prompts/list")
    if 'prompt_id' in locals() and prompt_id:
        print(f"   🔍 This prompt: http://localhost:5051/prompts/{prompt_id}")

if __name__ == "__main__":
    test_automatic_tracking()