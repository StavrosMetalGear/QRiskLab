# Architecture Guide

System design and architecture of QRiskLab Pro.

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Module Descriptions](#module-descriptions)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Performance Considerations](#performance-considerations)

## System Overview

QRiskLab Pro is a hybrid quantum-classical framework with three main layers:

1. **User Interface Layer** - Streamlit dashboard, FastAPI REST API, Python library
2. **Application Layer** - Finance, quantum, and portfolio modules
3. **Core Layer** - High-performance C++ implementations with Python bindings

### Key Characteristics

- **Modular Design** - Independent, reusable components
- **Hybrid Architecture** - Quantum and classical algorithms
- **High Performance** - C++ core with Python interface
- **Extensible** - Easy to add new algorithms and backends
- **Well-Tested** - Comprehensive test coverage

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Interfaces                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  Streamlit       │  │  FastAPI         │  │  Python      │  │
│  │  Dashboard       │  │  REST API        │  │  Library     │  │
│  │  (Web UI)        │  │  (HTTP)          │  │  (Direct)    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Python Application Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  Finance         │  │  Quantum         │  │  Portfolio   │  │
│  │  • Pricing       │  │  • Algorithms    │  │  • Management│  │
│  │  • Risk          │  │  • Backends      │  │  • Analysis  │  │
│  │  • Portfolio     │  │  • State         │  │              │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Utilities & Configuration                               │  │
│  │  • Logging  • Timing  • Config  • Error Handling         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    C++ Core Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  QuantumState    │  │  MonteCarlo      │  │  RiskMetrics │  │
│  │  • State Vector  │  │  • Pricing       │  │  • VaR       │  │
│  │  • Gates         │  │  • Simulation    │  │  • CVaR      │  │
│  │  • Measurement   │  │  • Paths         │  │  • Stats     │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Utilities                                               │  │
│  │  • Logger  • Timer  • Random Number Generation           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### User Interface Layer

#### Streamlit Dashboard (`qrisklab/app/`)
- **Purpose:** Interactive web interface for end users
- **Components:**
  - `dashboard.py` - Main application and navigation
  - `pages/pricing.py` - Option pricing interface
  - `pages/risk_analysis.py` - Risk metrics calculation
  - `pages/quantum.py` - Quantum algorithm execution
  - `pages/portfolio.py` - Portfolio management
- **Technology:** Streamlit, Plotly, Pandas

#### FastAPI REST API (`qrisklab/api/`)
- **Purpose:** HTTP API for programmatic access
- **Components:**
  - `main.py` - Application factory and middleware
  - `models.py` - Pydantic request/response models
  - `routes/pricing.py` - Pricing endpoints
  - `routes/risk.py` - Risk analysis endpoints
  - `routes/quantum.py` - Quantum algorithm endpoints
- **Technology:** FastAPI, Pydantic, Uvicorn

#### Python Library
- **Purpose:** Direct Python API for developers
- **Usage:** `from qrisklab.finance import EuropeanCallPricer`
- **Technology:** Pure Python with C++ bindings

### Application Layer

#### Finance Module (`qrisklab/finance/`)
- **pricing.py** - `EuropeanCallPricer` class
  - Wraps C++ MonteCarlo implementation
  - Provides caching and validation
  - Supports batch operations and sensitivity analysis
  
- **risk.py** - `RiskAnalyzer` class
  - Wraps C++ RiskMetrics implementation
  - Calculates VaR and CVaR
  - Supports multi-level analysis
  
- **portfolio.py** - `Portfolio` class
  - Portfolio construction and management
  - Position tracking and weighting
  - Risk simulation and analysis

#### Quantum Module (`qrisklab/quantum/`)
- **algorithms.py** - Quantum algorithm implementations
  - `QuantumAmplitudeEstimation` - QAE for pricing
  - `VariationalQuantumEigensolver` - VQE for optimization
  - `QuantumPhaseEstimation` - QPE for eigenvalues
  
- **backends.py** - Backend factory and management
  - `BackendFactory` - Backend selection and initialization
  - Support for Qiskit, PennyLane, Cirq, Amazon Braket
  - Graceful fallback for unavailable backends
  
- **state.py** - Quantum state management (future)
  - Quantum state wrapper
  - State visualization and serialization

#### Utilities (`qrisklab/utils/`)
- **logger.py** - Unified logging interface
  - Console and file output
  - Configurable log levels
  - Integration with C++ logger
  
- **timing.py** - Performance measurement
  - `@timer` decorator for functions
  - `timed_block()` context manager
  - `Timer` class for manual timing

### Core Layer (C++)

#### QuantumState (`src/core/QuantumState.cpp`)
- State vector representation
- Quantum gate operations (Hadamard, CNOT)
- Measurement and probability calculation
- State serialization

#### MonteCarlo (`src/finance/MonteCarlo.cpp`)
- European call option pricing
- Portfolio loss simulation
- Random number generation
- Path generation and aggregation

#### RiskMetrics (`src/finance/RiskMetrics.cpp`)
- Value at Risk calculation
- Conditional Value at Risk calculation
- Statistical analysis
- Percentile computation

## Data Flow

### Option Pricing Flow

```
User Input (Streamlit/API)
    ↓
EuropeanCallPricer.price()
    ↓
Input Validation (PricingParameters)
    ↓
Cache Check
    ├─ Hit → Return cached result
    └─ Miss → Continue
    ↓
MonteCarlo.price_european_call() [C++]
    ├─ Initialize random number generator
    ├─ Generate paths
    ├─ Calculate payoffs
    └─ Compute statistics
    ↓
OptionPricingResult
    ↓
Cache Storage
    ↓
Return to User
```

### Risk Analysis Flow

```
Portfolio Losses (Array)
    ↓
RiskAnalyzer.analyze_risk()
    ↓
Input Validation
    ↓
RiskMetrics.value_at_risk() [C++]
    ├─ Sort losses
    ├─ Find percentile
    └─ Return VaR
    ↓
RiskMetrics.conditional_value_at_risk() [C++]
    ├─ Find losses beyond VaR
    ├─ Calculate mean
    └─ Return CVaR
    ↓
Statistical Calculations
    ├─ Min/Max
    ├─ Mean
    └─ Standard Deviation
    ↓
RiskMetricsResult
    ↓
Return to User
```

### Quantum Algorithm Flow

```
Algorithm Parameters
    ↓
BackendFactory.get_backend()
    ├─ Check availability
    └─ Return backend instance
    ↓
QuantumAlgorithm.run()
    ├─ Validate parameters
    ├─ Initialize quantum circuit
    ├─ Apply gates/operations
    ├─ Measure
    └─ Aggregate results
    ↓
AlgorithmResult
    ├─ Success flag
    ├─ Results
    ├─ Execution time
    └─ Metadata
    ↓
Return to User
```

## Design Patterns

### Factory Pattern

**BackendFactory** - Creates and manages quantum backends
```python
backend = BackendFactory.get_backend("qiskit_aer")
```

### Wrapper Pattern

**EuropeanCallPricer** - Wraps C++ MonteCarlo
```python
pricer = EuropeanCallPricer()
result = pricer.price(...)  # Calls C++ implementation
```

### Strategy Pattern

**QuantumAlgorithm** - Different algorithm implementations
```python
algorithm = QuantumAmplitudeEstimation(backend="qiskit_aer")
result = algorithm.run(...)
```

### Singleton Pattern

**Configuration** - Single config instance
```python
from qrisklab.config import config
print(config.QUANTUM_BACKEND)
```

### Context Manager Pattern

**Timing** - Automatic timing measurement
```python
with timed_block("operation"):
    # Code to time
    pass
```

## Performance Considerations

### Optimization Strategies

1. **C++ Core** - Computationally intensive operations in C++
2. **Caching** - Results cached to avoid recomputation
3. **Batch Operations** - Process multiple items efficiently
4. **Lazy Loading** - Quantum backends loaded on demand
5. **Vectorization** - NumPy/SciPy for array operations

### Scalability

| Component | Scalability | Bottleneck |
|-----------|-------------|-----------|
| Option Pricing | O(paths) | Monte Carlo paths |
| Risk Analysis | O(n log n) | Sorting losses |
| Quantum Algorithms | O(2^qubits) | Quantum state size |
| Portfolio | O(positions) | Position count |

### Memory Usage

- **Option Pricing:** ~8 bytes per path
- **Risk Analysis:** ~8 bytes per loss sample
- **Quantum State:** 16 bytes per basis state (2^qubits)
- **Portfolio:** ~100 bytes per position

### Optimization Tips

1. Reduce Monte Carlo paths for speed
2. Use batch operations for multiple calculations
3. Cache results when possible
4. Adjust quantum precision based on accuracy needs
5. Use appropriate data types (float32 vs float64)

## Extension Points

### Adding New Algorithms

1. Create class inheriting from `QuantumAlgorithm`
2. Implement `run()` method
3. Return `AlgorithmResult` subclass
4. Add to `qrisklab/quantum/algorithms.py`

### Adding New Backends

1. Create class inheriting from `QuantumBackend`
2. Implement `_check_availability()` and `get_info()`
3. Register in `BackendFactory`
4. Add to `qrisklab/quantum/backends.py`

### Adding New Risk Metrics

1. Implement calculation in C++ (`src/finance/RiskMetrics.cpp`)
2. Create Python wrapper in `qrisklab/finance/risk.py`
3. Add API endpoint in `qrisklab/api/routes/risk.py`
4. Add dashboard page in `qrisklab/app/pages/`

## Testing Architecture

```
tests/
├── unit/
│   ├── test_config.py
│   ├── test_finance.py
│   ├── test_quantum.py
│   └── test_utils.py
└── integration/
    ├── test_api.py
    └── test_dashboard.py
```

- **Unit Tests** - Test individual components
- **Integration Tests** - Test component interactions
- **Fixtures** - Reusable test objects
- **Mocking** - Mock C++ bindings for testing

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Load Balancer (Optional)        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│    API Server (Uvicorn/Gunicorn)       │
│    • Multiple workers                   │
│    • Health checks                      │
│    • Logging                            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│    Application Layer (Python)           │
│    • Finance modules                    │
│    • Quantum algorithms                 │
│    • Portfolio management               │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│    C++ Core (Compiled Extensions)       │
│    • QuantumState                       │
│    • MonteCarlo                         │
│    • RiskMetrics                        │
└─────────────────────────────────────────┘
```

---

**Last Updated:** 2026-06-19
