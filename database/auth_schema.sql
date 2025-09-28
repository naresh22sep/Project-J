-- =====================================================
-- JobHunter Platform - Authentication & Authorization Schema
-- Created: September 28, 2025
-- Purpose: Complete ACL, JWT, and Subscription Management System
-- =====================================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS user_permissions;
DROP TABLE IF EXISTS role_permissions;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS subscription_features;
DROP TABLE IF EXISTS user_subscriptions;
DROP TABLE IF EXISTS subscription_plans;
DROP TABLE IF EXISTS jwt_blacklist;
DROP TABLE IF EXISTS security_logs;
DROP TABLE IF EXISTS csrf_tokens;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;

-- =====================================================
-- USERS TABLE - Core user management
-- =====================================================
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires DATETIME,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    last_login DATETIME,
    login_attempts INT DEFAULT 0,
    account_locked_until DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_users_email (email),
    INDEX idx_users_username (username),
    INDEX idx_users_uuid (uuid),
    INDEX idx_users_active (is_active)
);

-- =====================================================
-- ROLES TABLE - User roles management
-- =====================================================
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(150) NOT NULL,
    description TEXT,
    level INT NOT NULL DEFAULT 0,
    is_system_role BOOLEAN DEFAULT FALSE,
    permissions_json JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_roles_name (name),
    INDEX idx_roles_level (level)
);

-- =====================================================
-- USER ROLES TABLE - Many-to-many relationship
-- =====================================================
CREATE TABLE user_roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_by INT,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL,
    
    UNIQUE KEY unique_user_role (user_id, role_id),
    INDEX idx_user_roles_user (user_id),
    INDEX idx_user_roles_role (role_id)
);

-- =====================================================
-- PERMISSIONS TABLE - Granular permissions
-- =====================================================
CREATE TABLE permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL UNIQUE,
    display_name VARCHAR(200) NOT NULL,
    description TEXT,
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    conditions_json JSON,
    is_system_permission BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_permissions_resource (resource),
    INDEX idx_permissions_action (action),
    INDEX idx_permissions_name (name)
);

-- =====================================================
-- ROLE PERMISSIONS TABLE - Role-based permissions
-- =====================================================
CREATE TABLE role_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    granted_by INT,
    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    FOREIGN KEY (granted_by) REFERENCES users(id) ON DELETE SET NULL,
    
    UNIQUE KEY unique_role_permission (role_id, permission_id),
    INDEX idx_role_permissions_role (role_id),
    INDEX idx_role_permissions_permission (permission_id)
);

-- =====================================================
-- USER PERMISSIONS TABLE - Direct user permissions (overrides)
-- =====================================================
CREATE TABLE user_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    permission_id INT NOT NULL,
    granted BOOLEAN DEFAULT TRUE,
    granted_by INT,
    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    reason TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    FOREIGN KEY (granted_by) REFERENCES users(id) ON DELETE SET NULL,
    
    UNIQUE KEY unique_user_permission (user_id, permission_id),
    INDEX idx_user_permissions_user (user_id),
    INDEX idx_user_permissions_permission (permission_id)
);

-- =====================================================
-- SUBSCRIPTION PLANS TABLE - Pricing tiers
-- =====================================================
CREATE TABLE subscription_plans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(150) NOT NULL,
    description TEXT,
    price_monthly DECIMAL(10,2) DEFAULT 0.00,
    price_yearly DECIMAL(10,2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    max_users INT DEFAULT 1,
    max_jobs INT DEFAULT 0,
    max_applications INT DEFAULT 0,
    storage_limit_gb INT DEFAULT 1,
    api_rate_limit INT DEFAULT 100,
    features_json JSON,
    is_popular BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_subscription_plans_active (is_active),
    INDEX idx_subscription_plans_name (name)
);

