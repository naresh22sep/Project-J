# 🔐 JobHunter Authentication & Authorization System

A comprehensive, enterprise-grade authentication and authorization system built with Flask, featuring JWT tokens, role-based access control (RBAC), subscription management, and advanced security features.

## ✨ Features

### 🔑 Authentication
- **JWT Authentication** with exp, iss, and aud claims for enhanced security
- **Password hashing** using bcrypt with salt rounds
- **Multi-session management** with token blacklisting
- **Account lockout** protection after failed login attempts
- **Session timeout** and automatic token refresh

### 🛡️ Security
- **XSS Protection** with input sanitization using bleach
- **CSRF Token Protection** for all state-changing operations
- **Security headers** (CSP, HSTS, X-Frame-Options, etc.)
- **Rate limiting** to prevent brute force attacks
- **Security event logging** with severity levels
- **Suspicious activity monitoring** and alerts

### 👥 Role-Based Access Control (RBAC)
- **Four-tier role system**: SuperAdmin, Admin, Consultancy, JobSeeker
- **Granular permissions** system with resource-action mapping
- **Dynamic role assignment** and permission management
- **Subscription-based feature access** control

### 💳 Subscription Management
- **Four-tier subscription plans**: Starter (Free), Professional, Business, Enterprise
- **Feature-based access control** tied to subscription levels
- **Subscription status tracking** and expiration management
- **Usage limits** and quota enforcement

### 📊 SuperAdmin Dashboard
- **Minimalist admin interface** for comprehensive system management
- **User management** with role assignment and status control
- **Security monitoring** with real-time event tracking
- **Subscription oversight** with plan management capabilities
- **System maintenance** tools and analytics

## 🏗️ Architecture

### Database Schema
```
📁 database/
└── auth_schema.sql          # Complete database schema (13+ tables)
```

### Core Components
```
📁 app/
├── 📁 models/
│   └── auth_models.py       # Authentication data models
├── 📁 services/
│   └── auth_service.py      # JWT and security services  
├── 📁 middleware/
│   └── security_middleware.py # Security middleware layer
├── 📁 routes/
│   ├── auth_routes.py       # Authentication endpoints
│   └── superadmin_routes.py # SuperAdmin management
└── 📁 templates/
    └── 📁 superadmin/       # Admin interface templates
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the project
git clone <repository-url>
cd ProjectJ

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE jobhunter_auth;
EXIT;

# Import schema
mysql -u root -p jobhunter_auth < database/auth_schema.sql
```

### 3. Environment Variables
Create a `.env` file:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/jobhunter_auth
SECURITY_PASSWORD_SALT=your-security-salt-here
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access SuperAdmin Dashboard
- **URL**: http://localhost:5051/superadmin
- **Username**: `superadmin`
- **Password**: `SuperAdmin@2024`
- **⚠️ Important**: Change default password in production!

## 🎯 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login with JWT token generation |
| POST | `/auth/register` | User registration with role assignment |
| POST | `/auth/logout` | User logout with token blacklisting |
| POST | `/auth/refresh` | Refresh JWT access token |
| GET | `/auth/profile` | Get current user profile |
| PUT | `/auth/profile` | Update user profile |
| POST | `/auth/change-password` | Change user password |
| POST | `/auth/verify-token` | Verify JWT token validity |

### SuperAdmin Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/superadmin/dashboard` | Main admin dashboard |
| GET | `/superadmin/users` | List all users |
| GET | `/superadmin/users/<id>` | View user details |
| PUT | `/superadmin/users/<id>/edit` | Edit user information |
| POST | `/superadmin/users/<id>/toggle-active` | Toggle user status |
| GET | `/superadmin/roles` | List roles and permissions |
| POST | `/superadmin/roles/create` | Create new role |
| POST | `/superadmin/permissions/create` | Create new permission |
| GET | `/superadmin/subscriptions` | List all subscriptions |
| POST | `/superadmin/subscriptions/<id>/manage` | Manage subscription |
| GET | `/superadmin/security` | View security logs |
| GET | `/superadmin/api/security-stats` | Get security statistics |

## 🔧 Configuration

### JWT Configuration
```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_ALGORITHM = 'HS256'
JWT_ISSUER = 'JobHunter-Platform'
JWT_AUDIENCE = 'JobHunter-Users'
```

