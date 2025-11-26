param()
$venv = Join-Path $PSScriptRoot ".venv"
if (Test-Path $venv) {
    & "$venv\Scripts\Activate.ps1"
}
Write-Host "Running optimized display module"
python run_module.py
