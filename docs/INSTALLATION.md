# Installation Guide

Complete step-by-step instructions for installing QRiskLab Pro on your system.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Docker Setup](#docker-setup)

## System Requirements

### Minimum Requirements

- **Python:** 3.10 or higher
- **RAM:** 4 GB (8 GB recommended)
- **Disk Space:** 2 GB for installation and dependencies
- **Internet:** Required for downloading dependencies

### Operating Systems

- **Windows:** Windows 10 or later (64-bit)
- **macOS:** macOS 10.14 or later (Intel or Apple Silicon)
- **Linux:** Ubuntu 18.04+, Fedora 30+, Debian 10+, or equivalent

### C++ Build Tools

Required for compiling C++ extensions:

**Windows:**
```bash
# Install Visual Studio Build Tools with C++ support
# Or install Visual Studio Community with C++ workload
# Download from: https://visualstudio.microsoft.com/downloads/
```

**macOS:**
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev cmake ninja-build
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install gcc-c++ python3-devel cmake ninja-build
```

## Prerequisites

### 1. Python Installation

Verify Python 3.10+ is installed:

```bash
python --version
# or
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### 2. CMake Installation

Required for building C++ extensions:

```bash
cmake --version
```

If not installed:

**Windows:**
- Download from [cmake.org](https://cmake.org/download/)
- Add to PATH during installation

**macOS:**
```bash
brew install cmake
```

**Linux:**
```bash
sudo apt-get install cmake  # Ubuntu/Debian
sudo dnf install cmake      # Fedora/RHEL
```

### 3. Git Installation

```bash
git --version
```

If not installed, download from [git-scm.com](https://git-scm.com/downloads)

## Installation Steps

### Windows Development Setup

```bash
cd C:\Users\stavr\source\repos\QRiskLab
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel cmake ninja
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pybind11 --cmakedir
# Set pybind11_DIR using the printed path
python -m pip install -e .
powershell -ExecutionPolicy Bypass -File .\scripts\validate_dev.ps1
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/qrisklab/qrisklab.git
cd qrisklab
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Upgrade pip, setuptools, and wheel

```bash
python -m pip install --upgrade pip setuptools wheel
```

### Step 4: Install QRiskLab Pro

**Development Installation (Recommended for development):**

```bash
pip install -e .
```

This installs the package in editable mode, allowing you to modify code and see changes immediately.

**Production Installation:**

```bash
pip install .
```

### Step 5: Install Development Dependencies (Optional)

For development, testing, and documentation:

```bash
pip install -r requirements-dev.txt
```

### Step 6: Verify Installation

```bash
python -c "import qrisklab; print(f'QRiskLab {qrisklab.__version__} installed successfully')"
```

## Verification

### Test Python Bindings

```python
# Test C++ bindings
from qrisklab.core import QuantumState
from qrisklab.finance import MonteCarlo, RiskMetrics

print("✓ C++ bindings loaded successfully")
```

### Test Finance Module

```python
from qrisklab.finance.pricing import EuropeanCallPricer

pricer = EuropeanCallPricer()
result = pricer.price(
    spot_price=100.0,
    strike_price=105.0,
    risk_free_rate=0.05,
    volatility=0.2,
    maturity_years=1.0
)
print(f"✓ Option price: ${result.estimated_price:.4f}")
```

### Test Risk Module

```python
from qrisklab.finance.risk import RiskAnalyzer
import numpy as np

analyzer = RiskAnalyzer()
losses = np.random.normal(0, 100, 1000).tolist()
result = analyzer.analyze_risk(losses, confidence_level=0.95)
print(f"✓ VaR (95%): ${result.var:.2f}")
```

### Test Quantum Module

```python
from qrisklab.quantum.backends import BackendFactory

backends = BackendFactory.get_available_backends()
print(f"✓ Available quantum backends: {backends}")
```

### Test API

```bash
# Start API server
python -m uvicorn qrisklab.api.main:app --reload &

# Test health endpoint
curl http://127.0.0.1:8000/health

# Stop server
pkill -f uvicorn
```

### Test Dashboard

```bash
# Start dashboard
streamlit run qrisklab/app/dashboard.py
```

Then open `http://localhost:8501` in your browser.

## Troubleshooting

### Issue: CMake not found

**Solution:**
```bash
# Install CMake
# Windows: Download from cmake.org
# macOS: brew install cmake
# Linux: sudo apt-get install cmake
```

### Issue: C++ compiler not found

**Windows:**
- Install Visual Studio Build Tools with C++ support
- Or install Visual Studio Community

**macOS:**
```bash
xcode-select --install
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf install gcc-c++
```

### Issue: "ModuleNotFoundError: No module named '_qrisklab_core'"

**Solution:**
```bash
# Rebuild C++ extensions
pip install -e . --force-reinstall --no-cache-dir
```

### Issue: "Python version not supported"

**Solution:**
- Ensure Python 3.10 or higher is installed
- Check which Python is being used: `which python` or `where python`
- Use `python3` explicitly if needed

### Issue: Permission denied on Linux/macOS

**Solution:**
```bash
# Use --user flag
pip install --user -e .

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Issue: Out of memory during build

**Solution:**
```bash
# Reduce parallel build jobs
pip install -e . --global-option="--parallel=1"
```

### Issue: Quantum backends not available

**Solution:**
```bash
# Install quantum computing frameworks
pip install qiskit qiskit-aer pennylane cirq

# Verify installation
python -c "from qrisklab.quantum.backends import BackendFactory; print(BackendFactory.get_available_backends())"
```

## Docker Setup

### Build Docker Image

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Copy repository
COPY . .

# Install QRiskLab
RUN pip install --no-cache-dir -e .

# Expose API port
EXPOSE 8000

# Default command
CMD ["python", "-m", "uvicorn", "qrisklab.api.main:app", "--host", "0.0.0.0"]
```

### Run Docker Container

```bash
# Build image
docker build -t qrisklab:latest .

# Run container
docker run -p 8000:8000 qrisklab:latest

# Run with dashboard
docker run -p 8000:8000 -p 8501:8501 qrisklab:latest streamlit run qrisklab/app/dashboard.py --server.address 0.0.0.0
```

## Next Steps

1. Read the [Quick Start Guide](QUICKSTART.md)
2. Explore [API Documentation](API.md)
3. Check out [Examples](EXAMPLES.md)
4. Review [Development Guide](DEVELOPMENT.md)

## Support

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review [GitHub Issues](https://github.com/qrisklab/qrisklab/issues)
3. Create a new issue with:
   - Python version: `python --version`
   - OS and version
   - Error message and traceback
   - Steps to reproduce

---

**Last Updated:** 2026-06-19
