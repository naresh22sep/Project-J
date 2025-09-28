"""
Optional Prompt Tracking Configuration Settings

Add these to your config.py if you want to customize the prompt tracking behavior
"""

# Add to your Config class:

class Config:
    # ... existing configuration ...
    
    # ===== PROMPT TRACKING CONFIGURATION =====
    
    # Enable/disable prompt tracking globally
    PROMPT_TRACKING_ENABLED = True
    
    # Maximum length of prompt text to store (prevents huge prompts from breaking DB)
    PROMPT_MAX_LENGTH = 10000
    
    # Background thread timeout (seconds)
    PROMPT_SAVE_TIMEOUT = 30
    
    # Automatic cleanup - delete prompts older than X days (0 = never delete)
    PROMPT_RETENTION_DAYS = 365
    
    # Rate limiting - max prompts per session per hour
    PROMPT_RATE_LIMIT_PER_HOUR = 100
    
    # Categories to ignore (don't track these types)
    PROMPT_IGNORE_CATEGORIES = []  # e.g., ['GENERAL', 'OTHER']
    
    # Enable detailed logging of prompt tracking operations
    PROMPT_TRACKING_DEBUG = False
    
    # Store git commit hash with each prompt
    PROMPT_TRACK_GIT_COMMITS = True
    
    # Store file operation history
    PROMPT_TRACK_FILE_OPERATIONS = True
    
    # Store command execution history  
    PROMPT_TRACK_COMMANDS = True
    
    # Minimum complexity level to track (ignore simple prompts)
    PROMPT_MIN_COMPLEXITY = None  # Options: 'simple', 'moderate', 'complex', 'advanced'
    
    # Database table name (if you want to change it)
    PROMPT_TABLE_NAME = 'myprompts'
    
    # Export settings
    PROMPT_EXPORT_MAX_RECORDS = 10000
    PROMPT_EXPORT_FORMATS = ['json', 'csv']  # Future: could add 'xml', 'xlsx'
    
    # AI Analysis settings (future enhancement)
    PROMPT_AI_ANALYSIS_ENABLED = False
    PROMPT_SENTIMENT_ANALYSIS = False
    PROMPT_AUTO_TAGGING = True
    
    # Privacy settings
    PROMPT_ANONYMIZE_DATA = False  # Remove potentially sensitive info
    PROMPT_ENCRYPT_CONTENT = False  # Encrypt prompt text in database