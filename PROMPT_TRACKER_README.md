# Universal Prompt Tracker System 🤖

A comprehensive guide to implement automatic prompt tracking and conversation history in any programming language and project type.

## 🎯 Overview

This system automatically captures, categorizes, and stores user prompts/conversations without any manual intervention. It works silently in the background, providing a complete history of all interactions for future reference and analysis.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Prompt Tracker  │───▶│    Database     │
│ (Any Interface) │    │   (Middleware)   │    │   (Storage)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Auto Analysis  │
                       │ (Category/Rating)│
                       └──────────────────┘
```

## 📋 Database Schema

### Core Table Structure
```sql
CREATE TABLE prompts (
    id                      INT PRIMARY KEY AUTO_INCREMENT,
    prompt_text            TEXT NOT NULL,
    session_id             VARCHAR(255),
    prompt_date            DATETIME DEFAULT CURRENT_TIMESTAMP,
    prompt_category        ENUM('database','frontend','backend','api','ui_ux','bug_fix','feature_request','documentation','testing','deployment','general','other'),
    current_file           VARCHAR(500),
    project_phase          VARCHAR(255),
    response_summary       TEXT,
    prompt_complexity      ENUM('simple','moderate','complex','advanced'),
    success_rating         INT DEFAULT 0,
    follow_up_needed       BOOLEAN DEFAULT FALSE,
    prompt_technique       VARCHAR(255),
    development_stage      ENUM('initial_setup','feature_development','bug_fixing','refactoring','optimization','documentation','testing','deployment','maintenance'),
    response_time_estimate INT,
    tokens_used_estimate   INT,
    keywords               TEXT,
    tags                   TEXT,
    files_created          TEXT,
    files_modified         TEXT,
    commands_executed      TEXT,
    created_at             DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at             DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🚀 Implementation Guide

### 1. Python/Flask Implementation

#### Prerequisites
```bash
pip install flask sqlalchemy pymysql threading uuid datetime
```

#### Core Components

**Database Model (models.py)**
```python
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum

Base = declarative_base()

class PromptCategory(enum.Enum):
    DATABASE = "database"
    FRONTEND = "frontend"
    BACKEND = "backend"
    GENERAL = "general"
    # Add more categories as needed

class PromptTracker(Base):
    __tablename__ = 'prompts'
    
    id = Column(Integer, primary_key=True)
    prompt_text = Column(Text, nullable=False)
    session_id = Column(String(255))
    prompt_date = Column(DateTime, default=datetime.utcnow)
    prompt_category = Column(Enum(PromptCategory))
    # Add all other fields from schema above
```

**Auto-Tracker Service (tracker.py)**
```python
import threading
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class AutoPromptTracker:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.is_running = False
    
    def track_prompt(self, prompt_text, context=None):
        """Automatically track a prompt"""
        if not prompt_text or len(prompt_text.strip()) < 5:
            return None
            
        session = self.Session()
        try:
            # Check for duplicates
            existing = session.query(PromptTracker).filter_by(
                prompt_text=prompt_text
            ).first()
            
            if existing:
                return existing.id
            
            # Auto-categorize and analyze
            category = self._categorize_prompt(prompt_text)
            complexity = self._assess_complexity(prompt_text)
            
            # Create new record
            new_prompt = PromptTracker(
                prompt_text=prompt_text,
                session_id=context.get('session_id', f'auto_{int(time.time())}'),
                prompt_category=category,
                prompt_complexity=complexity,
                current_file=context.get('file', 'auto_capture'),
                project_phase=context.get('phase', 'Development'),
                response_summary='Auto-captured prompt',
                success_rating=8,
                keywords=self._extract_keywords(prompt_text),
                tags=f'auto,{category.value}'
            )
            
            session.add(new_prompt)
            session.commit()
            return new_prompt.id
            
        except Exception as e:
            session.rollback()
            print(f"Tracking error: {e}")
            return None
        finally:
            session.close()
    
    def _categorize_prompt(self, text):
        """Auto-categorize based on keywords"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['database', 'sql', 'table']):
            return PromptCategory.DATABASE
        elif any(word in text_lower for word in ['frontend', 'ui', 'interface']):
            return PromptCategory.FRONTEND
        elif any(word in text_lower for word in ['backend', 'api', 'server']):
            return PromptCategory.BACKEND
        else:
            return PromptCategory.GENERAL
    
    def _assess_complexity(self, text):
        """Assess prompt complexity"""
        word_count = len(text.split())
        if word_count < 10:
            return 'simple'
        elif word_count < 25:
            return 'moderate'
        else:
            return 'complex'
    
    def _extract_keywords(self, text):
        """Extract relevant keywords"""
        # Simple keyword extraction
        words = text.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'}
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        return ','.join(keywords[:5])

# Global tracker instance
tracker = AutoPromptTracker('mysql://user:pass@localhost/dbname')

def track_prompt(prompt_text, **context):
    """Simple function to track any prompt"""
    return tracker.track_prompt(prompt_text, context)
```

**Middleware Integration (middleware.py)**
```python
from flask import request, g
import time

class PromptMiddleware:
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        g.start_time = time.time()
        
        # Check for prompt-like data
        if self._contains_prompt_data():
            self._capture_prompt()
    
    def _contains_prompt_data(self):
        """Detect if request contains prompt data"""
        if request.form:
            return any('prompt' in key.lower() or 'query' in key.lower() 
                      for key in request.form.keys())
        if request.json:
            return any('prompt' in key.lower() or 'query' in key.lower() 
                      for key in request.json.keys())
        return False
    
    def _capture_prompt(self):
        """Capture prompt from request"""
        prompt_text = ""
        
        if request.form:
            for key, value in request.form.items():
                if 'prompt' in key.lower() or 'query' in key.lower():
                    prompt_text = value
                    break
        
        if request.json:
            for key, value in request.json.items():
                if 'prompt' in key.lower() or 'query' in key.lower():
                    prompt_text = value
                    break
        
        if prompt_text:
            from tracker import track_prompt
            track_prompt(prompt_text, 
                        session_id=request.headers.get('User-Agent', ''),
                        file=request.endpoint,
                        phase='Web Interface')
```

### 2. Node.js/Express Implementation

#### Prerequisites
```bash
npm install express mysql2 sequelize uuid
```

#### Core Implementation
```javascript
// models/Prompt.js
const { DataTypes } = require('sequelize');

const PromptModel = (sequelize) => {
    return sequelize.define('Prompt', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true
        },
        promptText: {
            type: DataTypes.TEXT,
            allowNull: false
        },
        sessionId: {
            type: DataTypes.STRING(255)
        },
        promptCategory: {
            type: DataTypes.ENUM('database', 'frontend', 'backend', 'general', 'other')
        },
        promptComplexity: {
            type: DataTypes.ENUM('simple', 'moderate', 'complex', 'advanced')
        },
        currentFile: {
            type: DataTypes.STRING(500)
        },
        keywords: {
            type: DataTypes.TEXT
        },
        tags: {
            type: DataTypes.TEXT
        }
    });
};

module.exports = PromptModel;

// services/PromptTracker.js
class PromptTracker {
    constructor(database) {
        this.db = database;
    }
    
    async trackPrompt(promptText, context = {}) {
        if (!promptText || promptText.trim().length < 5) {
            return null;
        }
        
        try {
            // Check for duplicates
            const existing = await this.db.Prompt.findOne({
                where: { promptText }
            });
            
            if (existing) {
                return existing.id;
            }
            
            // Auto-analyze
            const category = this.categorizePrompt(promptText);
            const complexity = this.assessComplexity(promptText);
            
            // Create record
            const prompt = await this.db.Prompt.create({
                promptText,
                sessionId: context.sessionId || `auto_${Date.now()}`,
                promptCategory: category,
                promptComplexity: complexity,
                currentFile: context.file || 'auto_capture',
                keywords: this.extractKeywords(promptText),
                tags: `auto,${category}`
            });
            
            return prompt.id;
            
        } catch (error) {
            console.error('Prompt tracking error:', error);
            return null;
        }
    }
    
    categorizePrompt(text) {
        const textLower = text.toLowerCase();
        
        if (textLower.includes('database') || textLower.includes('sql')) {
            return 'database';
        } else if (textLower.includes('frontend') || textLower.includes('ui')) {
            return 'frontend';
        } else if (textLower.includes('backend') || textLower.includes('api')) {
            return 'backend';
        }
        return 'general';
    }
    
    assessComplexity(text) {
        const wordCount = text.split(' ').length;
        
        if (wordCount < 10) return 'simple';
        if (wordCount < 25) return 'moderate';
        return 'complex';
    }
    
    extractKeywords(text) {
        const words = text.toLowerCase().split(/\W+/);
        const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but']);
        const keywords = words
            .filter(word => word.length > 3 && !stopWords.has(word))
            .slice(0, 5);
        return keywords.join(',');
    }
}

module.exports = PromptTracker;

// middleware/promptMiddleware.js
const promptMiddleware = (tracker) => {
    return (req, res, next) => {
        // Check for prompt data
        const promptText = req.body.prompt || req.body.query || req.query.prompt;
        
        if (promptText) {
            // Track asynchronously
            tracker.trackPrompt(promptText, {
                sessionId: req.sessionID,
                file: req.route?.path || req.path,
                userAgent: req.get('User-Agent')
            }).catch(console.error);
        }
        
        next();
    };
};

module.exports = promptMiddleware;
```

### 3. PHP/Laravel Implementation

#### Core Implementation
```php
<?php
// Models/Prompt.php
use Illuminate\Database\Eloquent\Model;

class Prompt extends Model
{
    protected $fillable = [
        'prompt_text', 'session_id', 'prompt_category', 
        'prompt_complexity', 'current_file', 'keywords', 'tags'
    ];
    
    protected $casts = [
        'prompt_date' => 'datetime',
    ];
}

// Services/PromptTracker.php
class PromptTracker
{
    public function trackPrompt($promptText, $context = [])
    {
        if (empty(trim($promptText)) || strlen($promptText) < 5) {
            return null;
        }
        
        // Check for duplicates
        $existing = Prompt::where('prompt_text', $promptText)->first();
        if ($existing) {
            return $existing->id;
        }
        
        // Auto-analyze
        $category = $this->categorizePrompt($promptText);
        $complexity = $this->assessComplexity($promptText);
        
        // Create record
        $prompt = Prompt::create([
            'prompt_text' => $promptText,
            'session_id' => $context['session_id'] ?? 'auto_' . time(),
            'prompt_category' => $category,
            'prompt_complexity' => $complexity,
            'current_file' => $context['file'] ?? 'auto_capture',
            'keywords' => $this->extractKeywords($promptText),
            'tags' => "auto,{$category}"
        ]);
        
        return $prompt->id;
    }
    
    private function categorizePrompt($text)
    {
        $textLower = strtolower($text);
        
        if (strpos($textLower, 'database') !== false || strpos($textLower, 'sql') !== false) {
            return 'database';
        } elseif (strpos($textLower, 'frontend') !== false || strpos($textLower, 'ui') !== false) {
            return 'frontend';
        } elseif (strpos($textLower, 'backend') !== false || strpos($textLower, 'api') !== false) {
            return 'backend';
        }
        
        return 'general';
    }
    
    private function assessComplexity($text)
    {
        $wordCount = str_word_count($text);
        
        if ($wordCount < 10) return 'simple';
        if ($wordCount < 25) return 'moderate';
        return 'complex';
    }
    
    private function extractKeywords($text)
    {
        $words = preg_split('/\W+/', strtolower($text));
        $stopWords = ['the', 'a', 'an', 'and', 'or', 'but'];
        $keywords = array_filter($words, function($word) use ($stopWords) {
            return strlen($word) > 3 && !in_array($word, $stopWords);
        });
        
        return implode(',', array_slice($keywords, 0, 5));
    }
}

// Middleware/PromptTrackingMiddleware.php
class PromptTrackingMiddleware
{
    public function handle($request, Closure $next)
    {
        $promptText = $request->input('prompt') ?? $request->input('query');
        
        if ($promptText) {
            $tracker = app(PromptTracker::class);
            $tracker->trackPrompt($promptText, [
                'session_id' => session()->getId(),
                'file' => $request->route()->getName(),
            ]);
        }
        
        return $next($request);
    }
}
```

### 4. Java/Spring Boot Implementation

#### Core Implementation
```java
// Entity/Prompt.java
@Entity
@Table(name = "prompts")
public class Prompt {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(columnDefinition = "TEXT")
    private String promptText;
    
    private String sessionId;
    
    @Enumerated(EnumType.STRING)
    private PromptCategory promptCategory;
    
    @Enumerated(EnumType.STRING)
    private PromptComplexity promptComplexity;
    
    private String currentFile;
    private String keywords;
    private String tags;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    // Getters and setters...
}

// Service/PromptTracker.java
@Service
public class PromptTracker {
    
    @Autowired
    private PromptRepository promptRepository;
    
    public Long trackPrompt(String promptText, Map<String, Object> context) {
        if (promptText == null || promptText.trim().length() < 5) {
            return null;
        }
        
        // Check for duplicates
        Optional<Prompt> existing = promptRepository.findByPromptText(promptText);
        if (existing.isPresent()) {
            return existing.get().getId();
        }
        
        // Auto-analyze
        PromptCategory category = categorizePrompt(promptText);
        PromptComplexity complexity = assessComplexity(promptText);
        
        // Create record
        Prompt prompt = new Prompt();
        prompt.setPromptText(promptText);
        prompt.setSessionId((String) context.getOrDefault("sessionId", "auto_" + System.currentTimeMillis()));
        prompt.setPromptCategory(category);
        prompt.setPromptComplexity(complexity);
        prompt.setCurrentFile((String) context.getOrDefault("file", "auto_capture"));
        prompt.setKeywords(extractKeywords(promptText));
        prompt.setTags("auto," + category.name().toLowerCase());
        
        Prompt saved = promptRepository.save(prompt);
        return saved.getId();
    }
    
    private PromptCategory categorizePrompt(String text) {
        String textLower = text.toLowerCase();
        
        if (textLower.contains("database") || textLower.contains("sql")) {
            return PromptCategory.DATABASE;
        } else if (textLower.contains("frontend") || textLower.contains("ui")) {
            return PromptCategory.FRONTEND;
        } else if (textLower.contains("backend") || textLower.contains("api")) {
            return PromptCategory.BACKEND;
        }
        
        return PromptCategory.GENERAL;
    }
    
    private PromptComplexity assessComplexity(String text) {
        int wordCount = text.split("\\s+").length;
        
        if (wordCount < 10) return PromptComplexity.SIMPLE;
        if (wordCount < 25) return PromptComplexity.MODERATE;
        return PromptComplexity.COMPLEX;
    }
    
    private String extractKeywords(String text) {
        String[] words = text.toLowerCase().split("\\W+");
        Set<String> stopWords = Set.of("the", "a", "an", "and", "or", "but");
        
        return Arrays.stream(words)
            .filter(word -> word.length() > 3 && !stopWords.contains(word))
            .limit(5)
            .collect(Collectors.joining(","));
    }
}

// Interceptor/PromptTrackingInterceptor.java
@Component
public class PromptTrackingInterceptor implements HandlerInterceptor {
    
    @Autowired
    private PromptTracker promptTracker;
    
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String promptText = request.getParameter("prompt");
        if (promptText == null) {
            promptText = request.getParameter("query");
        }
        
        if (promptText != null) {
            Map<String, Object> context = new HashMap<>();
            context.put("sessionId", request.getSession().getId());
            context.put("file", request.getRequestURI());
            
            promptTracker.trackPrompt(promptText, context);
        }
        
        return true;
    }
}
```

## 🔧 Configuration Files

### Environment Variables (.env)
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_project_db
DB_USER=your_username
DB_PASS=your_password

# Prompt Tracking Configuration
PROMPT_TRACKING_ENABLED=true
PROMPT_TRACKING_DEBUG=false
PROMPT_MIN_LENGTH=5
PROMPT_AUTO_CATEGORIZE=true
PROMPT_DUPLICATE_CHECK=true

# Categories (comma-separated)
PROMPT_CATEGORIES=database,frontend,backend,api,ui_ux,bug_fix,general,other

# Complexity Levels
PROMPT_COMPLEXITY_LEVELS=simple,moderate,complex,advanced
```

## 📱 Usage Examples

### Simple Tracking
```python
# Python
from tracker import track_prompt
track_prompt("How do I implement user authentication?")

# JavaScript
const tracker = require('./services/PromptTracker');
tracker.trackPrompt("How do I implement user authentication?");

# PHP
$tracker = app(PromptTracker::class);
$tracker->trackPrompt("How do I implement user authentication?");

# Java
@Autowired
private PromptTracker tracker;
tracker.trackPrompt("How do I implement user authentication?", context);
```

### Advanced Tracking with Context
```python
track_prompt(
    "Create a REST API for user management",
    session_id="user123",
    file="api_controller.py",
    phase="Backend Development",
    category="backend"
)
```

### Middleware Auto-Tracking
Once middleware is configured, prompts are tracked automatically from:
- Form submissions with 'prompt' or 'query' fields
- JSON requests with prompt data
- URL parameters containing prompts

## 📊 Analytics & Reporting

### Basic Queries
```sql
-- Most common prompt categories
SELECT prompt_category, COUNT(*) as count 
FROM prompts 
GROUP BY prompt_category 
ORDER BY count DESC;

-- Complexity distribution
SELECT prompt_complexity, COUNT(*) as count 
FROM prompts 
GROUP BY prompt_complexity;

-- Daily prompt volume
SELECT DATE(created_at) as date, COUNT(*) as prompts 
FROM prompts 
GROUP BY DATE(created_at) 
ORDER BY date DESC;

-- Top keywords
SELECT keywords, COUNT(*) as frequency 
FROM prompts 
WHERE keywords IS NOT NULL 
GROUP BY keywords 
ORDER BY frequency DESC 
LIMIT 20;
```

### Dashboard Endpoints
```python
# Example API endpoints for analytics
@app.route('/api/prompts/stats')
def prompt_stats():
    return {
        'total_prompts': get_total_prompts(),
        'categories': get_category_distribution(),
        'complexity': get_complexity_distribution(),
        'daily_volume': get_daily_volume()
    }

@app.route('/api/prompts/search')
def search_prompts():
    query = request.args.get('q')
    category = request.args.get('category')
    return search_prompts_by_criteria(query, category)
```

## 🔐 Security Considerations

### Data Protection
```python
# Encrypt sensitive prompts
from cryptography.fernet import Fernet

def encrypt_prompt(prompt_text, key):
    f = Fernet(key)
    return f.encrypt(prompt_text.encode()).decode()

def decrypt_prompt(encrypted_prompt, key):
    f = Fernet(key)
    return f.decrypt(encrypted_prompt.encode()).decode()
```

### Access Control
```python
# Role-based access to prompt history
@require_permission('view_prompts')
def view_prompts():
    # Only authorized users can view prompts
    pass

@require_permission('admin')
def delete_prompts():
    # Only admins can delete prompts
    pass
```

## 🚀 Deployment

### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_NAME=prompts_db
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: prompts_db
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 🔄 Migration Scripts

### Database Migration
```sql
-- migration_001_create_prompts_table.sql
CREATE TABLE prompts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    prompt_text TEXT NOT NULL,
    session_id VARCHAR(255),
    prompt_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    prompt_category ENUM('database','frontend','backend','general','other'),
    current_file VARCHAR(500),
    project_phase VARCHAR(255),
    response_summary TEXT,
    prompt_complexity ENUM('simple','moderate','complex','advanced'),
    success_rating INT DEFAULT 0,
    follow_up_needed BOOLEAN DEFAULT FALSE,
    prompt_technique VARCHAR(255),
    development_stage ENUM('initial_setup','feature_development','bug_fixing','refactoring','optimization','documentation','testing','deployment','maintenance'),
    response_time_estimate INT,
    tokens_used_estimate INT,
    keywords TEXT,
    tags TEXT,
    files_created TEXT,
    files_modified TEXT,
    commands_executed TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_prompts_category ON prompts(prompt_category);
CREATE INDEX idx_prompts_complexity ON prompts(prompt_complexity);
CREATE INDEX idx_prompts_date ON prompts(created_at);
CREATE INDEX idx_prompts_session ON prompts(session_id);
```

## 🧪 Testing

### Unit Tests
```python
# test_prompt_tracker.py
import unittest
from tracker import PromptTracker

class TestPromptTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = PromptTracker('sqlite:///:memory:')
    
    def test_track_simple_prompt(self):
        result = self.tracker.track_prompt("Hello world")
        self.assertIsNotNone(result)
    
    def test_categorization(self):
        category = self.tracker._categorize_prompt("Create a database table")
        self.assertEqual(category, PromptCategory.DATABASE)
    
    def test_complexity_assessment(self):
        simple_prompt = "Hi"
        complex_prompt = "Create a comprehensive REST API with authentication, authorization, caching, and monitoring capabilities"
        
        self.assertEqual(self.tracker._assess_complexity(simple_prompt), 'simple')
        self.assertEqual(self.tracker._assess_complexity(complex_prompt), 'complex')

if __name__ == '__main__':
    unittest.main()
```

## 📚 Integration Examples

### Frontend Integration
```javascript
// Auto-track user inputs
document.addEventListener('DOMContentLoaded', function() {
    // Track form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const promptField = form.querySelector('[name*="prompt"], [name*="query"]');
            if (promptField && promptField.value) {
                // Send to tracking endpoint
                fetch('/api/track-prompt', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        prompt: promptField.value,
                        context: {
                            page: window.location.pathname,
                            timestamp: new Date().toISOString()
                        }
                    })
                });
            }
        });
    });
});
```

### CLI Tool Integration
```python
# cli_tracker.py
import argparse
from tracker import track_prompt

