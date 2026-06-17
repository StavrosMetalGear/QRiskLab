"""
QRiskLab API module

Provides REST API endpoints for quantum and classical risk analysis.

Includes FastAPI application, routes for pricing, risk analysis, and quantum algorithms,
with automatic documentation and error handling.
"""

from qrisklab.api.main import app, create_app
from qrisklab.api.models import (
    HealthResponse,
    EuropeanCallRequest,
    OptionPricingResponse,
    BatchPricingRequest,
    BatchPricingResponse,
    SensitivityRequest,
    SensitivityResponse,
    RiskAnalysisRequest,
    RiskMetricsResponse,
    MultiLevelRiskRequest,
    MultiLevelRiskResponse,
    QuantumBackendListResponse,
    QuantumAmplitudeEstimationRequest,
    QuantumAlgorithmResponse,
    ErrorResponse,
)

__all__ = [
    "app",
    "create_app",
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
    "QuantumBackendListResponse",
    "QuantumAmplitudeEstimationRequest",
    "QuantumAlgorithmResponse",
    "ErrorResponse",
]
