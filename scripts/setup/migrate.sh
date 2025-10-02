#!/bin/bash

# Migration management script

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Set Flask app
export FLASK_APP=app.py

case "$1" in
    "init")
        echo "Initializing migrations..."
        flask db init
        ;;
    "migrate")
        echo "Creating migration..."
        if [ -z "$2" ]; then
            flask db migrate
        else
            flask db migrate -m "$2"
        fi
        ;;
    "upgrade")
        echo "Applying migrations..."
        flask db upgrade
        ;;
    "downgrade")
        echo "Rolling back migration..."
        flask db downgrade
        ;;
    "history")
        echo "Migration history..."
        flask db history
        ;;
    "current")
        echo "Current migration..."
        flask db current
        ;;
    "reset")
        echo "Resetting database..."
        flask reset-db
        ;;
    *)
        echo "Usage: $0 {init|migrate|upgrade|downgrade|history|current|reset}"
        echo ""
        echo "Commands:"
        echo "  init      - Initialize migration repository"
        echo "  migrate   - Create a new migration"
        echo "  upgrade   - Apply migrations to database"
        echo "  downgrade - Roll back migrations"
        echo "  history   - Show migration history"
        echo "  current   - Show current migration"
        echo "  reset     - Reset database (drop and recreate)"
        exit 1
        ;;
esac