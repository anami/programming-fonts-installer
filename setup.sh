#!/bin/bash

# Programming Fonts Installer - Setup Script

echo "===================================="
echo "Programming Fonts Installer Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✓ pip found"

# Install dependencies
echo ""
echo "Installing dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    python3 -m pip install -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
    echo ""
    echo "===================================="
    echo "Setup Complete!"
    echo "===================================="
    echo ""
    echo "To run the application:"
    echo "  ./font_installer.py"
    echo "  or"
    echo "  python3 font_installer.py"
    echo ""
else
    echo ""
    echo "❌ Failed to install dependencies"
    exit 1
fi
