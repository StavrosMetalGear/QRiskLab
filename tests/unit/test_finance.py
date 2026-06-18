"""
Unit tests for finance module.

Tests option pricing, risk analysis, and portfolio management.
"""

import pytest
from unittest.mock import MagicMock, patch

from qrisklab.finance.pricing import EuropeanCallPricer, PricingParameters
from qrisklab.finance.risk import RiskAnalyzer, RiskMetricsResult
from qrisklab.finance.portfolio import Portfolio, Position


class TestPricingParameters:
    """Tests for PricingParameters dataclass."""

    def test_valid_parameters(self, sample_option_params):
        """Test that valid parameters are accepted."""
        params = PricingParameters(**sample_option_params)
        assert params.spot_price == 100.0
        assert params.strike_price == 105.0

    def test_invalid_spot_price(self, sample_option_params):
        """Test that negative spot price raises error."""
        sample_option_params["spot_price"] = -100.0
        params = PricingParameters(**sample_option_params)
        with pytest.raises(ValueError):
            params.validate()

    def test_invalid_volatility(self, sample_option_params):
        """Test that zero volatility raises error."""
        sample_option_params["volatility"] = 0.0
        params = PricingParameters(**sample_option_params)
        with pytest.raises(ValueError):
            params.validate()

    def test_invalid_paths(self, sample_option_params):
        """Test that too few paths raises error."""
        sample_option_params["paths"] = 50
        params = PricingParameters(**sample_option_params)
        with pytest.raises(ValueError):
            params.validate()


class TestEuropeanCallPricer:
    """Tests for EuropeanCallPricer class."""

    def test_pricer_initialization(self):
        """Test that pricer initializes correctly."""
        pricer = EuropeanCallPricer(default_paths=5000, default_seed=123)
        assert pricer.default_paths == 5000
        assert pricer.default_seed == 123

    def test_pricer_has_empty_cache(self):
        """Test that pricer starts with empty cache."""
        pricer = EuropeanCallPricer()
        assert len(pricer._cache) == 0

    @patch("qrisklab.finance.pricing.MonteCarlo")
    def test_price_calls_monte_carlo(self, mock_mc, sample_option_params):
        """Test that price() calls MonteCarlo.price_european_call()."""
        mock_result = MagicMock()
        mock_result.estimated_price = 5.234
        mock_result.standard_error = 0.045
        mock_mc.price_european_call.return_value = mock_result

        pricer = EuropeanCallPricer()
        result = pricer.price(**sample_option_params)

        mock_mc.price_european_call.assert_called_once()
        assert result.estimated_price == 5.234

    @patch("qrisklab.finance.pricing.MonteCarlo")
    def test_price_caching(self, mock_mc, sample_option_params):
        """Test that price() caches results."""
        mock_result = MagicMock()
        mock_result.estimated_price = 5.234
        mock_result.standard_error = 0.045
        mock_mc.price_european_call.return_value = mock_result

        pricer = EuropeanCallPricer()
        
        # First call
        pricer.price(**sample_option_params)
        assert mock_mc.price_european_call.call_count == 1
        
        # Second call (should use cache)
        pricer.price(**sample_option_params)
        assert mock_mc.price_european_call.call_count == 1

    def test_clear_cache(self):
        """Test that clear_cache() empties the cache."""
        pricer = EuropeanCallPricer()
        pricer._cache["test_key"] = "test_value"
        assert len(pricer._cache) == 1
        
        pricer.clear_cache()
        assert len(pricer._cache) == 0


