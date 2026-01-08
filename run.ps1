# Cross-platform run script for Windows PowerShell
# Executes the optimized module and displays timing

param()

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
}

Write-Host "[MARKER] Running optimized user display module..."
python user_display_optimized.py
$EXIT_CODE = $LASTEXITCODE

if ($EXIT_CODE -eq 0) {
    Write-Host "[MARKER] Execution completed successfully"
} else {
    Write-Host "[ERROR] Execution failed with exit code $EXIT_CODE"
}

exit $EXIT_CODE
