# Flask Modular Application

A modern, modular Flask web application with MySQL database, featuring user authentication, user management, and dashboard functionality. Built with scalability and maintainability in mind.

## Features

- **Modular Architecture**: Clean separation of concerns with dedic2. **Database Connection Error**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database `jobhunter_fresh` exists modules
- **User Authentication**: Complete auth system with registration, login, logout
- **User Management**: User profile management and search functionality  
- **Dashboard**: Statistics and system monitoring
- **Database Migrations**: Full migration support with Flask-Migrate
- **Docker Support**: Complete containerization with docker-compose
- **MySQL Integration**: Robust database connectivity with SQLAlchemy
- **Security**: Password hashing, session management, input validation
- **REST API**: JSON-based API endpoints
- **Environment Configuration**: Separate configs for dev/prod/test

## Project Structure

```
ProjectJ/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   └── modules/                 # Feature modules
│       ├── auth/                # Authentication module
│       │   ├── __init__.py
│       │   ├── routes.py        # Auth endpoints
│       │   └── utils.py         # Auth utilities
│       ├── users/               # User management module
│       │   ├── __init__.py
│       │   └── routes.py        # User endpoints
│       └── dashboard/           # Dashboard module
│           ├── __init__.py
│           └── routes.py        # Dashboard endpoints
├── config/                      # Configuration files
│   ├── config.py               # Environment configurations
│   └── .env.example            # Environment variables template
├── migrations/                  # Database migrations (auto-generated)
├── mysql-init/                  # MySQL initialization scripts
│   └── init.sql                # Database setup script
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── setup.sh                    # Unix setup script
├── setup.bat                   # Windows setup script
├── migrate.sh                  # Unix migration script
├── migrate.bat                 # Windows migration script
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker services orchestration
└── README.md                   # This file
```

## Quick Start

### Option 1: Local Development with Virtual Environment

1. **Clone and setup:**
   ```bash
   cd ProjectJ
   
   # For Windows:
   setup.bat
   
   # For Unix/Linux/Mac:
   ./setup.sh
   ```

2. **Configure environment:**
   ```bash
   # Edit .env file with your database credentials
   cp config/.env.example .env
   # Update DATABASE_URL with your MySQL credentials
   ```

3. **Setup database:**
   ```bash
   # Create MySQL database
   mysql -u root -p -e "CREATE DATABASE jobhunter_fresh;"
   
   # Initialize migrations
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Run the application:**
   ```bash
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   
   # Unix/Linux/Mac:
   source venv/bin/activate
   
   # Start the application
   python app.py
   ```

### Option 2: Docker Development

1. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access services:**
   - Flask App: http://localhost:5051
   - phpMyAdmin: http://localhost:8080
   - MySQL: localhost:3306

## API Endpoints

### Health Check
- `GET /health` - Application health check
- `GET /` - Welcome message

### Authentication (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login  
- `POST /auth/logout` - User logout
- `GET /auth/verify` - Verify session

### Users (`/users`)
- `GET /users/profile` - Get current user profile
- `PUT /users/profile` - Update user profile
- `POST /users/change-password` - Change password
- `GET /users/list` - List all users (paginated)
- `GET /users/<id>` - Get specific user
- `GET /users/search` - Search users

### Dashboard (`/dashboard`)
- `GET /dashboard/stats` - Dashboard statistics
- `GET /dashboard/recent-users` - Recently registered users
- `GET /dashboard/active-sessions` - Active user sessions
- `GET /dashboard/system-info` - System information

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username  
- `email` - Unique email address
- `password_hash` - Encrypted password
- `first_name` - User's first name
- `last_name` - User's last name
- `is_active` - Account status
- `created_at` - Registration timestamp
- `updated_at` - Last update timestamp

### User Sessions Table  
- `id` - Primary key
- `user_id` - Foreign key to users
- `session_token` - Unique session identifier
- `expires_at` - Session expiration
- `created_at` - Session creation time

## Database Migrations

### Initialize Migrations (First Time Only)
```bash
# Windows
migrate.bat init

# Unix/Linux/Mac  
./migrate.sh init
```

### Create New Migration
```bash
# Windows
migrate.bat migrate "Description of changes"

