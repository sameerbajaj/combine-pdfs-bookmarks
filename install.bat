@echo off
REM PDF Combiner Installation Script for Windows
REM This script installs the required dependencies and sets up the PDF combiner utility

echo === PDF Combiner with Automatic Bookmarks - Installation ===
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher and try again.
    echo You can download it from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python -c "import sys; print(sys.version.split()[0])" 2^>nul') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM Install required dependencies
echo.
echo Installing required dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error installing dependencies. Trying alternative method...
    pip install PyPDF2
    if errorlevel 1 (
        echo ❌ Failed to install PyPDF2. Please check your internet connection and try again.
        pause
        exit /b 1
    ) else (
        echo ✅ PyPDF2 installed successfully
    )
) else (
    echo ✅ Dependencies installed successfully
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo You can now use the PDF Combiner in two ways:
echo.
echo 1. GUI Version (Recommended for most users):
echo    python pdf_combiner.py
echo.
echo 2. Command Line Version:
echo    python pdf_combiner_cli.py
echo.
echo For detailed instructions, see the README.md file.
echo.
echo Happy PDF combining! 📚✨
pause