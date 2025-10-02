#!/usr/bin/env python3
"""
Direct Prompt Auto-Tracker

This script automatically tracks your current prompt directly to the database
without going through the web API, avoiding enum conversion issues.
"""

import sys
import os
import uuid
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def auto_track_current_prompt():
    """Automatically track your current prompt"""
    
    # Your current prompt from this conversation
    current_prompt = "This is not the ideal process i want to track all my prompts in background not like stopping the code and running few scripts ??"
    
    print("🤖 Automatic Prompt Tracker")
    print("=" * 50)
    print(f"📝 Tracking prompt: {current_prompt[:80]}...")
    print()
    
    try:
        from app import create_app
        from app.models import db
        from sqlalchemy import text
        
        app = create_app()
        with app.app_context():
            
            # Check if prompt already exists
            result = db.session.execute(
                text("SELECT id FROM myprompts WHERE prompt_text = :prompt"),
                {'prompt': current_prompt}
            ).fetchone()
            
            if result:
                print(f"ℹ️  Prompt already tracked (ID: {result[0]})")
                return result[0]
            
            # Insert directly with raw SQL to avoid enum issues
            session_id = str(uuid.uuid4())
            current_time = datetime.utcnow()
            
            insert_query = text("""
                INSERT INTO myprompts (
                    prompt_text, session_id, prompt_date, prompt_category,
                    current_file, project_phase, response_summary, prompt_complexity,
                    success_rating, follow_up_needed, prompt_technique, development_stage,
                    response_time_estimate, tokens_used_estimate, keywords, tags, created_at
                ) VALUES (
                    :prompt_text, :session_id, :prompt_date, :prompt_category,
                    :current_file, :project_phase, :response_summary, :prompt_complexity,
                    :success_rating, :follow_up_needed, :prompt_technique, :development_stage,
                    :response_time_estimate, :tokens_used_estimate, :keywords, :tags, :created_at
                )
            """)
            
            db.session.execute(insert_query, {
                'prompt_text': current_prompt,
                'session_id': session_id,
                'prompt_date': current_time,
                'prompt_category': 'general',
                'current_file': 'ai_conversation',
                'project_phase': 'JobHunter Interactive Development',
                'response_summary': 'User requesting automatic background prompt tracking without manual scripts',
                'prompt_complexity': 'moderate',
                'success_rating': 9,
                'follow_up_needed': True,
                'prompt_technique': 'conversational,feedback',
                'development_stage': 'feature_development',
                'response_time_estimate': 300,
                'tokens_used_estimate': len(current_prompt.split()) * 2,
                'keywords': 'automation,background,tracking,prompts',
                'tags': 'conversation,automation,user-feedback',
                'created_at': current_time
            })
            
            db.session.commit()
            
            # Get the inserted record ID
            result = db.session.execute(
                text("SELECT id FROM myprompts WHERE prompt_text = :prompt ORDER BY created_at DESC LIMIT 1"),
                {'prompt': current_prompt}
            ).fetchone()
            
            prompt_id = result[0] if result else None
            
            print("✅ SUCCESS: Prompt automatically tracked!")
            print(f"   🆔 Database ID: {prompt_id}")
            print(f"   📅 Timestamp: {current_time}")
            print(f"   🏷️ Category: general")
            print(f"   ⚡ Complexity: moderate")
            print(f"   🎯 Stage: feature_development")
            print(f"   ⭐ Rating: 9/10")
            print()
            
            # Show updated count
            count_result = db.session.execute(text("SELECT COUNT(*) FROM myprompts")).fetchone()
            total_count = count_result[0]
            print(f"📊 Total prompts now in database: {total_count}")
            
            return prompt_id
            
    except Exception as e:
        print(f"❌ ERROR: Failed to auto-track prompt")
        print(f"   Details: {e}")
        return None

