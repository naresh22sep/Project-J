"""
Conversation Tracker Service

This service automatically tracks prompts from AI conversations in the background.
It monitors for new prompts and saves them to the database without manual intervention.
"""

import os
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import Flask
from app.models import MyPrompts, db
from app.services.prompt_tracker import PromptAnalyzer

class ConversationTracker:
    """Tracks AI conversation prompts automatically in the background"""
    
    def __init__(self, app: Flask = None):
        self.app = app
        self.analyzer = PromptAnalyzer()
        self.last_check = datetime.utcnow()
        self.conversation_history = []
        self.tracking_enabled = True
        self.check_interval = 30  # seconds
        self._stop_event = threading.Event()
        self._thread = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize the conversation tracker with Flask app"""
        self.app = app
        
        # Start background tracking thread
        if self.tracking_enabled and not self._thread:
            self._thread = threading.Thread(target=self._background_tracker, daemon=True)
            self._thread.start()
            print("🤖 Conversation Tracker: Started background monitoring")
    
    def _background_tracker(self):
        """Background thread that monitors for new prompts"""
        while not self._stop_event.wait(self.check_interval):
            try:
                with self.app.app_context():
                    self._check_for_new_prompts()
            except Exception as e:
                print(f"🚨 Conversation Tracker Error: {e}")
    
    def _check_for_new_prompts(self):
        """Check for new conversation prompts and save them"""
        # This method will be extended to detect new prompts from various sources
        
        # For now, we'll implement a simple file-based detection
        # In a real-world scenario, this could monitor:
        # - Chat logs
        # - API requests
        # - Conversation files
        # - Real-time chat streams
        
        pass
    
    def track_conversation_prompt(self, prompt_text: str, context: Dict = None):
        """Track a prompt from an ongoing conversation"""
        try:
            if not prompt_text or len(prompt_text.strip()) < 5:
                return False
                
            # Check if this prompt was already tracked
            existing = MyPrompts.query.filter_by(prompt_text=prompt_text).first()
            if existing:
                return False
                
            with self.app.app_context():
                # Analyze the prompt
                analysis = self.analyzer.analyze_prompt(prompt_text, context or {})
                
                # Create new prompt record
                new_prompt = MyPrompts(
                    prompt_text=prompt_text,
                    session_id=context.get('session_id', 'conversation'),
                    prompt_date=datetime.utcnow(),
                    prompt_category=analysis['category'],
                    current_file=context.get('current_file', 'ai_conversation'),
                    project_phase=context.get('project_phase', 'Interactive Development'),
                    response_summary=analysis.get('response_summary', 'AI conversation response'),
                    prompt_complexity=analysis['complexity'],
                    success_rating=context.get('rating', 8),
                    follow_up_needed=analysis.get('follow_up_needed', False),
                    prompt_technique=analysis.get('technique', 'conversational'),
                    development_stage=analysis['development_stage'],
                    response_time_estimate=analysis.get('response_time', 300),
                    tokens_used_estimate=len(prompt_text.split()) * 2,
                    keywords=analysis.get('keywords', ''),
                    tags=analysis.get('tags', ''),
                    created_at=datetime.utcnow()
                )
                
                db.session.add(new_prompt)
                db.session.commit()
                
                print(f"✅ Auto-tracked prompt: {prompt_text[:50]}...")
                return True
                
        except Exception as e:
            print(f"❌ Error tracking conversation prompt: {e}")
            return False
    
    def track_current_prompt(self, prompt: str):
        """Track the current user prompt automatically"""
        if self.tracking_enabled:
            context = {
                'session_id': f'session_{int(time.time())}',
                'current_file': 'ai_conversation',
                'project_phase': 'JobHunter Development',
                'rating': 8
            }
            return self.track_conversation_prompt(prompt, context)
        return False
    
    def stop(self):
        """Stop the background tracker"""
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        print("🛑 Conversation Tracker: Stopped background monitoring")

# Global conversation tracker instance
conversation_tracker = ConversationTracker()

def track_user_prompt(prompt_text: str) -> bool:
    """Convenience function to track a user prompt"""
    return conversation_tracker.track_current_prompt(prompt_text)