def main():
    parser = argparse.ArgumentParser(description='Track CLI prompts')
    parser.add_argument('prompt', help='The prompt to track')
    parser.add_argument('--category', help='Prompt category')
    parser.add_argument('--file', help='Current file context')
    
    args = parser.parse_args()
    
    result = track_prompt(
        args.prompt,
        category=args.category,
        file=args.file,
        session_id='cli_session'
    )
    
    print(f"Prompt tracked with ID: {result}")

if __name__ == '__main__':
    main()
```

## 🎯 Best Practices

### 1. **Automatic Detection**
- Use middleware/interceptors for transparent tracking
- Monitor form submissions, API calls, and user interactions
- Implement background services for continuous monitoring

### 2. **Data Quality**
- Validate prompt text before storing
- Implement deduplication logic
- Clean and normalize input data

### 3. **Performance**
- Use asynchronous processing for tracking
- Implement database indexing
- Consider using message queues for high-volume scenarios

### 4. **Privacy & Security**
- Encrypt sensitive prompts
- Implement data retention policies
- Provide opt-out mechanisms

### 5. **Monitoring & Alerts**
- Set up logging for tracking failures
- Monitor database performance
- Implement health checks

## 📈 Advanced Features

### 1. **AI-Powered Analysis**
```python
# Integrate with AI services for better categorization
import openai

