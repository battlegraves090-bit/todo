#!/bin/bash
# Quick Start Script for Todo Application
# Run this script to set up the project

echo "🚀 Todo App - Quick Setup"
echo "=========================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Create migrations
echo "🗄️  Creating database migrations..."
python manage.py makemigrations

echo "✅ Migrations created"
echo ""

# Apply migrations
echo "🗄️  Applying migrations..."
python manage.py migrate

echo "✅ Migrations applied"
echo ""

# Create superuser
echo "👤 Creating superuser account..."
python manage.py createsuperuser

echo "✅ Superuser created"
echo ""

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Static files collected"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Access the application at:"
echo "  http://127.0.0.1:8000/"
echo ""
echo "Access the admin panel at:"
echo "  http://127.0.0.1:8000/admin/"
