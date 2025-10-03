-- =====================================================
-- ADD MISSING PERMISSIONS FOR MENU ITEMS
-- =====================================================

USE jobhunter_fresh;

-- Add missing permissions for Job Data Management menu items
INSERT INTO permissions (name, display_name, description, resource, action, is_system_permission) VALUES

-- Industry Types permissions
('industry.create', 'Create Industry Types', 'Create new industry types', 'industry', 'create', 0),
('industry.read', 'View Industry Types', 'View industry type details', 'industry', 'read', 0),
('industry.update', 'Update Industry Types', 'Update industry types', 'industry', 'update', 0),
('industry.delete', 'Delete Industry Types', 'Delete industry types', 'industry', 'delete', 0),
('industry.list', 'List Industry Types', 'List all industry types', 'industry', 'list', 0),

-- Skills permissions  
('skill.create', 'Create Skills', 'Create new skills', 'skill', 'create', 0),
('skill.read', 'View Skills', 'View skill details', 'skill', 'read', 0),
('skill.update', 'Update Skills', 'Update skills', 'skill', 'update', 0),
('skill.delete', 'Delete Skills', 'Delete skills', 'skill', 'delete', 0),
('skill.list', 'List Skills', 'List all skills', 'skill', 'list', 0),

-- Experience Levels permissions
('experience.create', 'Create Experience Levels', 'Create new experience levels', 'experience', 'create', 0),
('experience.read', 'View Experience Levels', 'View experience level details', 'experience', 'read', 0),
('experience.update', 'Update Experience Levels', 'Update experience levels', 'experience', 'update', 0),
('experience.delete', 'Delete Experience Levels', 'Delete experience levels', 'experience', 'delete', 0),
('experience.list', 'List Experience Levels', 'List all experience levels', 'experience', 'list', 0),

-- Job Roles permissions
('job_role.create', 'Create Job Roles', 'Create new job roles', 'job_role', 'create', 0),
('job_role.read', 'View Job Roles', 'View job role details', 'job_role', 'read', 0),
('job_role.update', 'Update Job Roles', 'Update job roles', 'job_role', 'update', 0),
('job_role.delete', 'Delete Job Roles', 'Delete job roles', 'job_role', 'delete', 0),
('job_role.list', 'List Job Roles', 'List all job roles', 'job_role', 'list', 0),

-- Company Types permissions
('company_type.create', 'Create Company Types', 'Create new company types', 'company_type', 'create', 0),
('company_type.read', 'View Company Types', 'View company type details', 'company_type', 'read', 0),
('company_type.update', 'Update Company Types', 'Update company types', 'company_type', 'update', 0),
('company_type.delete', 'Delete Company Types', 'Delete company types', 'company_type', 'delete', 0),
('company_type.list', 'List Company Types', 'List all company types', 'company_type', 'list', 0),

-- Job Types permissions
('job_type.create', 'Create Job Types', 'Create new job types', 'job_type', 'create', 0),
('job_type.read', 'View Job Types', 'View job type details', 'job_type', 'read', 0),
('job_type.update', 'Update Job Types', 'Update job types', 'job_type', 'update', 0),
('job_type.delete', 'Delete Job Types', 'Delete job types', 'job_type', 'delete', 0),
('job_type.list', 'List Job Types', 'List all job types', 'job_type', 'list', 0),

-- Location Management permissions
-- Countries
('country.create', 'Create Countries', 'Create new countries', 'country', 'create', 0),
('country.read', 'View Countries', 'View country details', 'country', 'read', 0),
('country.update', 'Update Countries', 'Update countries', 'country', 'update', 0),
('country.delete', 'Delete Countries', 'Delete countries', 'country', 'delete', 0),
('country.list', 'List Countries', 'List all countries', 'country', 'list', 0),

-- States
('state.create', 'Create States', 'Create new states/provinces', 'state', 'create', 0),
('state.read', 'View States', 'View state/province details', 'state', 'read', 0),
('state.update', 'Update States', 'Update states/provinces', 'state', 'update', 0),
('state.delete', 'Delete States', 'Delete states/provinces', 'state', 'delete', 0),
('state.list', 'List States', 'List all states/provinces', 'state', 'list', 0),

