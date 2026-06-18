"""
Pytest configuration and shared fixtures.

Provides common fixtures, mocks, and configuration for all tests.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def config():
    """Provide test configuration."""
    from qrisklab.config import TestingConfig
    return TestingConfig()


@pytest.fixture
def temp_log_file(tmp_path):
    """Provide temporary log file path."""
    return str(tmp_path / "test.log")


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_quantum_state():
    """Mock QuantumState for testing without C++ bindings."""
    mock = MagicMock()
    mock.qubit_count.return_value = 2
    mock.dimension.return_value = 4
    mock.amplitudes.return_value = [1.0, 0.0, 0.0, 0.0]
    mock.probability_of_basis_state.return_value = 1.0
    return mock


@pytest.fixture
def mock_monte_carlo():
    """Mock MonteCarlo for testing without C++ bindings."""
    mock = MagicMock()
    
    # Mock option pricing result
    pricing_result = MagicMock()
    pricing_result.estimated_price = 5.234
    pricing_result.standard_error = 0.045
    pricing_result.discounted_payoffs = [5.0, 5.5, 4.8] * 100
    
    mock.price_european_call.return_value = pricing_result
    mock.simulate_portfolio_losses.return_value = [-100, -50, 0, 50, 100] * 100
    
    return mock


@pytest.fixture
def mock_risk_metrics():
    """Mock RiskMetrics for testing without C++ bindings."""
    mock = MagicMock()
    mock.value_at_risk.return_value = 75.5
    mock.conditional_value_at_risk.return_value = 112.3
    return mock


# ============================================================================
# Data Fixtures
# ============================================================================

@pytest.fixture
def sample_losses():
    """Provide sample loss data for risk analysis."""
    return [-100, -75, -50, -25, 0, 25, 50, 75, 100, -150, 200, -30] * 100


@pytest.fixture
def sample_option_params():
    """Provide sample option pricing parameters."""
    return {
        "spot_price": 100.0,
        "strike_price": 105.0,
        "risk_free_rate": 0.05,
        "volatility": 0.2,
        "maturity_years": 1.0,
    }


@pytest.fixture
def sample_portfolio_positions():
    """Provide sample portfolio positions."""
    return [
        {"name": "Stock A", "value": 100000, "expected_return": 0.07, "volatility": 0.15},
        {"name": "Stock B", "value": 150000, "expected_return": 0.08, "volatility": 0.18},
        {"name": "Bond", "value": 50000, "expected_return": 0.03, "volatility": 0.05},
    ]


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Register custom markers
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )


@pytest.fixture(autouse=True)
def reset_imports():
    """Reset imports between tests to avoid state pollution."""
    yield
    # Cleanup after each test
    pass
