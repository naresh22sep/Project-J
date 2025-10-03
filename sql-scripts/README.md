# SQL Scripts Directory

This directory contains all SQL scripts used for database setup, verification, and fixes.

## File Categories

### Permission & Role Management
- `add_missing_permissions.sql` - Adds missing permissions for menu items
- `check_missing_permissions.sql` - Verification script for missing permissions
- `verify_permissions.sql` - Comprehensive permissions verification
- `fix_missing_list_permissions.sql` - Fixes missing list permissions

### Security System
- `fix_security_logs_schema.sql` - Fixes security_logs table ENUM values
- `fix_security_logs_corrected.sql` - Corrected security logs schema fix
- `verify_security_logs_fix.sql` - Verification for security logs fix
- `check_security_system.sql` - Security system verification

### CRUD Verification
- `verify_crud_permissions.sql` - Verifies CRUD permissions for all resources
- `crud_audit_report.sql` - Comprehensive CRUD audit report

### Data Setup
- `job_data_it_ites.sql` - IT/ITES industry job data setup
- `location_data_usa_canada.sql` - Location data for USA and Canada

## Usage

These scripts are typically run during:
- Initial setup and configuration
- Debugging permission issues
- Verifying system integrity
- Adding new features and permissions

## Database Connection

Most scripts expect connection to the `jobhunter_fresh` database with proper credentials.