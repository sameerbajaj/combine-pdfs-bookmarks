#!/bin/bash

# PDF Combiner Installation Script
# This script installs the required dependencies and sets up the PDF combiner utility

echo "=== PDF Combiner with Automatic Bookmarks - Installation ==="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher and try again."
    echo "You can download it from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

echo "✅ Found Python $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "❌ Error: Python 3.7 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed or not in PATH"
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✅ Found pip3"

# Try to install required dependencies, handle externally-managed environments
USE_VENV=0

echo ""
echo "Installing required dependencies..."
if pip3 install -r requirements.txt 2>/dev/null; then
    echo "✅ Dependencies installed successfully"
else
    echo "ℹ️  Fallback: setting up a virtual environment (env/)"
    python3 -m venv env
    # shellcheck disable=SC1091
    source env/bin/activate
    pip install --upgrade pip
    if pip install -r requirements.txt; then
        echo "✅ Dependencies installed successfully in virtual environment"
        USE_VENV=1
    else
        echo "❌ Failed to install dependencies. Please check your internet connection and try again."
        exit 1
    fi
fi

# Make scripts executable
echo ""
echo "Setting up scripts..."
chmod +x pdf_combiner.py
chmod +x pdf_combiner_cli.py

echo "✅ Scripts made executable"

# Test the installation
echo ""
echo "Testing installation..."
if [ "$USE_VENV" -eq 1 ]; then
    python -c "import PyPDF2; print('✅ PyPDF2 import successful (venv)')"
else
    python3 -c "import PyPDF2; print('✅ PyPDF2 import successful')"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "You can now use the PDF Combiner in two ways:"
    echo ""
    echo "1. GUI Version (Recommended for most users):"
    if [ "$USE_VENV" -eq 1 ]; then
        echo "   source env/bin/activate && python pdf_combiner.py"
    else
        echo "   python3 pdf_combiner.py"
    fi
    echo ""
    echo "2. Command Line Version:"
    if [ "$USE_VENV" -eq 1 ]; then
        echo "   source env/bin/activate && python pdf_combiner_cli.py"
    else
        echo "   python3 pdf_combiner_cli.py"
    fi
    echo ""
    echo "For detailed instructions, see the README.md file."
    echo ""
    echo "Happy PDF combining! 📚✨"
else
    echo "❌ Installation test failed. Please check the error messages above."
    exit 1
fi