-- =====================================================
-- USER SUBSCRIPTIONS TABLE - User subscription management
-- =====================================================
CREATE TABLE user_subscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    plan_id INT NOT NULL,
    status ENUM('active', 'expired', 'cancelled', 'suspended', 'pending') DEFAULT 'pending',
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    cancelled_at DATETIME,
    billing_cycle ENUM('monthly', 'yearly', 'lifetime') DEFAULT 'monthly',
    payment_method VARCHAR(50),
    payment_gateway VARCHAR(50),
    gateway_subscription_id VARCHAR(255),
    last_payment_date DATETIME,
    next_payment_date DATETIME,
    auto_renew BOOLEAN DEFAULT TRUE,
    usage_stats_json JSON,
    metadata_json JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(id) ON DELETE RESTRICT,
    
    INDEX idx_user_subscriptions_user (user_id),
    INDEX idx_user_subscriptions_status (status),
    INDEX idx_user_subscriptions_expires (expires_at)
);

-- =====================================================
-- SUBSCRIPTION FEATURES TABLE - Feature access control
-- =====================================================
CREATE TABLE subscription_features (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plan_id INT NOT NULL,
    feature_key VARCHAR(150) NOT NULL,
    feature_name VARCHAR(200) NOT NULL,
    feature_value TEXT,
    is_boolean BOOLEAN DEFAULT FALSE,
    is_numeric BOOLEAN DEFAULT FALSE,
    is_unlimited BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_plan_feature (plan_id, feature_key),
    INDEX idx_subscription_features_plan (plan_id),
    INDEX idx_subscription_features_key (feature_key)
);

-- =====================================================
-- JWT BLACKLIST TABLE - Token management
-- =====================================================
CREATE TABLE jwt_blacklist (
    id INT PRIMARY KEY AUTO_INCREMENT,
    token_jti VARCHAR(255) NOT NULL UNIQUE,
    user_id INT,
    token_type ENUM('access', 'refresh') DEFAULT 'access',
    expires_at DATETIME NOT NULL,
    blacklisted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(255),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_jwt_blacklist_jti (token_jti),
    INDEX idx_jwt_blacklist_expires (expires_at),
    INDEX idx_jwt_blacklist_user (user_id)
);

-- =====================================================
-- CSRF TOKENS TABLE - CSRF protection
-- =====================================================
CREATE TABLE csrf_tokens (
    id INT PRIMARY KEY AUTO_INCREMENT,
    token VARCHAR(255) NOT NULL UNIQUE,
    user_id INT,
    session_id VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    used_at DATETIME,
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_csrf_tokens_token (token),
    INDEX idx_csrf_tokens_expires (expires_at),
    INDEX idx_csrf_tokens_user (user_id)
);

-- =====================================================
-- SECURITY LOGS TABLE - Security audit trail
-- =====================================================
CREATE TABLE security_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    event_type ENUM(
        'login_success', 'login_failed', 'logout', 'password_reset', 
        'permission_granted', 'permission_revoked', 'role_assigned', 
        'role_removed', 'account_locked', 'account_unlocked',
        'subscription_changed', 'suspicious_activity', 'xss_attempt',
        'csrf_violation', 'rate_limit_exceeded', 'unauthorized_access'
    ) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    details_json JSON,
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    resolved BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_security_logs_user (user_id),
    INDEX idx_security_logs_event (event_type),
    INDEX idx_security_logs_severity (severity),
    INDEX idx_security_logs_created (created_at)
);

-- =====================================================
-- INSERT DEFAULT DATA
-- =====================================================

-- Insert default roles
INSERT INTO roles (name, display_name, description, level, is_system_role) VALUES
('superadmin', 'Super Administrator', 'Full system access with all privileges', 100, TRUE),
('admin', 'Administrator', 'Administrative access to manage users and content', 80, TRUE),
('consultancy', 'Consultancy', 'Access to consultancy features and job postings', 60, TRUE),
('jobseeker', 'Job Seeker', 'Access to job search and application features', 40, TRUE),
('guest', 'Guest', 'Limited read-only access', 10, TRUE);

