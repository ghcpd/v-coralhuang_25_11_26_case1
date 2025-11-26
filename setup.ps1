Param()
Write-Host "Setting up virtual environment (PowerShell)"
$venv = "$PWD/.venv"
if (-not (Test-Path $venv)) {
    python -m venv $venv
    Write-Host "Created venv at $venv"
} else {
    Write-Host "Virtual environment already exists at $venv"
}

Start-Process -FilePath "$venv/Scripts/python.exe" -ArgumentList '-m','pip','install','--upgrade','pip' -NoNewWindow -Wait
Start-Process -FilePath "$venv/Scripts/python.exe" -ArgumentList '-m','pip','install','-r','requirements.txt' -NoNewWindow -Wait

Write-Host "Setup complete. Activate with: $venv\Scripts\Activate.ps1"
