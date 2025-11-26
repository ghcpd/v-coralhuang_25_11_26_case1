$ErrorActionPreference = 'Stop'
$RootDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$Venv = Join-Path $RootDir '.venv'

$activate = Join-Path $Venv 'Scripts\Activate.ps1'
if (Test-Path $activate) { & $activate }

pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-report=term --cov-fail-under=85
