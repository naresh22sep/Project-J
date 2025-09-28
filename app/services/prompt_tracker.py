"""
Prompt Tracking Service

This module provides functionality to track and analyze user prompts
automatically in the background for the JobHunter Flask application.
"""

import os
import re
import json
import uuid
import threading
from datetime import datetime
from typing import Optional, Dict, List, Any
import subprocess

from app.models import MyPrompts, PromptCategory, PromptComplexity, DevelopmentStage
from app import db

class PromptAnalyzer:
    """Analyzes prompts to automatically categorize and extract metadata"""
    
    # Keywords for categorizing prompts
    CATEGORY_KEYWORDS = {
        PromptCategory.DATABASE: ['database', 'mysql', 'table', 'query', 'sql', 'schema', 'migration'],
        PromptCategory.FRONTEND: ['html', 'css', 'javascript', 'ui', 'interface', 'template', 'jinja'],
        PromptCategory.BACKEND: ['flask', 'python', 'route', 'api', 'server', 'endpoint', 'function'],
        PromptCategory.API: ['api', 'rest', 'json', 'endpoint', 'request', 'response', 'http'],
        PromptCategory.UI_UX: ['design', 'layout', 'user interface', 'experience', 'usability'],
        PromptCategory.BUG_FIX: ['error', 'bug', 'fix', 'problem', 'issue', 'traceback', 'exception'],
        PromptCategory.FEATURE_REQUEST: ['add', 'create', 'implement', 'feature', 'functionality'],
        PromptCategory.DOCUMENTATION: ['document', 'readme', 'help', 'guide', 'tutorial', 'explain'],
        PromptCategory.TESTING: ['test', 'testing', 'unit', 'integration', 'pytest', 'validate'],
        PromptCategory.DEPLOYMENT: ['deploy', 'deployment', 'server', 'production', 'hosting']
    }
    
    # Complexity indicators
    COMPLEXITY_INDICATORS = {
        PromptComplexity.SIMPLE: ['simple', 'easy', 'basic', 'quick', 'small'],
        PromptComplexity.MODERATE: ['moderate', 'medium', 'standard', 'normal'],
        PromptComplexity.COMPLEX: ['complex', 'complicated', 'advanced', 'difficult', 'multiple'],
        PromptComplexity.ADVANCED: ['advanced', 'sophisticated', 'enterprise', 'architecture', 'system']
    }
    
    @classmethod
    def categorize_prompt(cls, prompt_text: str) -> PromptCategory:
        """Automatically categorize a prompt based on keywords"""
        prompt_lower = prompt_text.lower()
        
        category_scores = {}
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return PromptCategory.GENERAL
    
    @classmethod
    def assess_complexity(cls, prompt_text: str) -> PromptComplexity:
        """Assess the complexity of a prompt"""
        prompt_lower = prompt_text.lower()
        word_count = len(prompt_text.split())
        
        # Check for complexity keywords
        for complexity, keywords in cls.COMPLEXITY_INDICATORS.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return complexity
        
        # Assess by length and structure
        if word_count < 10:
            return PromptComplexity.SIMPLE
        elif word_count < 30:
            return PromptComplexity.MODERATE
        elif word_count < 100:
            return PromptComplexity.COMPLEX
        else:
            return PromptComplexity.ADVANCED
    
    @classmethod
    def extract_keywords(cls, prompt_text: str) -> str:
        """Extract key terms from the prompt"""
        # Simple keyword extraction using common technical terms
        technical_terms = re.findall(r'\b(?:flask|python|database|mysql|api|route|function|class|model|template|error|bug|fix|test|create|add|remove|update|delete)\b', 
                                   prompt_text.lower())
        return ','.join(list(set(technical_terms))[:10])  # Limit to 10 unique keywords
    
    @classmethod
    def determine_development_stage(cls, prompt_text: str, current_file: str = None) -> DevelopmentStage:
        """Determine the development stage based on prompt content"""
        prompt_lower = prompt_text.lower()
        
        stage_keywords = {
            DevelopmentStage.INITIAL_SETUP: ['setup', 'install', 'create project', 'initialize', 'scaffold'],
            DevelopmentStage.BUG_FIXING: ['error', 'bug', 'fix', 'problem', 'traceback', 'exception'],
            DevelopmentStage.FEATURE_DEVELOPMENT: ['add', 'create', 'implement', 'build', 'develop'],
            DevelopmentStage.REFACTORING: ['refactor', 'clean', 'organize', 'restructure', 'optimize'],
            DevelopmentStage.TESTING: ['test', 'testing', 'validate', 'verify', 'check'],
            DevelopmentStage.DOCUMENTATION: ['document', 'readme', 'comment', 'explain', 'describe'],
            DevelopmentStage.DEPLOYMENT: ['deploy', 'production', 'server', 'hosting', 'publish']
        }
        
        for stage, keywords in stage_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return stage
        
        return DevelopmentStage.FEATURE_DEVELOPMENT

