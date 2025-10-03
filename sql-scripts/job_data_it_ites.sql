-- =====================================================
-- JOB DATA MANAGEMENT - IT & ITES FOCUS
-- =====================================================

-- Clear existing data (optional - remove if you want to keep existing data)
-- DELETE FROM cities WHERE id > 0;
-- DELETE FROM states WHERE id > 0;
-- DELETE FROM countries WHERE id > 0;
-- DELETE FROM job_roles WHERE id > 0;
-- DELETE FROM skills WHERE id > 0;
-- DELETE FROM job_types WHERE id > 0;
-- DELETE FROM company_types WHERE id > 0;
-- DELETE FROM experience_levels WHERE id > 0;
-- DELETE FROM industry_types WHERE id > 0;

-- =====================================================
-- 1. INDUSTRY TYPES (IT & ITES Focus)
-- =====================================================

INSERT INTO industry_types (name, display_name, description, icon, sort_order, is_active, created_at) VALUES
('information_technology', 'Information Technology', 'Software development, hardware, system administration, and IT infrastructure', 'fas fa-laptop-code', 1, TRUE, NOW()),
('software_development', 'Software Development', 'Custom software development, web applications, mobile apps, and enterprise solutions', 'fas fa-code', 2, TRUE, NOW()),
('cybersecurity', 'Cybersecurity', 'Information security, threat analysis, penetration testing, and security consulting', 'fas fa-shield-alt', 3, TRUE, NOW()),
('data_science', 'Data Science & Analytics', 'Big data, machine learning, artificial intelligence, and business intelligence', 'fas fa-chart-line', 4, TRUE, NOW()),
('cloud_computing', 'Cloud Computing', 'Cloud infrastructure, DevOps, containerization, and cloud-native solutions', 'fas fa-cloud', 5, TRUE, NOW()),
('digital_marketing', 'Digital Marketing & SEO', 'Search engine optimization, digital advertising, content marketing, and social media', 'fas fa-bullhorn', 6, TRUE, NOW()),
('fintech', 'Financial Technology', 'Financial software, payment systems, blockchain, and cryptocurrency solutions', 'fas fa-coins', 7, TRUE, NOW()),
('healthtech', 'Healthcare Technology', 'Medical software, telemedicine, health informatics, and medical device software', 'fas fa-heartbeat', 8, TRUE, NOW()),
('edtech', 'Educational Technology', 'E-learning platforms, educational software, and online training solutions', 'fas fa-graduation-cap', 9, TRUE, NOW()),
('gaming', 'Gaming & Entertainment', 'Video game development, mobile gaming, VR/AR, and entertainment software', 'fas fa-gamepad', 10, TRUE, NOW());

-- =====================================================
-- 2. EXPERIENCE LEVELS
-- =====================================================

INSERT INTO experience_levels (name, display_name, description, min_years, max_years, sort_order, is_active, created_at) VALUES
('entry_level', 'Entry Level', 'Fresh graduates and candidates with 0-2 years of experience', 0, 2, 1, TRUE, NOW()),
('junior', 'Junior Level', 'Professionals with 2-4 years of relevant experience', 2, 4, 2, TRUE, NOW()),
('mid_level', 'Mid Level', 'Experienced professionals with 4-7 years in the field', 4, 7, 3, TRUE, NOW()),
('senior', 'Senior Level', 'Senior professionals with 7-12 years of extensive experience', 7, 12, 4, TRUE, NOW()),
('lead', 'Lead/Principal', 'Technical leads and principal engineers with 10-15 years experience', 10, 15, 5, TRUE, NOW()),
('architect', 'Architect/Manager', 'Solution architects and engineering managers with 12+ years', 12, NULL, 6, TRUE, NOW()),
('director', 'Director/VP', 'Senior leadership roles with 15+ years of experience', 15, NULL, 7, TRUE, NOW()),
('executive', 'C-Level/Executive', 'Executive leadership positions with 20+ years experience', 20, NULL, 8, TRUE, NOW()),
('intern', 'Internship', 'Students and recent graduates seeking internship opportunities', 0, 1, 0, TRUE, NOW()),
('consultant', 'Consultant', 'Independent consultants with varying years of specialized experience', 5, NULL, 9, TRUE, NOW());

-- =====================================================
-- 3. COMPANY TYPES
-- =====================================================

