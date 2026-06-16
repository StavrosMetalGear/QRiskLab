"""
QRiskLab core quantum module.

Provides bindings to C++ quantum state management and operations.
"""

try:
    from qrisklab._qrisklab_core import QuantumState
    __all__ = ["QuantumState"]
except ImportError as e:
    # Bindings not yet built
    import warnings
    warnings.warn(
        f"Could not import QuantumState from compiled C++ bindings: {e}. "
        "Please build the C++ extensions with: python -m pip install -e .",
        ImportWarning
    )
    __all__ = []
