#!/bin/bash

# Test Runner Script for Unix/Linux/Mac

echo "🧪 Flask Application Test Runner"
echo "================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables from .env..."
    export $(cat .env | grep -v '#' | xargs)
else
    echo "⚠️  .env file not found. Copy config/.env.example to .env"
fi

echo ""

# Check which test to run
case "$1" in
    "quick")
        echo "🚀 Running quick connection test..."
        python tests/test_connection.py
        ;;
    "database")
        echo "🗄️  Running database tests..."
        python tests/test_database.py
        ;;
    "app")
        echo "🌐 Running application tests..."
        python tests/test_app.py
        ;;
    "all")
        echo "🎯 Running all tests..."
        echo ""
        echo "1. Quick connection test:"
        python tests/test_connection.py
        echo ""
        echo "2. Database tests:"
        python tests/test_database.py
        echo ""
        echo "3. Application tests:"
        python tests/test_app.py
        ;;
    *)
        echo "Usage: $0 {quick|database|app|all}"
        echo ""
        echo "Test options:"
        echo "  quick    - Quick database connection test"
        echo "  database - Comprehensive database tests"
        echo "  app      - Flask application tests"
        echo "  all      - Run all tests"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh quick      # Quick test"
        echo "  ./run_tests.sh all        # All tests"
        exit 1
        ;;
esac

echo ""
echo "🏁 Test run completed!"