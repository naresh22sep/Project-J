# JobMilgaya Application

A modern, role-based Flask web application designed for job hunting and recruitment management. Features a public-facing frontend website, comprehensive role-based authentication system, and dynamic permission management. Built with scalability, security, and maintainability in mind.

## Features

- **Public Frontend Website**: Product information accessible without forced login redirects
- **Role-Based Authentication**: Comprehensive system supporting 4 user roles with dynamic permissions
- **Modular Architecture**: Clean separation of concerns with role-specific route files
- **Dynamic Permission System**: Database-driven permissions with 81 permissions across 17 resources
- **Responsive UI**: Bootstrap 5 with role-based theming and dynamic menus
- **Dual User System**: Separate authentication for admin/superadmin vs jobseeker/consultancy users
- **Security**: JWT for admin authentication, session-based for regular users
- **Database Management**: Full migration support with Flask-Migrate
- **Docker Support**: Complete containerization with docker-compose
- **MySQL Integration**: Robust database connectivity with SQLAlchemy

## User Roles & Access Control

### 1. **Public Access**
- **Homepage**: Product information, features, pricing
- **Login Options**: Role-based login dropdown (Admin, Jobseeker, Consultancy)
- **No Forced Redirects**: Users can browse product information without authentication

### 2. **Jobseeker** (users table)
- **Authentication**: Session-based login
- **Dashboard**: Job search, application tracking, profile management
- **Theme**: Blue color scheme with jobseeker-specific navigation
- **Access**: Playground layout with jobseeker menu options

### 3. **Consultancy** (users table)  
- **Authentication**: Session-based login
- **Dashboard**: Job posting, candidate management, company profile
- **Theme**: Purple color scheme with consultancy-specific navigation
- **Access**: Playground layout with consultancy menu options

### 4. **Admin/SuperAdmin** (auth_users table)
- **Authentication**: JWT-based secure authentication
- **Dashboard**: Dynamic menu based on database permissions
- **Permissions**: 81 granular permissions across 17 resources
- **Access**: Full system administration capabilities

## Database Structure

### User Tables
```sql
-- Admin and SuperAdmin users
auth_users (
    id, username, email, password_hash, role, 
    first_name, last_name, is_active, 
    created_at, updated_at
)

-- Jobseeker and Consultancy users  
users (
    id, username, email, password_hash, role,
    first_name, last_name, is_active,
    created_at, updated_at
)
```

### Permission System
```sql
-- 17 Resources with CRUD operations
resources (id, name, description)
permissions (id, resource_id, action, description)
role_permissions (role_id, permission_id)

-- Examples:
- users_view, users_create, users_edit, users_delete
- jobs_view, jobs_create, jobs_edit, jobs_delete  
- applications_view, applications_create, etc.
```

## Project Structure

