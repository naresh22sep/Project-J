from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

class UserType(Enum):
    JOBSEEKER = "jobseeker"
    CONSULTANCY = "consultancy"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class User(db.Model):
    """Base User model for all user types"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    user_type = db.Column(db.Enum(UserType), nullable=False, default=UserType.JOBSEEKER)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobseeker_profile = db.relationship('JobSeekerProfile', backref='user', uselist=False)
    consultancy_profile = db.relationship('ConsultancyProfile', backref='user', uselist=False)
    sessions = db.relationship('UserSession', backref='user', lazy=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'user_type': self.user_type.value if self.user_type else None,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserSession(db.Model):
    """User session model for tracking active sessions"""
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserSession {self.user_id}>'

class JobSeekerProfile(db.Model):
    """JobSeeker specific profile information"""
    __tablename__ = 'jobseeker_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    resume_url = db.Column(db.String(255), nullable=True)
    skills = db.Column(db.Text, nullable=True)  # JSON string of skills
    experience_years = db.Column(db.Integer, default=0)
    current_location = db.Column(db.String(100), nullable=True)
    preferred_location = db.Column(db.String(100), nullable=True)
    expected_salary = db.Column(db.Numeric(10, 2), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    education = db.Column(db.Text, nullable=True)  # JSON string of education
    certifications = db.Column(db.Text, nullable=True)  # JSON string of certifications
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resume_url': self.resume_url,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'current_location': self.current_location,
            'preferred_location': self.preferred_location,
            'expected_salary': str(self.expected_salary) if self.expected_salary else None,
            'job_title': self.job_title,
            'education': self.education,
            'certifications': self.certifications,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ConsultancyProfile(db.Model):
    """Consultancy specific profile information"""
    __tablename__ = 'consultancy_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(150), nullable=False)
    company_description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    company_size = db.Column(db.String(50), nullable=True)  # e.g., "1-10", "11-50", etc.
    industry = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    license_number = db.Column(db.String(100), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    specializations = db.Column(db.Text, nullable=True)  # JSON string of specializations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with jobs
    jobs = db.relationship('Job', backref='consultancy', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'company_description': self.company_description,
            'website': self.website,
            'company_size': self.company_size,
            'industry': self.industry,
            'address': self.address,
            'license_number': self.license_number,
            'verified': self.verified,
            'specializations': self.specializations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Job(db.Model):
    """Job postings by consultancies"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    consultancy_id = db.Column(db.Integer, db.ForeignKey('consultancy_profiles.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)  # job category (e.g., Technology, Healthcare, Finance)
    salary_min = db.Column(db.Numeric(10, 2), nullable=True)
    salary_max = db.Column(db.Numeric(10, 2), nullable=True)
    job_type = db.Column(db.String(50), nullable=True)  # full-time, part-time, contract
    experience_required = db.Column(db.Integer, default=0)
    skills_required = db.Column(db.Text, nullable=True)  # JSON string
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with applications
    applications = db.relationship('JobApplication', backref='job', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'consultancy_id': self.consultancy_id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'location': self.location,
            'salary_min': str(self.salary_min) if self.salary_min else None,
            'salary_max': str(self.salary_max) if self.salary_max else None,
            'job_type': self.job_type,
            'experience_required': self.experience_required,
            'skills_required': self.skills_required,
            'is_active': self.is_active,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class JobApplication(db.Model):
    """Job applications by job seekers"""
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseeker_profiles.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='applied')  # applied, reviewed, interviewed, rejected, hired
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobseeker = db.relationship('JobSeekerProfile', backref='applications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'jobseeker_id': self.jobseeker_id,
            'cover_letter': self.cover_letter,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AuditLog(db.Model):
    """Audit log for admin/superadmin actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_type = db.Column(db.String(50), nullable=True)  # user, job, consultancy
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='audit_logs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PromptCategory(Enum):
    DATABASE = "database"
    FRONTEND = "frontend"
    BACKEND = "backend"
    API = "api"
    UI_UX = "ui_ux"
    BUG_FIX = "bug_fix"
    FEATURE_REQUEST = "feature_request"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    GENERAL = "general"
    OTHER = "other"

class PromptComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ADVANCED = "advanced"

class DevelopmentStage(Enum):
    INITIAL_SETUP = "initial_setup"
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_FIXING = "bug_fixing"
    REFACTORING = "refactoring"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"

class MyPrompts(db.Model):
    """Model for storing user prompts and AI interactions"""
    __tablename__ = 'myprompts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prompt_text = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.String(100), nullable=True)
    prompt_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    prompt_category = db.Column(db.Enum(PromptCategory), nullable=True, default=PromptCategory.GENERAL)
    current_file = db.Column(db.String(500), nullable=True)
    project_phase = db.Column(db.String(100), nullable=True)
    response_summary = db.Column(db.Text, nullable=True)
    files_created = db.Column(db.Text, nullable=True)  # JSON string of created files
    files_modified = db.Column(db.Text, nullable=True)  # JSON string of modified files
    commands_executed = db.Column(db.Text, nullable=True)  # JSON string of commands
    prompt_complexity = db.Column(db.Enum(PromptComplexity), nullable=True, default=PromptComplexity.MODERATE)
    success_rating = db.Column(db.Integer, nullable=True)  # 1-10 scale
    follow_up_needed = db.Column(db.Boolean, default=False)
    prompt_technique = db.Column(db.String(200), nullable=True)
    lessons_learned = db.Column(db.Text, nullable=True)
    git_commit_hash = db.Column(db.String(100), nullable=True)
    development_stage = db.Column(db.Enum(DevelopmentStage), nullable=True, default=DevelopmentStage.FEATURE_DEVELOPMENT)
    response_time_estimate = db.Column(db.Integer, nullable=True)  # in seconds
    tokens_used_estimate = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.Text, nullable=True)  # Comma-separated tags
    keywords = db.Column(db.Text, nullable=True)  # Comma-separated keywords
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert prompt to dictionary"""
        return {
            'id': self.id,
            'prompt_text': self.prompt_text,
            'session_id': self.session_id,
            'prompt_date': self.prompt_date.isoformat() if self.prompt_date else None,
            'prompt_category': self.prompt_category.value if self.prompt_category else None,
            'current_file': self.current_file,
            'project_phase': self.project_phase,
            'response_summary': self.response_summary,
            'files_created': self.files_created,
            'files_modified': self.files_modified,
            'commands_executed': self.commands_executed,
            'prompt_complexity': self.prompt_complexity.value if self.prompt_complexity else None,
            'success_rating': self.success_rating,
            'follow_up_needed': self.follow_up_needed,
            'prompt_technique': self.prompt_technique,
            'lessons_learned': self.lessons_learned,
            'git_commit_hash': self.git_commit_hash,
            'development_stage': self.development_stage.value if self.development_stage else None,
            'response_time_estimate': self.response_time_estimate,
            'tokens_used_estimate': self.tokens_used_estimate,
            'tags': self.tags,
            'keywords': self.keywords,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ===========================
# JOB-RELATED MODELS
# ===========================

class ExperienceLevel(Enum):
    """Experience levels for job positions"""
    ENTRY_LEVEL = "entry_level"
    JUNIOR = "junior"
    MID_LEVEL = "mid_level"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"
    ARCHITECT = "architect"
    DIRECTOR = "director"
    VP = "vp"
    C_LEVEL = "c_level"

class JobTypeEnum(Enum):
    """Job types and employment models"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"
    W2 = "w2"
    C2C = "c2c"
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on_site"

class CompanyTypeEnum(Enum):
    """Company types and sizes"""
    STARTUP = "startup"
    SMALL_BUSINESS = "small_business"
    MEDIUM_BUSINESS = "medium_business"
    LARGE_ENTERPRISE = "large_enterprise"
    FORTUNE_500 = "fortune_500"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"
    CONSULTING = "consulting"
    AGENCY = "agency"

# Industry Types Model
class IndustryType(db.Model):
    """Industry classifications for companies and jobs"""
    __tablename__ = 'industry_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # FontAwesome icon class
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'icon': self.icon,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# Skills Model
class Skill(db.Model):
    """Skills and technologies"""
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # technical, soft, language, etc.
    industry_id = db.Column(db.Integer, db.ForeignKey('industry_types.id'))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    industry = db.relationship('IndustryType', backref='skills')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'industry_id': self.industry_id,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# Experience Levels Model
class Experience(db.Model):
    """Experience levels for job positions"""
    __tablename__ = 'experience_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    min_years = db.Column(db.Integer)
    max_years = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'min_years': self.min_years,
            'max_years': self.max_years,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# Job Roles Model
class JobRole(db.Model):
    """Job roles and positions"""
    __tablename__ = 'job_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # engineering, management, sales, etc.
    industry_id = db.Column(db.Integer, db.ForeignKey('industry_types.id'))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    industry = db.relationship('IndustryType', backref='job_roles')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'industry_id': self.industry_id,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# Company Types Model
class CompanyType(db.Model):
    """Company types and sizes"""
    __tablename__ = 'company_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    employee_range_min = db.Column(db.Integer)
    employee_range_max = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'employee_range_min': self.employee_range_min,
            'employee_range_max': self.employee_range_max,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# Job Types Model
class JobType(db.Model):
    """Job types and employment models"""
    __tablename__ = 'job_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # employment_type, work_model, contract_type
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# Countries Model
class Country(db.Model):
    """Countries for location data"""
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code_alpha2 = db.Column(db.String(2), unique=True, nullable=False)  # US, CA, IN
    code_alpha3 = db.Column(db.String(3), unique=True, nullable=False)  # USA, CAN, IND
    numeric_code = db.Column(db.String(3))
    currency_code = db.Column(db.String(3))  # USD, CAD, INR
    phone_code = db.Column(db.String(10))  # +1, +91
    timezone_primary = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    states = db.relationship('State', backref='country', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code_alpha2': self.code_alpha2,
            'code_alpha3': self.code_alpha3,
            'numeric_code': self.numeric_code,
            'currency_code': self.currency_code,
            'phone_code': self.phone_code,
            'timezone_primary': self.timezone_primary,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# States/Provinces Model
class State(db.Model):
    """States/Provinces for location data"""
    __tablename__ = 'states'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10))  # CA, TX, ON, etc.
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    timezone_primary = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cities = db.relationship('City', backref='state', cascade='all, delete-orphan')
    
    # Unique constraint for name+country combination
    __table_args__ = (db.UniqueConstraint('name', 'country_id', name='_state_country_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'country_id': self.country_id,
            'country_name': self.country.name if self.country else None,
            'timezone_primary': self.timezone_primary,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

# Cities Model
class City(db.Model):
    """Cities for location data"""
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    population = db.Column(db.Integer)
    timezone = db.Column(db.String(50))
    is_metro = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint for name+state combination
    __table_args__ = (db.UniqueConstraint('name', 'state_id', name='_city_state_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'state_id': self.state_id,
            'state_name': self.state.name if self.state else None,
            'country_name': self.state.country.name if self.state and self.state.country else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'population': self.population,
            'timezone': self.timezone,
            'is_metro': self.is_metro,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }