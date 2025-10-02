#!/usr/bin/env python3
"""
Initialize Job Data - Add sample data for industry types, skills, experience levels, job roles, company types, job types, and locations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
import app.models as models

def init_industry_types():
    """Initialize industry types"""
    industries = [
        {
            'name': 'technology',
            'display_name': 'Technology & Software',
            'description': 'Software development, IT services, tech startups, and digital products',
            'icon': 'fas fa-laptop-code',
            'sort_order': 1
        },
        {
            'name': 'healthcare',
            'display_name': 'Healthcare & Medical',
            'description': 'Medical services, pharmaceuticals, biotechnology, and health tech',
            'icon': 'fas fa-heartbeat',
            'sort_order': 2
        },
        {
            'name': 'finance',
            'display_name': 'Finance & Banking',
            'description': 'Banking, investment, insurance, fintech, and financial services',
            'icon': 'fas fa-chart-line',
            'sort_order': 3
        },
        {
            'name': 'education',
            'display_name': 'Education & Training',
            'description': 'Schools, universities, online learning, and educational technology',
            'icon': 'fas fa-graduation-cap',
            'sort_order': 4
        },
        {
            'name': 'retail',
            'display_name': 'Retail & E-commerce',
            'description': 'Retail stores, e-commerce platforms, and consumer goods',
            'icon': 'fas fa-shopping-cart',
            'sort_order': 5
        },
        {
            'name': 'manufacturing',
            'display_name': 'Manufacturing & Industrial',
            'description': 'Manufacturing, automotive, aerospace, and industrial equipment',
            'icon': 'fas fa-industry',
            'sort_order': 6
        },
        {
            'name': 'consulting',
            'display_name': 'Consulting & Professional Services',
            'description': 'Management consulting, professional services, and advisory',
            'icon': 'fas fa-handshake',
            'sort_order': 7
        },
        {
            'name': 'media',
            'display_name': 'Media & Entertainment',
            'description': 'Publishing, broadcasting, gaming, and entertainment industry',
            'icon': 'fas fa-film',
            'sort_order': 8
        }
    ]
    
    print("🏭 Initializing industry types...")
    for industry_data in industries:
        existing = models.IndustryType.query.filter_by(name=industry_data['name']).first()
        if not existing:
            industry = models.IndustryType(**industry_data)
            db.session.add(industry)
            print(f"  ✅ Added: {industry_data['display_name']}")
        else:
            print(f"  ⏭️ Exists: {industry_data['display_name']}")

def init_experience_levels():
    """Initialize experience levels"""
    experiences = [
        {
            'name': 'entry_level',
            'display_name': 'Entry Level',
            'description': 'New graduates or professionals with minimal experience',
            'min_years': 0,
            'max_years': 2,
            'sort_order': 1
        },
        {
            'name': 'junior',
            'display_name': 'Junior',
            'description': 'Early career professionals with some experience',
            'min_years': 1,
            'max_years': 3,
            'sort_order': 2
        },
        {
            'name': 'mid_level',
            'display_name': 'Mid-Level',
            'description': 'Experienced professionals with solid foundation',
            'min_years': 3,
            'max_years': 6,
            'sort_order': 3
        },
        {
            'name': 'senior',
            'display_name': 'Senior',
            'description': 'Highly experienced professionals and technical experts',
            'min_years': 5,
            'max_years': 10,
            'sort_order': 4
        },
        {
            'name': 'lead',
            'display_name': 'Lead',
            'description': 'Team leads and technical leadership roles',
            'min_years': 7,
            'max_years': 12,
            'sort_order': 5
        },
        {
            'name': 'principal',
            'display_name': 'Principal',
            'description': 'Principal engineers and senior technical experts',
            'min_years': 10,
            'max_years': 15,
            'sort_order': 6
        },
        {
            'name': 'director',
            'display_name': 'Director',
            'description': 'Directors and senior management positions',
            'min_years': 12,
            'max_years': None,
            'sort_order': 7
        },
        {
            'name': 'executive',
            'display_name': 'Executive',
            'description': 'C-level and executive leadership positions',
            'min_years': 15,
            'max_years': None,
            'sort_order': 8
        }
    ]
    
    print("🎓 Initializing experience levels...")
    for exp_data in experiences:
        existing = Experience.query.filter_by(name=exp_data['name']).first()
        if not existing:
            experience = Experience(**exp_data)
            db.session.add(experience)
            print(f"  ✅ Added: {exp_data['display_name']}")
        else:
            print(f"  ⏭️ Exists: {exp_data['display_name']}")

def init_job_types():
    """Initialize job types"""
    job_types = [
        # Employment Types
        {'name': 'full_time', 'display_name': 'Full-Time', 'category': 'employment_type', 'description': 'Full-time permanent position', 'sort_order': 1},
        {'name': 'part_time', 'display_name': 'Part-Time', 'category': 'employment_type', 'description': 'Part-time position', 'sort_order': 2},
        {'name': 'contract', 'display_name': 'Contract', 'category': 'employment_type', 'description': 'Contract-based employment', 'sort_order': 3},
        {'name': 'freelance', 'display_name': 'Freelance', 'category': 'employment_type', 'description': 'Freelance or project-based work', 'sort_order': 4},
        {'name': 'internship', 'display_name': 'Internship', 'category': 'employment_type', 'description': 'Internship position', 'sort_order': 5},
        {'name': 'temporary', 'display_name': 'Temporary', 'category': 'employment_type', 'description': 'Temporary position', 'sort_order': 6},
        
        # Contract Types
        {'name': 'w2', 'display_name': 'W2', 'category': 'contract_type', 'description': 'W2 employee status', 'sort_order': 10},
        {'name': 'c2c', 'display_name': 'C2C (Corp-to-Corp)', 'category': 'contract_type', 'description': 'Corporation to corporation contract', 'sort_order': 11},
        {'name': '1099', 'display_name': '1099', 'category': 'contract_type', 'description': 'Independent contractor (1099)', 'sort_order': 12},
        
        # Work Models
        {'name': 'remote', 'display_name': 'Remote', 'category': 'work_model', 'description': 'Fully remote work', 'sort_order': 20},
        {'name': 'hybrid', 'display_name': 'Hybrid', 'category': 'work_model', 'description': 'Combination of remote and on-site work', 'sort_order': 21},
        {'name': 'on_site', 'display_name': 'On-Site', 'category': 'work_model', 'description': 'Work from office/company location', 'sort_order': 22}
    ]
    
    print("💼 Initializing job types...")
    for job_type_data in job_types:
        existing = JobType.query.filter_by(name=job_type_data['name']).first()
        if not existing:
            job_type = JobType(**job_type_data)
            db.session.add(job_type)
            print(f"  ✅ Added: {job_type_data['display_name']} ({job_type_data['category']})")
        else:
            print(f"  ⏭️ Exists: {job_type_data['display_name']}")

def init_company_types():
    """Initialize company types"""
    company_types = [
        {
            'name': 'startup',
            'display_name': 'Startup',
            'description': 'Early-stage companies with high growth potential',
            'employee_range_min': 1,
            'employee_range_max': 50,
            'sort_order': 1
        },
        {
            'name': 'small_business',
            'display_name': 'Small Business',
            'description': 'Small to medium-sized businesses',
            'employee_range_min': 10,
            'employee_range_max': 200,
            'sort_order': 2
        },
        {
            'name': 'medium_business',
            'display_name': 'Medium Business',
            'description': 'Medium-sized established businesses',
            'employee_range_min': 200,
            'employee_range_max': 1000,
            'sort_order': 3
        },
        {
            'name': 'large_enterprise',
            'display_name': 'Large Enterprise',
            'description': 'Large corporations and enterprises',
            'employee_range_min': 1000,
            'employee_range_max': 10000,
            'sort_order': 4
        },
        {
            'name': 'fortune_500',
            'display_name': 'Fortune 500',
            'description': 'Fortune 500 companies',
            'employee_range_min': 10000,
            'employee_range_max': None,
            'sort_order': 5
        },
        {
            'name': 'non_profit',
            'display_name': 'Non-Profit',
            'description': 'Non-profit organizations and NGOs',
            'employee_range_min': None,
            'employee_range_max': None,
            'sort_order': 6
        },
        {
            'name': 'government',
            'display_name': 'Government',
            'description': 'Government agencies and public sector',
            'employee_range_min': None,
            'employee_range_max': None,
            'sort_order': 7
        },
        {
            'name': 'consulting',
            'display_name': 'Consulting',
            'description': 'Consulting firms and professional services',
            'employee_range_min': None,
            'employee_range_max': None,
            'sort_order': 8
        }
    ]
    
    print("🏢 Initializing company types...")
    for company_data in company_types:
        existing = CompanyType.query.filter_by(name=company_data['name']).first()
        if not existing:
            company_type = CompanyType(**company_data)
            db.session.add(company_type)
            print(f"  ✅ Added: {company_data['display_name']}")
        else:
            print(f"  ⏭️ Exists: {company_data['display_name']}")

def init_countries():
    """Initialize major countries"""
    countries = [
        {
            'name': 'United States',
            'code_alpha2': 'US',
            'code_alpha3': 'USA',
            'numeric_code': '840',
            'currency_code': 'USD',
            'phone_code': '+1',
            'timezone_primary': 'America/New_York',
            'sort_order': 1
        },
        {
            'name': 'Canada',
            'code_alpha2': 'CA',
            'code_alpha3': 'CAN',
            'numeric_code': '124',
            'currency_code': 'CAD',
            'phone_code': '+1',
            'timezone_primary': 'America/Toronto',
            'sort_order': 2
        },
        {
            'name': 'United Kingdom',
            'code_alpha2': 'GB',
            'code_alpha3': 'GBR',
            'numeric_code': '826',
            'currency_code': 'GBP',
            'phone_code': '+44',
            'timezone_primary': 'Europe/London',
            'sort_order': 3
        },
        {
            'name': 'India',
            'code_alpha2': 'IN',
            'code_alpha3': 'IND',
            'numeric_code': '356',
            'currency_code': 'INR',
            'phone_code': '+91',
            'timezone_primary': 'Asia/Kolkata',
            'sort_order': 4
        },
        {
            'name': 'Germany',
            'code_alpha2': 'DE',
            'code_alpha3': 'DEU',
            'numeric_code': '276',
            'currency_code': 'EUR',
            'phone_code': '+49',
            'timezone_primary': 'Europe/Berlin',
            'sort_order': 5
        },
        {
            'name': 'Australia',
            'code_alpha2': 'AU',
            'code_alpha3': 'AUS',
            'numeric_code': '036',
            'currency_code': 'AUD',
            'phone_code': '+61',
            'timezone_primary': 'Australia/Sydney',
            'sort_order': 6
        }
    ]
    
    print("🌍 Initializing countries...")
    for country_data in countries:
        existing = Country.query.filter_by(code_alpha2=country_data['code_alpha2']).first()
        if not existing:
            country = Country(**country_data)
            db.session.add(country)
            print(f"  ✅ Added: {country_data['name']}")
        else:
            print(f"  ⏭️ Exists: {country_data['name']}")

def init_sample_skills():
    """Initialize sample skills for technology industry"""
    tech_industry = IndustryType.query.filter_by(name='technology').first()
    if not tech_industry:
        print("⚠️ Technology industry not found, skipping skills initialization")
        return
    
    skills = [
        # Programming Languages
        {'name': 'python', 'display_name': 'Python', 'category': 'programming_language', 'industry_id': tech_industry.id, 'sort_order': 1},
        {'name': 'javascript', 'display_name': 'JavaScript', 'category': 'programming_language', 'industry_id': tech_industry.id, 'sort_order': 2},
        {'name': 'java', 'display_name': 'Java', 'category': 'programming_language', 'industry_id': tech_industry.id, 'sort_order': 3},
        {'name': 'csharp', 'display_name': 'C#', 'category': 'programming_language', 'industry_id': tech_industry.id, 'sort_order': 4},
        {'name': 'react', 'display_name': 'React', 'category': 'framework', 'industry_id': tech_industry.id, 'sort_order': 10},
        {'name': 'nodejs', 'display_name': 'Node.js', 'category': 'framework', 'industry_id': tech_industry.id, 'sort_order': 11},
        {'name': 'angular', 'display_name': 'Angular', 'category': 'framework', 'industry_id': tech_industry.id, 'sort_order': 12},
        {'name': 'vue', 'display_name': 'Vue.js', 'category': 'framework', 'industry_id': tech_industry.id, 'sort_order': 13},
        
        # Databases
        {'name': 'mysql', 'display_name': 'MySQL', 'category': 'database', 'industry_id': tech_industry.id, 'sort_order': 20},
        {'name': 'postgresql', 'display_name': 'PostgreSQL', 'category': 'database', 'industry_id': tech_industry.id, 'sort_order': 21},
        {'name': 'mongodb', 'display_name': 'MongoDB', 'category': 'database', 'industry_id': tech_industry.id, 'sort_order': 22},
        
        # Cloud & DevOps
        {'name': 'aws', 'display_name': 'Amazon Web Services (AWS)', 'category': 'cloud', 'industry_id': tech_industry.id, 'sort_order': 30},
        {'name': 'docker', 'display_name': 'Docker', 'category': 'devops', 'industry_id': tech_industry.id, 'sort_order': 31},
        {'name': 'kubernetes', 'display_name': 'Kubernetes', 'category': 'devops', 'industry_id': tech_industry.id, 'sort_order': 32}
    ]
    
    print("⚙️ Initializing sample skills...")
    for skill_data in skills:
        existing = Skill.query.filter_by(name=skill_data['name']).first()
        if not existing:
            skill = Skill(**skill_data)
            db.session.add(skill)
            print(f"  ✅ Added: {skill_data['display_name']} ({skill_data['category']})")
        else:
            print(f"  ⏭️ Exists: {skill_data['display_name']}")

def init_sample_job_roles():
    """Initialize sample job roles"""
    tech_industry = IndustryType.query.filter_by(name='technology').first()
    if not tech_industry:
        print("⚠️ Technology industry not found, skipping job roles initialization")
        return
    
    job_roles = [
        # Engineering Roles
        {'name': 'software_engineer', 'display_name': 'Software Engineer', 'category': 'engineering', 'industry_id': tech_industry.id, 'sort_order': 1},
        {'name': 'senior_software_engineer', 'display_name': 'Senior Software Engineer', 'category': 'engineering', 'industry_id': tech_industry.id, 'sort_order': 2},
        {'name': 'tech_lead', 'display_name': 'Tech Lead', 'category': 'leadership', 'industry_id': tech_industry.id, 'sort_order': 3},
        {'name': 'team_lead', 'display_name': 'Team Lead', 'category': 'leadership', 'industry_id': tech_industry.id, 'sort_order': 4},
        {'name': 'engineering_manager', 'display_name': 'Engineering Manager', 'category': 'management', 'industry_id': tech_industry.id, 'sort_order': 5},
        {'name': 'principal_engineer', 'display_name': 'Principal Engineer', 'category': 'engineering', 'industry_id': tech_industry.id, 'sort_order': 6},
        {'name': 'architect', 'display_name': 'Software Architect', 'category': 'architecture', 'industry_id': tech_industry.id, 'sort_order': 7},
        
        # Specialized Roles
        {'name': 'fullstack_developer', 'display_name': 'Full Stack Developer', 'category': 'engineering', 'industry_id': tech_industry.id, 'sort_order': 10},
        {'name': 'frontend_developer', 'display_name': 'Frontend Developer', 'category': 'engineering', 'industry_id': tech_industry.id, 'sort_order': 11},
        {'name': 'backend_developer', 'display_name': 'Backend Developer', 'category': 'engineering', 'industry_id': tech_industry.id, 'sort_order': 12},
        {'name': 'devops_engineer', 'display_name': 'DevOps Engineer', 'category': 'engineering', 'industry_id': tech_industry.id, 'sort_order': 13},
        {'name': 'data_scientist', 'display_name': 'Data Scientist', 'category': 'data', 'industry_id': tech_industry.id, 'sort_order': 14},
        {'name': 'product_manager', 'display_name': 'Product Manager', 'category': 'product', 'industry_id': tech_industry.id, 'sort_order': 15},
        {'name': 'qa_engineer', 'display_name': 'QA Engineer', 'category': 'quality', 'industry_id': tech_industry.id, 'sort_order': 16}
    ]
    
    print("👔 Initializing sample job roles...")
    for role_data in job_roles:
        existing = JobRole.query.filter_by(name=role_data['name']).first()
        if not existing:
            job_role = JobRole(**role_data)
            db.session.add(job_role)
            print(f"  ✅ Added: {role_data['display_name']} ({role_data['category']})")
        else:
            print(f"  ⏭️ Exists: {role_data['display_name']}")

def main():
    """Initialize all job data"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 Initializing Job Data...")
            print("=" * 50)
            
            # Create tables if they don't exist
            print("📋 Creating database tables...")
            db.create_all()
            
            # Initialize data in order (due to foreign key relationships)
            init_industry_types()
            init_experience_levels()
            init_job_types()
            init_company_types()
            init_countries()
            init_sample_skills()
            init_sample_job_roles()
            
            # Commit all changes
            db.session.commit()
            
            print("\n" + "=" * 50)
            print("✅ Job data initialization completed successfully!")
            
            # Print summary
            print("\n📊 Summary:")
            print(f"  Industry Types: {IndustryType.query.count()}")
            print(f"  Experience Levels: {Experience.query.count()}")
            print(f"  Job Types: {JobType.query.count()}")
            print(f"  Company Types: {CompanyType.query.count()}")
            print(f"  Skills: {Skill.query.count()}")
            print(f"  Job Roles: {JobRole.query.count()}")
            print(f"  Countries: {Country.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error during initialization: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)