"""
Prompt Tracking Middleware

This module provides middleware to automatically capture and track
user interactions and prompts in the Flask application.
"""

import json
import time
from datetime import datetime
from flask import request, g, current_app
from app.services.prompt_tracker import prompt_tracker

class PromptMiddleware:
    """Middleware to track prompts and interactions"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the middleware with the Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_appcontext(self.teardown)
    
    def before_request(self):
        """Called before each request"""
        g.start_time = time.time()
        g.request_data = {
            'method': request.method,
            'path': request.path,
            'args': dict(request.args),
            'form_data': dict(request.form) if request.form else None,
            'json_data': request.get_json() if request.is_json else None,
            'user_agent': request.headers.get('User-Agent', ''),
            'ip_address': request.remote_addr
        }
        
        # Track if this looks like a prompt-related request
        if self._is_prompt_request():
            self._track_prompt_request()
    
    def after_request(self, response):
        """Called after each request"""
        if hasattr(g, 'start_time'):
            response_time = time.time() - g.start_time
            
            # Log long-running requests that might indicate AI processing
            if response_time > 5:  # More than 5 seconds
                self._track_long_request(response_time)
        
        return response
    
    def teardown(self, exception):
        """Called when request context is torn down"""
        pass
    
    def _is_prompt_request(self) -> bool:
        """Determine if this request contains a prompt"""
        # Check for form data that might contain prompts
        if request.form and 'prompt' in str(request.form).lower():
            return True
        
        # Check for JSON data that might contain prompts
        if request.is_json:
            json_data = request.get_json()
            if json_data and isinstance(json_data, dict):
                for key, value in json_data.items():
                    if 'prompt' in key.lower() or (isinstance(value, str) and len(value) > 50):
                        return True
        
        # Check URL parameters
        if request.args:
            for key, value in request.args.items():
                if 'prompt' in key.lower() or 'query' in key.lower():
                    return True
        
        return False
    
    def _track_prompt_request(self):
        """Track a request that contains a prompt"""
        try:
            prompt_text = self._extract_prompt_text()
            if prompt_text:
                # Get current file from referer or other context
                current_file = self._get_current_file_context()
                
                # Track the prompt
                prompt_tracker.track_prompt(
                    prompt_text=prompt_text,
                    current_file=current_file,
                    project_phase="Web Interface Request"
                )
                
        except Exception as e:
            current_app.logger.error(f"Error tracking prompt request: {e}")
    
    def _extract_prompt_text(self) -> str:
        """Extract prompt text from the request"""
        # Try form data first
        if request.form:
            for key, value in request.form.items():
                if 'prompt' in key.lower() or 'query' in key.lower() or 'message' in key.lower():
                    return str(value)
        
        # Try JSON data
        if request.is_json:
            json_data = request.get_json()
            if json_data and isinstance(json_data, dict):
                for key, value in json_data.items():
                    if 'prompt' in key.lower() or 'query' in key.lower() or 'message' in key.lower():
                        return str(value)
                    # If value is a long string, it might be a prompt
                    if isinstance(value, str) and len(value) > 50:
                        return value
        
        # Try URL parameters
        if request.args:
            for key, value in request.args.items():
                if 'prompt' in key.lower() or 'query' in key.lower():
                    return str(value)
        
        return ""
    
    def _get_current_file_context(self) -> str:
        """Get current file context from referer or other sources"""
        referer = request.headers.get('Referer', '')
        if referer:
            return referer
        return request.path
    
    def _track_long_request(self, response_time: float):
        """Track requests that take a long time (might indicate AI processing)"""
        try:
            request_info = {
                'path': request.path,
                'method': request.method,
                'response_time': response_time,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # This could be logged or saved for analysis
            current_app.logger.info(f"Long request detected: {json.dumps(request_info)}")
            
        except Exception as e:
            current_app.logger.error(f"Error tracking long request: {e}")

def track_manual_prompt(prompt_text: str, current_file: str = None, 
                       response_summary: str = None, success_rating: int = None):
    """Manually track a prompt (for use in views or other parts of the application)"""
    try:
        prompt_tracker.track_prompt(
            prompt_text=prompt_text,
            current_file=current_file,
            response_summary=response_summary,
            success_rating=success_rating,
            project_phase="Manual Entry"
        )
    except Exception as e:
        current_app.logger.error(f"Error manually tracking prompt: {e}")

def track_file_operation(operation: str, file_path: str):
    """Track file operations"""
    try:
        if operation == 'created':
            prompt_tracker.track_file_created(file_path)
        elif operation == 'modified':
            prompt_tracker.track_file_modified(file_path)
    except Exception as e:
        current_app.logger.error(f"Error tracking file operation: {e}")

def track_command_execution(command: str):
    """Track command execution"""
    try:
        prompt_tracker.track_command_executed(command)
    except Exception as e:
        current_app.logger.error(f"Error tracking command execution: {e}")