-- Add new columns to subscription_plans table
ALTER TABLE subscription_plans 
ADD COLUMN plan_type ENUM('consultancy', 'jobseeker') DEFAULT 'consultancy' AFTER description,
ADD COLUMN max_job_portals INT DEFAULT 0 AFTER max_applications;

-- Update existing plans to be consultancy type
UPDATE subscription_plans SET plan_type = 'consultancy' WHERE plan_type IS NULL;

-- Create job_portals table
CREATE TABLE IF NOT EXISTS job_portals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    website_url VARCHAR(255) NOT NULL,
    logo_url VARCHAR(255),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    api_integration BOOLEAN DEFAULT FALSE,
    api_endpoint VARCHAR(255),
    job_categories JSON,
    supported_countries JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create user_portal_access table
CREATE TABLE IF NOT EXISTS user_portal_access (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    portal_id INT NOT NULL,
    subscription_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    jobs_posted_this_month INT DEFAULT 0,
    last_job_posted DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_users(id) ON DELETE CASCADE,
    FOREIGN KEY (portal_id) REFERENCES job_portals(id) ON DELETE CASCADE,
    FOREIGN KEY (subscription_id) REFERENCES user_subscriptions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_portal (user_id, portal_id)
);

-- Insert popular job portals
INSERT INTO job_portals (name, display_name, website_url, description, is_active, sort_order) VALUES
('linkedin', 'LinkedIn', 'https://www.linkedin.com/jobs/', 'Professional networking platform with extensive job opportunities across all industries', TRUE, 1),
('dice', 'Dice', 'https://www.dice.com/', 'Technology-focused job board specializing in IT, software development, and tech roles', TRUE, 2),
('naukri', 'Naukri.com', 'https://www.naukri.com/', 'India''s leading job portal with opportunities across all sectors and experience levels', TRUE, 3),
('indeed', 'Indeed', 'https://www.indeed.com/', 'Global job search engine aggregating listings from thousands of websites', TRUE, 4),
('glassdoor', 'Glassdoor', 'https://www.glassdoor.com/Jobs/', 'Job search platform with company reviews, salary insights, and interview experiences', TRUE, 5),
('monster', 'Monster', 'https://www.monster.com/', 'Established job board with career advice and resume services', TRUE, 6),
('ziprecruiter', 'ZipRecruiter', 'https://www.ziprecruiter.com/', 'AI-powered job matching platform connecting employers with job seekers', TRUE, 7),
('careerbuilder', 'CareerBuilder', 'https://www.careerbuilder.com/', 'Comprehensive job search platform with career resources and employer solutions', TRUE, 8),
('angellist', 'AngelList (Wellfound)', 'https://wellfound.com/', 'Startup-focused job platform connecting talent with innovative companies', TRUE, 9),
('stackoverflow', 'Stack Overflow Jobs', 'https://stackoverflow.com/jobs/', 'Developer-focused job board from the popular programming Q&A platform', TRUE, 10);

-- Insert job seeker subscription plans
INSERT INTO subscription_plans (name, display_name, description, plan_type, price_monthly, price_yearly, max_users, max_jobs, max_job_portals, sort_order, is_active, features_json) VALUES
('jobseeker_free', 'Free Job Seeker', 'Basic plan for job seekers to get started with job tracking', 'jobseeker', 0.00, 0.00, 1, 0, 0, 1, TRUE, 
 '{"job_tracking": false, "portal_access": 0, "monthly_job_limit": 0, "resume_storage": 1, "job_alerts": false, "application_tracking": false}'),

('jobseeker_basic', 'Basic Job Seeker', 'Perfect for focused job searching with one preferred portal', 'jobseeker', 10.00, 100.00, 1, 100, 1, 2, TRUE,
 '{"job_tracking": true, "portal_access": 1, "monthly_job_limit": 100, "resume_storage": 3, "job_alerts": true, "application_tracking": true, "basic_analytics": true}'),

