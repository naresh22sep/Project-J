#!/usr/bin/env python3
"""
Check actual enum values in the database
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import MyPrompts, db

def check_enum_values():
    """Check what enum values are actually in the database"""
    
    app = create_app()
    with app.app_context():
        
        print("🔍 Checking existing prompts and their enum values...")
        
        # Get all prompts to see actual values
        try:
            prompts = MyPrompts.query.limit(10).all()
            print(f"\n📊 Found {len(prompts)} prompts:")
            
            for i, prompt in enumerate(prompts, 1):
                print(f"{i}. ID: {prompt.id}")
                print(f"   Text: {prompt.prompt_text[:60]}...")
                print(f"   Category: '{prompt.prompt_category}' (type: {type(prompt.prompt_category)})")
                print(f"   Complexity: '{prompt.prompt_complexity}' (type: {type(prompt.prompt_complexity)})")
                print(f"   Stage: '{prompt.development_stage}' (type: {type(prompt.development_stage)})")
                print()
        except Exception as e:
            print(f"❌ Error reading prompts: {e}")
            
            # Try raw SQL instead
            print("🔄 Trying raw SQL...")
            with db.engine.connect() as connection:
                result = connection.execute(db.text("""
                    SELECT 
                        id,
                        prompt_category,
                        prompt_complexity, 
                        development_stage,
                        LEFT(prompt_text, 60) as sample_text
                    FROM myprompts 
                    LIMIT 5
                """))
                
                print("\n📊 Raw SQL results:")
                for row in result:
                    print(f"ID: {row.id} | Category: '{row.prompt_category}' | Complexity: '{row.prompt_complexity}' | Stage: '{row.development_stage}'")
                    print(f"   Sample: {row.sample_text}...")
                    print()

if __name__ == "__main__":
    check_enum_values()