# Unix/Linux/Mac
./migrate.sh migrate "Description of changes"
```

### Apply Migrations
```bash
# Windows
migrate.bat upgrade

# Unix/Linux/Mac
./migrate.sh upgrade
```

### Migration Commands
- `init` - Initialize migration repository
- `migrate` - Create new migration 
- `upgrade` - Apply migrations to database
- `downgrade` - Roll back migrations
- `history` - Show migration history
- `current` - Show current migration
- `reset` - Reset database (drop and recreate)

## Configuration

### Environment Variables (.env)
```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# Database Configuration  
DEV_DATABASE_URL=mysql+pymysql://root:Naresh123@localhost:3306/jobhunter_fresh
DATABASE_URL=mysql+pymysql://root:Naresh123@localhost:3306/jobhunter_fresh
TEST_DATABASE_URL=mysql+pymysql://root:Naresh123@localhost:3306/jobhunter_fresh

# MySQL Configuration (for Docker)
MYSQL_ROOT_PASSWORD=Naresh123
MYSQL_DATABASE=jobhunter_fresh
MYSQL_USER=root
MYSQL_PASSWORD=Naresh123
```

### Configuration Classes
- `DevelopmentConfig` - Development settings
- `ProductionConfig` - Production settings  
- `TestingConfig` - Testing settings

## Docker Deployment

### Services Included
- **Flask Application** - Main web service (Port 5051)
- **MySQL Database** - Data persistence (Port 3306)
- **phpMyAdmin** - Database management UI (Port 8080)

### Docker Commands
```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services  
docker-compose down

# View logs
docker-compose logs -f web
docker-compose logs -f mysql

# Rebuild specific service
docker-compose build web
docker-compose up web
```

## Development

### Adding New Modules
1. Create module directory in `app/modules/`
2. Add `__init__.py` and `routes.py`
3. Create Blueprint in `routes.py`
4. Register Blueprint in `app/__init__.py`

### Example Module Structure
```python
# app/modules/newmodule/routes.py
from flask import Blueprint

newmodule_bp = Blueprint('newmodule', __name__)

@newmodule_bp.route('/endpoint')
def endpoint():
    return {'message': 'New module endpoint'}
```

```python
# app/__init__.py (add to create_app function)
from app.modules.newmodule.routes import newmodule_bp
app.register_blueprint(newmodule_bp, url_prefix='/newmodule')
```

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- SQL injection prevention with SQLAlchemy ORM  
- Input validation and sanitization
- CORS protection
- Environment-based configuration
- Secure session tokens

## Testing

### Manual API Testing
```bash
# Register a new user
curl -X POST http://localhost:5051/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# Login  
curl -X POST http://localhost:5051/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Get dashboard stats
curl -X GET http://localhost:5051/dashboard/stats \
  -H "Cookie: session=<session_cookie>"
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database exists

2. **Migration Errors**
   - Run `flask db init` if migrations folder is missing
   - Check database permissions
   - Verify Flask-Migrate is installed

3. **Import Errors**  
   - Ensure virtual environment is activated
   - Install requirements: `pip install -r requirements.txt`
   - Check Python path

4. **Docker Issues**
   - Ensure Docker and Docker Compose are installed
   - Check port availability (5051, 3306, 8080)
   - Review docker-compose logs

### Logs and Debugging
```bash
# Application logs (if running in Docker)
docker-compose logs -f web

# Database logs  
docker-compose logs -f mysql

# Enable Flask debug mode
export FLASK_ENV=development
```

## Production Deployment

### Environment Setup
1. Set `FLASK_ENV=production`
2. Use strong `SECRET_KEY`
3. Configure production database
4. Use reverse proxy (nginx)
5. Set up SSL/HTTPS
6. Configure monitoring

### Example Production Deployment
```bash
# Using gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:5051 --workers 4 app:app

# With Docker
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable  
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Create an issue in the repository

---

**Application URL:** http://localhost:5051  
**Database Management:** http://localhost:8080 (phpMyAdmin)  
**Port:** 5051 (configurable via PORT environment variable)