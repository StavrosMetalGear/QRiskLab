# REST API Reference

Complete documentation for the QRiskLab Pro REST API.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Endpoints](#endpoints)

## Overview

The QRiskLab Pro REST API provides endpoints for:
- European call option pricing
- Risk metrics calculation (VaR, CVaR)
- Quantum algorithm execution
- Portfolio analysis

Built with FastAPI and automatically documented with Swagger UI.

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

**Note:** For production deployments, implement authentication (API keys, OAuth2, etc.)

## Base URL

```
http://127.0.0.1:8000
```

For production, replace with your deployment URL.

## Response Format

All responses are JSON with the following structure:

### Success Response

```json
{
  "data": { /* response data */ },
  "status": "success",
  "timestamp": "2026-06-19T12:00:00Z"
}
```

### Error Response

```json
{
  "error": "ErrorType",
  "message": "Human-readable error message",
  "details": { /* optional error details */ },
  "timestamp": "2026-06-19T12:00:00Z"
}
```

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid parameters |
| 404 | Not Found | Endpoint not found |
| 500 | Internal Server Error | Server error |

### Error Response Example

```json
{
  "error": "ValueError",
  "message": "Spot price must be positive",
  "details": {
    "field": "spot_price",
    "value": -100.0
  }
}
```

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "message": "QRiskLab API is running"
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/health
```

---

### Pricing Endpoints

#### POST /api/pricing/european-call

Price a single European call option.

**Request Body:**
```json
{
  "spot_price": 100.0,
  "strike_price": 105.0,
  "risk_free_rate": 0.05,
  "volatility": 0.2,
  "maturity_years": 1.0,
  "paths": 10000,
  "seed": 42
}
```

**Response:**
```json
{
  "estimated_price": 5.234,
  "standard_error": 0.045,
  "paths": 10000,
  "spot_price": 100.0,
  "strike_price": 105.0
}
```

**Parameters:**
- `spot_price` (float, required): Current stock price (> 0)
- `strike_price` (float, required): Option strike price (> 0)
- `risk_free_rate` (float, required): Risk-free interest rate (≥ 0)
- `volatility` (float, required): Stock volatility, annualized (> 0)
- `maturity_years` (float, required): Time to maturity in years (> 0)
- `paths` (int, optional): Number of Monte Carlo paths (default: 10000, ≥ 100)
- `seed` (int, optional): Random seed for reproducibility (default: 42)

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/pricing/european-call \
  -H "Content-Type: application/json" \
  -d '{
    "spot_price": 100.0,
    "strike_price": 105.0,
    "risk_free_rate": 0.05,
    "volatility": 0.2,
    "maturity_years": 1.0
  }'
```

---

#### POST /api/pricing/batch

Price multiple European call options.

**Request Body:**
```json
{
  "options": [
    {
      "spot_price": 100.0,
      "strike_price": 105.0,
      "risk_free_rate": 0.05,
      "volatility": 0.2,
      "maturity_years": 1.0
    },
    {
      "spot_price": 100.0,
      "strike_price": 95.0,
      "risk_free_rate": 0.05,
      "volatility": 0.2,
      "maturity_years": 1.0
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "estimated_price": 5.234,
      "standard_error": 0.045,
      "paths": 10000,
      "spot_price": 100.0,
      "strike_price": 105.0
    },
    {
      "estimated_price": 7.891,
      "standard_error": 0.052,
      "paths": 10000,
      "spot_price": 100.0,
      "strike_price": 95.0
    }
  ],
  "total_options": 2
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/pricing/batch \
  -H "Content-Type: application/json" \
  -d '{
    "options": [
      {"spot_price": 100.0, "strike_price": 105.0, "risk_free_rate": 0.05, "volatility": 0.2, "maturity_years": 1.0},
      {"spot_price": 100.0, "strike_price": 95.0, "risk_free_rate": 0.05, "volatility": 0.2, "maturity_years": 1.0}
    ]
  }'
```

---

#### POST /api/pricing/sensitivity

Perform sensitivity analysis on option pricing.

**Request Body:**
```json
{
  "spot_price": 100.0,
  "strike_price": 105.0,
  "risk_free_rate": 0.05,
  "volatility": 0.2,
  "maturity_years": 1.0,
  "parameter": "spot_price",
  "range_pct": 0.2,
  "steps": 5
}
```

**Response:**
```json
{
  "parameter": "spot_price",
  "results": {
    "80.0": 0.123,
    "90.0": 1.456,
    "100.0": 5.234,
    "110.0": 10.891,
    "120.0": 17.234
  },
  "base_price": 5.234
}
```

**Parameters:**
- `parameter` (string): Parameter to vary: "spot_price", "volatility", or "risk_free_rate"
- `range_pct` (float): Range as percentage (0.01 to 1.0, default: 0.2 for ±20%)
- `steps` (int): Number of steps in range (3 to 20, default: 5)

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/pricing/sensitivity \
  -H "Content-Type: application/json" \
  -d '{
    "spot_price": 100.0,
    "strike_price": 105.0,
    "risk_free_rate": 0.05,
    "volatility": 0.2,
    "maturity_years": 1.0,
    "parameter": "volatility",
    "range_pct": 0.3,
    "steps": 7
  }'
```

---

### Risk Analysis Endpoints

#### POST /api/risk/analyze

Calculate comprehensive risk metrics (VaR and CVaR).

**Request Body:**
```json
{
  "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
  "confidence_level": 0.95
}
```

**Response:**
```json
{
  "var": 75.5,
  "cvar": 112.3,
  "confidence_level": 0.95,
  "sample_count": 10,
  "min_loss": -150.0,
  "max_loss": 200.0,
  "mean_loss": 0.5,
  "std_loss": 125.3
}
```

**Parameters:**
- `losses` (array of floats, required): Portfolio losses
- `confidence_level` (float, required): Confidence level (0.01 to 0.99, default: 0.95)

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/risk/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
    "confidence_level": 0.95
  }'
```

