#!/bin/bash
# Setup script for Unix-based systems (Linux/macOS)
# Creates virtual environment and installs dependencies

set -e  # Exit on error

echo "=========================================="
echo "Setting up User Display Optimizer"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.10+
required_version="3.10"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "ERROR: Python 3.10 or higher is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the optimized module:"
echo "  bash run.sh"
echo ""
echo "To run tests:"
echo "  bash test.sh"
echo "=========================================="
