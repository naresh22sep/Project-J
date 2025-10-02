#!/bin/bash

# Setup script for Flask application (Linux/Mac)

echo "Setting up Flask Application..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Copy environment file
echo "Setting up environment configuration..."
cp config/.env.example .env

echo "Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "source venv/bin/activate"
echo ""
echo "To start the application, run:"
echo "python app.py"
echo ""
echo "Don't forget to:"
echo "1. Update database credentials in .env file"
echo "2. Create MySQL database"
echo "3. Run 'flask db init' and 'flask db migrate' for migrations"