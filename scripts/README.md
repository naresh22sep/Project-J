# Scripts Directory

This directory contains utility scripts organized by purpose.

## 📁 database/
Database-related scripts for setup, maintenance, and fixes:
- `add_*.py` - Scripts to add missing data or features
- `check_*.py` - Scripts to validate database state
- `fix_*.py` - Scripts to repair database issues
- `create_*.py` - Scripts to create tables or initial data
- `init_*.py` - Database initialization scripts
- `populate_*.py` - Scripts to populate data
- `cleanup_*.py` - Scripts to clean up duplicates or bad data

## 📁 setup/
Setup and build scripts:
- `*.bat` - Windows batch files for setup and running
- `*.sh` - Unix shell scripts for setup and running
- Migration and testing scripts

## 📄 Root scripts/
Application monitoring and tracking:
- `auto_tracker.py` - Automatic conversation tracking
- `auto_track_current.py` - Current session tracking
- `passive_tracker.py` - Passive monitoring script

## Usage
Run scripts from the project root directory to maintain proper import paths:

```bash
# Database scripts
python scripts/database/init_db.py
python scripts/database/create_job_tables.py

# Setup scripts
scripts/setup/quick_start.bat  # Windows
scripts/setup/setup.sh         # Unix

# Tracking scripts
python scripts/auto_tracker.py
```