"""
QRiskLab finance module.

Provides bindings to C++ Monte Carlo and risk metrics calculations,
plus high-level Python wrappers for option pricing, risk analysis,
and portfolio management.
"""

try:
    from qrisklab.finance._qrisklab_core import MonteCarlo, RiskMetrics, OptionPricingResult
    __all__ = ["MonteCarlo", "RiskMetrics", "OptionPricingResult"]
except ImportError as e:
    # Bindings not yet built
    import warnings
    warnings.warn(
        f"Could not import finance bindings from compiled C++ module: {e}. "
        "Please build the C++ extensions with: python -m pip install -e .",
        ImportWarning
    )
    __all__ = []
