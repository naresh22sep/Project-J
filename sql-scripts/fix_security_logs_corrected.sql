-- =====================================================
-- FIX SECURITY LOGS TABLE SCHEMA (CORRECTED)
-- =====================================================

USE jobhunter_fresh;

-- Add ROLE_MODIFIED to the existing ENUM
ALTER TABLE security_logs 
MODIFY COLUMN event_type ENUM(
    'LOGIN_SUCCESS',
    'LOGIN_FAILED',
    'LOGOUT',
    'PASSWORD_RESET',
    'PASSWORD_CHANGED',
    'PASSWORD_CHANGE_FAILED',
    'USER_REGISTERED',
    'USER_MODIFIED',
    'PROFILE_UPDATED',
    'PERMISSION_GRANTED',
    'PERMISSION_REVOKED',
    'ROLE_ASSIGNED',
    'ROLE_REMOVED',
    'ROLE_CREATED',
    'ROLE_MODIFIED',  -- Adding this missing value
    'PERMISSION_CREATED',
    'ACCOUNT_LOCKED',
    'ACCOUNT_UNLOCKED',
    'SUBSCRIPTION_CHANGED',
    'SUBSCRIPTION_MODIFIED',
    'SUSPICIOUS_ACTIVITY',
    'XSS_ATTEMPT',
    'CSRF_VIOLATION',
    'RATE_LIMIT_EXCEEDED',
    'UNAUTHORIZED_ACCESS',
    'INVALID_TOKEN',
    'SQL_INJECTION_ATTEMPT',
    'SLOW_REQUEST',
    'ERROR_RESPONSE',
    'DATA_EXPORT',
    'SYSTEM_ERROR',
    'SYSTEM_MAINTENANCE'
) NOT NULL 
COMMENT 'Type of security event';

-- Ensure proper indexes exist for performance (corrected syntax)
CREATE INDEX idx_security_logs_user_id ON security_logs(user_id);
CREATE INDEX idx_security_logs_event_type ON security_logs(event_type);
CREATE INDEX idx_security_logs_created_at ON security_logs(created_at);
CREATE INDEX idx_security_logs_severity ON security_logs(severity);

-- Show the updated ENUM values
SELECT 'UPDATED EVENT_TYPE ENUM:' as info;
SHOW COLUMNS FROM security_logs WHERE Field = 'event_type';

-- Test insert to verify ROLE_MODIFIED now works
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
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 
    '{"role_id": 2, "role_name": "admin", "test": true}', 
    'medium', 
    0, 
    NOW()
);

-- Verify the test insert worked
SELECT 'TEST INSERT VERIFICATION:' as info;
SELECT event_type, user_id, severity, created_at 
FROM security_logs 
WHERE user_id = 999 
ORDER BY created_at DESC 
LIMIT 1;

-- Clean up test data
DELETE FROM security_logs WHERE user_id = 999;

SELECT 'Security logs schema fix completed - ROLE_MODIFIED added!' as final_status;