-- Cities
('city.create', 'Create Cities', 'Create new cities', 'city', 'create', 0),
('city.read', 'View Cities', 'View city details', 'city', 'read', 0),
('city.update', 'Update Cities', 'Update cities', 'city', 'update', 0),
('city.delete', 'Delete Cities', 'Delete cities', 'city', 'delete', 0),
('city.list', 'List Cities', 'List all cities', 'city', 'list', 0),

-- Job Portals permissions
('job_portal.create', 'Create Job Portals', 'Create new job portals', 'job_portal', 'create', 0),
('job_portal.read', 'View Job Portals', 'View job portal details', 'job_portal', 'read', 0),
('job_portal.update', 'Update Job Portals', 'Update job portals', 'job_portal', 'update', 0),
('job_portal.delete', 'Delete Job Portals', 'Delete job portals', 'job_portal', 'delete', 0),
('job_portal.list', 'List Job Portals', 'List all job portals', 'job_portal', 'list', 0)

ON DUPLICATE KEY UPDATE 
    display_name = VALUES(display_name),
    description = VALUES(description);

-- =====================================================
-- ASSIGN NEW PERMISSIONS TO ROLES
-- =====================================================

-- Get role IDs
SET @superadmin_role_id = (SELECT id FROM roles WHERE name = 'superadmin');
SET @admin_role_id = (SELECT id FROM roles WHERE name = 'admin');

-- Assign ALL new permissions to SuperAdmin
INSERT INTO role_permissions (role_id, permission_id, granted_by, granted_at)
SELECT 
    @superadmin_role_id,
    id,
    NULL,
    NOW()
FROM permissions 
WHERE resource IN ('industry', 'skill', 'experience', 'job_role', 'company_type', 'job_type', 'country', 'state', 'city', 'job_portal')
ON DUPLICATE KEY UPDATE granted_at = NOW();

-- Assign READ permissions to Admin role for all new resources
INSERT INTO role_permissions (role_id, permission_id, granted_by, granted_at)
SELECT 
    @admin_role_id,
    id,
    NULL,
    NOW()
FROM permissions 
WHERE resource IN ('industry', 'skill', 'experience', 'job_role', 'company_type', 'job_type', 'country', 'state', 'city', 'job_portal')
AND action IN ('read', 'list')
ON DUPLICATE KEY UPDATE granted_at = NOW();

-- =====================================================
-- VERIFICATION
-- =====================================================

SELECT 'NEW PERMISSIONS ADDED SUCCESSFULLY!' as status;

-- Show all permissions by resource
SELECT 'UPDATED PERMISSIONS BY RESOURCE:' as info;
SELECT 
    resource,
    COUNT(*) as permission_count,
    GROUP_CONCAT(action ORDER BY action SEPARATOR ', ') as actions
FROM permissions 
GROUP BY resource
ORDER BY resource;

-- Show SuperAdmin role permissions count
SELECT 'SUPERADMIN ROLE PERMISSIONS:' as info;
SELECT 
    r.name as role_name,
    COUNT(rp.permission_id) as total_permissions
FROM roles r
LEFT JOIN role_permissions rp ON r.id = rp.role_id
WHERE r.name = 'superadmin'
GROUP BY r.id, r.name;

-- Show Admin role permissions count  
SELECT 'ADMIN ROLE PERMISSIONS:' as info;
SELECT 
    r.name as role_name,
    COUNT(rp.permission_id) as total_permissions
FROM roles r
LEFT JOIN role_permissions rp ON r.id = rp.role_id
WHERE r.name = 'admin'
GROUP BY r.id, r.name;

-- Show new resource permissions
SELECT 'NEW RESOURCE PERMISSIONS:' as info;
SELECT 
    p.resource,
    p.action,
    p.name as permission_name,
    COUNT(rp.role_id) as assigned_to_roles
FROM permissions p
LEFT JOIN role_permissions rp ON p.id = rp.permission_id
WHERE p.resource IN ('industry', 'skill', 'experience', 'job_role', 'company_type', 'job_type', 'country', 'state', 'city', 'job_portal')
GROUP BY p.id, p.resource, p.action, p.name
ORDER BY p.resource, p.action;

SELECT 'All menu items now have proper permissions!' as final_status;