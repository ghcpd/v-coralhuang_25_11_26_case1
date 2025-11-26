$ErrorActionPreference = 'Stop'
$RootDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$Venv = Join-Path $RootDir '.venv'

if (Test-Path $Venv) { Remove-Item -Recurse -Force $Venv }

Get-ChildItem -Path $RootDir -Recurse -Directory -Force | Where-Object { $_.Name -eq '__pycache__' -or $_.Name -eq '.pytest_cache' } | Remove-Item -Recurse -Force

Write-Host 'Clean completed.'