INSERT INTO company_types (name, display_name, description, employee_range_min, employee_range_max, sort_order, is_active, created_at) VALUES
('startup', 'Startup', 'Early-stage companies with innovative products and high growth potential', 1, 50, 1, TRUE, NOW()),
('small_business', 'Small Business', 'Established small businesses with steady growth', 10, 100, 2, TRUE, NOW()),
('mid_size', 'Mid-size Company', 'Growing companies with established market presence', 100, 1000, 3, TRUE, NOW()),
('large_enterprise', 'Large Enterprise', 'Established corporations with extensive operations', 1000, 10000, 4, TRUE, NOW()),
('fortune_500', 'Fortune 500', 'Top-tier global corporations with massive scale', 10000, NULL, 5, TRUE, NOW()),
('tech_giant', 'Tech Giant', 'Major technology companies like FAANG and similar', 50000, NULL, 6, TRUE, NOW()),
('consulting_firm', 'Consulting Firm', 'Professional services and consulting companies', 50, 5000, 7, TRUE, NOW()),
('software_vendor', 'Software Vendor', 'Companies specializing in software products and solutions', 20, 2000, 8, TRUE, NOW()),
('digital_agency', 'Digital Agency', 'Creative and digital marketing agencies', 5, 200, 9, TRUE, NOW()),
('government', 'Government/Public Sector', 'Government agencies and public sector organizations', 100, NULL, 10, TRUE, NOW()),
('non_profit', 'Non-Profit', 'Non-profit organizations and NGOs with technology needs', 5, 500, 11, TRUE, NOW()),
('freelance', 'Freelance/Independent', 'Individual contractors and freelance professionals', 1, 1, 12, TRUE, NOW());

-- =====================================================
-- 4. JOB TYPES
-- =====================================================

INSERT INTO job_types (name, display_name, description, category, sort_order, is_active, created_at) VALUES
('full_time', 'Full-time', 'Standard full-time employment with benefits', 'employment', 1, TRUE, NOW()),
('part_time', 'Part-time', 'Part-time positions with flexible hours', 'employment', 2, TRUE, NOW()),
('contract', 'Contract', 'Fixed-term contract positions', 'contract', 3, TRUE, NOW()),
('freelance', 'Freelance', 'Project-based freelance work', 'contract', 4, TRUE, NOW()),
('consultant', 'Consultant', 'Independent consulting engagements', 'contract', 5, TRUE, NOW()),
('remote', 'Remote', 'Fully remote work opportunities', 'location', 6, TRUE, NOW()),
('hybrid', 'Hybrid', 'Combination of remote and office work', 'location', 7, TRUE, NOW()),
('on_site', 'On-site', 'Traditional office-based work', 'location', 8, TRUE, NOW()),
('internship', 'Internship', 'Student and graduate internship programs', 'temporary', 9, TRUE, NOW()),
('temp', 'Temporary', 'Short-term temporary positions', 'temporary', 10, TRUE, NOW()),
('seasonal', 'Seasonal', 'Seasonal or project-specific roles', 'temporary', 11, TRUE, NOW()),
('volunteer', 'Volunteer', 'Unpaid volunteer opportunities', 'volunteer', 12, TRUE, NOW());

-- =====================================================
-- 5. SKILLS (IT & ITES Focus with Industry Relations)
-- =====================================================

-- Programming Languages & Frameworks
INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'javascript', 'JavaScript', 'Modern JavaScript development including ES6+, Node.js, and frameworks', 'programming', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'python', 'Python', 'Python programming for web development, data science, and automation', 'programming', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'java', 'Java', 'Enterprise Java development, Spring framework, and microservices', 'programming', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'react', 'React.js', 'Modern React development with hooks, context, and state management', 'framework', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'angular', 'Angular', 'TypeScript-based Angular framework for enterprise applications', 'framework', id, 5, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'vue', 'Vue.js', 'Progressive Vue.js framework for modern web applications', 'framework', id, 6, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'nodejs', 'Node.js', 'Server-side JavaScript development with Node.js and Express', 'backend', id, 7, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

-- Cloud & DevOps Skills
INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'aws', 'Amazon Web Services', 'AWS cloud services, EC2, S3, Lambda, and cloud architecture', 'cloud', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'azure', 'Microsoft Azure', 'Azure cloud platform, services, and enterprise integration', 'cloud', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'gcp', 'Google Cloud Platform', 'GCP services, BigQuery, and cloud-native development', 'cloud', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'docker', 'Docker', 'Containerization with Docker and container orchestration', 'devops', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'kubernetes', 'Kubernetes', 'Container orchestration and cluster management with K8s', 'devops', id, 5, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'terraform', 'Terraform', 'Infrastructure as Code (IaC) with Terraform', 'devops', id, 6, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

-- Data Science & AI Skills
INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'machine_learning', 'Machine Learning', 'ML algorithms, model training, and predictive analytics', 'data_science', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'tensorflow', 'TensorFlow', 'Deep learning and neural networks with TensorFlow', 'ai', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'pytorch', 'PyTorch', 'Deep learning research and production with PyTorch', 'ai', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'sql', 'SQL', 'Database querying, optimization, and data manipulation', 'database', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'pandas', 'Pandas', 'Data manipulation and analysis with Python Pandas', 'data_analysis', id, 5, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

-- Cybersecurity Skills
INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'ethical_hacking', 'Ethical Hacking', 'Penetration testing and vulnerability assessment', 'security', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'network_security', 'Network Security', 'Firewall management, intrusion detection, and network protection', 'security', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'cryptography', 'Cryptography', 'Encryption, digital signatures, and cryptographic protocols', 'security', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'incident_response', 'Incident Response', 'Security incident handling and forensic analysis', 'security', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

