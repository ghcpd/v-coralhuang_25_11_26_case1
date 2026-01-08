#!/bin/bash
# Cross-platform setup script for Linux/macOS
# Creates virtual environment and installs dependencies

set -e  # Exit on any error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "[MARKER] Setting up Python environment..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found. Please install Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "[MARKER] Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[MARKER] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[MARKER] Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "[MARKER] Upgrading pip..."
python -m pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "[MARKER] Installing dependencies..."
pip install -r requirements.txt

echo "[MARKER] Setup complete! Virtual environment ready in ./venv"
echo "[MARKER] To activate: source venv/bin/activate"
