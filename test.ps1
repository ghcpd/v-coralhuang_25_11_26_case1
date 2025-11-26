# Cross-platform test script for Windows PowerShell
# Runs pytest with coverage reporting (78% minimum for production code with defensive error handling)

param()

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
}

Write-Host "[MARKER] Running tests with coverage..."

# Run pytest with coverage
pytest tests/ `
    --cov=user_display_optimized `
    --cov-report=term-missing `
    --cov-report=html `
    --cov-fail-under=78 `
    -v

$EXIT_CODE = $LASTEXITCODE

if ($EXIT_CODE -eq 0) {
    Write-Host "[MARKER] All tests passed with coverage ≥78%"
    Write-Host "[MARKER] HTML coverage report: htmlcov\index.html"
} else {
    Write-Host "[ERROR] Tests failed or coverage insufficient"
}

exit $EXIT_CODE
