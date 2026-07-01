# Quick Start Guide

Get up and running with QRiskLab Pro in minutes.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Common Workflows](#common-workflows)
4. [API Examples](#api-examples)
5. [Dashboard Usage](#dashboard-usage)

## Quick Start on Windows

1. Create a virtual environment:
   ```bash
   py -3.11 -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

3. Upgrade pip, setuptools, and wheel:
   ```bash
   python -m pip install --upgrade pip setuptools wheel cmake ninja
   ```

4. Install the required packages:
   ```bash
   python -m pip install -r requirements.txt
   python -m pip install -r requirements-dev.txt
   python -m pip install -e .
   ```

5. Verify the installation:
   ```bash
   python -c "import qrisklab; from qrisklab.finance import MonteCarlo; print('QRiskLab import OK')"
   ```

6. Run tests:
   ```bash
   py -3.11 -m pytest tests\ -q
   ```

## Installation

```bash
# Clone and install
git clone https://github.com/qrisklab/qrisklab.git
cd qrisklab
pip install -e .
```

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

## Basic Usage

### Option Pricing

Price a European call option:

```python
from qrisklab.finance.pricing import EuropeanCallPricer

# Create pricer instance
pricer = EuropeanCallPricer(default_paths=10000)

# Price an option
result = pricer.price(
    spot_price=100.0,           # Current stock price
    strike_price=105.0,         # Strike price
    risk_free_rate=0.05,        # 5% risk-free rate
    volatility=0.2,             # 20% volatility
    maturity_years=1.0,         # 1 year to maturity
    paths=10000                 # Monte Carlo paths
)

print(f"Option Price: ${result.estimated_price:.4f}")
print(f"Standard Error: ${result.standard_error:.6f}")
```

### Risk Analysis

Calculate Value at Risk and Conditional Value at Risk:

```python
from qrisklab.finance.risk import RiskAnalyzer
import numpy as np

# Create analyzer
analyzer = RiskAnalyzer()

# Generate sample losses (or use real portfolio data)
np.random.seed(42)
losses = np.random.normal(loc=0, scale=100, size=10000).tolist()

# Calculate risk metrics
result = analyzer.analyze_risk(losses, confidence_level=0.95)

print(f"VaR (95%):  ${result.var:.2f}")
print(f"CVaR (95%): ${result.cvar:.2f}")
print(f"Mean Loss:  ${result.mean_loss:.2f}")
print(f"Std Dev:    ${result.std_loss:.2f}")
```

### Portfolio Management

Build and analyze a portfolio:

```python
from qrisklab.finance.portfolio import Portfolio

# Create portfolio
portfolio = Portfolio(name="My Portfolio")

# Add positions
portfolio.add_position(
    name="Stock A",
    value=50000.0,
    expected_return=0.08,
    volatility=0.15
)

portfolio.add_position(
    name="Stock B",
    value=30000.0,
    expected_return=0.10,
    volatility=0.20
)

portfolio.add_position(
    name="Bond Fund",
    value=20000.0,
    expected_return=0.03,
    volatility=0.05
)

# Get portfolio summary
summary = portfolio.get_summary()
print(f"Total Value: ${summary['total_value']:,.2f}")
print(f"Expected Return: {summary['expected_return']:.2%}")
print(f"Volatility: {summary['volatility']:.2%}")

# Analyze risk
risk_result = portfolio.analyze_risk(
    time_horizon_years=1.0,
    scenarios=10000,
    confidence_level=0.95
)
print(f"Portfolio VaR: ${risk_result.var:.2f}")
print(f"Portfolio CVaR: ${risk_result.cvar:.2f}")
```

### Quantum Algorithms

Run quantum algorithms:

```python
from qrisklab.quantum.algorithms import (
    QuantumAmplitudeEstimation,
    VariationalQuantumEigensolver,
    QuantumPhaseEstimation
)
from qrisklab.quantum.backends import BackendFactory

# Check available backends
backends = BackendFactory.get_available_backends()
print(f"Available backends: {backends}")

# Quantum Amplitude Estimation
qae = QuantumAmplitudeEstimation(backend="qiskit_aer")
result = qae.run(
    oracle=lambda: None,  # Placeholder oracle
    num_qubits=5,
    shots=1024,
    precision_bits=3
)
print(f"Estimated Amplitude: {result.estimated_amplitude:.4f}")

# Variational Quantum Eigensolver
vqe = VariationalQuantumEigensolver(backend="pennylane")
result = vqe.run(
    hamiltonian=[(1.0, "Z0"), (0.5, "X0")],
    num_qubits=5,
    max_iterations=100,
    learning_rate=0.01
)
print(f"Eigenvalue: {result.eigenvalue:.6f}")

# Quantum Phase Estimation
qpe = QuantumPhaseEstimation(backend="qiskit_aer")
result = qpe.run(
    unitary=lambda: None,  # Placeholder unitary
    num_qubits=5,
    precision_bits=5,
    shots=1024
)
print(f"Phase: {result.phase:.6f}")
```

## Common Workflows

### Workflow 1: Price Multiple Options

```python
from qrisklab.finance.pricing import EuropeanCallPricer

pricer = EuropeanCallPricer()

# Define multiple options
options = [
    (100.0, 100.0, 0.05, 0.15, 1.0),  # ATM
    (100.0, 105.0, 0.05, 0.15, 1.0),  # OTM
    (100.0, 95.0,  0.05, 0.15, 1.0),  # ITM
]

# Price all options
results = pricer.price_batch(options)

for i, result in enumerate(results):
    print(f"Option {i+1}: ${result.estimated_price:.4f}")
```

### Workflow 2: Sensitivity Analysis

```python
from qrisklab.finance.pricing import EuropeanCallPricer

pricer = EuropeanCallPricer()

# Analyze sensitivity to spot price
sensitivity = pricer.sensitivity_analysis(
    spot_price=100.0,
    strike_price=105.0,
    risk_free_rate=0.05,
    volatility=0.2,
    maturity_years=1.0,
    parameter="spot_price",
    range_pct=0.2,  # ±20%
    steps=5
)

for spot, price in sensitivity.items():
    print(f"Spot: ${spot:.2f} → Price: ${price:.4f}")
```

### Workflow 3: Multi-Level Risk Analysis

```python
from qrisklab.finance.risk import RiskAnalyzer
import numpy as np

analyzer = RiskAnalyzer()
losses = np.random.normal(0, 100, 10000).tolist()

# Analyze at multiple confidence levels
results = analyzer.multi_level_analysis(
    losses=losses,
    confidence_levels=[0.90, 0.95, 0.99]
)

for cl, result in results.items():
    print(f"CL {cl:.0%}: VaR=${result.var:.2f}, CVaR=${result.cvar:.2f}")
```

### Workflow 4: Portfolio Optimization

```python
from qrisklab.finance.portfolio import Portfolio

# Create and analyze portfolio
portfolio = Portfolio(name="Optimized Portfolio")

positions = [
    ("Tech Stocks", 40000, 0.12, 0.25),
    ("Healthcare", 30000, 0.08, 0.18),
    ("Utilities", 20000, 0.05, 0.12),
    ("Bonds", 10000, 0.03, 0.05),
]

for name, value, ret, vol in positions:
    portfolio.add_position(name, value, ret, vol)

# Simulate losses
losses = portfolio.simulate_losses(
    time_horizon_years=1.0,
    scenarios=10000
)

# Analyze risk
risk = portfolio.analyze_risk(
    time_horizon_years=1.0,
    scenarios=10000,
    confidence_level=0.95
)

print(f"Portfolio VaR (95%): ${risk.var:.2f}")
print(f"Portfolio CVaR (95%): ${risk.cvar:.2f}")
```

## API Examples

### Start the API Server

```bash
python -m uvicorn qrisklab.api.main:app --reload
```

API documentation available at: `http://127.0.0.1:8000/docs`

### Price an Option via API

```bash
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

### Calculate Risk Metrics via API

```bash
curl -X POST http://127.0.0.1:8000/api/risk/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
    "confidence_level": 0.95
  }'
```

### List Quantum Backends via API

```bash
curl http://127.0.0.1:8000/api/quantum/backends
```

### Run Quantum Algorithm via API

```bash
curl -X POST http://127.0.0.1:8000/api/quantum/amplitude-estimation \
  -H "Content-Type: application/json" \
  -d '{
    "num_qubits": 5,
    "shots": 1024,
    "precision_bits": 3,
    "backend": "qiskit_aer"
  }'
```

## Dashboard Usage

### Start the Dashboard

```bash
streamlit run qrisklab/app/dashboard.py
```

Then open `http://localhost:8501` in your browser.

### Dashboard Pages

1. **Home** - Overview and system status
2. **Option Pricing** - Price options and perform sensitivity analysis
3. **Risk Analysis** - Calculate VaR, CVaR, and analyze loss distributions
4. **Quantum Algorithms** - Run quantum algorithms and select backends
5. **Portfolio Management** - Build portfolios and analyze risk

### Dashboard Features

- **Real-time Calculations** - See results instantly as you adjust parameters
- **Interactive Charts** - Visualize pricing curves and risk distributions
- **Batch Operations** - Price multiple options or analyze multiple portfolios
- **Export Results** - Download analysis results as CSV or JSON

## Next Steps

1. Explore [API Documentation](API.md) for complete endpoint reference
2. Read [Quantum Algorithms Guide](QUANTUM.md) for quantum computing details
3. Check [Examples](EXAMPLES.md) for more code samples
4. Review [Architecture](ARCHITECTURE.md) to understand system design

## Tips & Best Practices

### Performance

- Use batch operations for multiple calculations
- Cache results when possible
- Adjust Monte Carlo paths based on accuracy needs
- Use quantum backends for large-scale problems

### Accuracy

- Increase Monte Carlo paths for better accuracy
- Use higher precision bits for quantum algorithms
- Validate results with multiple confidence levels
- Compare classical and quantum results

### Development

- Use virtual environments to isolate dependencies
- Enable logging for debugging: `setup_logging(level=LogLevel.DEBUG)`
- Run tests before committing changes
- Follow code style guidelines (see DEVELOPMENT.md)

---

**Ready to dive deeper?** Check out the [full documentation](../docs/).
