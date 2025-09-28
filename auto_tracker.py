#!/usr/bin/env python3
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
