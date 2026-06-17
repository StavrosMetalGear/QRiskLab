"""
QRiskLab quantum algorithms module.

Provides quantum algorithms for finance applications including amplitude estimation,
variational quantum eigensolver, and quantum phase estimation, with support for
multiple quantum backends (Qiskit, PennyLane, Cirq, Amazon Braket).
"""

from qrisklab.quantum.state import (
    QuantumStateWrapper,
    MeasurementResult,
    StateSnapshot,
)
from qrisklab.quantum.algorithms import (
    QuantumAlgorithm,
    QuantumAmplitudeEstimation,
    VariationalQuantumEigensolver,
    QuantumPhaseEstimation,
    AlgorithmResult,
    AmplitudeEstimationResult,
    VQEResult,
    QPEResult,
)
from qrisklab.quantum.backends import (
    BackendFactory,
    QuantumBackend,
    QiskitAerBackend,
    PennyLaneBackend,
    CirqBackend,
    AmazonBraketBackend,
    BackendType,
)

__all__ = [
    # State management
    "QuantumStateWrapper",
    "MeasurementResult",
    "StateSnapshot",
    # Algorithms
    "QuantumAlgorithm",
    "QuantumAmplitudeEstimation",
    "VariationalQuantumEigensolver",
    "QuantumPhaseEstimation",
    "AlgorithmResult",
    "AmplitudeEstimationResult",
    "VQEResult",
    "QPEResult",
    # Backends
    "BackendFactory",
    "QuantumBackend",
    "QiskitAerBackend",
    "PennyLaneBackend",
    "CirqBackend",
    "AmazonBraketBackend",
    "BackendType",
]
