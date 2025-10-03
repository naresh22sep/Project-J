-- =====================================================
-- ADDITIONAL SECURITY SYSTEM CHECKS
-- =====================================================

USE jobhunter_fresh;

-- Check if there are any other ENUM columns that might need updates
SELECT 'CHECKING OTHER ENUM COLUMNS:' as info;
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    COLUMN_TYPE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'jobhunter_fresh' 
AND DATA_TYPE = 'enum'
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Check for any other potential truncation issues in security-related tables
SELECT 'CHECKING VARCHAR COLUMN SIZES:' as info;
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'jobhunter_fresh' 
AND TABLE_NAME IN ('security_logs', 'auth_users', 'auth_roles', 'auth_permissions')
AND DATA_TYPE IN ('varchar', 'char')
AND CHARACTER_MAXIMUM_LENGTH < 50
ORDER BY TABLE_NAME, CHARACTER_MAXIMUM_LENGTH;

-- Check recent security logs to see what event types are being used
SELECT 'RECENT SECURITY LOG ACTIVITY:' as info;
SELECT 
    event_type,
    COUNT(*) as count,
    MAX(created_at) as last_occurrence
FROM security_logs 
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY)
GROUP BY event_type
ORDER BY count DESC;

-- Show security logs table indexes
SELECT 'SECURITY_LOGS INDEXES:' as info;
SHOW INDEX FROM security_logs;

SELECT 'Security system schema analysis complete!' as final_status;