-- Insert default permissions
INSERT INTO permissions (name, display_name, description, resource, action, is_system_permission) VALUES
-- User Management
('users.view', 'View Users', 'View user profiles and information', 'users', 'view', TRUE),
('users.create', 'Create Users', 'Create new user accounts', 'users', 'create', TRUE),
('users.update', 'Update Users', 'Modify user information', 'users', 'update', TRUE),
('users.delete', 'Delete Users', 'Delete user accounts', 'users', 'delete', TRUE),
('users.manage_roles', 'Manage User Roles', 'Assign and remove user roles', 'users', 'manage_roles', TRUE),
('users.manage_permissions', 'Manage User Permissions', 'Grant and revoke user permissions', 'users', 'manage_permissions', TRUE),

-- Role Management
('roles.view', 'View Roles', 'View system roles', 'roles', 'view', TRUE),
('roles.create', 'Create Roles', 'Create new roles', 'roles', 'create', TRUE),
('roles.update', 'Update Roles', 'Modify role information', 'roles', 'update', TRUE),
('roles.delete', 'Delete Roles', 'Delete roles', 'roles', 'delete', TRUE),

-- Permission Management
('permissions.view', 'View Permissions', 'View system permissions', 'permissions', 'view', TRUE),
('permissions.create', 'Create Permissions', 'Create new permissions', 'permissions', 'create', TRUE),
('permissions.update', 'Update Permissions', 'Modify permissions', 'permissions', 'update', TRUE),
('permissions.delete', 'Delete Permissions', 'Delete permissions', 'permissions', 'delete', TRUE),

-- Subscription Management
('subscriptions.view', 'View Subscriptions', 'View subscription information', 'subscriptions', 'view', TRUE),
('subscriptions.create', 'Create Subscriptions', 'Create subscription plans', 'subscriptions', 'create', TRUE),
('subscriptions.update', 'Update Subscriptions', 'Modify subscription plans', 'subscriptions', 'update', TRUE),
('subscriptions.delete', 'Delete Subscriptions', 'Delete subscription plans', 'subscriptions', 'delete', TRUE),
('subscriptions.manage', 'Manage User Subscriptions', 'Manage user subscription assignments', 'subscriptions', 'manage', TRUE),

-- Job Management
('jobs.view', 'View Jobs', 'View job postings', 'jobs', 'view', TRUE),
('jobs.create', 'Create Jobs', 'Create new job postings', 'jobs', 'create', TRUE),
('jobs.update', 'Update Jobs', 'Modify job postings', 'jobs', 'update', TRUE),
('jobs.delete', 'Delete Jobs', 'Delete job postings', 'jobs', 'delete', TRUE),

-- System Management
('system.logs', 'View System Logs', 'Access system and security logs', 'system', 'logs', TRUE),
('system.settings', 'System Settings', 'Modify system configuration', 'system', 'settings', TRUE),
('system.maintenance', 'System Maintenance', 'Perform system maintenance tasks', 'system', 'maintenance', TRUE);

-- Assign permissions to SuperAdmin role
INSERT INTO role_permissions (role_id, permission_id, granted_by)
SELECT 
    (SELECT id FROM roles WHERE name = 'superadmin') as role_id,
    id as permission_id,
    NULL as granted_by
FROM permissions;

-- Assign basic permissions to Admin role
INSERT INTO role_permissions (role_id, permission_id, granted_by)
SELECT 
    (SELECT id FROM roles WHERE name = 'admin') as role_id,
    id as permission_id,
    NULL as granted_by
FROM permissions 
WHERE name IN (
    'users.view', 'users.create', 'users.update', 'users.manage_roles',
    'jobs.view', 'jobs.create', 'jobs.update', 'jobs.delete',
    'subscriptions.view'
);

-- Assign permissions to Consultancy role
INSERT INTO role_permissions (role_id, permission_id, granted_by)
SELECT 
    (SELECT id FROM roles WHERE name = 'consultancy') as role_id,
    id as permission_id,
    NULL as granted_by
FROM permissions 
WHERE name IN (
    'jobs.view', 'jobs.create', 'jobs.update', 'jobs.delete',
    'users.view'
);

-- Assign permissions to Job Seeker role
INSERT INTO role_permissions (role_id, permission_id, granted_by)
SELECT 
    (SELECT id FROM roles WHERE name = 'jobseeker') as role_id,
    id as permission_id,
    NULL as granted_by
