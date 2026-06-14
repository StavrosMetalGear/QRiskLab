"""
Portfolio management module.

Provides portfolio construction, position management, and risk analysis
with integration to Monte Carlo simulations.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import logging

from qrisklab.finance._qrisklab_core import MonteCarlo
from qrisklab.finance.risk import RiskAnalyzer, RiskMetricsResult
from qrisklab.utils.logger import get_logger
from qrisklab.utils.timing import timer, timed_block

logger = get_logger(__name__)


@dataclass
class Position:
    """Represents a single portfolio position."""
    name: str
    value: float
    expected_return: float
    volatility: float

    def validate(self) -> None:
        """Validate position parameters."""
        if self.value <= 0:
            raise ValueError(f"Position value must be positive: {self.name}")
        if self.volatility <= 0:
            raise ValueError(f"Position volatility must be positive: {self.name}")


@dataclass
class Portfolio:
    """
    Portfolio management and risk analysis.

    Manages multiple positions and provides portfolio-level risk metrics
    and Monte Carlo simulations.
    """
    name: str
    positions: List[Position] = field(default_factory=list)
    _risk_analyzer: RiskAnalyzer = field(default_factory=RiskAnalyzer, init=False)

    def add_position(
        self,
        name: str,
        value: float,
        expected_return: float,
        volatility: float,
    ) -> None:
        """
        Add a position to the portfolio.

        Args:
            name: Position name/identifier
            value: Position value
            expected_return: Expected return (annualized)
            volatility: Volatility (annualized)

        Raises:
            ValueError: If parameters are invalid
        """
        position = Position(
            name=name,
            value=value,
            expected_return=expected_return,
            volatility=volatility,
        )
        position.validate()
        self.positions.append(position)
        logger.info(f"Added position to {self.name}: {name} (value={value:.2f})")

    def remove_position(self, name: str) -> bool:
        """
        Remove a position from the portfolio.

        Args:
            name: Position name to remove

        Returns:
            True if position was removed, False if not found
        """
        initial_count = len(self.positions)
        self.positions = [p for p in self.positions if p.name != name]
        removed = len(self.positions) < initial_count
        if removed:
            logger.info(f"Removed position from {self.name}: {name}")
        return removed

    def get_position(self, name: str) -> Optional[Position]:
        """Get a position by name."""
        for position in self.positions:
            if position.name == name:
                return position
        return None

    def total_value(self) -> float:
        """Get total portfolio value."""
        return sum(p.value for p in self.positions)

    def position_weights(self) -> Dict[str, float]:
        """Get position weights as fractions of total portfolio value."""
        total = self.total_value()
        if total <= 0:
            return {}
        return {p.name: p.value / total for p in self.positions}

    def portfolio_expected_return(self) -> float:
        """Calculate portfolio expected return (weighted average)."""
        total = self.total_value()
        if total <= 0:
            return 0.0
        return sum(p.value * p.expected_return for p in self.positions) / total

    def portfolio_volatility(self) -> float:
        """
        Estimate portfolio volatility (simplified, assumes independence).

        Note: This is a simplified calculation that assumes positions are independent.
        For more accurate results, use correlation matrix.
        """
        total = self.total_value()
        if total <= 0:
            return 0.0

        variance = sum(
            (p.value / total) ** 2 * p.volatility ** 2
            for p in self.positions
        )
        return variance ** 0.5

    @timer
    def simulate_losses(
        self,
        time_horizon_years: float = 1.0,
        scenarios: int = 10000,
        seed: int = 42,
    ) -> List[float]:
        """
        Simulate portfolio losses using Monte Carlo.

        Args:
            time_horizon_years: Time horizon for simulation
            scenarios: Number of simulation scenarios
            seed: Random seed for reproducibility

        Returns:
            List of simulated portfolio losses

        Raises:
            ValueError: If portfolio is empty
        """
        if not self.positions:
            raise ValueError("Portfolio must contain at least one position")

        total_value = self.total_value()
        expected_return = self.portfolio_expected_return()
        volatility = self.portfolio_volatility()

        with timed_block("Portfolio loss simulation"):
            losses = MonteCarlo.simulate_portfolio_losses(
                initial_portfolio_value=total_value,
                expected_return=expected_return,
                volatility=volatility,
                time_horizon_years=time_horizon_years,
                scenarios=scenarios,
                seed=seed,
            )

        logger.info(
            f"Simulated {len(losses)} portfolio loss scenarios for {self.name}"
        )
        return losses

    @timer
    def analyze_risk(
        self,
        time_horizon_years: float = 1.0,
        scenarios: int = 10000,
        confidence_level: float = 0.95,
        seed: int = 42,
    ) -> RiskMetricsResult:
        """
        Analyze portfolio risk using Monte Carlo simulation.

        Args:
            time_horizon_years: Time horizon for simulation
            scenarios: Number of simulation scenarios
            confidence_level: Confidence level for VaR/CVaR
            seed: Random seed for reproducibility

        Returns:
            RiskMetricsResult with portfolio risk metrics

        Raises:
            ValueError: If portfolio is empty
        """
        losses = self.simulate_losses(
            time_horizon_years=time_horizon_years,
            scenarios=scenarios,
            seed=seed,
        )

        result = self._risk_analyzer.analyze_risk(losses, confidence_level)
        logger.info(f"Portfolio risk analysis complete for {self.name}")
        return result

    def get_summary(self) -> Dict:
        """Get portfolio summary statistics."""
        return {
            "name": self.name,
            "total_value": self.total_value(),
            "position_count": len(self.positions),
            "expected_return": self.portfolio_expected_return(),
            "volatility": self.portfolio_volatility(),
            "positions": [
                {
                    "name": p.name,
                    "value": p.value,
                    "weight": p.value / self.total_value() if self.total_value() > 0 else 0,
                    "expected_return": p.expected_return,
                    "volatility": p.volatility,
                }
                for p in self.positions
            ],
        }


__all__ = [
    "Portfolio",
    "Position",
]
````

qrisklab/finance/__init__.py
````python
<<<<<<< SEARCH
"""
QRiskLab finance module.

Provides bindings to C++ Monte Carlo and risk metrics calculations.
"""

from qrisklab.finance._qrisklab_core import (
    MonteCarlo,
    RiskMetrics,
    OptionPricingResult,
)

__all__ = [
    "MonteCarlo",
    "RiskMetrics",
    "OptionPricingResult",
]