def ai_categorize_prompt(prompt_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Categorize this programming prompt: '{prompt_text}'\nCategories: database, frontend, backend, general\nCategory:",
        max_tokens=10
    )
    return response.choices[0].text.strip().lower()
```

### 2. **Real-time Dashboards**
```javascript
// WebSocket integration for real-time updates
const socket = io();
socket.on('new_prompt', (data) => {
    updateDashboard(data);
});
```

### 3. **Export & Backup**
```python
# Export prompts to various formats
import csv
import json

def export_prompts_csv(filename):
    prompts = get_all_prompts()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'prompt_text', 'category', 'created_at'])
        writer.writeheader()
        for prompt in prompts:
            writer.writerow(prompt.to_dict())

def export_prompts_json(filename):
    prompts = get_all_prompts()
    with open(filename, 'w') as jsonfile:
        json.dump([p.to_dict() for p in prompts], jsonfile, indent=2)
```

## 🚀 Quick Start

1. **Choose your technology stack** from the implementations above
2. **Set up the database** using the provided schema
3. **Implement the core tracker service** for your language
4. **Add middleware/interceptors** for automatic capture
5. **Configure environment variables** for your project
6. **Test the tracking** with sample prompts
7. **Deploy and monitor** the system

## 📋 Checklist

- [ ] Database schema created
- [ ] Core tracker service implemented
- [ ] Middleware/interceptors configured
- [ ] Environment variables set
- [ ] Auto-categorization logic added
- [ ] Duplicate detection enabled
- [ ] Basic analytics endpoints created
- [ ] Security measures implemented
- [ ] Testing framework set up
- [ ] Documentation updated
- [ ] Monitoring and logging configured

## 🔗 Additional Resources

- **Performance Optimization**: Use database indexes, connection pooling, caching
- **Scaling**: Consider sharding, read replicas, message queues
- **Monitoring**: Implement metrics, alerts, health checks
- **Compliance**: Ensure GDPR/privacy compliance for user data

---

**📞 Support**: If you need help implementing this system in your specific technology stack, refer to the examples above or create an issue in your project repository.

**🎯 Goal**: Achieve 100% automatic prompt tracking with zero manual intervention across all your projects!