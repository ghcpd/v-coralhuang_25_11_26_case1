#!/bin/bash
# Test script for Unix-based systems (Linux/macOS)
# Runs pytest with coverage reporting

set -e  # Exit on error

echo "=========================================="
echo "Running Tests with Coverage"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found."
    echo "Please run: bash setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run tests with coverage
echo "Running pytest with coverage..."
echo ""
pytest tests/ \
    --cov=user_display_optimized \
    --cov-config=.coveragerc \
    --cov-report=term-missing \
    --cov-report=html \
    -v

echo ""
echo "=========================================="
echo "Coverage report generated in htmlcov/"
echo "Open htmlcov/index.html to view details"
echo "=========================================="

exit 0
