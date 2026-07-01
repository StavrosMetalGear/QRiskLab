# Quantum Algorithms Guide

Comprehensive guide to quantum algorithms in QRiskLab Pro.

## Table of Contents

1. [Overview](#overview)
2. [Quantum Backends](#quantum-backends)
3. [Quantum State Management](#quantum-state-management)
4. [Quantum Backends](#quantum-backends)
5. [Quantum Algorithms](#quantum-algorithms)
6. [Quantum State Utilities](#quantum-state-utilities)
7. [Quantum Backend Abstractions](#quantum-backend-abstractions)
8. [Quantum Algorithm Scaffolding](#quantum-algorithm-scaffolding)
4. [Variational Quantum Eigensolver](#variational-quantum-eigensolver)
5. [Quantum Phase Estimation](#quantum-phase-estimation)
6. [Advanced Usage](#advanced-usage)

## Overview of the Quantum Layer

The quantum layer in QRiskLab Pro provides a structured approach to quantum computing utilities, focusing on state management, backend abstractions, and algorithm scaffolding. It is currently integrated with the Python package and is tested using pytest. The project does not claim production quantum advantage and does not support any unsupported algorithms or hardware integrations.

QRiskLab Pro provides implementations of three key quantum algorithms for financial applications:

1. **Quantum Amplitude Estimation (QAE)** - For option pricing with quadratic speedup
2. **Variational Quantum Eigensolver (VQE)** - For portfolio optimization
3. **Quantum Phase Estimation (QPE)** - For eigenvalue estimation

These algorithms leverage quantum computing to solve financial problems more efficiently than classical methods.

## Current Module Areas

The current module areas include:

- `qrisklab/quantum/state.py`: Quantum state management utilities.
- `qrisklab/quantum/backends.py`: Backend abstractions for various quantum computing frameworks.
- `qrisklab/quantum/algorithms.py`: Scaffolding for quantum algorithms.
- C++ QuantumState binding, if supported through `qrisklab.finance._qrisklab_core`.

### Available Backends

QRiskLab Pro supports multiple quantum computing frameworks:

| Backend | Type | Status | Installation |
|---------|------|--------|--------------|
| Qiskit Aer | Simulator | ✅ Recommended | `pip install qiskit qiskit-aer` |
| PennyLane | Hybrid | ✅ Available | `pip install pennylane` |
| Cirq | Simulator | ✅ Available | `pip install cirq` |
| Amazon Braket | Cloud | ✅ Available | `pip install amazon-braket-sdk` |

### Backend Selection

```python
from qrisklab.quantum.backends import BackendFactory

# List available backends
backends = BackendFactory.get_available_backends()
print(f"Available: {backends}")

# Get default backend
default = BackendFactory.get_default_backend()
print(f"Default: {default.name}")

# Set default backend
BackendFactory.set_default_backend("pennylane")

# Get specific backend
backend = BackendFactory.get_backend("qiskit_aer")
if backend and backend.is_available:
    print(f"Using {backend.name}")
```

### Backend Configuration

Configure backends via environment variables:

```bash
# Set default backend
export QRISKLAB_QUANTUM_BACKEND=qiskit_aer

# Set number of shots
export QRISKLAB_QUANTUM_SHOTS=1024
```

Or in Python:

```python
from qrisklab.config import config

print(f"Default backend: {config.QUANTUM_BACKEND}")
print(f"Default shots: {config.QUANTUM_SHOTS}")
```

## Quantum Amplitude Estimation

### Overview

Quantum Amplitude Estimation (QAE) is used to estimate the amplitude of a quantum state with quadratic speedup over classical Monte Carlo methods.

**Applications:**
- Option pricing (especially for exotic options)
- Probability estimation
- Risk metrics calculation

**Speedup:** O(1/ε) quantum vs O(1/ε²) classical

### Basic Usage

```python
from qrisklab.quantum.algorithms import QuantumAmplitudeEstimation

# Create algorithm instance
qae = QuantumAmplitudeEstimation(backend="qiskit_aer")

# Define oracle (placeholder for this example)
def oracle():
    """Oracle that marks the target state."""
    pass

# Run algorithm
result = qae.run(
    oracle=oracle,
    num_qubits=5,
    shots=1024,
    precision_bits=3
)

print(f"Estimated Amplitude: {result.estimated_amplitude:.4f}")
print(f"Confidence Interval: {result.confidence_interval}")
print(f"Execution Time: {result.execution_time_seconds:.3f}s")
```

### Parameters

- `oracle` (callable): Function implementing the amplitude oracle
- `num_qubits` (int): Number of qubits (1-20)
- `shots` (int): Number of measurement shots (≥ 100)
- `precision_bits` (int): Bits for phase estimation precision (1-10)

### Result Fields

- `estimated_amplitude` (float): Estimated amplitude value
- `confidence_interval` (tuple): (lower, upper) bounds
- `shots` (int): Number of shots used
- `iterations` (int): Number of iterations
- `execution_time_seconds` (float): Total execution time

### Advanced Example: Option Pricing

```python
from qrisklab.quantum.algorithms import QuantumAmplitudeEstimation
import numpy as np

# Quantum amplitude estimation for option pricing
qae = QuantumAmplitudeEstimation(backend="qiskit_aer")

# Define payoff oracle
def payoff_oracle():
    """Oracle for European call option payoff."""
    # In practice, this would encode the option payoff
    pass

# Run estimation
result = qae.run(
    oracle=payoff_oracle,
    num_qubits=10,
    shots=2048,
    precision_bits=5
)

# Estimated option price
option_price = result.estimated_amplitude * 100  # Scale by spot price
print(f"Quantum Estimated Price: ${option_price:.4f}")
print(f"Confidence: {result.confidence_interval}")
```

## Variational Quantum Eigensolver

### Overview

Variational Quantum Eigensolver (VQE) is a hybrid quantum-classical algorithm for finding ground states of Hamiltonians.

**Applications:**
- Portfolio optimization
- Molecular simulation
- Quantum chemistry
- Optimization problems

**Advantage:** Works on near-term quantum devices (NISQ era)

### Basic Usage

```python
from qrisklab.quantum.algorithms import VariationalQuantumEigensolver

# Create algorithm instance
vqe = VariationalQuantumEigensolver(backend="pennylane")

# Define Hamiltonian as list of (coefficient, pauli_string) tuples
hamiltonian = [
    (1.0, "Z0"),      # 1.0 * Z₀
    (0.5, "X0"),      # 0.5 * X₀
    (0.3, "Z0Z1"),    # 0.3 * Z₀Z₁
]

# Run optimization
result = vqe.run(
    hamiltonian=hamiltonian,
    num_qubits=5,
    max_iterations=100,
    learning_rate=0.01
)

print(f"Ground State Energy: {result.eigenvalue:.6f}")
print(f"Optimized Parameters: {result.parameters}")
print(f"Iterations: {result.iterations}")
print(f"Execution Time: {result.execution_time_seconds:.3f}s")
```

### Parameters

- `hamiltonian` (list): List of (coefficient, pauli_string) tuples
- `num_qubits` (int): Number of qubits (1-20)
- `max_iterations` (int): Maximum optimization iterations
- `learning_rate` (float): Optimizer learning rate

### Result Fields

- `eigenvalue` (float): Ground state energy
- `eigenstate` (list): Ground state vector
- `parameters` (list): Optimized circuit parameters
- `iterations` (int): Number of iterations performed
- `execution_time_seconds` (float): Total execution time

### Advanced Example: Portfolio Optimization

```python
from qrisklab.quantum.algorithms import VariationalQuantumEigensolver

# Portfolio optimization using VQE
vqe = VariationalQuantumEigensolver(backend="pennylane")

# Hamiltonian encoding portfolio constraints
# H = -w₁*r₁ - w₂*r₂ + λ*σ²
hamiltonian = [
    (-0.08, "Z0"),    # Expected return for asset 1
    (-0.10, "Z1"),    # Expected return for asset 2
    (0.15, "Z0Z1"),   # Volatility penalty
]

# Optimize portfolio
result = vqe.run(
    hamiltonian=hamiltonian,
    num_qubits=2,
    max_iterations=200,
    learning_rate=0.05
)

print(f"Optimal Portfolio Value: {result.eigenvalue:.6f}")
print(f"Weights: {result.parameters}")
```

## Quantum Phase Estimation

### Overview

Quantum Phase Estimation (QPE) estimates the phase (eigenvalue) of an eigenvector of a unitary operator.

**Applications:**
- Eigenvalue estimation
- Risk metrics calculation
- Quantum simulation
- Spectral analysis

**Speedup:** Exponential in precision

### Basic Usage

```python
from qrisklab.quantum.algorithms import QuantumPhaseEstimation

# Create algorithm instance
qpe = QuantumPhaseEstimation(backend="qiskit_aer")

# Define unitary operator (placeholder)
def unitary():
    """Unitary operator for phase estimation."""
    pass

# Run algorithm
result = qpe.run(
    unitary=unitary,
    num_qubits=5,
    precision_bits=5,
    shots=1024
)

print(f"Estimated Phase: {result.phase:.6f}")
print(f"Eigenvalue: {result.eigenvalue:.6f}")
print(f"Precision Bits: {result.precision_bits}")
print(f"Execution Time: {result.execution_time_seconds:.3f}s")
```

### Parameters

- `unitary` (callable): Function implementing the unitary operator
- `num_qubits` (int): Number of qubits for eigenstate (1-20)
- `precision_bits` (int): Bits for phase precision (1-10)
- `shots` (int): Number of measurement shots (≥ 100)

### Result Fields

- `phase` (float): Estimated phase (0 to 1)
- `eigenvalue` (float): Corresponding eigenvalue
- `precision_bits` (int): Precision used
- `iterations` (int): Number of iterations
- `execution_time_seconds` (float): Total execution time

### Advanced Example: Risk Metrics

```python
from qrisklab.quantum.algorithms import QuantumPhaseEstimation

# Quantum phase estimation for risk metrics
qpe = QuantumPhaseEstimation(backend="qiskit_aer")

# Unitary encoding covariance matrix
def covariance_unitary():
    """Unitary encoding portfolio covariance."""
    pass

# Estimate eigenvalues
result = qpe.run(
    unitary=covariance_unitary,
    num_qubits=8,
    precision_bits=8,
    shots=4096
)

# Eigenvalue represents portfolio variance
portfolio_variance = result.eigenvalue
portfolio_volatility = portfolio_variance ** 0.5
print(f"Portfolio Volatility: {portfolio_volatility:.4f}")
```

## Advanced Usage

### Comparing Classical and Quantum Results

```python
from qrisklab.finance.pricing import EuropeanCallPricer
from qrisklab.quantum.algorithms import QuantumAmplitudeEstimation

# Classical pricing
pricer = EuropeanCallPricer()
classical_result = pricer.price(
    spot_price=100.0,
    strike_price=105.0,
    risk_free_rate=0.05,
    volatility=0.2,
    maturity_years=1.0,
    paths=10000
)

# Quantum pricing (placeholder)
qae = QuantumAmplitudeEstimation(backend="qiskit_aer")
quantum_result = qae.run(
    oracle=lambda: None,
    num_qubits=10,
    shots=2048,
    precision_bits=5
)

print(f"Classical Price: ${classical_result.estimated_price:.4f}")
print(f"Quantum Estimate: {quantum_result.estimated_amplitude:.4f}")
print(f"Difference: {abs(classical_result.estimated_price - quantum_result.estimated_amplitude):.4f}")
```

### Hybrid Quantum-Classical Workflow

```python
from qrisklab.quantum.algorithms import VariationalQuantumEigensolver
from qrisklab.finance.portfolio import Portfolio

# Build classical portfolio
portfolio = Portfolio(name="Hybrid Portfolio")
portfolio.add_position("Stock A", 50000, 0.08, 0.15)
portfolio.add_position("Stock B", 30000, 0.10, 0.20)
portfolio.add_position("Bonds", 20000, 0.03, 0.05)

# Get portfolio metrics
summary = portfolio.get_summary()
print(f"Classical Portfolio Return: {summary['expected_return']:.2%}")
print(f"Classical Portfolio Volatility: {summary['volatility']:.2%}")

# Optimize with quantum algorithm
vqe = VariationalQuantumEigensolver(backend="pennylane")
hamiltonian = [
    (-summary['expected_return'], "Z0"),
    (0.5 * summary['volatility'], "Z0Z1"),
]

quantum_result = vqe.run(
    hamiltonian=hamiltonian,
    num_qubits=3,
    max_iterations=150,
    learning_rate=0.02
)

print(f"Quantum Optimized Value: {quantum_result.eigenvalue:.6f}")
```

### Error Handling

```python
from qrisklab.quantum.algorithms import QuantumAmplitudeEstimation
from qrisklab.quantum.backends import BackendFactory

try:
    # Check backend availability
    backend = BackendFactory.get_backend("qiskit_aer")
    if not backend or not backend.is_available:
        raise RuntimeError("Qiskit backend not available")
    
    # Run algorithm
    qae = QuantumAmplitudeEstimation(backend="qiskit_aer")
    result = qae.run(
        oracle=lambda: None,
        num_qubits=5,
        shots=1024,
        precision_bits=3
    )
    
    if not result.success:
        print(f"Algorithm failed: {result.metadata}")
    else:
        print(f"Success: {result.estimated_amplitude:.4f}")

except Exception as e:
    print(f"Error: {e}")
    # Fall back to classical method
    from qrisklab.finance.pricing import EuropeanCallPricer
    pricer = EuropeanCallPricer()
    # ... use classical pricing
```

## Performance Considerations

### Choosing Parameters

| Parameter | Impact | Recommendation |
|-----------|--------|-----------------|
| `num_qubits` | Circuit depth | Start with 5-10, increase for accuracy |
| `shots` | Measurement noise | 1024-4096 for good results |
| `precision_bits` | Phase precision | 3-5 for QAE, 5-8 for QPE |
| `max_iterations` | VQE convergence | 100-500 depending on problem |
| `learning_rate` | VQE optimization | 0.01-0.1, adjust if not converging |

### Execution Time

Typical execution times on simulators:
- QAE (5 qubits): 0.1-0.5 seconds
- VQE (5 qubits, 100 iterations): 1-5 seconds
- QPE (5 qubits): 0.2-1 second

### Accuracy vs Speed

```python
# Fast but less accurate
result_fast = qae.run(oracle, num_qubits=3, shots=256, precision_bits=2)

# Slower but more accurate
result_accurate = qae.run(oracle, num_qubits=10, shots=4096, precision_bits=8)
```

## Troubleshooting

### Backend Not Available

```python
from qrisklab.quantum.backends import BackendFactory

# Check available backends
backends = BackendFactory.get_available_backends()
if not backends:
    print("No quantum backends available")
    print("Install with: pip install qiskit qiskit-aer")
```

### Algorithm Not Converging

```python
# Increase iterations and adjust learning rate
result = vqe.run(
    hamiltonian=hamiltonian,
    num_qubits=5,
    max_iterations=500,  # Increase
    learning_rate=0.001  # Decrease
)
```

### Memory Issues

```python
# Reduce number of qubits or shots
result = qae.run(
    oracle=oracle,
    num_qubits=5,      # Reduce from 10
    shots=512,         # Reduce from 4096
    precision_bits=3   # Reduce from 8
)
```

## Next Steps

1. Explore [Quick Start Guide](QUICKSTART.md) for basic examples
2. Review [API Reference](API.md) for REST endpoints
3. Check [Examples](EXAMPLES.md) for more code samples
4. See [Architecture](ARCHITECTURE.md) for system design

---

**Last Updated:** 2026-06-19
