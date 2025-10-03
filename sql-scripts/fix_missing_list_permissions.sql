-- =====================================================
-- ADD MISSING LIST PERMISSIONS
-- =====================================================

USE jobhunter_fresh;

-- Add missing list permissions
INSERT INTO permissions (name, display_name, description, resource, action, is_system_permission) VALUES
('job.list', 'List Jobs', 'List all jobs', 'job', 'list', 0),
('permission.list', 'List Permissions', 'List all permissions', 'permission', 'list', 0),
('role.list', 'List Roles', 'List all roles', 'role', 'list', 0),
('subscription.list', 'List Subscriptions', 'List all subscriptions', 'subscription', 'list', 0)
ON DUPLICATE KEY UPDATE 
    display_name = VALUES(display_name),
    description = VALUES(description);

-- Assign these to SuperAdmin
INSERT INTO role_permissions (role_id, permission_id, granted_by, granted_at)
SELECT 
    (SELECT id FROM roles WHERE name = 'superadmin'),
    id,
    NULL,
    NOW()
FROM permissions 
WHERE name IN ('job.list', 'permission.list', 'role.list', 'subscription.list')
ON DUPLICATE KEY UPDATE granted_at = NOW();

-- Assign list permissions to Admin role too  
INSERT INTO role_permissions (role_id, permission_id, granted_by, granted_at)
SELECT 
    (SELECT id FROM roles WHERE name = 'admin'),
    id,
    NULL,
    NOW()
FROM permissions 
WHERE name IN ('job.list', 'permission.list', 'role.list', 'subscription.list')
ON DUPLICATE KEY UPDATE granted_at = NOW();

SELECT 'Missing list permissions added!' as status;