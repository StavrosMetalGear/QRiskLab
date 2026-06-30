# QRiskLab Pro - Hybrid Quantum-Classical Risk Analysis Framework ![CI](https://github.com/qrisklab/qrisklab/actions/workflows/ci.yml/badge.svg)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

QRiskLab is a hybrid Python/C++ quantum finance and risk simulation platform that combines advanced quantum computing algorithms with classical Monte Carlo simulations for comprehensive financial risk analysis and option pricing.

## 🚀 Key Features

## 🏗️ Engineering Highlights
- Python package with C++/pybind11 extension
- CMake-based native build
- FastAPI API layer
- Streamlit dashboard
- Monte Carlo option pricing
- Quantum state / algorithm modules
- pytest test suite and GitHub Actions CI

### 📈 Option Pricing
- **European Call Option Pricing** using Monte Carlo simulation
- **Batch pricing** for multiple options
- **Sensitivity analysis** on spot price, volatility, and risk-free rate
- High-performance C++ backend with Python bindings

### 📊 Risk Analysis
- **Value at Risk (VaR)** calculation at configurable confidence levels
- **Conditional Value at Risk (CVaR)** / Expected Shortfall
- **Multi-level analysis** across multiple confidence levels
- Portfolio loss simulation and reporting

### 🔬 Quantum Algorithms
- **Quantum Amplitude Estimation** for option pricing with quadratic speedup
- **Variational Quantum Eigensolver (VQE)** for portfolio optimization
- **Quantum Phase Estimation (QPE)** for eigenvalue estimation
- Multi-backend support (Qiskit, PennyLane, Cirq, Amazon Braket)

### 💼 Portfolio Management
- Portfolio construction and position management
- Risk metrics calculation and reporting
- Monte Carlo-based loss simulation
- Position weighting and allocation analysis

### 🌐 REST API
- FastAPI-based REST API with automatic documentation
- Comprehensive request/response validation with Pydantic
- CORS support for cross-origin requests
- Health check and status endpoints

### 📱 Interactive Dashboard
- Streamlit-based web interface
- Real-time pricing and risk calculations
- Interactive visualizations and charts
- Portfolio analysis and optimization tools

## 📋 Current Status
- 102 tests passing
- CI install, smoke import, package build, and tests
- Windows local development supported

- **Python:** 3.10 or higher
- **OS:** Windows, macOS, or Linux
- **C++ Compiler:** C++17 compatible (MSVC, GCC, or Clang)
- **CMake:** 3.27 or higher
- **Build Tools:** ninja or make

## 🔧 Installation

### Virtual Environment

For a professional setup, refer to [INSTALLATION.md](docs/INSTALLATION.md) for instructions on using a local `.venv`.

### Quick Start (Development)

```bash
# Clone the repository
git clone https://github.com/qrisklab/qrisklab.git
cd qrisklab

# Install in development mode with all dependencies
python -m pip install -e .

# Install development dependencies
python -m pip install -r requirements-dev.txt
```

### Detailed Installation

See [INSTALLATION.md](docs/INSTALLATION.md) for:
- System-specific setup instructions
- Troubleshooting common issues
- Verification steps
- Docker setup (if available)

## 🚀 Quick Start

### Developer Validation
Windows users can run:
```bash
powershell -ExecutionPolicy Bypass -File .\scripts\validate_dev.ps1
```

### Python API

```python
from qrisklab.finance.pricing import EuropeanCallPricer
from qrisklab.finance.risk import RiskAnalyzer

# Price a European call option
pricer = EuropeanCallPricer()
result = pricer.price(
    spot_price=100.0,
    strike_price=105.0,
    risk_free_rate=0.05,
    volatility=0.2,
    maturity_years=1.0,
    paths=10000
)
print(f"Option Price: ${result.estimated_price:.4f}")

# Analyze portfolio risk
import numpy as np
losses = np.random.normal(0, 100, 10000).tolist()
analyzer = RiskAnalyzer()
risk_result = analyzer.analyze_risk(losses, confidence_level=0.95)
print(f"VaR (95%): ${risk_result.var:.2f}")
print(f"CVaR (95%): ${risk_result.cvar:.2f}")
```

