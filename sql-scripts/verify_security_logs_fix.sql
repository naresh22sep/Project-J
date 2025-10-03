-- =====================================================
-- VERIFY SECURITY LOGS FIX IS WORKING
-- =====================================================

USE jobhunter_fresh;

-- Show the updated ENUM with ROLE_MODIFIED
SELECT 'UPDATED EVENT_TYPE ENUM:' as info;
SHOW COLUMNS FROM security_logs WHERE Field = 'event_type';

-- Show existing valid user_ids for testing
SELECT 'VALID USER IDS FOR TESTING:' as info;
SELECT id, username FROM auth_users LIMIT 5;

-- Test with a real user_id (get the first one)
SET @test_user_id = (SELECT id FROM auth_users LIMIT 1);

-- Test insert with ROLE_MODIFIED using a real user_id
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
    @test_user_id,
    'ROLE_MODIFIED', 
    '127.0.0.1', 
    'Test User Agent', 
    '{"role_id": 2, "role_name": "admin", "test_fix": true}', 
    'medium', 
    0, 
    NOW()
);

-- Verify the test worked
SELECT 'ROLE_MODIFIED TEST SUCCESS:' as info;
SELECT 
    sl.id,
    au.username,
    sl.event_type,
    sl.severity,
    sl.details_json,
    sl.created_at
FROM security_logs sl
JOIN auth_users au ON sl.user_id = au.id
WHERE sl.event_type = 'ROLE_MODIFIED' 
AND JSON_EXTRACT(sl.details_json, '$.test_fix') = true
ORDER BY sl.created_at DESC 
LIMIT 1;

-- Clean up test data
DELETE FROM security_logs 
WHERE event_type = 'ROLE_MODIFIED' 
AND JSON_EXTRACT(details_json, '$.test_fix') = true;

SELECT 'ROLE_MODIFIED is now working in security_logs!' as final_status;
SELECT 'Your Python app should no longer get the data truncation error.' as note;