FROM permissions 
WHERE name IN ('jobs.view');

-- Insert subscription plans
INSERT INTO subscription_plans (
    name, display_name, description, 
    price_monthly, price_yearly, 
    max_users, max_jobs, max_applications, 
    storage_limit_gb, api_rate_limit, 
    features_json, is_popular, sort_order
) VALUES
-- Free Plan
(
    'starter', 'Starter Plan', 'Perfect for getting started with basic job hunting features',
    0.00, 0.00,
    1, 5, 10,
    1, 50,
    '{"basic_search": true, "email_alerts": false, "premium_support": false, "analytics": false}',
    FALSE, 1
),
-- Professional Plan (Bronze equivalent)
(
    'professional', 'Professional Plan', 'Advanced features for serious job seekers and small consultancies',
    19.99, 199.99,
    5, 25, 100,
    10, 200,
    '{"basic_search": true, "email_alerts": true, "premium_support": false, "analytics": true, "custom_branding": false}',
    FALSE, 2
),
-- Business Plan (Silver equivalent)  
(
    'business', 'Business Plan', 'Comprehensive solution for growing consultancies and teams',
    49.99, 499.99,
    20, 100, 500,
    50, 500,
    '{"basic_search": true, "email_alerts": true, "premium_support": true, "analytics": true, "custom_branding": true, "api_access": true}',
    TRUE, 3
),
-- Enterprise Plan (Gold equivalent)
(
    'enterprise', 'Enterprise Plan', 'Full-featured platform for large organizations with unlimited access',
    99.99, 999.99,
    -1, -1, -1,
    -1, 1000,
    '{"basic_search": true, "email_alerts": true, "premium_support": true, "analytics": true, "custom_branding": true, "api_access": true, "white_label": true, "dedicated_support": true}',
    FALSE, 4
);

-- Insert subscription features
INSERT INTO subscription_features (plan_id, feature_key, feature_name, feature_value, is_boolean) VALUES
-- Starter Plan Features
((SELECT id FROM subscription_plans WHERE name = 'starter'), 'job_alerts', 'Email Job Alerts', 'false', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'starter'), 'profile_views', 'Profile View Analytics', 'false', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'starter'), 'priority_support', 'Priority Support', 'false', TRUE),

-- Professional Plan Features
((SELECT id FROM subscription_plans WHERE name = 'professional'), 'job_alerts', 'Email Job Alerts', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'professional'), 'profile_views', 'Profile View Analytics', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'professional'), 'priority_support', 'Priority Support', 'false', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'professional'), 'advanced_search', 'Advanced Search Filters', 'true', TRUE),

-- Business Plan Features
((SELECT id FROM subscription_plans WHERE name = 'business'), 'job_alerts', 'Email Job Alerts', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'business'), 'profile_views', 'Profile View Analytics', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'business'), 'priority_support', 'Priority Support', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'business'), 'advanced_search', 'Advanced Search Filters', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'business'), 'team_management', 'Team Management', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'business'), 'custom_branding', 'Custom Branding', 'true', TRUE),

-- Enterprise Plan Features
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'job_alerts', 'Email Job Alerts', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'profile_views', 'Profile View Analytics', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'priority_support', 'Priority Support', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'advanced_search', 'Advanced Search Filters', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'team_management', 'Team Management', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'custom_branding', 'Custom Branding', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'white_label', 'White Label Solution', 'true', TRUE),
((SELECT id FROM subscription_plans WHERE name = 'enterprise'), 'dedicated_manager', 'Dedicated Account Manager', 'true', TRUE);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Additional performance indexes
CREATE INDEX idx_users_last_login ON users(last_login);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_user_subscriptions_expires_status ON user_subscriptions(expires_at, status);
CREATE INDEX idx_jwt_blacklist_expires_type ON jwt_blacklist(expires_at, token_type);
CREATE INDEX idx_security_logs_severity_created ON security_logs(severity, created_at);

-- =====================================================
-- CLEANUP PROCEDURES
-- =====================================================

DELIMITER //

