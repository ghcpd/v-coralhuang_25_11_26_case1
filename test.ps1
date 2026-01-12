# Test script for Windows PowerShell
# Runs pytest with coverage reporting

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Running Tests with Coverage" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "ERROR: Virtual environment not found." -ForegroundColor Red
    Write-Host "Please run: powershell -File setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run tests with coverage
Write-Host "Running pytest with coverage..." -ForegroundColor Yellow
Write-Host ""
& pytest tests/ `
    --cov=user_display_optimized `
    --cov-config=.coveragerc `
    --cov-report=term-missing `
    --cov-report=html `
    -v

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Coverage report generated in htmlcov/" -ForegroundColor Green
Write-Host "Open htmlcov/index.html to view details" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

exit 0
