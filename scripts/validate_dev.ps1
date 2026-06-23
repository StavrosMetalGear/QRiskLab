$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "=== $Message ==="
}

Write-Step "Checking Python import"
py -3.11 -c "import qrisklab; print('qrisklab imported')"

Write-Step "Checking config import"
py -3.11 -c "from qrisklab.config import get_config; print('config imported')"

Write-Step "Checking finance extension import"
py -3.11 -c "from qrisklab.finance._qrisklab_core import MonteCarlo; print('finance extension imported')"

Write-Step "Running tests"
py -3.11 -m pytest tests\ -q

Write-Host ""
Write-Host "Developer validation passed."
Write-Host "If editable install fails on Windows, set pybind11_DIR first:"
Write-Host '$env:pybind11_DIR="C:\Users\<you>\AppData\Local\Programs\Python\Python311\Lib\site-packages\pybind11\share\cmake\pybind11"'
