#!/usr/bin/env python3
"""
Direct database population script - no threading
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import MyPrompts, PromptCategory, PromptComplexity, DevelopmentStage, db
from datetime import datetime
import uuid

def populate_directly():
    """Populate the database directly without background threading"""
    
    app = create_app()
    with app.app_context():
        
        print("🔍 Checking current prompt count...")
        current_count = MyPrompts.query.count()
        print(f"Current prompts in database: {current_count}")
        
        if current_count > 0:
            print("✅ Database already has prompts. Showing first 5:")
            prompts = MyPrompts.query.order_by(MyPrompts.created_at.desc()).limit(5).all()
            for i, prompt in enumerate(prompts, 1):
                print(f"{i}. [{prompt.created_at}] {prompt.prompt_text[:50]}...")
            return
        
        print("\n📝 Adding test prompts directly to database...")
        
        session_id = str(uuid.uuid4())
        
        # Test prompts that represent our conversation
        test_prompts = [
            {
                'text': 'test this route "http://localhost:5051/jobseeker/jobs?" for 4 module flask application',
                'category': PromptCategory.BACKEND,
                'complexity': PromptComplexity.MODERATE,
                'stage': DevelopmentStage.TESTING,
                'rating': 8,
                'keywords': 'flask,route,test,jobseeker',
                'tags': 'backend,flask,routing,testing'
            },
            {
                'text': 'remove complete authentication from all modules temporarly',
                'category': PromptCategory.BACKEND,
                'complexity': PromptComplexity.COMPLEX,
                'stage': DevelopmentStage.REFACTORING,
                'rating': 9,
                'keywords': 'authentication,remove,modules',
                'tags': 'backend,authentication,refactoring'
            },
            {
                'text': 'For all modules and all routes remove the code and print some message, No layout css required just to check the url remove all code lines related to authentication',
                'category': PromptCategory.BACKEND,
                'complexity': PromptComplexity.COMPLEX,
                'stage': DevelopmentStage.REFACTORING,
                'rating': 10,
                'keywords': 'modules,routes,remove,authentication',
                'tags': 'backend,refactoring,simplification'
            },
            {
                'text': 'show me all prompts related to this application?',
                'category': PromptCategory.DOCUMENTATION,
                'complexity': PromptComplexity.SIMPLE,
                'stage': DevelopmentStage.DOCUMENTATION,
                'rating': 7,
                'keywords': 'prompts,show,application',
                'tags': 'documentation,history,prompts'
            },
            {
                'text': 'how many prompts i can see?',
                'category': PromptCategory.GENERAL,
                'complexity': PromptComplexity.SIMPLE,
                'stage': DevelopmentStage.DOCUMENTATION,
                'rating': 6,
                'keywords': 'prompts,count,see',
                'tags': 'general,query,count'
            },
            {
                'text': 'i just want some model to save the prompts (history) and infuture by using the below schema',
                'category': PromptCategory.DATABASE,
                'complexity': PromptComplexity.ADVANCED,
                'stage': DevelopmentStage.FEATURE_DEVELOPMENT,
                'rating': 10,
                'keywords': 'model,prompts,history,schema,database',
                'tags': 'database,model,feature,schema'
            },
            {
                'text': 'The table is empty?',
                'category': PromptCategory.DATABASE,
                'complexity': PromptComplexity.SIMPLE,
                'stage': DevelopmentStage.BUG_FIXING,
                'rating': 5,
                'keywords': 'table,empty,database',
                'tags': 'database,debugging,issue'
            }
        ]
        
        print(f"Adding {len(test_prompts)} test prompts...")
        
        for i, prompt_data in enumerate(test_prompts, 1):
            print(f"  Adding prompt {i}: {prompt_data['text'][:50]}...")
            
            new_prompt = MyPrompts(
                prompt_text=prompt_data['text'],
                session_id=session_id,
                prompt_date=datetime.utcnow(),
                prompt_category=prompt_data['category'],
                current_file="conversation_history",
                project_phase="JobHunter Development",
                response_summary="Successfully processed user request with comprehensive solution",
                prompt_complexity=prompt_data['complexity'],
                success_rating=prompt_data['rating'],
                follow_up_needed=False,
                prompt_technique="conversational,task-oriented",
                development_stage=prompt_data['stage'],
                response_time_estimate=300,  # 5 minutes average
                tokens_used_estimate=len(prompt_data['text'].split()) * 2,
                keywords=prompt_data['keywords'],
                tags=prompt_data['tags']
            )
            
            db.session.add(new_prompt)
        
        # Commit all at once
        db.session.commit()
        
        print("\n✅ Test data added! Checking results...")
        new_count = MyPrompts.query.count()
        print(f"Total prompts now: {new_count}")
        
        if new_count > 0:
            print("\n📊 Recent prompts:")
            recent_prompts = MyPrompts.query.order_by(MyPrompts.created_at.desc()).limit(5).all()
            for i, prompt in enumerate(recent_prompts, 1):
                print(f"{i}. [{prompt.created_at}] Category: {prompt.prompt_category.value if prompt.prompt_category else 'N/A'}")
                print(f"   Text: {prompt.prompt_text[:80]}...")
                print(f"   Complexity: {prompt.prompt_complexity.value if prompt.prompt_complexity else 'N/A'}")
                print(f"   Rating: {prompt.success_rating}/10")
                print()
        
        print("🎉 Test data population complete!")
        print("\n🌐 You can now visit these URLs to see your prompts:")
        print("   📋 List all prompts: http://localhost:5051/prompts/list")
        print("   📊 View statistics: http://localhost:5051/prompts/stats") 
        print("   🧪 Test tracking: http://localhost:5051/test-prompt")

if __name__ == "__main__":
    populate_directly()