"""
Risk metrics analysis module.

Provides high-level interface for Value at Risk (VaR) and Conditional Value at Risk
(CVaR) calculations with result formatting and reporting.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

from qrisklab.finance._qrisklab_core import RiskMetrics
from qrisklab.utils.logger import get_logger
from qrisklab.utils.timing import timer, timed_block

logger = get_logger(__name__)


@dataclass
class RiskMetricsResult:
    """Result of risk metrics calculation."""
    var: float
    cvar: float
    confidence_level: float
    sample_count: int
    min_loss: float
    max_loss: float
    mean_loss: float
    std_loss: float

    def __str__(self) -> str:
        """Format result as string."""
        return (
            f"Risk Metrics (CL={self.confidence_level:.1%}):\n"
            f"  VaR:  {self.var:>12.4f}\n"
            f"  CVaR: {self.cvar:>12.4f}\n"
            f"  Mean: {self.mean_loss:>12.4f}\n"
            f"  Std:  {self.std_loss:>12.4f}\n"
            f"  Min:  {self.min_loss:>12.4f}\n"
            f"  Max:  {self.max_loss:>12.4f}"
        )


class RiskAnalyzer:
    """
    High-level interface for risk metrics calculations.

    Wraps C++ RiskMetrics implementation with validation, statistics,
    and reporting capabilities.
    """

    def __init__(self):
        """Initialize the risk analyzer."""
        logger.debug("RiskAnalyzer initialized")

    @staticmethod
    def _validate_losses(losses: List[float]) -> None:
        """Validate loss data."""
        if not losses:
            raise ValueError("Loss list cannot be empty")
        if len(losses) < 10:
            logger.warning(
                f"Small sample size ({len(losses)} losses) may produce unreliable results"
            )

    @staticmethod
    def _validate_confidence_level(confidence_level: float) -> None:
        """Validate confidence level."""
        if not (0 < confidence_level < 1):
            raise ValueError("Confidence level must be between 0 and 1")

    @staticmethod
    def _calculate_statistics(losses: List[float]) -> Dict[str, float]:
        """Calculate basic statistics on losses."""
        import statistics
        return {
            "min": min(losses),
            "max": max(losses),
            "mean": statistics.mean(losses),
            "stdev": statistics.stdev(losses) if len(losses) > 1 else 0.0,
        }

    @timer
    def calculate_var(
        self,
        losses: List[float],
        confidence_level: float = 0.95,
    ) -> float:
        """
        Calculate Value at Risk (VaR).

        Args:
            losses: List of portfolio losses
            confidence_level: Confidence level (e.g., 0.95 for 95%)

        Returns:
            Value at Risk at the specified confidence level

        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_losses(losses)
        self._validate_confidence_level(confidence_level)

        with timed_block("VaR calculation"):
            var = RiskMetrics.value_at_risk(losses, confidence_level)

        logger.info(
            f"VaR calculated: {var:.4f} at {confidence_level:.1%} confidence"
        )
        return var

    @timer
    def calculate_cvar(
        self,
        losses: List[float],
        confidence_level: float = 0.95,
    ) -> float:
        """
        Calculate Conditional Value at Risk (CVaR / Expected Shortfall).

        Args:
            losses: List of portfolio losses
            confidence_level: Confidence level (e.g., 0.95 for 95%)

        Returns:
            Conditional Value at Risk at the specified confidence level

        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_losses(losses)
        self._validate_confidence_level(confidence_level)

        with timed_block("CVaR calculation"):
            cvar = RiskMetrics.conditional_value_at_risk(losses, confidence_level)

        logger.info(
            f"CVaR calculated: {cvar:.4f} at {confidence_level:.1%} confidence"
        )
        return cvar

    @timer
    def analyze_risk(
        self,
        losses: List[float],
        confidence_level: float = 0.95,
    ) -> RiskMetricsResult:
        """
        Perform comprehensive risk analysis.

        Args:
            losses: List of portfolio losses
            confidence_level: Confidence level (e.g., 0.95 for 95%)

        Returns:
            RiskMetricsResult with VaR, CVaR, and statistics

        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_losses(losses)
        self._validate_confidence_level(confidence_level)

        with timed_block("Comprehensive risk analysis"):
            var = RiskMetrics.value_at_risk(losses, confidence_level)
            cvar = RiskMetrics.conditional_value_at_risk(losses, confidence_level)
            stats = self._calculate_statistics(losses)

        result = RiskMetricsResult(
            var=var,
            cvar=cvar,
            confidence_level=confidence_level,
            sample_count=len(losses),
            min_loss=stats["min"],
            max_loss=stats["max"],
            mean_loss=stats["mean"],
            std_loss=stats["stdev"],
        )

        logger.info(f"Risk analysis complete: {result}")
        return result

    def multi_level_analysis(
        self,
        losses: List[float],
        confidence_levels: Optional[List[float]] = None,
    ) -> Dict[float, RiskMetricsResult]:
        """
        Perform risk analysis at multiple confidence levels.

        Args:
            losses: List of portfolio losses
            confidence_levels: List of confidence levels (defaults to [0.90, 0.95, 0.99])

        Returns:
            Dictionary mapping confidence levels to RiskMetricsResult objects
        """
        if confidence_levels is None:
            confidence_levels = [0.90, 0.95, 0.99]

        results = {}
        for cl in confidence_levels:
            results[cl] = self.analyze_risk(losses, cl)

        logger.info(f"Multi-level analysis complete: {len(results)} confidence levels")
        return results


__all__ = [
    "RiskAnalyzer",
    "RiskMetricsResult",
]