-- Digital Marketing Skills
INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'seo', 'Search Engine Optimization', 'SEO strategy, keyword research, and organic traffic growth', 'marketing', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'google_ads', 'Google Ads', 'PPC advertising, campaign management, and Google Ads optimization', 'marketing', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'social_media', 'Social Media Marketing', 'Social media strategy, content creation, and community management', 'marketing', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'google_analytics', 'Google Analytics', 'Web analytics, data interpretation, and performance tracking', 'analytics', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

-- General IT Skills
INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'linux', 'Linux Administration', 'Linux system administration, shell scripting, and server management', 'system_admin', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'windows_server', 'Windows Server', 'Windows Server administration and Active Directory management', 'system_admin', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'database_admin', 'Database Administration', 'MySQL, PostgreSQL, SQL Server database administration', 'database', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO skills (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'network_admin', 'Network Administration', 'Network configuration, troubleshooting, and infrastructure management', 'networking', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

-- =====================================================
-- 6. JOB ROLES (IT & ITES Focus with Industry Relations)
-- =====================================================

-- Software Development Roles
INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'software_engineer', 'Software Engineer', 'Design, develop, and maintain software applications and systems', 'development', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'frontend_developer', 'Frontend Developer', 'Create user interfaces and user experiences for web applications', 'development', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'backend_developer', 'Backend Developer', 'Develop server-side logic, databases, and application architecture', 'development', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'fullstack_developer', 'Full Stack Developer', 'Work on both frontend and backend development', 'development', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'mobile_developer', 'Mobile Developer', 'Develop native and cross-platform mobile applications', 'development', id, 5, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'tech_lead', 'Technical Lead', 'Lead development teams and make technical architecture decisions', 'leadership', id, 6, TRUE, NOW() 
FROM industry_types WHERE name = 'software_development';

-- Data Science Roles
INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'data_scientist', 'Data Scientist', 'Analyze complex data to derive business insights and build predictive models', 'analytics', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'data_analyst', 'Data Analyst', 'Collect, process, and analyze data to support business decisions', 'analytics', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'ml_engineer', 'Machine Learning Engineer', 'Design and implement machine learning systems and algorithms', 'engineering', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'data_engineer', 'Data Engineer', 'Build and maintain data pipelines and infrastructure', 'engineering', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'data_science';

-- Cloud & DevOps Roles
INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'devops_engineer', 'DevOps Engineer', 'Automate deployment, manage infrastructure, and ensure system reliability', 'operations', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'cloud_engineer', 'Cloud Engineer', 'Design and manage cloud infrastructure and services', 'operations', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'site_reliability_engineer', 'Site Reliability Engineer', 'Ensure system reliability, performance, and scalability', 'operations', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'cloud_architect', 'Cloud Architect', 'Design enterprise cloud solutions and migration strategies', 'architecture', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'cloud_computing';

-- Cybersecurity Roles
INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'security_analyst', 'Security Analyst', 'Monitor and analyze security events, threats, and vulnerabilities', 'security', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'penetration_tester', 'Penetration Tester', 'Conduct security assessments and vulnerability testing', 'security', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'security_engineer', 'Security Engineer', 'Design and implement security systems and protocols', 'security', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'security_consultant', 'Security Consultant', 'Provide security expertise and recommendations to organizations', 'consulting', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'cybersecurity';

-- Digital Marketing Roles
INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'digital_marketer', 'Digital Marketer', 'Plan and execute digital marketing campaigns across various channels', 'marketing', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'seo_specialist', 'SEO Specialist', 'Optimize websites for search engines and improve organic rankings', 'marketing', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'ppc_specialist', 'PPC Specialist', 'Manage paid advertising campaigns on Google Ads and social platforms', 'marketing', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'content_marketer', 'Content Marketer', 'Create and distribute valuable content to attract and engage audiences', 'marketing', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'digital_marketing';

-- General IT Roles
INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'system_administrator', 'System Administrator', 'Manage and maintain computer systems and network infrastructure', 'administration', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'network_administrator', 'Network Administrator', 'Configure, manage, and troubleshoot network systems', 'administration', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'database_administrator', 'Database Administrator', 'Design, implement, and maintain database systems', 'administration', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'it_support', 'IT Support Specialist', 'Provide technical support and troubleshoot user issues', 'support', id, 4, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'product_manager', 'Product Manager', 'Define product strategy, roadmap, and coordinate development efforts', 'management', id, 5, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'scrum_master', 'Scrum Master', 'Facilitate agile development processes and remove team obstacles', 'management', id, 6, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

-- Leadership & Management Roles
INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'engineering_manager', 'Engineering Manager', 'Lead engineering teams and manage technical projects', 'management', id, 1, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'cto', 'Chief Technology Officer', 'Executive leadership for technology strategy and innovation', 'executive', id, 2, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';

INSERT INTO job_roles (name, display_name, description, category, industry_id, sort_order, is_active, created_at) 
SELECT 'solution_architect', 'Solution Architect', 'Design enterprise-level technical solutions and architectures', 'architecture', id, 3, TRUE, NOW() 
FROM industry_types WHERE name = 'information_technology';