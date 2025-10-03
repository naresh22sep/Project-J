-- Check current permissions vs menu items

USE jobhunter_fresh;

-- Show all current permissions
SELECT 'CURRENT PERMISSIONS IN DATABASE:' as info;
SELECT 
    name as permission_name,
    display_name,
    resource,
    action,
    CASE WHEN is_system_permission = 1 THEN 'Yes' ELSE 'No' END as is_system
FROM permissions 
ORDER BY resource, action;

-- Show permissions by resource category
SELECT 'PERMISSIONS GROUPED BY RESOURCE:' as info;
SELECT 
    resource,
    GROUP_CONCAT(CONCAT(action, ' (', name, ')') ORDER BY action SEPARATOR ', ') as actions
FROM permissions 
GROUP BY resource
ORDER BY resource;

-- Check what menu items are missing permissions
SELECT 'MENU ITEMS THAT NEED PERMISSIONS:' as info;

-- The menu items that should have permissions:
-- Job Data Management:
--   - industry_types (industry.*)
--   - skills (skill.*)  
--   - experience_levels (experience.*)
--   - job_roles (job_role.*)
--   - company_types (company_type.*)
--   - job_types (job_type.*)
-- Location Management:
--   - countries (country.*)
--   - states (state.*)
--   - cities (city.*)
-- Other:
--   - job_portals (job_portal.*)
--   - security_logs (security.*)

-- Check which resources are missing
SELECT 
    'Missing Permission Resources' as category,
    missing_resource
FROM (
    SELECT 'industry' as missing_resource
    UNION SELECT 'skill' 
    UNION SELECT 'experience'
    UNION SELECT 'job_role'
    UNION SELECT 'company_type'
    UNION SELECT 'job_type'
    UNION SELECT 'country'
    UNION SELECT 'state' 
    UNION SELECT 'city'
    UNION SELECT 'job_portal'
) expected
WHERE missing_resource NOT IN (
    SELECT DISTINCT resource FROM permissions
);

-- Count permissions per resource
SELECT 'PERMISSION COUNT BY RESOURCE:' as info;
SELECT 
    resource,
    COUNT(*) as permission_count
FROM permissions 
GROUP BY resource
ORDER BY permission_count DESC, resource;