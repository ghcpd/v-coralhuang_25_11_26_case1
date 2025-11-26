$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvDir = Join-Path $root ".venv"
$reqs = Join-Path $root "requirements.txt"

function Find-Python {
    $candidates = @()
    if ($env:PYTHON) { $candidates += $env:PYTHON }
    $candidates += @("py -3", "python3", "python")
    foreach ($cand in $candidates) {
        try {
            $null = Invoke-Expression "$cand --version" 2>$null
            return $cand
        } catch {
            continue
        }
    }
    throw "Python 3.10+ not found"
}

$pythonCmd = Find-Python

if (-not (Test-Path $venvDir)) {
    Invoke-Expression "$pythonCmd -m venv `"$venvDir`""
}

$venvPython = Join-Path $venvDir "Scripts/python.exe"

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r $reqs

Write-Host "[setup] Virtual environment ready at $venvDir"
