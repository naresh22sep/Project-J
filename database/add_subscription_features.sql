-- Migration: Add Subscription Features Management
-- Date: 2025-01-01
-- Description: Add subscription_features table and enhance subscription plans management

-- Create subscription_features table
CREATE TABLE IF NOT EXISTS subscription_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plan_id INT NOT NULL,
    feature_key VARCHAR(150) NOT NULL,
    feature_name VARCHAR(200) NOT NULL,
    feature_value TEXT,
    is_boolean BOOLEAN DEFAULT FALSE,
    is_numeric BOOLEAN DEFAULT FALSE,
    is_unlimited BOOLEAN DEFAULT FALSE,
    feature_category VARCHAR(100) DEFAULT 'general',
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(id) ON DELETE CASCADE,
    UNIQUE KEY unique_plan_feature (plan_id, feature_key),
    INDEX idx_plan_features (plan_id, is_active),
    INDEX idx_feature_category (feature_category),
    INDEX idx_display_order (display_order)
);

-- Add sample features for existing job seeker plans
-- Free Job Seeker Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'job_portals', 'Job Portal Access', '1', FALSE, 'limits', 1 
FROM subscription_plans WHERE name = 'jobseeker_free';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_numeric, feature_category, display_order) 
SELECT id, 'jobs_per_month', 'Jobs per Month', '50', TRUE, 'limits', 2 
FROM subscription_plans WHERE name = 'jobseeker_free';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'email_support', 'Email Support', 'true', TRUE, 'support', 3 
FROM subscription_plans WHERE name = 'jobseeker_free';

-- Basic Job Seeker Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'job_portals', 'Job Portal Access', '1', FALSE, 'limits', 1 
FROM subscription_plans WHERE name = 'jobseeker_basic';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_numeric, feature_category, display_order) 
SELECT id, 'jobs_per_month', 'Jobs per Month', '100', TRUE, 'limits', 2 
FROM subscription_plans WHERE name = 'jobseeker_basic';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'resume_builder', 'Resume Builder', 'true', TRUE, 'features', 3 
FROM subscription_plans WHERE name = 'jobseeker_basic';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'email_support', 'Email Support', 'true', TRUE, 'support', 4 
FROM subscription_plans WHERE name = 'jobseeker_basic';

-- Standard Job Seeker Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'job_portals', 'Job Portal Access', '3', FALSE, 'limits', 1 
FROM subscription_plans WHERE name = 'jobseeker_standard';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_numeric, feature_category, display_order) 
SELECT id, 'jobs_per_month', 'Jobs per Month', '300', TRUE, 'limits', 2 
FROM subscription_plans WHERE name = 'jobseeker_standard';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'resume_builder', 'Resume Builder', 'true', TRUE, 'features', 3 
FROM subscription_plans WHERE name = 'jobseeker_standard';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'interview_prep', 'Interview Preparation', 'true', TRUE, 'features', 4 
FROM subscription_plans WHERE name = 'jobseeker_standard';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'priority_support', 'Priority Support', 'true', TRUE, 'support', 5 
FROM subscription_plans WHERE name = 'jobseeker_standard';

-- Premium Job Seeker Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'job_portals', 'Job Portal Access', '5', FALSE, 'limits', 1 
FROM subscription_plans WHERE name = 'jobseeker_premium';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_numeric, feature_category, display_order) 
SELECT id, 'jobs_per_month', 'Jobs per Month', '400', TRUE, 'limits', 2 
FROM subscription_plans WHERE name = 'jobseeker_premium';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'resume_builder', 'Resume Builder', 'true', TRUE, 'features', 3 
FROM subscription_plans WHERE name = 'jobseeker_premium';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'interview_prep', 'Interview Preparation', 'true', TRUE, 'features', 4 
FROM subscription_plans WHERE name = 'jobseeker_premium';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'ai_assistance', 'AI Job Assistance', 'true', TRUE, 'features', 5 
FROM subscription_plans WHERE name = 'jobseeker_premium';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'priority_support', 'Priority Support', 'true', TRUE, 'support', 6 
FROM subscription_plans WHERE name = 'jobseeker_premium';

-- Unlimited Job Seeker Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_unlimited, feature_category, display_order) 
SELECT id, 'job_portals', 'Job Portal Access', 'unlimited', TRUE, 'limits', 1 
FROM subscription_plans WHERE name = 'jobseeker_unlimited';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_unlimited, feature_category, display_order) 
SELECT id, 'jobs_per_month', 'Jobs per Month', 'unlimited', TRUE, 'limits', 2 
FROM subscription_plans WHERE name = 'jobseeker_unlimited';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'resume_builder', 'Resume Builder', 'true', TRUE, 'features', 3 
FROM subscription_plans WHERE name = 'jobseeker_unlimited';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'interview_prep', 'Interview Preparation', 'true', TRUE, 'features', 4 
FROM subscription_plans WHERE name = 'jobseeker_unlimited';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'ai_assistance', 'AI Job Assistance', 'true', TRUE, 'features', 5 
FROM subscription_plans WHERE name = 'jobseeker_unlimited';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'dedicated_manager', 'Dedicated Account Manager', 'true', TRUE, 'support', 6 
FROM subscription_plans WHERE name = 'jobseeker_unlimited';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'phone_support', 'Phone Support', 'true', TRUE, 'support', 7 
FROM subscription_plans WHERE name = 'jobseeker_unlimited';

-- Add some features for consultancy plans as well
-- Starter Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_numeric, feature_category, display_order) 
SELECT id, 'job_postings', 'Job Postings per Month', '5', TRUE, 'limits', 1 
FROM subscription_plans WHERE name = 'starter';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'basic_analytics', 'Basic Analytics', 'true', TRUE, 'features', 2 
FROM subscription_plans WHERE name = 'starter';

-- Professional Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_numeric, feature_category, display_order) 
SELECT id, 'job_postings', 'Job Postings per Month', '25', TRUE, 'limits', 1 
FROM subscription_plans WHERE name = 'professional';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'advanced_analytics', 'Advanced Analytics', 'true', TRUE, 'features', 2 
FROM subscription_plans WHERE name = 'professional';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'candidate_database', 'Candidate Database Access', 'true', TRUE, 'features', 3 
FROM subscription_plans WHERE name = 'professional';

-- Enterprise Plan Features
INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_unlimited, feature_category, display_order) 
SELECT id, 'job_postings', 'Job Postings per Month', 'unlimited', TRUE, 'limits', 1 
FROM subscription_plans WHERE name = 'enterprise';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'advanced_analytics', 'Advanced Analytics', 'true', TRUE, 'features', 2 
FROM subscription_plans WHERE name = 'enterprise';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'candidate_database', 'Candidate Database Access', 'true', TRUE, 'features', 3 
FROM subscription_plans WHERE name = 'enterprise';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'api_access', 'API Access', 'true', TRUE, 'features', 4 
FROM subscription_plans WHERE name = 'enterprise';

INSERT IGNORE INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean, feature_category, display_order) 
SELECT id, 'dedicated_manager', 'Dedicated Account Manager', 'true', TRUE, 'support', 5 
FROM subscription_plans WHERE name = 'enterprise';

COMMIT;

-- Verify the data
SELECT sp.display_name, sp.plan_type, COUNT(sf.id) as feature_count
FROM subscription_plans sp 
LEFT JOIN subscription_features sf ON sp.id = sf.plan_id 
GROUP BY sp.id, sp.display_name, sp.plan_type
ORDER BY sp.plan_type, sp.sort_order;