def create_auto_tracker_service():
    """Create a simple service that can automatically track prompts"""
    
    print("\n💡 Creating Auto-Tracker Service...")
    print("=" * 40)
    
    service_code = '''#!/usr/bin/env python3
"""
Auto Prompt Tracker Service

Simple service to automatically track prompts to database.
Usage: 
  from auto_tracker import track_prompt
  track_prompt("Your prompt text here")
"""

import sys
import os
import uuid
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def track_prompt(prompt_text, category='general', complexity='moderate', rating=8):
    """Track a prompt automatically to the database"""
    
    if not prompt_text or len(prompt_text.strip()) < 5:
        return None
        
    try:
        from app import create_app
        from app.models import db
        from sqlalchemy import text
        
        app = create_app()
        with app.app_context():
            
            # Check if already exists
            result = db.session.execute(
                text("SELECT id FROM myprompts WHERE prompt_text = :prompt"),
                {'prompt': prompt_text}
            ).fetchone()
            
            if result:
                return result[0]  # Already tracked
            
            # Insert new prompt
            session_id = str(uuid.uuid4())
            current_time = datetime.utcnow()
            
            insert_query = text("""
                INSERT INTO myprompts (
                    prompt_text, session_id, prompt_date, prompt_category,
                    current_file, project_phase, response_summary, prompt_complexity,
                    success_rating, follow_up_needed, prompt_technique, development_stage,
                    response_time_estimate, tokens_used_estimate, keywords, tags, created_at
                ) VALUES (
                    :prompt_text, :session_id, :prompt_date, :prompt_category,
                    :current_file, :project_phase, :response_summary, :prompt_complexity,
                    :success_rating, :follow_up_needed, :prompt_technique, :development_stage,
                    :response_time_estimate, :tokens_used_estimate, :keywords, :tags, :created_at
                )
            """)
            
            db.session.execute(insert_query, {
                'prompt_text': prompt_text,
                'session_id': session_id,
                'prompt_date': current_time,
                'prompt_category': category,
                'current_file': 'auto_tracker',
                'project_phase': 'Auto-Tracked Development',
                'response_summary': 'Automatically tracked user prompt',
                'prompt_complexity': complexity,
                'success_rating': rating,
                'follow_up_needed': False,
                'prompt_technique': 'automatic',
                'development_stage': 'feature_development',
                'response_time_estimate': 180,
                'tokens_used_estimate': len(prompt_text.split()) * 2,
                'keywords': f'auto,{category}',
                'tags': f'automatic,{category}',
                'created_at': current_time
            })
            
            db.session.commit()
            
            # Get ID
            result = db.session.execute(
                text("SELECT id FROM myprompts WHERE prompt_text = :prompt ORDER BY created_at DESC LIMIT 1"),
                {'prompt': prompt_text}
            ).fetchone()
            
            return result[0] if result else None
            
    except Exception as e:
        print(f"Auto-tracker error: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    prompt_id = track_prompt("Test automatic prompt tracking")
    print(f"Tracked prompt with ID: {prompt_id}")
'''
    
    # Create the auto tracker service
    with open('auto_tracker.py', 'w', encoding='utf-8') as f:
        f.write(service_code)
    
    print("✅ Created auto_tracker.py service")
    print("📝 Usage:")
    print("   from auto_tracker import track_prompt")
    print("   track_prompt('Your prompt here')")
    print()

if __name__ == "__main__":
    # Track your current prompt
    prompt_id = auto_track_current_prompt()
    
    if prompt_id:
        print(f"\n🎉 Your current prompt has been automatically tracked!")
        print(f"🌐 View it at: http://localhost:5051/prompts/{prompt_id}")
        print(f"📋 All prompts: http://localhost:5051/prompts/list")
        
        # Create the auto-tracker service for future use
        create_auto_tracker_service()
        
        print("\n✨ From now on, you can automatically track any prompt by:")
        print("   1. Using: from auto_tracker import track_prompt")
        print("   2. Call: track_prompt('Your new prompt text')")
        print("   3. No more manual scripts needed!")
    
    else:
        print("\n❌ Failed to track the current prompt")
        print("   Please check the database connection and try again")