-- =====================================================
-- VERIFY PERMISSION ASSIGNMENTS AND TEST ACCESS
-- =====================================================

USE jobhunter_fresh;

-- Show detailed role permission assignments
SELECT 'DETAILED ROLE PERMISSIONS:' as info;
SELECT 
    r.name as role_name,
    p.resource,
    GROUP_CONCAT(p.action ORDER BY p.action SEPARATOR ', ') as permissions
FROM roles r
JOIN role_permissions rp ON r.id = rp.role_id
JOIN permissions p ON rp.permission_id = p.id
WHERE r.name IN ('superadmin', 'admin')
GROUP BY r.name, p.resource
ORDER BY r.name, p.resource;

-- Check if there are any menu items without proper permissions by checking superadmin routes
SELECT 'MENU COVERAGE CHECK:' as info;
SELECT 
    'All Job Data Management items' as menu_section,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'industry' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as industry_types,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'skill' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as skills,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'experience' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as experience_levels,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'job_role' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as job_roles,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'company_type' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as company_types,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'job_type' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as job_types
FROM permissions p;

SELECT 'LOCATION MANAGEMENT COVERAGE:' as info;
SELECT 
    'All Location Management items' as menu_section,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'country' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as countries,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'state' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as states,
    CASE 
        WHEN COUNT(CASE WHEN p.resource = 'city' THEN 1 END) >= 4 THEN '✅ Covered'
        ELSE '❌ Missing'
    END as cities
FROM permissions p;

-- Show role assignment summary for current users
SELECT 'USER ROLE ASSIGNMENTS:' as info;
SELECT 
    au.username,
    GROUP_CONCAT(r.name ORDER BY r.name SEPARATOR ', ') as roles,
    COUNT(DISTINCT p.id) as total_permissions
FROM auth_users au
LEFT JOIN user_roles ur ON au.id = ur.user_id AND ur.is_active = 1
LEFT JOIN roles r ON ur.role_id = r.id
LEFT JOIN role_permissions rp ON r.id = rp.role_id
LEFT JOIN permissions p ON rp.permission_id = p.id
GROUP BY au.id, au.username
ORDER BY au.username;

-- Test specific permission checks for important menu items
SELECT 'PERMISSION TEST FOR MENU ITEMS:' as info;
SELECT 
    permission_name,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM role_permissions rp 
            JOIN roles r ON rp.role_id = r.id 
            WHERE r.name = 'superadmin' AND rp.permission_id = p.id
        ) THEN '✅ SuperAdmin has access'
        ELSE '❌ SuperAdmin missing access'
    END as superadmin_access,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM role_permissions rp 
            JOIN roles r ON rp.role_id = r.id 
            WHERE r.name = 'admin' AND rp.permission_id = p.id
        ) THEN '✅ Admin has access'
        ELSE '❌ Admin missing access'
    END as admin_access
FROM (
    SELECT 'industry.list' as permission_name, id FROM permissions WHERE name = 'industry.list'
    UNION ALL SELECT 'skill.list', id FROM permissions WHERE name = 'skill.list'
    UNION ALL SELECT 'job_role.list', id FROM permissions WHERE name = 'job_role.list'
    UNION ALL SELECT 'country.list', id FROM permissions WHERE name = 'country.list'
    UNION ALL SELECT 'city.list', id FROM permissions WHERE name = 'city.list'
    UNION ALL SELECT 'job_portal.list', id FROM permissions WHERE name = 'job_portal.list'
    UNION ALL SELECT 'security.read', id FROM permissions WHERE name = 'security.read'
) test_perms
JOIN permissions p ON test_perms.id = p.id;

SELECT 'Permission system is now fully configured!' as final_status;