### Security Configuration
```python
# Password Policy
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True
PASSWORD_REQUIRE_SPECIAL = True

# Account Lockout
MAX_LOGIN_ATTEMPTS = 5
ACCOUNT_LOCKOUT_DURATION = timedelta(minutes=30)

# Rate Limiting
RATE_LIMITS = {
    'login': '10 per minute',
    'register': '5 per minute',
    'api_calls': '1000 per hour'
}
```

### Subscription Plans
| Plan | Price | Features |
|------|--------|----------|
| **Starter** | Free | 10 applications/month, Basic search |
| **Professional** | $29.99 | 100 applications/month, Advanced search |
| **Business** | $79.99 | 500 applications/month, Team management |
| **Enterprise** | $199.99 | Unlimited, Custom integrations |

## 🛡️ Security Features

### XSS Protection
```python
# Automatic input sanitization
@sanitize_inputs(['username', 'email', 'comment'])
def create_user():
    # Input is automatically cleaned
    pass
```

### CSRF Protection
```python
# Automatic CSRF validation
@csrf_protect
def sensitive_operation():
    # CSRF token is automatically validated
    pass
```

### JWT Token Security
```python
# Token with comprehensive claims
{
    "user_id": 123,
    "username": "john_doe",
    "roles": ["jobseeker"],
    "exp": 1640995200,  # Expiration
    "iss": "JobHunter-Platform",  # Issuer
    "aud": "JobHunter-Users",     # Audience
    "jti": "unique-token-id"      # JWT ID for blacklisting
}
```

### Role-Based Access Control
```python
# Decorators for easy authorization
@require_role('superadmin')
def admin_only_function():
    pass

@require_permission('user.create')  
def create_user_function():
    pass

@require_subscription_feature('advanced_search')
def advanced_search_function():
    pass
```

## 📈 Monitoring & Logging

### Security Event Types
- `LOGIN_SUCCESS` / `LOGIN_FAILED`
- `USER_REGISTERED` / `USER_MODIFIED`
- `PASSWORD_CHANGED` / `PASSWORD_CHANGE_FAILED`
- `UNAUTHORIZED_ACCESS`
- `XSS_ATTEMPT` / `CSRF_VIOLATION`
- `SQL_INJECTION_ATTEMPT`
- `RATE_LIMIT_EXCEEDED`
- `SUSPICIOUS_ACTIVITY`

### Security Severity Levels
- **Low**: Normal operations, successful authentications
- **Medium**: Failed authentications, permission violations
- **High**: Security attacks, system errors
- **Critical**: System compromise attempts

## 🔄 Development Workflow

### Adding New Roles
1. Create role in database or via SuperAdmin interface
2. Define permissions for the role
3. Update role assignment logic in registration
4. Test role-based access controls

### Adding New Permissions
1. Create permission via SuperAdmin interface
2. Assign to appropriate roles
3. Use `@require_permission()` decorator
4. Test access control

### Adding New Features
1. Define feature in subscription plans
2. Use `@require_subscription_feature()` decorator
3. Update plan feature mappings
4. Test feature access limits

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

### Test Categories
- **Unit Tests**: Individual function testing
- **Integration Tests**: API endpoint testing
- **Security Tests**: Vulnerability testing
- **Performance Tests**: Load and stress testing

## 🚀 Production Deployment

### Environment Setup
```bash
# Production environment variables
FLASK_ENV=production
SECRET_KEY=strong-production-secret-key
DATABASE_URL=mysql+pymysql://user:pass@host:port/db
REDIS_URL=redis://host:port/db
```

### Security Checklist
- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure Redis for rate limiting
- [ ] Set up database backups
- [ ] Enable security monitoring
- [ ] Configure log rotation
- [ ] Test security headers
- [ ] Perform security audit

### Docker Deployment
```dockerfile
# Example Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5051
CMD ["gunicorn", "--bind", "0.0.0.0:5051", "app:app"]
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- 📧 Email: support@jobhunter.com
- 📖 Documentation: [docs.jobhunter.com](https://docs.jobhunter.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourrepo/issues)

---

**🎉 Your complete authentication system is ready!** The SuperAdmin can now manage all users, roles, permissions, and subscriptions through a secure, enterprise-grade interface.