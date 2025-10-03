-- =====================================================
-- ROUTE AND CRUD OPERATIONS AUDIT
-- =====================================================

USE jobhunter_fresh;

-- This will help us track which functionalities have complete CRUD support
SELECT 'CRUD FUNCTIONALITY AUDIT REPORT' as report_title;

-- Based on the search results, let's map what exists:
SELECT 'EXISTING ROUTES AND CRUD OPERATIONS:' as section;

-- Create a summary table of what we found
SELECT 
    'Route Analysis' as analysis_type,
    'Functionality' as functionality,
    'List Route' as list_exists,
    'Create Route' as create_exists,
    'Edit Route' as edit_exists,
    'Delete Route' as delete_exists,
    'CRUD Status' as crud_status
UNION ALL

-- Industry Types
SELECT 
    'Audit Result',
    'Industry Types',
    'Yes (industry_types)', 
    'Partial (industry_types/create)',
    'Partial (industry_types/edit)',
    'Not Found',
    'Incomplete - Missing Delete'
UNION ALL

-- Skills  
SELECT 
    'Audit Result',
    'Skills',
    'Yes (/skills)',
    'Yes (/skills/create)',
    'Yes (/skills/<id>/edit)',
    'Yes (/skills/<id>/delete)',
    'Complete CRUD'
UNION ALL

-- Experience Levels
SELECT 
    'Audit Result', 
    'Experience Levels',
    'Yes (/experience_levels)',
    'Partial (experience_levels/create)',
    'Partial (experience_levels/edit)', 
    'Not Found',
    'Incomplete - Missing Delete'
UNION ALL

-- Job Roles
SELECT 
    'Audit Result',
    'Job Roles', 
    'Yes (/job_roles)',
    'Partial (job_roles/create)',
    'Partial (job_roles/edit)',
    'Not Found',
    'Incomplete - Missing Delete'
UNION ALL

-- Company Types
SELECT 
    'Audit Result',
    'Company Types',
    'Yes (/company_types)',
    'Not Found',
    'Not Found',
    'Not Found', 
    'Incomplete - Only List'
UNION ALL

-- Job Types  
SELECT 
    'Audit Result',
    'Job Types',
    'Not Found',
    'Not Found', 
    'Not Found',
    'Not Found',
    'Missing - No CRUD'
UNION ALL

-- Countries
SELECT 
    'Audit Result',
    'Countries',
    'Yes (/countries)',
    'Yes (/countries/create)',
    'Yes (/countries/<id>/edit)',
    'Yes (/countries/<id>/delete)',
    'Complete CRUD'
UNION ALL

-- States
SELECT 
    'Audit Result', 
    'States',
    'Yes (/states)',
    'Yes (/states/create)',
    'Yes (/states/<id>/edit)',
    'Yes (/states/<id>/delete)',
    'Complete CRUD'
UNION ALL

-- Cities
SELECT 
    'Audit Result',
    'Cities', 
    'Yes (/cities)',
    'Yes (/cities/create)',
    'Yes (/cities/<id>/edit)',
    'Yes (/cities/<id>/delete)',
    'Complete CRUD'
UNION ALL

-- Job Portals
SELECT 
    'Audit Result',
    'Job Portals',
    'Yes (/job_portals)',
    'Partial Found',
    'Partial Found', 
    'Partial Found',
    'Needs Verification';

-- Now let's see what needs to be implemented
SELECT '' as spacer;
SELECT 'MISSING CRUD OPERATIONS TO IMPLEMENT:' as section;

SELECT 
    'Priority' as priority,
    'Functionality' as functionality, 
    'Missing Operations' as missing_operations,
    'Impact' as impact
UNION ALL
SELECT 'HIGH', 'Job Types', 'Complete CRUD (List, Create, Edit, Delete)', 'Menu item exists but no functionality'
UNION ALL  
SELECT 'HIGH', 'Company Types', 'Create, Edit, Delete operations', 'Only list view exists'
UNION ALL
SELECT 'MEDIUM', 'Industry Types', 'Delete operation', 'Create/Edit exist, missing Delete'
UNION ALL
SELECT 'MEDIUM', 'Experience Levels', 'Delete operation', 'Create/Edit exist, missing Delete'  
UNION ALL
SELECT 'MEDIUM', 'Job Roles', 'Delete operation', 'Create/Edit exist, missing Delete'
UNION ALL
SELECT 'LOW', 'Job Portals', 'Verify complete CRUD implementation', 'Partial routes found, need verification';

-- Permission coverage summary
SELECT '' as spacer;
SELECT 'PERMISSION COVERAGE SUMMARY:' as section;
SELECT 
    p.resource,
    COUNT(*) as total_permissions,
    SUM(CASE WHEN rp.role_id = (SELECT id FROM roles WHERE name = 'superadmin') THEN 1 ELSE 0 END) as superadmin_assigned,
    SUM(CASE WHEN rp.role_id = (SELECT id FROM roles WHERE name = 'admin') THEN 1 ELSE 0 END) as admin_assigned,
    CASE 
        WHEN COUNT(*) = SUM(CASE WHEN rp.role_id = (SELECT id FROM roles WHERE name = 'superadmin') THEN 1 ELSE 0 END)
        THEN '✅ Full Access'
        ELSE '❌ Partial Access'  
    END as superadmin_status
FROM permissions p
LEFT JOIN role_permissions rp ON p.id = rp.permission_id
WHERE p.resource IN ('industry', 'skill', 'experience', 'job_role', 'company_type', 'job_type', 'country', 'state', 'city', 'job_portal')
GROUP BY p.resource
ORDER BY p.resource;