('jobseeker_standard', 'Standard Job Seeker', 'Expand your reach with multiple job portals', 'jobseeker', 13.00, 130.00, 1, 300, 3, 3, TRUE,
 '{"job_tracking": true, "portal_access": 3, "monthly_job_limit": 300, "resume_storage": 5, "job_alerts": true, "application_tracking": true, "basic_analytics": true, "priority_support": true}'),

('jobseeker_premium', 'Premium Job Seeker', 'Maximum coverage across top job portals', 'jobseeker', 20.00, 200.00, 1, 400, 5, 4, TRUE,
 '{"job_tracking": true, "portal_access": 5, "monthly_job_limit": 400, "resume_storage": 10, "job_alerts": true, "application_tracking": true, "advanced_analytics": true, "priority_support": true, "interview_prep": true}'),

('jobseeker_unlimited', 'Unlimited Job Seeker', 'Unlimited access to all features and portals', 'jobseeker', 30.00, 300.00, 1, -1, -1, 5, TRUE,
 '{"job_tracking": true, "portal_access": -1, "monthly_job_limit": -1, "resume_storage": -1, "job_alerts": true, "application_tracking": true, "advanced_analytics": true, "priority_support": true, "interview_prep": true, "career_coaching": true, "resume_review": true}');

-- Add subscription features for job seeker plans
INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'job_tracking', 'Job Tracking', 'false', TRUE, FALSE 
FROM subscription_plans p WHERE p.name = 'jobseeker_free';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'portal_access_count', 'Job Portal Access', '0', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_free';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'monthly_job_limit', 'Monthly Job Limit', '0', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_free';

-- Basic plan features
INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'job_tracking', 'Job Tracking', 'true', TRUE, FALSE 
FROM subscription_plans p WHERE p.name = 'jobseeker_basic';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'portal_access_count', 'Job Portal Access', '1', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_basic';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'monthly_job_limit', 'Monthly Job Limit', '100', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_basic';

-- Standard plan features
INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'job_tracking', 'Job Tracking', 'true', TRUE, FALSE 
FROM subscription_plans p WHERE p.name = 'jobseeker_standard';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'portal_access_count', 'Job Portal Access', '3', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_standard';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'monthly_job_limit', 'Monthly Job Limit', '300', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_standard';

-- Premium plan features
INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'job_tracking', 'Job Tracking', 'true', TRUE, FALSE 
FROM subscription_plans p WHERE p.name = 'jobseeker_premium';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'portal_access_count', 'Job Portal Access', '5', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_premium';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric) 
SELECT p.id, 'monthly_job_limit', 'Monthly Job Limit', '400', FALSE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_premium';

-- Unlimited plan features
INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric, is_unlimited) 
SELECT p.id, 'job_tracking', 'Job Tracking', 'true', TRUE, FALSE, FALSE 
FROM subscription_plans p WHERE p.name = 'jobseeker_unlimited';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric, is_unlimited) 
SELECT p.id, 'portal_access_count', 'Job Portal Access', '-1', FALSE, TRUE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_unlimited';

INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, is_numeric, is_unlimited) 
SELECT p.id, 'monthly_job_limit', 'Monthly Job Limit', '-1', FALSE, TRUE, TRUE 
FROM subscription_plans p WHERE p.name = 'jobseeker_unlimited';

-- Verify the data was inserted
SELECT 'Subscription Plans Added:' as status;
SELECT name, display_name, price_monthly, plan_type FROM subscription_plans WHERE plan_type = 'jobseeker' ORDER BY sort_order;

SELECT 'Job Portals Added:' as status;
SELECT name, display_name FROM job_portals ORDER BY sort_order;

SELECT 'Features Added:' as status;
SELECT COUNT(*) as feature_count FROM subscription_features sf 
JOIN subscription_plans sp ON sf.plan_id = sp.id 
WHERE sp.plan_type = 'jobseeker';
