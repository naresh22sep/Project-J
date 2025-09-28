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