```
ProjectJ/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── templates/               # Template files
│   │   ├── public/              # Public website templates
│   │   │   ├── base.html        # Public layout
│   │   │   └── homepage.html    # Public homepage
│   │   ├── layouts/             # Shared layouts
│   │   │   └── playground_layout.html  # Jobseeker/Consultancy layout
│   │   └── admin/               # Admin templates
│   │       └── dashboard.html   # Admin dashboard
│   └── routes/                  # Route modules
│       ├── public_routes.py     # Public website routes
│       ├── auth_routes.py       # Authentication routes
│       └── roles/               # Role-specific routes
│           ├── admin_routes.py      # Admin/SuperAdmin routes
│           ├── jobseeker_routes.py  # Jobseeker routes
│           └── consultancy_routes.py # Consultancy routes
├── sql-scripts/                 # SQL initialization scripts
│   └── init.sql                # Database setup script
├── tests/                       # Test files
├── config/                      # Configuration files
│   ├── config.py               # Environment configurations
│   └── .env.example            # Environment variables template
├── migrations/                  # Database migrations (auto-generated)
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
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
   
   # Run initialization script
   mysql -u root -p jobhunter_fresh < sql-scripts/init.sql
   
   # Initialize Flask migrations
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

### Public Routes
- `GET /` - Public homepage with product information
- `GET /about` - About page
- `GET /contact` - Contact information
- `GET /pricing` - Pricing information

### Authentication Routes
- `POST /login` - Universal login endpoint (role detection)
- `GET /login/admin` - Admin login page
- `GET /login/jobseeker` - Jobseeker login page  
- `GET /login/consultancy` - Consultancy login page
- `POST /logout` - Logout (all roles)
- `POST /register` - User registration

### Admin Routes (`/admin`) - JWT Protected
- `GET /admin/dashboard` - Admin dashboard with dynamic menu
- `GET /admin/users` - User management (based on permissions)
- `GET /admin/permissions` - Permission management
- `GET /admin/reports` - System reports
- `POST /admin/api/*` - Admin API endpoints

### Jobseeker Routes (`/jobseeker`) - Session Protected
- `GET /jobseeker/dashboard` - Jobseeker dashboard
- `GET /jobseeker/profile` - Profile management
- `GET /jobseeker/jobs` - Job search and listings
- `GET /jobseeker/applications` - Application tracking
- `POST /jobseeker/apply` - Job application submission

### Consultancy Routes (`/consultancy`) - Session Protected  
- `GET /consultancy/dashboard` - Consultancy dashboard
- `GET /consultancy/profile` - Company profile management
- `GET /consultancy/jobs` - Job posting management
- `GET /consultancy/candidates` - Candidate management
- `POST /consultancy/post-job` - Job posting creation

## Database Schema

### Authentication Tables

#### auth_users (Admin/SuperAdmin)
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address  
- `password_hash` - Encrypted password
- `role` - 'admin' or 'superadmin'
- `first_name` - User's first name
- `last_name` - User's last name
- `is_active` - Account status
- `created_at` - Registration timestamp
- `updated_at` - Last update timestamp

#### users (Jobseeker/Consultancy)
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Encrypted password  
- `role` - 'jobseeker' or 'consultancy'
- `first_name` - User's first name
- `last_name` - User's last name
- `is_active` - Account status
- `created_at` - Registration timestamp
- `updated_at` - Last update timestamp

### Permission System Tables

#### resources
- `id` - Primary key
- `name` - Resource name (users, jobs, applications, etc.)
- `description` - Resource description

#### permissions  
- `id` - Primary key
- `resource_id` - Foreign key to resources
- `action` - Action type (view, create, edit, delete, manage)
- `description` - Permission description

#### role_permissions
- `role_id` - Foreign key to roles
- `permission_id` - Foreign key to permissions

### Session Management
- `user_sessions` - Session tracking for jobseeker/consultancy users
- `admin_tokens` - JWT token management for admin users

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

### Adding New Role-Specific Features
1. Create route file in `app/routes/roles/`
2. Define role-specific Blueprint
3. Add authentication middleware
4. Register Blueprint in `app/__init__.py`

### Example Role Route Structure
```python
# app/routes/roles/newrole_routes.py
from flask import Blueprint, render_template, session, redirect, url_for

newrole_bp = Blueprint('newrole', __name__)

@newrole_bp.before_request
def require_auth():
    if 'user_id' not in session or session.get('role') != 'newrole':
        return redirect(url_for('auth.login'))

@newrole_bp.route('/dashboard')
def dashboard():
    return render_template('newrole/dashboard.html')
```

### Adding Public Pages
```python
# app/routes/public_routes.py
@public_bp.route('/new-page')
def new_page():
    return render_template('public/new_page.html')
```

### Dynamic Menu Configuration
Menus are automatically generated based on:
- User role and permissions (admin)
- Role-specific menu configurations (jobseeker/consultancy)
- Database-driven permission checks

## Security Features

- **Role-Based Access Control**: 4 distinct user roles with specific permissions
- **Dual Authentication System**: JWT for admin users, sessions for regular users
- **Dynamic Permission Management**: Database-driven permissions with 81 granular controls
- **Password Security**: Werkzeug password hashing with salt
- **Session Security**: Secure session tokens with expiration
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Input Validation**: Comprehensive form and API input validation
- **CORS Protection**: Cross-origin request security
- **Environment Security**: Secure configuration management
- **Route Protection**: Middleware-based authentication on all protected routes

## Permission System

### Resources (17 total)
1. **users** - User management
2. **jobs** - Job posting and management  
3. **applications** - Job application tracking
4. **companies** - Company profile management
5. **candidates** - Candidate management
6. **reports** - System reporting
7. **analytics** - Analytics and insights
8. **notifications** - Notification management
9. **settings** - System settings
10. **roles** - Role management
11. **permissions** - Permission management
12. **audit_logs** - Audit trail management
13. **templates** - Template management
14. **categories** - Category management
15. **locations** - Location management
16. **skills** - Skills management
17. **system** - System administration

### Actions per Resource
- **view** - Read access
- **create** - Creation rights
- **edit** - Modification rights  
- **delete** - Deletion rights
- **manage** - Full administrative access

**Total: 81 permissions (17 resources × 5 actions each)**

## Testing

### Manual API Testing
```bash
# Test public homepage (no auth required)
curl -X GET http://localhost:5051/

# Admin login
curl -X POST http://localhost:5051/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password", "role": "admin"}'

# Jobseeker login
curl -X POST http://localhost:5051/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jobseeker1", "password": "password", "role": "jobseeker"}'

# Access role-specific dashboard
curl -X GET http://localhost:5051/jobseeker/dashboard \
  -H "Cookie: session=<session_cookie>"

# Admin API access (JWT required)
curl -X GET http://localhost:5051/admin/dashboard \
  -H "Authorization: Bearer <jwt_token>"
```

## User Access Guide

### For Public Users
1. Visit http://localhost:5051
2. Browse product information without login
3. Use login dropdown to select appropriate role
4. Register or login based on role

### For Jobseekers
1. Register/Login at http://localhost:5051/login/jobseeker
2. Access dashboard with blue theme
3. Search jobs, manage applications, update profile
4. Session-based authentication

### For Consultancies  
1. Register/Login at http://localhost:5051/login/consultancy
2. Access dashboard with purple theme
3. Post jobs, manage candidates, company profile
4. Session-based authentication

### For Administrators
1. Login at http://localhost:5051/login/admin
2. Access dynamic admin dashboard
3. Menu options based on database permissions
4. JWT-based secure authentication

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database `jobhunter_fresh` exists
   - Run initialization script: `mysql -u root -p jobhunter_fresh < sql-scripts/init.sql`

2. **Permission/Access Errors**
   - Check user role in database
   - Verify permission assignments in `role_permissions` table
   - Ensure session/JWT token is valid
   - Check route authentication middleware

3. **Role-Based Login Issues**
   - Verify user exists in correct table (auth_users vs users)
   - Check role field matches login attempt
   - Ensure password hash is correct
   - Verify authentication method (JWT vs session)

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
   - Verify database initialization in docker

5. **Template/UI Issues**
   - Check template file paths match route returns
   - Verify Bootstrap 5 CDN accessibility  
   - Ensure role-based CSS variables are defined
   - Check menu generation logic for user permissions

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