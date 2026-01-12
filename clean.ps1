# Clean script for Windows PowerShell
# Removes virtual environment and build artifacts

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Cleaning User Display Optimizer" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Remove virtual environment
if (Test-Path "venv") {
    Write-Host "Removing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Path "venv" -Recurse -Force
    Write-Host "Virtual environment removed." -ForegroundColor Green
} else {
    Write-Host "No virtual environment found." -ForegroundColor Yellow
}

# Remove Python cache
Write-Host "Removing __pycache__ directories..." -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force

if (Test-Path ".pytest_cache") {
    Write-Host "Removing .pytest_cache..." -ForegroundColor Yellow
    Remove-Item -Path ".pytest_cache" -Recurse -Force
}

# Remove coverage files
if (Test-Path "htmlcov") {
    Write-Host "Removing coverage reports..." -ForegroundColor Yellow
    Remove-Item -Path "htmlcov" -Recurse -Force
}

if (Test-Path ".coverage") {
    Remove-Item -Path ".coverage" -Force
}

# Remove .pyc files
Write-Host "Removing .pyc files..." -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "*.pyc" -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "To set up again, run: powershell -File setup.ps1" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

exit 0
