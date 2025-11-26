$ErrorActionPreference = 'Stop'
$RootDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$Venv = Join-Path $RootDir '.venv'

if (-Not (Test-Path $Venv)) {
    python -m venv $Venv
}

$activate = Join-Path $Venv 'Scripts\Activate.ps1'
if (Test-Path $activate) {
    & $activate
    python -m pip install --upgrade pip
    pip install -r (Join-Path $RootDir 'requirements.txt')
}
Write-Host 'Setup completed.'