### REST API

```bash
# Start the API server
python -m uvicorn qrisklab.api.main:app --reload

# Price an option via API
curl -X POST http://127.0.0.1:8000/api/pricing/european-call \
  -H "Content-Type: application/json" \
  -d '{
    "spot_price": 100.0,
    "strike_price": 105.0,
    "risk_free_rate": 0.05,
    "volatility": 0.2,
    "maturity_years": 1.0,
    "paths": 10000
  }'
```

### Interactive Dashboard

```bash
# Start the Streamlit dashboard
streamlit run qrisklab/app/dashboard.py
```

Then open your browser to `http://localhost:8501`

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[Quick Start Guide](docs/QUICKSTART.md)** - Common workflows and examples
- **[API Reference](docs/API.md)** - Complete REST API documentation
- **[Quantum Algorithms](docs/QUANTUM.md)** - Quantum computing guide
- **[Development Guide](docs/DEVELOPMENT.md)** - Contributing and development
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[Examples](docs/EXAMPLES.md)** - Code examples and tutorials

## 🏗️ Architecture

QRiskLab Pro uses a hybrid architecture:

```
┌─────────────────────────────────────────────────────────┐
│                  User Interfaces                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Streamlit   │  │   FastAPI    │  │   Python     │  │
│  │  Dashboard   │  │   REST API   │  │   Library    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Python Application Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Finance    │  │   Quantum    │  │  Portfolio   │  │
│  │   Modules    │  │  Algorithms  │  │  Management  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│           C++ Core (High Performance)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ QuantumState │  │  MonteCarlo  │  │ RiskMetrics  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=qrisklab --cov-report=html

# Run specific test file
pytest tests/unit/test_finance.py -v
```

## 📦 Project Structure

```
qrisklab/
├── api/                    # FastAPI REST API
│   ├── main.py            # API application factory
│   ├── models.py          # Pydantic request/response models
│   └── routes/            # API endpoint routes
│       ├── pricing.py     # Option pricing endpoints
│       ├── risk.py        # Risk analysis endpoints
│       └── quantum.py     # Quantum algorithm endpoints
├── app/                    # Streamlit dashboard
│   ├── dashboard.py       # Main dashboard application
│   └── pages/             # Dashboard pages
│       ├── pricing.py     # Option pricing page
│       ├── risk_analysis.py
│       ├── quantum.py
│       └── portfolio.py
├── finance/               # Financial calculations
│   ├── pricing.py        # Option pricing wrapper
│   ├── risk.py           # Risk metrics wrapper
│   └── portfolio.py      # Portfolio management
├── quantum/              # Quantum algorithms
│   ├── algorithms.py     # Quantum algorithm implementations
│   ├── backends.py       # Quantum backend factory
│   └── state.py          # Quantum state management
├── utils/                # Utilities
│   ├── logger.py         # Logging configuration
│   └── timing.py         # Performance timing utilities
├── config.py             # Configuration management
└── __init__.py           # Package initialization

src/                       # C++ source code
├── core/                 # Core quantum state
├── finance/              # Financial calculations
└── utils/                # C++ utilities

tests/                     # Test suite
├── unit/                 # Unit tests
└── integration/          # Integration tests
```

## 🤝 Contributing

We welcome contributions! Please see [DEVELOPMENT.md](docs/DEVELOPMENT.md) for:
- Development setup
- Code style guidelines
- Testing procedures
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

**QRiskLab Team**
- Email: team@qrisklab.dev
- GitHub: [@qrisklab](https://github.com/qrisklab)

## 🙏 Acknowledgments

- Quantum computing frameworks: Qiskit, PennyLane, Cirq
- Financial libraries: QuantLib, statsmodels
- Web frameworks: FastAPI, Streamlit
- Scientific computing: NumPy, SciPy, Pandas

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/qrisklab/qrisklab/issues)
- **Discussions:** [GitHub Discussions](https://github.com/qrisklab/qrisklab/discussions)

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and development phases.

---

**QRiskLab Pro v0.1.0** - Hybrid Quantum-Classical Risk Analysis Framework