class PromptTracker:
    """Main service for tracking prompts in the background"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.files_created = []
        self.files_modified = []
        self.commands_executed = []
    
    def track_prompt(self, 
                    prompt_text: str, 
                    current_file: str = None,
                    response_summary: str = None,
                    success_rating: int = None,
                    project_phase: str = None) -> None:
        """Track a prompt asynchronously"""
        
        # Run in background thread to avoid blocking the main application
        thread = threading.Thread(target=self._save_prompt_async, 
                                args=(prompt_text, current_file, response_summary, success_rating, project_phase))
        thread.daemon = True
        thread.start()
    
    def _save_prompt_async(self, 
                          prompt_text: str,
                          current_file: str = None,
                          response_summary: str = None,
                          success_rating: int = None,
                          project_phase: str = None) -> None:
        """Save prompt to database asynchronously"""
        try:
            from flask import current_app
            
            # Get the current app context
            if current_app:
                app = current_app._get_current_object()
            else:
                # If no current app, import and create one
                from app import create_app
                app = create_app()
            
            with app.app_context():
                # Analyze the prompt
                category = PromptAnalyzer.categorize_prompt(prompt_text)
                complexity = PromptAnalyzer.assess_complexity(prompt_text)
                keywords = PromptAnalyzer.extract_keywords(prompt_text)
                dev_stage = PromptAnalyzer.determine_development_stage(prompt_text, current_file)
                
                # Get current git commit hash if possible
                git_hash = self._get_git_commit_hash()
                
                # Estimate response time based on complexity
                response_time_estimate = self._estimate_response_time(complexity)
                
                # Estimate tokens used (rough approximation)
                tokens_estimate = len(prompt_text.split()) * 1.3  # Rough token estimation
                
                # Determine if follow-up is needed
                follow_up_needed = any(word in prompt_text.lower() 
                                     for word in ['continue', 'more', 'also', 'additionally', 'next'])
                
                # Create new prompt record
                new_prompt = MyPrompts(
                    prompt_text=prompt_text,
                    session_id=self.session_id,
                    prompt_date=datetime.utcnow(),
                    prompt_category=category,
                    current_file=current_file,
                    project_phase=project_phase or "Development",
                    response_summary=response_summary,
                    files_created=json.dumps(self.files_created) if self.files_created else None,
                    files_modified=json.dumps(self.files_modified) if self.files_modified else None,
                    commands_executed=json.dumps(self.commands_executed) if self.commands_executed else None,
                    prompt_complexity=complexity,
                    success_rating=success_rating,
                    follow_up_needed=follow_up_needed,
                    prompt_technique=self._detect_prompt_technique(prompt_text),
                    git_commit_hash=git_hash,
                    development_stage=dev_stage,
                    response_time_estimate=int(response_time_estimate),
                    tokens_used_estimate=int(tokens_estimate),
                    keywords=keywords,
                    tags=self._generate_tags(prompt_text, category)
                )
                
                # Save to database
                db.session.add(new_prompt)
                db.session.commit()
                
                # Reset tracking lists
                self.files_created.clear()
                self.files_modified.clear()
                self.commands_executed.clear()
            
        except Exception as e:
            print(f"Error saving prompt: {e}")
            # Don't let prompt tracking errors crash the main application
            pass
    
    def track_file_created(self, file_path: str) -> None:
        """Track when a file is created"""
        self.files_created.append(file_path)
    
    def track_file_modified(self, file_path: str) -> None:
        """Track when a file is modified"""
        self.files_modified.append(file_path)
    
    def track_command_executed(self, command: str) -> None:
        """Track when a command is executed"""
        self.commands_executed.append(command)
    
    def _get_git_commit_hash(self) -> Optional[str]:
        """Get current git commit hash"""
        try:
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode == 0:
                return result.stdout.strip()[:40]  # Full hash
        except:
            pass
        return None
    
    def _estimate_response_time(self, complexity: PromptComplexity) -> float:
        """Estimate response time based on complexity"""
        time_estimates = {
            PromptComplexity.SIMPLE: 30,      # 30 seconds
            PromptComplexity.MODERATE: 120,   # 2 minutes
            PromptComplexity.COMPLEX: 300,    # 5 minutes
            PromptComplexity.ADVANCED: 600    # 10 minutes
        }
        return time_estimates.get(complexity, 120)
    
    def _detect_prompt_technique(self, prompt_text: str) -> str:
        """Detect the prompting technique used"""
        prompt_lower = prompt_text.lower()
        
        techniques = []
        if any(word in prompt_lower for word in ['step by step', 'explain', 'how to']):
            techniques.append("instructional")
        if any(word in prompt_lower for word in ['example', 'show me', 'demonstrate']):
            techniques.append("example-based")
        if '?' in prompt_text:
            techniques.append("question")
        if any(word in prompt_lower for word in ['create', 'build', 'make', 'implement']):
            techniques.append("task-oriented")
        if any(word in prompt_lower for word in ['fix', 'debug', 'error', 'problem']):
            techniques.append("problem-solving")
        
        return ','.join(techniques) if techniques else "direct-request"
    
    def _generate_tags(self, prompt_text: str, category: PromptCategory) -> str:
        """Generate relevant tags for the prompt"""
        tags = [category.value]
        
        # Add technology tags
        tech_tags = {
            'flask': 'flask',
            'python': 'python',
            'mysql': 'database',
            'html': 'frontend',
            'css': 'styling',
            'javascript': 'frontend',
            'api': 'api',
            'route': 'routing',
            'model': 'data-model',
            'template': 'templating'
        }
        
        prompt_lower = prompt_text.lower()
        for keyword, tag in tech_tags.items():
            if keyword in prompt_lower:
                tags.append(tag)
        
        return ','.join(list(set(tags))[:8])  # Limit to 8 unique tags

# Global instance for the application
prompt_tracker = PromptTracker()