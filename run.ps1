$ErrorActionPreference = 'Stop'
$RootDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$Venv = Join-Path $RootDir '.venv'

$activate = Join-Path $Venv 'Scripts\Activate.ps1'
if (Test-Path $activate) { & $activate }

python -m user_display_optimized