-- Procedure to cleanup expired JWT tokens
CREATE PROCEDURE CleanupExpiredTokens()
BEGIN
    DELETE FROM jwt_blacklist WHERE expires_at < NOW();
    DELETE FROM csrf_tokens WHERE expires_at < NOW();
END //

-- Procedure to cleanup old security logs (older than 1 year)
CREATE PROCEDURE CleanupOldSecurityLogs()
BEGIN
    DELETE FROM security_logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR);
END //

DELIMITER ;

-- =====================================================
-- VIEWS FOR EASY DATA ACCESS
-- =====================================================

-- User with roles view
CREATE VIEW user_roles_view AS
SELECT 
    u.id as user_id,
    u.username,
    u.email,
    u.is_active,
    r.name as role_name,
    r.display_name as role_display_name,
    r.level as role_level,
    ur.assigned_at,
    ur.expires_at,
    ur.is_active as role_is_active
FROM users u
LEFT JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = TRUE
LEFT JOIN roles r ON ur.role_id = r.id;

-- User permissions view  
CREATE VIEW user_permissions_view AS
SELECT DISTINCT
    u.id as user_id,
    u.username,
    p.name as permission_name,
    p.display_name as permission_display_name,
    p.resource,
    p.action,
    'role' as permission_source,
    r.name as source_name
FROM users u
JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = TRUE
JOIN roles r ON ur.role_id = r.id  
JOIN role_permissions rp ON r.id = rp.role_id
JOIN permissions p ON rp.permission_id = p.id

UNION ALL

SELECT 
    u.id as user_id,
    u.username,
    p.name as permission_name,
    p.display_name as permission_display_name,
    p.resource,
    p.action,
    'direct' as permission_source,
    'user_override' as source_name
FROM users u
JOIN user_permissions up ON u.id = up.user_id AND up.granted = TRUE
JOIN permissions p ON up.permission_id = p.id;

-- Active subscriptions view
CREATE VIEW active_subscriptions_view AS
SELECT 
    us.user_id,
    u.username,
    u.email,
    sp.name as plan_name,
    sp.display_name as plan_display_name,
    us.status,
    us.started_at,
    us.expires_at,
    us.billing_cycle,
    sp.price_monthly,
    sp.price_yearly
FROM user_subscriptions us
JOIN users u ON us.user_id = u.id
JOIN subscription_plans sp ON us.plan_id = sp.id
WHERE us.status = 'active' AND (us.expires_at IS NULL OR us.expires_at > NOW());

-- =====================================================
-- TRIGGERS FOR AUDIT TRAIL
-- =====================================================

DELIMITER //

-- Trigger for user role changes
CREATE TRIGGER tr_user_roles_audit 
AFTER INSERT ON user_roles
FOR EACH ROW
BEGIN
    INSERT INTO security_logs (user_id, event_type, details_json, severity)
    VALUES (
        NEW.user_id, 
        'role_assigned',
        JSON_OBJECT(
            'role_id', NEW.role_id,
            'assigned_by', NEW.assigned_by,
            'expires_at', NEW.expires_at
        ),
        'medium'
    );
END //

-- Trigger for permission changes
CREATE TRIGGER tr_user_permissions_audit 
AFTER INSERT ON user_permissions
FOR EACH ROW
BEGIN
    INSERT INTO security_logs (user_id, event_type, details_json, severity)
    VALUES (
        NEW.user_id, 
        IF(NEW.granted = TRUE, 'permission_granted', 'permission_revoked'),
        JSON_OBJECT(
            'permission_id', NEW.permission_id,
            'granted_by', NEW.granted_by,
            'reason', NEW.reason
        ),
        'high'
    );
END //

DELIMITER ;

-- =====================================================
-- END OF SCHEMA
-- =====================================================

-- Summary
SELECT 'Authentication & Authorization Schema Created Successfully!' as status;
SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema = DATABASE();
SELECT COUNT(*) as total_roles FROM roles;
SELECT COUNT(*) as total_permissions FROM permissions;
SELECT COUNT(*) as total_subscription_plans FROM subscription_plans;