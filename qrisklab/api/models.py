"""
Pydantic models for API request/response validation.

Provides type-safe request and response models for all API endpoints
with automatic validation and documentation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict


# ============================================================================
# Health Check Models
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    message: str = Field(..., description="Status message")


# ============================================================================
# Pricing Models
# ============================================================================

class EuropeanCallRequest(BaseModel):
    """Request for European call option pricing."""
    spot_price: float = Field(..., gt=0, description="Current stock price")
    strike_price: float = Field(..., gt=0, description="Option strike price")
    risk_free_rate: float = Field(..., ge=0, description="Risk-free interest rate")
    volatility: float = Field(..., gt=0, description="Stock volatility (annualized)")
    maturity_years: float = Field(..., gt=0, description="Time to maturity in years")
    paths: int = Field(10000, ge=100, description="Number of Monte Carlo paths")
    seed: int = Field(42, description="Random seed for reproducibility")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "spot_price": 100.0,
            "strike_price": 105.0,
            "risk_free_rate": 0.05,
            "volatility": 0.2,
            "maturity_years": 1.0,
            "paths": 10000,
            "seed": 42,
        }
    })


class OptionPricingResponse(BaseModel):
    """Response for option pricing."""
    estimated_price: float = Field(..., description="Estimated option price")
    standard_error: float = Field(..., description="Standard error of the estimate")
    paths: int = Field(..., description="Number of Monte Carlo paths used")
    spot_price: float = Field(..., description="Input spot price")
    strike_price: float = Field(..., description="Input strike price")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "estimated_price": 5.234,
            "standard_error": 0.045,
            "paths": 10000,
            "spot_price": 100.0,
            "strike_price": 105.0,
        }
    })


class BatchPricingRequest(BaseModel):
    """Request for batch option pricing."""
    options: List[EuropeanCallRequest] = Field(..., description="List of options to price")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "options": [
                {
                    "spot_price": 100.0,
                    "strike_price": 105.0,
                    "risk_free_rate": 0.05,
                    "volatility": 0.2,
                    "maturity_years": 1.0,
                },
                {
                    "spot_price": 100.0,
                    "strike_price": 95.0,
                    "risk_free_rate": 0.05,
                    "volatility": 0.2,
                    "maturity_years": 1.0,
                },
            ]
        }
    })


class BatchPricingResponse(BaseModel):
    """Response for batch option pricing."""
    results: List[OptionPricingResponse] = Field(..., description="Pricing results")
    total_options: int = Field(..., description="Total options priced")


class SensitivityRequest(BaseModel):
    """Request for sensitivity analysis."""
    spot_price: float = Field(..., gt=0, description="Current stock price")
    strike_price: float = Field(..., gt=0, description="Option strike price")
    risk_free_rate: float = Field(..., ge=0, description="Risk-free interest rate")
    volatility: float = Field(..., gt=0, description="Stock volatility")
    maturity_years: float = Field(..., gt=0, description="Time to maturity")
    parameter: str = Field(
        "spot_price",
        description="Parameter to vary: 'spot_price', 'volatility', or 'risk_free_rate'"
    )
    range_pct: float = Field(0.2, ge=0.01, le=1.0, description="Range as percentage")
    steps: int = Field(5, ge=3, le=20, description="Number of steps in range")

    @field_validator("parameter")
    def validate_parameter(cls, v):
        if v not in ["spot_price", "volatility", "risk_free_rate"]:
            raise ValueError("Parameter must be 'spot_price', 'volatility', or 'risk_free_rate'")
        return v


class SensitivityResponse(BaseModel):
    """Response for sensitivity analysis."""
    parameter: str = Field(..., description="Parameter that was varied")
    results: Dict[float, float] = Field(..., description="Mapping of parameter values to prices")
    base_price: float = Field(..., description="Price at base parameter value")


# ============================================================================
# Risk Analysis Models
# ============================================================================

class RiskAnalysisRequest(BaseModel):
    """Request for risk analysis."""
    losses: List[float] = Field(..., description="Portfolio losses")
    confidence_level: float = Field(
        0.95,
        ge=0.01,
        le=0.99,
        description="Confidence level for VaR/CVaR (e.g., 0.95 for 95%)"
    )

    class Config:
        schema_extra = {
            "example": {
                "losses": [-100, -50, 0, 50, 100, -75, 25, -150, 200, -30],
                "confidence_level": 0.95,
            }
        }


class RiskMetricsResponse(BaseModel):
    """Response for risk metrics calculation."""
    var: float = Field(..., description="Value at Risk")
    cvar: float = Field(..., description="Conditional Value at Risk (Expected Shortfall)")
    confidence_level: float = Field(..., description="Confidence level used")
    sample_count: int = Field(..., description="Number of loss samples")
    min_loss: float = Field(..., description="Minimum loss")
    max_loss: float = Field(..., description="Maximum loss")
    mean_loss: float = Field(..., description="Mean loss")
    std_loss: float = Field(..., description="Standard deviation of losses")

    class Config:
        schema_extra = {
            "example": {
                "var": 75.5,
                "cvar": 112.3,
                "confidence_level": 0.95,
                "sample_count": 10000,
                "min_loss": -500.0,
                "max_loss": 500.0,
                "mean_loss": 0.5,
                "std_loss": 125.3,
            }
        }


class MultiLevelRiskRequest(BaseModel):
    """Request for multi-level risk analysis."""
    losses: List[float] = Field(..., description="Portfolio losses")
    confidence_levels: Optional[List[float]] = Field(
        None,
        description="Confidence levels (defaults to [0.90, 0.95, 0.99])"
    )


class MultiLevelRiskResponse(BaseModel):
    """Response for multi-level risk analysis."""
    results: Dict[float, RiskMetricsResponse] = Field(
        ...,
        description="Risk metrics at each confidence level"
    )


# ============================================================================
# Portfolio Models
# ============================================================================

class PositionRequest(BaseModel):
    """Request to add a position to portfolio."""
    name: str = Field(..., description="Position name/identifier")
    value: float = Field(..., gt=0, description="Position value")
    expected_return: float = Field(..., description="Expected return (annualized)")
    volatility: float = Field(..., gt=0, description="Volatility (annualized)")


class PortfolioRequest(BaseModel):
    """Request for portfolio operations."""
    name: str = Field(..., description="Portfolio name")
    positions: List[PositionRequest] = Field(..., description="List of positions")


class PortfolioSummaryResponse(BaseModel):
    """Response with portfolio summary."""
    name: str = Field(..., description="Portfolio name")
    total_value: float = Field(..., description="Total portfolio value")
    position_count: int = Field(..., description="Number of positions")
    expected_return: float = Field(..., description="Portfolio expected return")
    volatility: float = Field(..., description="Portfolio volatility")
    positions: List[Dict[str, Any]] = Field(..., description="Position details")


class PortfolioRiskRequest(BaseModel):
    """Request for portfolio risk analysis."""
    name: str = Field(..., description="Portfolio name")
    positions: List[PositionRequest] = Field(..., description="List of positions")
    time_horizon_years: float = Field(1.0, gt=0, description="Time horizon for simulation")
    scenarios: int = Field(10000, ge=100, description="Number of simulation scenarios")
    confidence_level: float = Field(0.95, ge=0.01, le=0.99, description="Confidence level")


class PortfolioRiskResponse(BaseModel):
    """Response for portfolio risk analysis."""
    portfolio_name: str = Field(..., description="Portfolio name")
    var: float = Field(..., description="Value at Risk")
    cvar: float = Field(..., description="Conditional Value at Risk")
    confidence_level: float = Field(..., description="Confidence level")
    scenarios: int = Field(..., description="Number of scenarios simulated")
    portfolio_summary: PortfolioSummaryResponse = Field(..., description="Portfolio summary")


# ============================================================================
# Quantum Models
# ============================================================================

class QuantumBackendListResponse(BaseModel):
    """Response listing available quantum backends."""
    available_backends: List[str] = Field(..., description="List of available backend names")
    default_backend: Optional[str] = Field(..., description="Default backend name")
    backend_info: Dict[str, Dict[str, Any]] = Field(..., description="Detailed backend info")


class QuantumAmplitudeEstimationRequest(BaseModel):
    """Request for quantum amplitude estimation."""
    num_qubits: int = Field(..., ge=1, le=20, description="Number of qubits")
    shots: int = Field(1024, ge=100, description="Number of measurement shots")
    precision_bits: int = Field(3, ge=1, le=10, description="Precision bits for phase estimation")
    backend: Optional[str] = Field(None, description="Quantum backend to use")

    class Config:
        schema_extra = {
            "example": {
                "num_qubits": 5,
                "shots": 1024,
                "precision_bits": 3,
                "backend": "qiskit_aer",
            }
        }


class QuantumAlgorithmResponse(BaseModel):
    """Response for quantum algorithm execution."""
    algorithm_name: str = Field(..., description="Algorithm name")
    success: bool = Field(..., description="Whether execution was successful")
    iterations: int = Field(..., description="Number of iterations")
    execution_time_seconds: float = Field(..., description="Execution time in seconds")
    result: Dict[str, Any] = Field(..., description="Algorithm-specific results")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class QuantumStateRequest(BaseModel):
    """Request for quantum state operations."""
    qubit_count: int = Field(..., ge=1, le=20, description="Number of qubits")
    operations: List[Dict[str, Any]] = Field(
        ...,
        description="List of gate operations to apply"
    )

    class Config:
        schema_extra = {
            "example": {
                "qubit_count": 2,
                "operations": [
                    {"gate": "hadamard", "target": 0},
                    {"gate": "cnot", "control": 0, "target": 1},
                ],
            }
        }


class QuantumStateResponse(BaseModel):
    """Response with quantum state information."""
    qubit_count: int = Field(..., description="Number of qubits")
    dimension: int = Field(..., description="State vector dimension")
    basis_probabilities: Dict[str, float] = Field(
        ...,
        description="Probabilities for basis states"
    )


# ============================================================================
# Error Models
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

    class Config:
        schema_extra = {
            "example": {
                "error": "ValueError",
                "message": "Invalid input parameters",
                "details": {"field": "spot_price", "reason": "must be positive"},
            }
        }


__all__ = [
    "HealthResponse",
    "EuropeanCallRequest",
    "OptionPricingResponse",
    "BatchPricingRequest",
    "BatchPricingResponse",
    "SensitivityRequest",
    "SensitivityResponse",
    "RiskAnalysisRequest",
    "RiskMetricsResponse",
    "MultiLevelRiskRequest",
    "MultiLevelRiskResponse",
    "PositionRequest",
    "PortfolioRequest",
    "PortfolioSummaryResponse",
    "PortfolioRiskRequest",
    "PortfolioRiskResponse",
    "QuantumBackendListResponse",
    "QuantumAmplitudeEstimationRequest",
    "QuantumAlgorithmResponse",
    "QuantumStateRequest",
    "QuantumStateResponse",
    "ErrorResponse",
]
