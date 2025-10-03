-- =====================================================
-- COMPREHENSIVE CRUD AND PERMISSIONS VERIFICATION
-- =====================================================

USE jobhunter_fresh;

-- 1. Check all current permissions and their CRUD coverage
SELECT 'CRUD PERMISSIONS COVERAGE BY RESOURCE:' as info;
SELECT 
    resource,
    COUNT(*) as total_permissions,
    SUM(CASE WHEN action = 'create' THEN 1 ELSE 0 END) as has_create,
    SUM(CASE WHEN action = 'read' THEN 1 ELSE 0 END) as has_read,
    SUM(CASE WHEN action = 'update' THEN 1 ELSE 0 END) as has_update,
    SUM(CASE WHEN action = 'delete' THEN 1 ELSE 0 END) as has_delete,
    SUM(CASE WHEN action = 'list' THEN 1 ELSE 0 END) as has_list,
    CASE 
        WHEN SUM(CASE WHEN action IN ('create', 'read', 'update', 'delete', 'list') THEN 1 ELSE 0 END) >= 4 
        THEN '✅ Complete CRUD'
        ELSE '❌ Incomplete CRUD'
    END as crud_status
FROM permissions 
GROUP BY resource
ORDER BY resource;

-- 2. Check specific menu items from admin layout
SELECT 'MENU ITEM PERMISSION STATUS:' as info;
SELECT 
    menu_item,
    expected_resource,
    CASE 
        WHEN EXISTS (SELECT 1 FROM permissions WHERE resource = expected_resource AND action = 'create') THEN '✅'
        ELSE '❌'
    END as create_perm,
    CASE 
        WHEN EXISTS (SELECT 1 FROM permissions WHERE resource = expected_resource AND action = 'read') THEN '✅'
        ELSE '❌'
    END as read_perm,
    CASE 
        WHEN EXISTS (SELECT 1 FROM permissions WHERE resource = expected_resource AND action = 'update') THEN '✅'
        ELSE '❌'
    END as update_perm,
    CASE 
        WHEN EXISTS (SELECT 1 FROM permissions WHERE resource = expected_resource AND action = 'delete') THEN '✅'
        ELSE '❌'
    END as delete_perm,
    CASE 
        WHEN EXISTS (SELECT 1 FROM permissions WHERE resource = expected_resource AND action = 'list') THEN '✅'
        ELSE '❌'
    END as list_perm
FROM (
    SELECT 'Industry Types' as menu_item, 'industry' as expected_resource
    UNION ALL SELECT 'Skills', 'skill'
    UNION ALL SELECT 'Experience Levels', 'experience'
    UNION ALL SELECT 'Job Roles', 'job_role'
    UNION ALL SELECT 'Company Types', 'company_type'
    UNION ALL SELECT 'Job Types', 'job_type'
    UNION ALL SELECT 'Countries', 'country'
    UNION ALL SELECT 'States', 'state'
    UNION ALL SELECT 'Cities', 'city'
    UNION ALL SELECT 'Job Portals', 'job_portal'
    UNION ALL SELECT 'Users Management', 'user'
    UNION ALL SELECT 'Roles Management', 'role'
    UNION ALL SELECT 'Permissions Management', 'permission'
    UNION ALL SELECT 'Subscriptions', 'subscription'
    UNION ALL SELECT 'Security Logs', 'security'
    UNION ALL SELECT 'System Management', 'system'
) menu_items;

-- 3. Check role assignments for complete access
SELECT 'ROLE ACCESS VERIFICATION:' as info;
SELECT 
    r.name as role_name,
    COUNT(DISTINCT p.resource) as resources_accessible,
    COUNT(rp.permission_id) as total_permissions,
    GROUP_CONCAT(DISTINCT p.resource ORDER BY p.resource SEPARATOR ', ') as accessible_resources
FROM roles r
LEFT JOIN role_permissions rp ON r.id = rp.role_id
LEFT JOIN permissions p ON rp.permission_id = p.id
WHERE r.name IN ('superadmin', 'admin')
GROUP BY r.id, r.name
ORDER BY r.name;

-- 4. Find missing CRUD operations
SELECT 'MISSING CRUD OPERATIONS:' as info;
SELECT 
    all_resources.resource,
    all_resources.action,
    'Missing Permission' as status
FROM (
    SELECT DISTINCT p.resource, required_actions.action
    FROM permissions p
    CROSS JOIN (
        SELECT 'create' as action
        UNION ALL SELECT 'read'
        UNION ALL SELECT 'update' 
        UNION ALL SELECT 'delete'
        UNION ALL SELECT 'list'
    ) required_actions
    WHERE p.resource NOT IN ('security', 'system') -- These have different action patterns
) all_resources
LEFT JOIN permissions existing_perms ON all_resources.resource = existing_perms.resource 
    AND all_resources.action = existing_perms.action
WHERE existing_perms.id IS NULL
ORDER BY all_resources.resource, all_resources.action;

-- 5. Check for resources that have incomplete CRUD
SELECT 'RESOURCES WITH INCOMPLETE CRUD:' as info;
SELECT 
    resource,
    GROUP_CONCAT(action ORDER BY action SEPARATOR ', ') as available_actions,
    CASE 
        WHEN SUM(CASE WHEN action = 'create' THEN 1 ELSE 0 END) = 0 THEN 'Missing CREATE, '
        ELSE ''
    END +
    CASE 
        WHEN SUM(CASE WHEN action = 'read' THEN 1 ELSE 0 END) = 0 THEN 'Missing READ, '
        ELSE ''
    END +
    CASE 
        WHEN SUM(CASE WHEN action = 'update' THEN 1 ELSE 0 END) = 0 THEN 'Missing UPDATE, '
        ELSE ''
    END +
    CASE 
        WHEN SUM(CASE WHEN action = 'delete' THEN 1 ELSE 0 END) = 0 THEN 'Missing DELETE, '
        ELSE ''
    END +
    CASE 
        WHEN SUM(CASE WHEN action = 'list' THEN 1 ELSE 0 END) = 0 THEN 'Missing LIST'
        ELSE ''
    END as missing_operations
FROM permissions 
WHERE resource NOT IN ('security', 'system') -- Special cases
GROUP BY resource
HAVING COUNT(*) < 5 -- Should have 5 basic CRUD operations
ORDER BY resource;

-- 6. SuperAdmin permission coverage check
SELECT 'SUPERADMIN COMPLETE ACCESS CHECK:' as info;
SELECT 
    p.resource,
    COUNT(*) as permissions_in_resource,
    SUM(CASE WHEN rp.permission_id IS NOT NULL THEN 1 ELSE 0 END) as superadmin_has,
    CASE 
        WHEN COUNT(*) = SUM(CASE WHEN rp.permission_id IS NOT NULL THEN 1 ELSE 0 END) 
        THEN '✅ Complete Access'
        ELSE '❌ Incomplete Access'
    END as access_status
FROM permissions p
LEFT JOIN role_permissions rp ON p.id = rp.permission_id 
    AND rp.role_id = (SELECT id FROM roles WHERE name = 'superadmin')
GROUP BY p.resource
ORDER BY p.resource;

SELECT 'CRUD and Permissions Verification Complete!' as final_status;