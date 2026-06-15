"""
QRiskLab core quantum module.

Provides bindings to C++ quantum state management and operations.
"""

try:
    from qrisklab._qrisklab_core import QuantumState
    __all__ = ["QuantumState"]
except ImportError:
    # Bindings not yet built
    __all__ = []
