#!/usr/bin/env python3
"""
Add Missing Prompts using Raw SQL to avoid enum conversion issues
"""

import sys
import os
import uuid
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db

def add_missing_prompts_raw():
    """Add all the prompts from our conversation using raw SQL"""
    
    app = create_app()
    with app.app_context():
        
        print("🔍 Checking current prompts...")
        
        # Get current count using raw SQL
        result = db.session.execute(db.text("SELECT COUNT(*) as count FROM myprompts"))
        current_count = result.fetchone()[0]
        print(f"Current prompts in database: {current_count}")
        
        # Get existing texts to avoid duplicates
        result = db.session.execute(db.text("SELECT prompt_text FROM myprompts"))
        existing_prompts = {row[0] for row in result.fetchall()}
        print(f"Existing unique prompts: {len(existing_prompts)}")
        
        session_id = str(uuid.uuid4())
        base_time = datetime.utcnow() - timedelta(hours=2)
        
        # Complete conversation history
        conversation_prompts = [
            {
                'text': 'test this route "http://localhost:5051/jobseeker/jobs?" for 4 module flask application',
                'category': 'backend', 'complexity': 'moderate', 'stage': 'testing',
                'rating': 8, 'offset_minutes': 0
            },
            {
                'text': 'remove complete authentication from all modules temporarly',
                'category': 'backend', 'complexity': 'complex', 'stage': 'refactoring',
                'rating': 9, 'offset_minutes': 15
            },
            {
                'text': 'Continue: "Continue to iterate?"',
                'category': 'general', 'complexity': 'simple', 'stage': 'feature_development',
                'rating': 5, 'offset_minutes': 30
            },
            {
                'text': 'For all modules and all routes remove the code and print some message, No layout css required just to check the url remove all code lines related to authentication .. make sure routes should display the name of the route and path',
                'category': 'backend', 'complexity': 'complex', 'stage': 'refactoring',
                'rating': 10, 'offset_minutes': 45
            },
            {
                'text': '🎯 JobHunter Platform - 4-Module Flask Application [ERROR TRACEBACK] SyntaxError: source code string cannot contain null bytes',
                'category': 'bug_fix', 'complexity': 'moderate', 'stage': 'bug_fixing',
                'rating': 8, 'offset_minutes': 60
            },
            {
                'text': 'show me all prompts related to this application ?',
                'category': 'documentation', 'complexity': 'simple', 'stage': 'documentation',
                'rating': 7, 'offset_minutes': 75
            },
            {
                'text': 'how many prompts i can see ?',
                'category': 'general', 'complexity': 'simple', 'stage': 'documentation',
                'rating': 6, 'offset_minutes': 80
            },
            {
                'text': 'i just want some model to save the prompts (history) and infuture by using the below schema [FULL SCHEMA PROVIDED] the table(myprompts) is already availale in database , add code for this functionality',
                'category': 'database', 'complexity': 'advanced', 'stage': 'feature_development',
                'rating': 10, 'offset_minutes': 85
            },
            {
                'text': 'Continue: "Continue to iterate?" (second iteration)',
                'category': 'general', 'complexity': 'simple', 'stage': 'feature_development',
                'rating': 6, 'offset_minutes': 120
            },
            {
                'text': 'The table is empty ?',
                'category': 'database', 'complexity': 'simple', 'stage': 'bug_fixing',
                'rating': 7, 'offset_minutes': 125
            },
            {
                'text': 'Do we need to configure anything to store this prompts ?',
                'category': 'general', 'complexity': 'moderate', 'stage': 'documentation',
                'rating': 8, 'offset_minutes': 130
            },
            {
                'text': 'When exactly the prompts will be saved !',
                'category': 'general', 'complexity': 'moderate', 'stage': 'documentation',
                'rating': 8, 'offset_minutes': 135
            },
            {
                'text': 'I have provided few other prompts those are not in the database ?',
                'category': 'bug_fix', 'complexity': 'moderate', 'stage': 'bug_fixing',
                'rating': 8, 'offset_minutes': 140
            }
        ]
        
        added_count = 0
        skipped_count = 0
        
        print(f"\n📝 Adding missing prompts using raw SQL...")
        
        for prompt_data in conversation_prompts:
            if prompt_data['text'] not in existing_prompts:
                print(f"  ✅ Adding: {prompt_data['text'][:60]}...")
                
                prompt_time = base_time + timedelta(minutes=prompt_data['offset_minutes'])
                
                # Use raw SQL INSERT to avoid enum conversion issues
                insert_query = db.text("""
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
                    'prompt_text': prompt_data['text'],
                    'session_id': session_id,
                    'prompt_date': prompt_time,
                    'prompt_category': prompt_data['category'],
                    'current_file': 'conversation_history',
                    'project_phase': 'JobHunter Development',
                    'response_summary': 'Successfully processed user request with comprehensive solution',
                    'prompt_complexity': prompt_data['complexity'],
                    'success_rating': prompt_data['rating'],
                    'follow_up_needed': False,
                    'prompt_technique': 'conversational,task-oriented',
                    'development_stage': prompt_data['stage'],
                    'response_time_estimate': 300,
                    'tokens_used_estimate': len(prompt_data['text'].split()) * 2,
                    'keywords': f"flask,jobhunter,{prompt_data['category']}",
                    'tags': f"conversation,{prompt_data['category']},{prompt_data['stage']}",
                    'created_at': datetime.utcnow()
                })
                
                added_count += 1
            else:
                print(f"  ⏭️ Skipping existing: {prompt_data['text'][:60]}...")
                skipped_count += 1
        
        # Commit all at once
        if added_count > 0:
            db.session.commit()
            print(f"\n✅ Successfully added {added_count} new prompts!")
        else:
            print(f"\n✅ All prompts already exist in database!")
        
        print(f"📊 Summary:")
        print(f"   Added: {added_count}")
        print(f"   Skipped: {skipped_count}")
        print(f"   Total conversation prompts: {len(conversation_prompts)}")
        
        # Final count using raw SQL
        result = db.session.execute(db.text("SELECT COUNT(*) as count FROM myprompts"))
        final_count = result.fetchone()[0]
        print(f"\n🎉 Final database count: {final_count} prompts")
        
        if final_count > 0:
            print("\n📋 Latest prompts:")
            result = db.session.execute(db.text("""
                SELECT id, created_at, LEFT(prompt_text, 70) as sample_text 
                FROM myprompts 
                ORDER BY created_at DESC 
                LIMIT 5
            """))
            for i, row in enumerate(result.fetchall(), 1):
                print(f"{i}. [{row.created_at}] {row.sample_text}...")
        
        print("\n🌐 View your prompts at:")
        print("   📋 http://localhost:5051/prompts/list")
        print("   📊 http://localhost:5051/prompts/stats")
        print("   🧪 http://localhost:5051/test-prompt")

if __name__ == "__main__":
    add_missing_prompts_raw()