class TestRiskAnalyzer:
    """Tests for RiskAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly."""
        analyzer = RiskAnalyzer()
        assert analyzer is not None

    def test_validate_losses_empty_list(self):
        """Test that empty loss list raises error."""
        with pytest.raises(ValueError):
            RiskAnalyzer._validate_losses([])

    def test_validate_confidence_level_invalid(self):
        """Test that invalid confidence level raises error."""
        with pytest.raises(ValueError):
            RiskAnalyzer._validate_confidence_level(1.5)
        
        with pytest.raises(ValueError):
            RiskAnalyzer._validate_confidence_level(-0.1)

    def test_calculate_statistics(self, sample_losses):
        """Test that statistics are calculated correctly."""
        stats = RiskAnalyzer._calculate_statistics(sample_losses)
        assert "min" in stats
        assert "max" in stats
        assert "mean" in stats
        assert "stdev" in stats
        assert stats["min"] < stats["mean"] < stats["max"]

    @patch("qrisklab.finance.risk.RiskMetrics")
    def test_calculate_var(self, mock_rm, sample_losses):
        """Test VaR calculation."""
        mock_rm.value_at_risk.return_value = 75.5
        
        analyzer = RiskAnalyzer()
        var = analyzer.calculate_var(sample_losses, 0.95)
        
        assert var == 75.5
        mock_rm.value_at_risk.assert_called_once()

    @patch("qrisklab.finance.risk.RiskMetrics")
    def test_analyze_risk(self, mock_rm, sample_losses):
        """Test comprehensive risk analysis."""
        mock_rm.value_at_risk.return_value = 75.5
        mock_rm.conditional_value_at_risk.return_value = 112.3
        
        analyzer = RiskAnalyzer()
        result = analyzer.analyze_risk(sample_losses, 0.95)
        
        assert isinstance(result, RiskMetricsResult)
        assert result.var == 75.5
        assert result.cvar == 112.3
        assert result.confidence_level == 0.95


class TestPosition:
    """Tests for Position class."""

    def test_position_initialization(self):
        """Test that position initializes correctly."""
        pos = Position(
            name="Stock A",
            value=100000,
            expected_return=0.07,
            volatility=0.15
        )
        assert pos.name == "Stock A"
        assert pos.value == 100000

    def test_position_validation_invalid_value(self):
        """Test that invalid position value raises error."""
        pos = Position(
            name="Stock A",
            value=-100000,
            expected_return=0.07,
            volatility=0.15
        )
        with pytest.raises(ValueError):
            pos.validate()

    def test_position_validation_invalid_volatility(self):
        """Test that invalid volatility raises error."""
        pos = Position(
            name="Stock A",
            value=100000,
            expected_return=0.07,
            volatility=0.0
        )
        with pytest.raises(ValueError):
            pos.validate()


class TestPortfolio:
    """Tests for Portfolio class."""

    def test_portfolio_initialization(self):
        """Test that portfolio initializes correctly."""
        portfolio = Portfolio(name="My Portfolio")
        assert portfolio.name == "My Portfolio"
        assert len(portfolio.positions) == 0

    def test_add_position(self, sample_portfolio_positions):
        """Test adding positions to portfolio."""
        portfolio = Portfolio(name="My Portfolio")
        
        for pos in sample_portfolio_positions:
            portfolio.add_position(**pos)
        
        assert len(portfolio.positions) == 3

    def test_remove_position(self, sample_portfolio_positions):
        """Test removing positions from portfolio."""
        portfolio = Portfolio(name="My Portfolio")
        
        for pos in sample_portfolio_positions:
            portfolio.add_position(**pos)
        
        removed = portfolio.remove_position("Stock A")
        assert removed is True
        assert len(portfolio.positions) == 2

    def test_total_value(self, sample_portfolio_positions):
        """Test total portfolio value calculation."""
        portfolio = Portfolio(name="My Portfolio")
        
        for pos in sample_portfolio_positions:
            portfolio.add_position(**pos)
        
        total = portfolio.total_value()
        assert total == 300000

    def test_position_weights(self, sample_portfolio_positions):
        """Test position weight calculation."""
        portfolio = Portfolio(name="My Portfolio")
        
        for pos in sample_portfolio_positions:
            portfolio.add_position(**pos)
        
        weights = portfolio.position_weights()
        assert len(weights) == 3
        assert abs(sum(weights.values()) - 1.0) < 0.001

    def test_portfolio_expected_return(self, sample_portfolio_positions):
        """Test portfolio expected return calculation."""
        portfolio = Portfolio(name="My Portfolio")
        
        for pos in sample_portfolio_positions:
            portfolio.add_position(**pos)
        
        ret = portfolio.portfolio_expected_return()
        assert 0.03 < ret < 0.08

    def test_get_summary(self, sample_portfolio_positions):
        """Test portfolio summary generation."""
        portfolio = Portfolio(name="My Portfolio")
        
        for pos in sample_portfolio_positions:
            portfolio.add_position(**pos)
        
        summary = portfolio.get_summary()
        assert summary["name"] == "My Portfolio"
        assert summary["total_value"] == 300000
        assert summary["position_count"] == 3
        assert "expected_return" in summary
        assert "volatility" in summary
