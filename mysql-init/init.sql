-- MySQL initialization script
-- This script runs when the MySQL container starts for the first time

-- Create additional databases if needed (optional - using same database for all environments)
-- CREATE DATABASE IF NOT EXISTS jobhunter_fresh_prod;

-- Grant permissions to the root user (already has all privileges)
-- Additional users can be created if needed
-- CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'Naresh123';
-- GRANT ALL PRIVILEGES ON jobhunter_fresh.* TO 'appuser'@'%';

FLUSH PRIVILEGES;