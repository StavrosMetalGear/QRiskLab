# Code Examples

Practical examples for using QRiskLab Pro.

## Table of Contents

1. [Option Pricing Examples](#option-pricing-examples)
2. [Risk Analysis Examples](#risk-analysis-examples)
3. [Portfolio Examples](#portfolio-examples)
4. [Quantum Algorithm Examples](#quantum-algorithm-examples)
5. [API Examples](#api-examples)
6. [Advanced Examples](#advanced-examples)

## Option Pricing Examples

### Example 1: Basic Option Pricing

```python
from qrisklab.finance.pricing import EuropeanCallPricer

# Create pricer
pricer = EuropeanCallPricer(default_paths=10000)

# Price a single option
result = pricer.price(
    spot_price=100.0,
    strike_price=105.0,
    risk_free_rate=0.05,
    volatility=0.2,
    maturity_years=1.0
)

print(f"Option Price: ${result.estimated_price:.4f}")
print(f"Standard Error: ${result.standard_error:.6f}")
```

### Example 2: Batch Pricing

```python
from qrisklab.finance.pricing import EuropeanCallPricer

pricer = EuropeanCallPricer()

# Define multiple options
options = [
    (100.0, 100.0, 0.05, 0.15, 1.0),  # ATM
    (100.0, 105.0, 0.05, 0.15, 1.0),  # OTM
    (100.0, 95.0,  0.05, 0.15, 1.0),  # ITM
    (100.0, 110.0, 0.05, 0.20, 2.0),  # OTM, longer maturity
]

# Price all options
results = pricer.price_batch(options)

# Display results
for i, (opt, result) in enumerate(zip(options, results)):
    s, k, r, v, t = opt
    print(f"Option {i+1}: S=${s:.0f}, K=${k:.0f}, Price=${result.estimated_price:.4f}")
```

### Example 3: Sensitivity Analysis

```python
from qrisklab.finance.pricing import EuropeanCallPricer
import matplotlib.pyplot as plt

pricer = EuropeanCallPricer()

# Analyze sensitivity to spot price
sensitivity = pricer.sensitivity_analysis(
    spot_price=100.0,
    strike_price=105.0,
    risk_free_rate=0.05,
    volatility=0.2,
    maturity_years=1.0,
    parameter="spot_price",
    range_pct=0.3,  # ±30%
    steps=11
)

# Plot results
spots = sorted(sensitivity.keys())
prices = [sensitivity[s] for s in spots]

plt.figure(figsize=(10, 6))
plt.plot(spots, prices, 'b-', linewidth=2)
plt.xlabel('Spot Price ($)')
plt.ylabel('Option Price ($)')
plt.title('Option Price Sensitivity to Spot Price')
plt.grid(True, alpha=0.3)
plt.show()
```

### Example 4: Greeks Approximation

```python
from qrisklab.finance.pricing import EuropeanCallPricer

pricer = EuropeanCallPricer()

# Base parameters
base_params = {
    'spot_price': 100.0,
    'strike_price': 105.0,
    'risk_free_rate': 0.05,
    'volatility': 0.2,
    'maturity_years': 1.0,
}

# Calculate base price
base_result = pricer.price(**base_params)
base_price = base_result.estimated_price

# Delta (sensitivity to spot price)
delta_params = base_params.copy()
delta_params['spot_price'] = 101.0
delta_result = pricer.price(**delta_params)
delta = delta_result.estimated_price - base_price

# Vega (sensitivity to volatility)
vega_params = base_params.copy()
vega_params['volatility'] = 0.21
vega_result = pricer.price(**vega_params)
vega = (vega_result.estimated_price - base_price) / 0.01

print(f"Base Price: ${base_price:.4f}")
print(f"Delta: {delta:.4f}")
print(f"Vega: {vega:.4f}")
```

## Risk Analysis Examples

### Example 1: Basic Risk Metrics

```python
from qrisklab.finance.risk import RiskAnalyzer
import numpy as np

# Create analyzer
analyzer = RiskAnalyzer()

# Generate sample losses
np.random.seed(42)
losses = np.random.normal(loc=0, scale=100, size=10000).tolist()

# Calculate risk metrics
result = analyzer.analyze_risk(losses, confidence_level=0.95)

print(f"VaR (95%):  ${result.var:.2f}")
print(f"CVaR (95%): ${result.cvar:.2f}")
print(f"Mean Loss:  ${result.mean_loss:.2f}")
print(f"Std Dev:    ${result.std_loss:.2f}")
print(f"Min Loss:   ${result.min_loss:.2f}")
print(f"Max Loss:   ${result.max_loss:.2f}")
```

### Example 2: Multi-Level Analysis

```python
from qrisklab.finance.risk import RiskAnalyzer
import numpy as np
import pandas as pd

analyzer = RiskAnalyzer()
losses = np.random.normal(0, 100, 10000).tolist()

# Analyze at multiple confidence levels
results = analyzer.multi_level_analysis(
    losses=losses,
    confidence_levels=[0.90, 0.95, 0.99]
)

# Create summary table
data = []
for cl, result in results.items():
    data.append({
        'Confidence Level': f'{cl:.0%}',
        'VaR': f'${result.var:.2f}',
        'CVaR': f'${result.cvar:.2f}',
        'Ratio (CVaR/VaR)': f'{result.cvar/result.var:.2f}x',
    })

df = pd.DataFrame(data)
print(df.to_string(index=False))
```

### Example 3: Loss Distribution Analysis

```python
from qrisklab.finance.risk import RiskAnalyzer
import numpy as np
import matplotlib.pyplot as plt

analyzer = RiskAnalyzer()
losses = np.random.normal(0, 100, 10000)

# Calculate VaR at different levels
var_90 = analyzer.calculate_var(losses.tolist(), 0.90)
var_95 = analyzer.calculate_var(losses.tolist(), 0.95)
var_99 = analyzer.calculate_var(losses.tolist(), 0.99)

# Plot distribution
plt.figure(figsize=(12, 6))
plt.hist(losses, bins=50, alpha=0.7, edgecolor='black')
plt.axvline(var_90, color='yellow', linestyle='--', linewidth=2, label=f'VaR 90%: ${var_90:.2f}')
plt.axvline(var_95, color='orange', linestyle='--', linewidth=2, label=f'VaR 95%: ${var_95:.2f}')
plt.axvline(var_99, color='red', linestyle='--', linewidth=2, label=f'VaR 99%: ${var_99:.2f}')
plt.xlabel('Loss ($)')
plt.ylabel('Frequency')
plt.title('Portfolio Loss Distribution with VaR Levels')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## Portfolio Examples

### Example 1: Portfolio Construction

```python
from qrisklab.finance.portfolio import Portfolio

# Create portfolio
portfolio = Portfolio(name="Balanced Portfolio")

# Add positions
positions = [
    ("US Stocks", 40000, 0.10, 0.18),
    ("International Stocks", 20000, 0.08, 0.20),
    ("Bonds", 30000, 0.03, 0.05),
    ("Real Estate", 10000, 0.06, 0.12),
]

for name, value, ret, vol in positions:
    portfolio.add_position(name, value, ret, vol)

# Get summary
summary = portfolio.get_summary()

print(f"Portfolio: {summary['name']}")
print(f"Total Value: ${summary['total_value']:,.2f}")
print(f"Expected Return: {summary['expected_return']:.2%}")
print(f"Volatility: {summary['volatility']:.2%}")
print(f"\nPositions:")
for pos in summary['positions']:
    print(f"  {pos['name']}: ${pos['value']:,.2f} ({pos['weight']:.1%})")
```

### Example 2: Portfolio Risk Analysis

```python
from qrisklab.finance.portfolio import Portfolio

portfolio = Portfolio(name="Growth Portfolio")
portfolio.add_position("Tech Stocks", 50000, 0.15, 0.30)
portfolio.add_position("Healthcare", 30000, 0.10, 0.20)
portfolio.add_position("Utilities", 20000, 0.05, 0.10)

# Analyze risk
risk_result = portfolio.analyze_risk(
    time_horizon_years=1.0,
    scenarios=10000,
    confidence_level=0.95
)

print(f"Portfolio VaR (95%):  ${risk_result.var:,.2f}")
print(f"Portfolio CVaR (95%): ${risk_result.cvar:,.2f}")
print(f"Expected Loss: ${risk_result.mean_loss:,.2f}")
print(f"Loss Std Dev: ${risk_result.std_loss:,.2f}")
```

### Example 3: Position Rebalancing

```python
from qrisklab.finance.portfolio import Portfolio

# Original portfolio
portfolio = Portfolio(name="Original")
portfolio.add_position("Stock A", 50000, 0.08, 0.15)
portfolio.add_position("Stock B", 50000, 0.10, 0.20)

# Get original weights
original = portfolio.get_summary()
print("Original Allocation:")
for pos in original['positions']:
    print(f"  {pos['name']}: {pos['weight']:.1%}")

# Rebalance
portfolio.remove_position("Stock B")
portfolio.add_position("Stock B", 30000, 0.10, 0.20)
portfolio.add_position("Bonds", 20000, 0.03, 0.05)

# Get new weights
rebalanced = portfolio.get_summary()
print("\nRebalanced Allocation:")
for pos in rebalanced['positions']:
    print(f"  {pos['name']}: {pos['weight']:.1%}")
```

## Quantum Algorithm Examples

### Example 1: Quantum Amplitude Estimation

```python
from qrisklab.quantum.algorithms import QuantumAmplitudeEstimation
from qrisklab.quantum.backends import BackendFactory

# Check available backends
backends = BackendFactory.get_available_backends()
print(f"Available backends: {backends}")

# Create algorithm
qae = QuantumAmplitudeEstimation(backend="qiskit_aer")

# Run algorithm
result = qae.run(
    oracle=lambda: None,  # Placeholder oracle
    num_qubits=5,
    shots=1024,
    precision_bits=3
)

print(f"Estimated Amplitude: {result.estimated_amplitude:.4f}")
print(f"Confidence Interval: {result.confidence_interval}")
print(f"Execution Time: {result.execution_time_seconds:.3f}s")
```

### Example 2: Variational Quantum Eigensolver

```python
from qrisklab.quantum.algorithms import VariationalQuantumEigensolver

# Create algorithm
vqe = VariationalQuantumEigensolver(backend="pennylane")

# Define Hamiltonian
hamiltonian = [
    (1.0, "Z0"),
    (0.5, "X0"),
    (0.3, "Z0Z1"),
]

# Run optimization
result = vqe.run(
    hamiltonian=hamiltonian,
    num_qubits=2,
    max_iterations=100,
    learning_rate=0.01
)

print(f"Ground State Energy: {result.eigenvalue:.6f}")
print(f"Optimized Parameters: {result.parameters}")
print(f"Iterations: {result.iterations}")
```

### Example 3: Quantum Phase Estimation

```python
from qrisklab.quantum.algorithms import QuantumPhaseEstimation

# Create algorithm
qpe = QuantumPhaseEstimation(backend="qiskit_aer")

# Run algorithm
result = qpe.run(
    unitary=lambda: None,  # Placeholder unitary
    num_qubits=5,
    precision_bits=5,
    shots=1024
)

print(f"Estimated Phase: {result.phase:.6f}")
print(f"Eigenvalue: {result.eigenvalue:.6f}")
print(f"Precision Bits: {result.precision_bits}")
```

## API Examples

### Example 1: Using curl

```bash
# Price an option
curl -X POST http://127.0.0.1:8000/api/pricing/european-call \
  -H "Content-Type: application/json" \
  -d '{
    "spot_price": 100.0,
    "strike_price": 105.0,
    "risk_free_rate": 0.05,
    "volatility": 0.2,
    "maturity_years": 1.0
  }'

# Calculate risk metrics
curl -X POST http://127.0.0.1:8000/api/risk/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "losses": [-100, -50, 0, 50, 100],
    "confidence_level": 0.95
  }'
```

### Example 2: Using Python requests

```python
import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000"

# Price an option
response = requests.post(
    f"{BASE_URL}/api/pricing/european-call",
    json={
        "spot_price": 100.0,
        "strike_price": 105.0,
        "risk_free_rate": 0.05,
        "volatility": 0.2,
        "maturity_years": 1.0,
    }
)

result = response.json()
print(f"Option Price: ${result['estimated_price']:.4f}")

# Batch pricing
response = requests.post(
    f"{BASE_URL}/api/pricing/batch",
    json={
        "options": [
            {"spot_price": 100, "strike_price": 100, "risk_free_rate": 0.05, "volatility": 0.2, "maturity_years": 1},
            {"spot_price": 100, "strike_price": 105, "risk_free_rate": 0.05, "volatility": 0.2, "maturity_years": 1},
        ]
    }
)

results = response.json()
print(f"Priced {results['total_options']} options")
```

## Advanced Examples

### Example 1: Comparing Classical and Quantum

```python
from qrisklab.finance.pricing import EuropeanCallPricer
from qrisklab.quantum.algorithms import QuantumAmplitudeEstimation
import time

# Classical pricing
pricer = EuropeanCallPricer()
start = time.time()
classical = pricer.price(
    spot_price=100.0,
    strike_price=105.0,
    risk_free_rate=0.05,
    volatility=0.2,
    maturity_years=1.0,
    paths=10000
)
classical_time = time.time() - start

# Quantum pricing (placeholder)
qae = QuantumAmplitudeEstimation(backend="qiskit_aer")
start = time.time()
quantum = qae.run(
    oracle=lambda: None,
    num_qubits=10,
    shots=2048,
    precision_bits=5
)
quantum_time = time.time() - start

print(f"Classical Price: ${classical.estimated_price:.4f} ({classical_time:.3f}s)")
print(f"Quantum Estimate: {quantum.estimated_amplitude:.4f} ({quantum_time:.3f}s)")
print(f"Difference: {abs(classical.estimated_price - quantum.estimated_amplitude):.4f}")
```

### Example 2: Hybrid Workflow

```python
from qrisklab.finance.portfolio import Portfolio
from qrisklab.quantum.algorithms import VariationalQuantumEigensolver

# Build portfolio
portfolio = Portfolio(name="Hybrid Portfolio")
portfolio.add_position("Stock A", 50000, 0.08, 0.15)
portfolio.add_position("Stock B", 30000, 0.10, 0.20)
portfolio.add_position("Bonds", 20000, 0.03, 0.05)

# Get portfolio metrics
summary = portfolio.get_summary()
print(f"Classical Portfolio Return: {summary['expected_return']:.2%}")
print(f"Classical Portfolio Volatility: {summary['volatility']:.2%}")

# Optimize with quantum
vqe = VariationalQuantumEigensolver(backend="pennylane")
hamiltonian = [
    (-summary['expected_return'], "Z0"),
    (0.5 * summary['volatility'], "Z0Z1"),
]

result = vqe.run(
    hamiltonian=hamiltonian,
    num_qubits=3,
    max_iterations=150,
    learning_rate=0.02
)

print(f"Quantum Optimized Value: {result.eigenvalue:.6f}")
```

### Example 3: Real-time Dashboard Updates

```python
import streamlit as st
from qrisklab.finance.pricing import EuropeanCallPricer

st.title("Real-time Option Pricing")

# Sliders for parameters
spot = st.slider("Spot Price", 80.0, 120.0, 100.0)
strike = st.slider("Strike Price", 80.0, 120.0, 105.0)
rate = st.slider("Risk-Free Rate", 0.0, 0.1, 0.05)
vol = st.slider("Volatility", 0.1, 0.5, 0.2)
maturity = st.slider("Maturity (years)", 0.1, 5.0, 1.0)

# Calculate price
pricer = EuropeanCallPricer()
result = pricer.price(spot, strike, rate, vol, maturity)

# Display results
col1, col2, col3 = st.columns(3)
col1.metric("Option Price", f"${result.estimated_price:.4f}")
col2.metric("Standard Error", f"${result.standard_error:.6f}")
col3.metric("Intrinsic Value", f"${max(spot - strike, 0):.4f}")
```

---

**Last Updated:** 2026-06-19
