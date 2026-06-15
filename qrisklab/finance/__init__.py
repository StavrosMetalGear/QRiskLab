"""
QRiskLab finance module.

Provides bindings to C++ Monte Carlo and risk metrics calculations,
plus high-level Python wrappers for option pricing, risk analysis,
and portfolio management.
"""

try:
    from qrisklab._qrisklab_core import MonteCarlo, RiskMetrics, OptionPricingResult
    __all__ = ["MonteCarlo", "RiskMetrics", "OptionPricingResult"]
except ImportError:
    # Bindings not yet built
    __all__ = []
