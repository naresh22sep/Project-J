#!/usr/bin/env python3
"""
Test script to populate the myprompts table with sample data
and demonstrate the prompt tracking functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import MyPrompts, PromptCategory, PromptComplexity, DevelopmentStage
from app.services.prompt_tracker import prompt_tracker
from datetime import datetime
import time

def populate_test_data():
    """Populate the database with test prompt data"""
    
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
        
        print("\n📝 Adding test prompts...")
        
        # Test prompts that represent our conversation
        test_prompts = [
            {
                'text': 'test this route "http://localhost:5051/jobseeker/jobs?" for 4 module flask application',
                'category': PromptCategory.BACKEND,
                'complexity': PromptComplexity.MODERATE,
                'stage': DevelopmentStage.TESTING,
                'rating': 8
            },
            {
                'text': 'remove complete authentication from all modules temporarly',
                'category': PromptCategory.BACKEND,
                'complexity': PromptComplexity.COMPLEX,
                'stage': DevelopmentStage.REFACTORING,
                'rating': 9
            },
            {
                'text': 'For all modules and all routes remove the code and print some message, No layout css required just to check the url remove all code lines related to authentication',
                'category': PromptCategory.BACKEND,
                'complexity': PromptComplexity.COMPLEX,
                'stage': DevelopmentStage.REFACTORING,
                'rating': 10
            },
            {
                'text': 'show me all prompts related to this application?',
                'category': PromptCategory.DOCUMENTATION,
                'complexity': PromptComplexity.SIMPLE,
                'stage': DevelopmentStage.DOCUMENTATION,
                'rating': 7
            },
            {
                'text': 'how many prompts i can see?',
                'category': PromptCategory.GENERAL,
                'complexity': PromptComplexity.SIMPLE,
                'stage': DevelopmentStage.DOCUMENTATION,
                'rating': 6
            },
            {
                'text': 'i just want some model to save the prompts (history) and infuture by using the below schema',
                'category': PromptCategory.DATABASE,
                'complexity': PromptComplexity.ADVANCED,
                'stage': DevelopmentStage.FEATURE_DEVELOPMENT,
                'rating': 10
            }
        ]
        
        print(f"Adding {len(test_prompts)} test prompts...")
        
        for i, prompt_data in enumerate(test_prompts, 1):
            print(f"  Adding prompt {i}: {prompt_data['text'][:50]}...")
            
            # Use the prompt tracker service
            prompt_tracker.track_prompt(
                prompt_text=prompt_data['text'],
                current_file="test_script.py",
                response_summary="Test prompt added successfully",
                success_rating=prompt_data['rating'],
                project_phase="Test Data Population"
            )
            
            # Small delay to ensure different timestamps
            time.sleep(0.1)
        
        # Wait a moment for background threads to complete
        time.sleep(2)
        
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
                print()
        
        print("🎉 Test data population complete!")
        print("\n🌐 You can now visit these URLs to see your prompts:")
        print("   📋 List all prompts: http://localhost:5051/prompts/list")
        print("   📊 View statistics: http://localhost:5051/prompts/stats") 
        print("   🧪 Test tracking: http://localhost:5051/test-prompt")

if __name__ == "__main__":
    populate_test_data()