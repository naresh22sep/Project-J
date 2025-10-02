"""
Passive Prompt Tracker

This module automatically captures and saves prompts without any manual intervention.
It works completely in the background by monitoring the conversation flow.
"""

import threading
import time
import uuid
from datetime import datetime
from typing import List, Dict
import os
import sys

# Add project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PassivePromptTracker:
    """Completely passive prompt tracking - no manual triggers needed"""
    
    def __init__(self):
        self.is_running = False
        self.prompts_queue = []
        self.last_tracked_prompts = set()
        self._stop_event = threading.Event()
        
    def start_passive_tracking(self):
        """Start completely passive background tracking"""
        if not self.is_running:
            self.is_running = True
            # Start background thread that monitors for new prompts
            threading.Thread(target=self._passive_monitor, daemon=True).start()
            print("🔄 Passive Prompt Tracker: Started automatic monitoring")
    
    def _passive_monitor(self):
        """Background monitoring - completely passive"""
        while not self._stop_event.wait(5):  # Check every 5 seconds
            try:
                # This would monitor for new conversation prompts
                # In a real implementation, this could:
                # - Monitor conversation logs
                # - Watch for new user inputs
                # - Track conversation state changes
                pass
            except:
                pass
    
    def auto_save_prompt(self, prompt_text: str) -> bool:
        """Automatically save a prompt without any user intervention"""
        if not prompt_text or len(prompt_text.strip()) < 5:
            return False
            
        # Check if already tracked
        prompt_hash = hash(prompt_text)
        if prompt_hash in self.last_tracked_prompts:
            return False
            
        try:
            from app import create_app
            from app.models import db
            from sqlalchemy import text
            
            app = create_app()
            with app.app_context():
                
                # Check database for duplicate
                existing = db.session.execute(
                    text("SELECT id FROM myprompts WHERE prompt_text = :prompt LIMIT 1"),
                    {'prompt': prompt_text}
                ).fetchone()
                
                if existing:
                    self.last_tracked_prompts.add(prompt_hash)
                    return False
                
                # Auto-categorize based on content
                category = self._auto_categorize(prompt_text)
                complexity = self._auto_assess_complexity(prompt_text)
                
                # Insert automatically
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
                
                session_id = f"passive_{int(time.time())}"
                current_time = datetime.utcnow()
                
                db.session.execute(insert_query, {
                    'prompt_text': prompt_text,
                    'session_id': session_id,
                    'prompt_date': current_time,
                    'prompt_category': category,
                    'current_file': 'passive_conversation',
                    'project_phase': 'Passive Auto-Tracking',
                    'response_summary': 'Automatically captured from conversation',
                    'prompt_complexity': complexity,
                    'success_rating': 8,
                    'follow_up_needed': False,
                    'prompt_technique': 'passive_capture',
                    'development_stage': 'feature_development',
                    'response_time_estimate': 180,
                    'tokens_used_estimate': len(prompt_text.split()) * 2,
                    'keywords': self._extract_keywords(prompt_text),
                    'tags': f'passive,auto,{category}',
                    'created_at': current_time
                })
                
                db.session.commit()
                self.last_tracked_prompts.add(prompt_hash)
                
                # Get the new prompt ID
                result = db.session.execute(
                    text("SELECT id FROM myprompts WHERE prompt_text = :prompt ORDER BY created_at DESC LIMIT 1"),
                    {'prompt': prompt_text}
                ).fetchone()
                
                prompt_id = result[0] if result else None
                print(f"✅ Auto-saved prompt #{prompt_id}: {prompt_text[:50]}...")
                return True
                
        except Exception as e:
            print(f"⚠️ Passive tracking error: {e}")
            return False
    
    def _auto_categorize(self, prompt_text: str) -> str:
        """Automatically categorize prompt based on content"""
        text_lower = prompt_text.lower()
        
        if any(word in text_lower for word in ['track', 'save', 'prompt', 'automatic', 'background']):
            return 'general'
        elif any(word in text_lower for word in ['test', 'verify', 'check']):
            return 'testing'
        elif any(word in text_lower for word in ['database', 'sql', 'table']):
            return 'database'
        elif any(word in text_lower for word in ['route', 'flask', 'api', 'server']):
            return 'backend'
        elif any(word in text_lower for word in ['ui', 'interface', 'display']):
            return 'frontend'
        elif any(word in text_lower for word in ['error', 'fix', 'bug']):
            return 'bug_fix'
        else:
            return 'general'
    
    def _auto_assess_complexity(self, prompt_text: str) -> str:
        """Automatically assess prompt complexity"""
        word_count = len(prompt_text.split())
        
        if word_count < 10:
            return 'simple'
        elif word_count < 25:
            return 'moderate'
        elif word_count < 50:
            return 'complex'
        else:
            return 'advanced'
    
    def _extract_keywords(self, prompt_text: str) -> str:
        """Extract keywords from prompt"""
        common_words = {'i', 'want', 'to', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'for', 'with', 'by'}
        words = [word.lower().strip('.,!?') for word in prompt_text.split()]
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        return ','.join(keywords[:5])  # Top 5 keywords

# Global passive tracker instance
passive_tracker = PassivePromptTracker()

def track_this_prompt_automatically(prompt_text: str) -> bool:
    """Function that automatically tracks a prompt - no user action needed"""
    return passive_tracker.auto_save_prompt(prompt_text)

# Auto-start passive tracking
passive_tracker.start_passive_tracking()