-- =====================================================
-- FIX SECURITY LOGS TABLE SCHEMA
-- =====================================================

USE jobhunter_fresh;

-- Check current schema first
SELECT 'CURRENT SECURITY_LOGS SCHEMA:' as info;
DESCRIBE security_logs;

-- Check current column constraints
SELECT 'CURRENT COLUMN DETAILS:' as info;
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    COLUMN_TYPE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'jobhunter_fresh' 
AND TABLE_NAME = 'security_logs' 
ORDER BY ORDINAL_POSITION;

-- Show existing data to understand current usage
SELECT 'EXISTING EVENT TYPES:' as info;
SELECT DISTINCT event_type, LENGTH(event_type) as length 
FROM security_logs 
ORDER BY LENGTH(event_type) DESC 
LIMIT 10;

-- =====================================================
-- FIX THE SCHEMA ISSUES
-- =====================================================

-- Fix event_type column (main issue)
ALTER TABLE security_logs 
MODIFY COLUMN event_type VARCHAR(50) NOT NULL 
COMMENT 'Type of security event (LOGIN_SUCCESS, ROLE_MODIFIED, etc.)';

-- Fix severity column  
ALTER TABLE security_logs 
MODIFY COLUMN severity ENUM('low', 'medium', 'high', 'critical') 
DEFAULT 'low' 
COMMENT 'Security event severity level';

-- Fix user_agent column (can be very long)
ALTER TABLE security_logs 
MODIFY COLUMN user_agent TEXT 
COMMENT 'Browser user agent string';

-- Fix details_json column (ensure it can handle JSON)
ALTER TABLE security_logs 
MODIFY COLUMN details_json JSON 
COMMENT 'Additional event details in JSON format';

-- Fix ip_address column (IPv6 support)
ALTER TABLE security_logs 
MODIFY COLUMN ip_address VARCHAR(45) 
COMMENT 'IP address (supports both IPv4 and IPv6)';

-- Ensure proper indexes exist for performance
CREATE INDEX IF NOT EXISTS idx_security_logs_user_id ON security_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_security_logs_event_type ON security_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_security_logs_created_at ON security_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_security_logs_severity ON security_logs(severity);

-- =====================================================
-- VERIFICATION
-- =====================================================

SELECT 'UPDATED SECURITY_LOGS SCHEMA:' as info;
DESCRIBE security_logs;

-- Show the fixed column details
SELECT 'UPDATED COLUMN DETAILS:' as info;
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    COLUMN_TYPE,
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'jobhunter_fresh' 
AND TABLE_NAME = 'security_logs' 
ORDER BY ORDINAL_POSITION;

-- Show indexes
SELECT 'SECURITY_LOGS INDEXES:' as info;
SHOW INDEX FROM security_logs;

-- Test insert to verify fix
SELECT 'TESTING INSERT WITH ROLE_MODIFIED:' as info;
INSERT INTO security_logs (
    user_id, 
    event_type, 
    ip_address, 
    user_agent, 
    details_json, 
    severity, 
    resolved, 
    created_at
) VALUES (
    999,  -- test user_id
    'ROLE_MODIFIED', 
    '127.0.0.1', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0', 
    '{"role_id": 2, "role_name": "admin", "permissions": ["23", "7", "26", "10", "11", "12", "2", "3", "5"], "test": true}', 
    'medium', 
    0, 
    NOW()
);

-- Verify the test insert worked
SELECT 'TEST INSERT VERIFICATION:' as info;
SELECT * FROM security_logs WHERE user_id = 999 ORDER BY created_at DESC LIMIT 1;

-- Clean up test data
DELETE FROM security_logs WHERE user_id = 999;

SELECT 'Security logs schema fix completed successfully!' as final_status;