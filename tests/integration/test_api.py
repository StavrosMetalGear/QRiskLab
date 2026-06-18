"""
Integration tests for FastAPI backend.

Tests API endpoints, request/response validation, and error handling.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from qrisklab.api.main import create_app
from qrisklab.api.models import (
    EuropeanCallRequest,
    RiskAnalysisRequest,
    QuantumAmplitudeEstimationRequest,
)


@pytest.fixture
def client():
    """Provide FastAPI test client."""
    app = create_app()
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Test that health check returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_format(self, client):
        """Test that health check response has correct format."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_returns_200(self, client):
        """Test that root endpoint returns 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_response_format(self, client):
        """Test that root response has correct format."""
        response = client.get("/")
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data


class TestPricingEndpoints:
    """Tests for pricing API endpoints."""

    @patch("qrisklab.api.routes.pricing.pricer")
    def test_european_call_pricing(self, mock_pricer, client):
        """Test European call option pricing endpoint."""
        mock_result = MagicMock()
        mock_result.estimated_price = 5.234
        mock_result.standard_error = 0.045
        mock_pricer.price.return_value = mock_result

        request_data = {
            "spot_price": 100.0,
            "strike_price": 105.0,
            "risk_free_rate": 0.05,
            "volatility": 0.2,
            "maturity_years": 1.0,
        }

        response = client.post("/api/pricing/european-call", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "estimated_price" in data
        assert data["estimated_price"] == 5.234

    @patch("qrisklab.api.routes.pricing.pricer")
    def test_european_call_invalid_input(self, mock_pricer, client):
        """Test that invalid input returns 400."""
        request_data = {
            "spot_price": -100.0,  # Invalid: negative
            "strike_price": 105.0,
            "risk_free_rate": 0.05,
            "volatility": 0.2,
            "maturity_years": 1.0,
        }

        response = client.post("/api/pricing/european-call", json=request_data)
        assert response.status_code == 422  # Validation error


class TestRiskEndpoints:
    """Tests for risk analysis API endpoints."""

    @patch("qrisklab.api.routes.risk.analyzer")
    def test_var_calculation(self, mock_analyzer, client):
        """Test Value at Risk calculation endpoint."""
        mock_result = MagicMock()
        mock_result.var = 75.5
        mock_analyzer.calculate_var.return_value = 75.5

        request_data = {
            "losses": [-100, -50, 0, 50, 100] * 10,
            "confidence_level": 0.95,
        }

        response = client.post("/api/risk/var", json=request_data)
        assert response.status_code == 200
        assert response.json() == 75.5

    @patch("qrisklab.api.routes.risk.analyzer")
    def test_cvar_calculation(self, mock_analyzer, client):
        """Test Conditional Value at Risk calculation endpoint."""
        mock_analyzer.calculate_cvar.return_value = 112.3

        request_data = {
            "losses": [-100, -50, 0, 50, 100] * 10,
            "confidence_level": 0.95,
        }

        response = client.post("/api/risk/cvar", json=request_data)
        assert response.status_code == 200
        assert response.json() == 112.3


class TestQuantumEndpoints:
    """Tests for quantum algorithm API endpoints."""

    @patch("qrisklab.api.routes.quantum.BackendFactory")
    def test_list_backends(self, mock_factory, client):
        """Test quantum backends listing endpoint."""
        mock_factory.get_available_backends.return_value = ["qiskit_aer", "pennylane"]
        mock_factory.list_backends.return_value = {
            "qiskit_aer": {"status": "available"},
            "pennylane": {"status": "available"},
        }
        mock_factory.get_default_backend.return_value = MagicMock(name="qiskit_aer")

        response = client.get("/api/quantum/backends")
        assert response.status_code == 200
        data = response.json()
        assert "available_backends" in data
        assert "default_backend" in data


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_not_found(self, client):
        """Test that 404 is returned for unknown endpoint."""
        response = client.get("/api/unknown/endpoint")
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """Test that 405 is returned for wrong HTTP method."""
        response = client.get("/api/pricing/european-call")
        assert response.status_code == 405
