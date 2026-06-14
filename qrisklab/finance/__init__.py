"""
QRiskLab finance module.

Provides bindings to C++ Monte Carlo and risk metrics calculations,
plus high-level Python wrappers for option pricing, risk analysis,
and portfolio management.
"""

from qrisklab.finance._qrisklab_core import (
    MonteCarlo,
    RiskMetrics,
    OptionPricingResult,
)
from qrisklab.finance.pricing import EuropeanCallPricer, PricingParameters
from qrisklab.finance.risk import RiskAnalyzer, RiskMetricsResult
from qrisklab.finance.portfolio import Portfolio, Position

__all__ = [
    # C++ bindings
    "MonteCarlo",
    "RiskMetrics",
    "OptionPricingResult",
    # Python wrappers
    "EuropeanCallPricer",
    "PricingParameters",
    "RiskAnalyzer",
    "RiskMetricsResult",
    "Portfolio",
    "Position",
]
