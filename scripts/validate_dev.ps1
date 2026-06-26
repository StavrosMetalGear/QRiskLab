$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "=== $Message ==="
}

if ($env:VIRTUAL_ENV -and (Test-Path "$env:VIRTUAL_ENV\Scripts\python.exe")) {
    $PythonExe = "$env:VIRTUAL_ENV\Scripts\python.exe"
    $PythonArgs = @()
} else {
    $PythonExe = "py"
    $PythonArgs = @("-3.11")
}

Write-Step "Using Python"
& $PythonExe @PythonArgs --version
& $PythonExe @PythonArgs -c "import sys; print(sys.executable)"

Write-Step "Checking Python import"
& $PythonExe @PythonArgs -c "import qrisklab; print('qrisklab imported')"

Write-Step "Checking config import"
& $PythonExe @PythonArgs -c "from qrisklab.config import get_config; print('config imported')"

Write-Step "Checking finance extension import"
& $PythonExe @PythonArgs -c "from qrisklab.finance._qrisklab_core import MonteCarlo; print('finance extension imported')"

Write-Step "Running tests"
& $PythonExe @PythonArgs -m pytest tests\ -q

Write-Host ""
Write-Host "Developer validation passed."
Write-Host "If editable install fails on Windows, set pybind11_DIR first:"
Write-Host '$env:pybind11_DIR="C:\Users\<you>\AppData\Local\Programs\Python\Python311\Lib\site-packages\pybind11\share\cmake\pybind11"'