---

#### POST /api/risk/var

Calculate Value at Risk (VaR).

**Request Body:**
```json
{
  "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
  "confidence_level": 0.95
}
```

**Response:**
```json
75.5
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/risk/var \
  -H "Content-Type: application/json" \
  -d '{
    "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
    "confidence_level": 0.95
  }'
```

---

#### POST /api/risk/cvar

Calculate Conditional Value at Risk (CVaR / Expected Shortfall).

**Request Body:**
```json
{
  "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
  "confidence_level": 0.95
}
```

**Response:**
```json
112.3
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/risk/cvar \
  -H "Content-Type: application/json" \
  -d '{
    "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
    "confidence_level": 0.95
  }'
```

---

#### POST /api/risk/multi-level

Perform risk analysis at multiple confidence levels.

**Request Body:**
```json
{
  "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
  "confidence_levels": [0.90, 0.95, 0.99]
}
```

**Response:**
```json
{
  "results": {
    "0.9": {
      "var": 50.0,
      "cvar": 87.5,
      "confidence_level": 0.9,
      "sample_count": 10,
      "min_loss": -150.0,
      "max_loss": 200.0,
      "mean_loss": 0.5,
      "std_loss": 125.3
    },
    "0.95": {
      "var": 75.5,
      "cvar": 112.3,
      "confidence_level": 0.95,
      "sample_count": 10,
      "min_loss": -150.0,
      "max_loss": 200.0,
      "mean_loss": 0.5,
      "std_loss": 125.3
    },
    "0.99": {
      "var": 150.0,
      "cvar": 175.0,
      "confidence_level": 0.99,
      "sample_count": 10,
      "min_loss": -150.0,
      "max_loss": 200.0,
      "mean_loss": 0.5,
      "std_loss": 125.3
    }
  }
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/risk/multi-level \
  -H "Content-Type: application/json" \
  -d '{
    "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
    "confidence_levels": [0.90, 0.95, 0.99]
  }'
```

---

### Quantum Endpoints

#### GET /api/quantum/backends

List available quantum backends.

**Response:**
```json
{
  "available_backends": ["qiskit_aer", "pennylane", "cirq"],
  "default_backend": "qiskit_aer",
  "backend_info": {
    "qiskit_aer": {
      "name": "qiskit_aer",
      "version": "0.14.0",
      "type": "simulator",
      "status": "available"
    },
    "pennylane": {
      "name": "pennylane",
      "version": "0.35.0",
      "type": "hybrid",
      "status": "available"
    },
    "cirq": {
      "name": "cirq",
      "version": "1.3.0",
      "type": "simulator",
      "status": "available"
    }
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/quantum/backends
```

---

#### POST /api/quantum/amplitude-estimation

Run quantum amplitude estimation algorithm.

**Request Body:**
```json
{
  "num_qubits": 5,
  "shots": 1024,
  "precision_bits": 3,
  "backend": "qiskit_aer"
}
```

**Response:**
```json
{
  "algorithm_name": "QuantumAmplitudeEstimation",
  "success": true,
  "iterations": 3,
  "execution_time_seconds": 0.234,
  "result": {
    "estimated_amplitude": 0.5,
    "confidence_interval": [0.45, 0.55],
    "shots": 1024
  },
  "metadata": {}
}
```

**Example:**
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

---

#### POST /api/quantum/vqe

Run Variational Quantum Eigensolver (VQE) algorithm.

**Request Body:**
```json
{
  "num_qubits": 5,
  "shots": 1024,
  "precision_bits": 3,
  "backend": "pennylane"
}
```

**Response:**
```json
{
  "algorithm_name": "VariationalQuantumEigensolver",
  "success": true,
  "iterations": 100,
  "execution_time_seconds": 1.234,
  "result": {
    "eigenvalue": -1.0,
    "parameters": [0.0, 0.0, 0.0, 0.0, 0.0]
  },
  "metadata": {}
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/quantum/vqe \
  -H "Content-Type: application/json" \
  -d '{
    "num_qubits": 5,
    "shots": 1024,
    "precision_bits": 3,
    "backend": "pennylane"
  }'
```

---

#### POST /api/quantum/phase-estimation

Run quantum phase estimation algorithm.

**Request Body:**
```json
{
  "num_qubits": 5,
  "shots": 1024,
  "precision_bits": 5,
  "backend": "qiskit_aer"
}
```

**Response:**
```json
{
  "algorithm_name": "QuantumPhaseEstimation",
  "success": true,
  "iterations": 5,
  "execution_time_seconds": 0.567,
  "result": {
    "phase": 0.25,
    "eigenvalue": 1.5708,
    "precision_bits": 5
  },
  "metadata": {}
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/quantum/phase-estimation \
  -H "Content-Type: application/json" \
  -d '{
    "num_qubits": 5,
    "shots": 1024,
    "precision_bits": 5,
    "backend": "qiskit_aer"
  }'
```

---

## Interactive API Documentation

Access the interactive API documentation at:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
- **OpenAPI Schema:** `http://127.0.0.1:8000/openapi.json`

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider implementing:
- Request rate limiting
- Concurrent request limits
- Timeout policies

## Versioning

API version: `0.1.0`

Future versions will maintain backward compatibility where possible.

## Support

For API issues or questions:
- Check [GitHub Issues](https://github.com/qrisklab/qrisklab/issues)
- Review [Quick Start Guide](QUICKSTART.md)
- See [Examples](EXAMPLES.md)

---

**Last Updated:** 2026-06-19
