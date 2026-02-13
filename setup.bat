@echo off
REM Quick Start Script for Todo Application (Windows)
REM Run this script to set up the project

echo.
echo 🚀 Todo App - Quick Setup
echo ==========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

echo ✅ Virtual environment activated
echo.

REM Install dependencies
echo 📚 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Dependencies installed
echo.

REM Create migrations
echo 🗄️  Creating database migrations...
python manage.py makemigrations

echo ✅ Migrations created
echo.

REM Apply migrations
echo 🗄️  Applying migrations...
python manage.py migrate

echo ✅ Migrations applied
echo.

REM Create superuser
echo 👤 Creating superuser account...
python manage.py createsuperuser

echo ✅ Superuser created
echo.

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo ✅ Static files collected
echo.

echo 🎉 Setup complete!
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Access the application at:
echo   http://127.0.0.1:8000/
echo.
echo Access the admin panel at:
echo   http://127.0.0.1:8000/admin/
echo.
pause
