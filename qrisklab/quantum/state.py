"""
Quantum state management module.

Provides high-level wrapper around C++ QuantumState with state visualization,
serialization, and integration with logging and timing utilities.
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import logging

from qrisklab.utils.logger import get_logger
from qrisklab.utils.timing import timer, timed_block

logger = get_logger(__name__)

try:
    from qrisklab.core import QuantumState
    HAS_QUANTUM_STATE = True
except ImportError:
    HAS_QUANTUM_STATE = False
    logger.warning("QuantumState C++ bindings not available. Install with: python -m pip install -e .")


@dataclass
class MeasurementResult:
    """Result of a quantum measurement."""
    qubit: int
    outcome: int  # 0 or 1
    probability: float


@dataclass
class StateSnapshot:
    """Snapshot of quantum state for serialization."""
    qubit_count: int
    amplitudes: List[complex]
    basis_probabilities: Dict[str, float]


class QuantumStateWrapper:
    """
    High-level wrapper around C++ QuantumState.

    Provides convenient interface for quantum state operations, measurement,
    visualization, and serialization.
    """

    def __init__(self, qubit_count: int):
        """
        Initialize a quantum state.

        Args:
            qubit_count: Number of qubits in the state

        Raises:
            ValueError: If qubit_count is invalid
            RuntimeError: If C++ bindings are not available
        """
        if not HAS_QUANTUM_STATE:
            raise RuntimeError(
                "QuantumState C++ bindings not available. "
                "Please build the C++ extensions with: python -m pip install -e ."
            )

        if qubit_count <= 0:
            raise ValueError("Qubit count must be positive")

        self._state = QuantumState(qubit_count)
        self._qubit_count = qubit_count
        logger.debug(f"Initialized QuantumStateWrapper with {qubit_count} qubits")

    @property
    def qubit_count(self) -> int:
        """Get the number of qubits."""
        return self._qubit_count

    @property
    def dimension(self) -> int:
        """Get the dimension of the state vector (2^qubit_count)."""
        return self._state.dimension()

    @timer
    def reset(self) -> None:
        """Reset the quantum state to |0...0>."""
        self._state.reset()
        logger.debug(f"Reset quantum state to |0...0>")

    @timer
    def apply_hadamard(self, target: int) -> None:
        """
        Apply Hadamard gate to target qubit.

        Args:
            target: Target qubit index (0-indexed)

        Raises:
            ValueError: If target is out of range
        """
        if not (0 <= target < self._qubit_count):
            raise ValueError(f"Target qubit {target} out of range [0, {self._qubit_count})")

        self._state.apply_hadamard(target)
        logger.debug(f"Applied Hadamard gate to qubit {target}")

    @timer
    def apply_x(self, target: int) -> None:
        """
        Apply Pauli-X (NOT) gate to target qubit.

        Args:
            target: Target qubit index (0-indexed)

        Raises:
            ValueError: If target is out of range
        """
        if not (0 <= target < self._qubit_count):
            raise ValueError(f"Target qubit {target} out of range [0, {self._qubit_count})")

        self._state.apply_x(target)
        logger.debug(f"Applied X gate to qubit {target}")

    @timer
    def apply_z(self, target: int) -> None:
        """
        Apply Pauli-Z gate to target qubit.

        Args:
            target: Target qubit index (0-indexed)

        Raises:
            ValueError: If target is out of range
        """
        if not (0 <= target < self._qubit_count):
            raise ValueError(f"Target qubit {target} out of range [0, {self._qubit_count})")

        self._state.apply_z(target)
        logger.debug(f"Applied Z gate to qubit {target}")

    @timer
    def apply_cnot(self, control: int, target: int) -> None:
        """
        Apply CNOT (controlled-NOT) gate.

        Args:
            control: Control qubit index (0-indexed)
            target: Target qubit index (0-indexed)

        Raises:
            ValueError: If qubits are out of range or identical
        """
        if not (0 <= control < self._qubit_count):
            raise ValueError(f"Control qubit {control} out of range [0, {self._qubit_count})")
        if not (0 <= target < self._qubit_count):
            raise ValueError(f"Target qubit {target} out of range [0, {self._qubit_count})")
        if control == target:
            raise ValueError("Control and target qubits must be different")

        self._state.apply_cnot(control, target)
        logger.debug(f"Applied CNOT gate: control={control}, target={target}")

    @timer
    def measure(self, target: int, seed: int = 42) -> int:
        """
        Measure a qubit and collapse the state.

        Args:
            target: Target qubit index (0-indexed)
            seed: Random seed for reproducibility

        Returns:
            Measurement outcome (0 or 1)

        Raises:
            ValueError: If target is out of range
        """
        if not (0 <= target < self._qubit_count):
            raise ValueError(f"Target qubit {target} out of range [0, {self._qubit_count})")

        import random
        rng = random.Random(seed)
        outcome = self._state.measure(target, rng)
        logger.debug(f"Measured qubit {target}: outcome={outcome}")
        return outcome

    def get_amplitudes(self) -> List[complex]:
        """
        Get the state vector amplitudes.

        Returns:
            List of complex amplitudes
        """
        return list(self._state.amplitudes())

    def get_probability(self, basis_state_index: int) -> float:
        """
        Get probability of measuring a specific basis state.

        Args:
            basis_state_index: Index of the basis state (0 to 2^qubit_count - 1)

        Returns:
            Probability of measuring that basis state

        Raises:
            ValueError: If index is out of range
        """
        if not (0 <= basis_state_index < self.dimension):
            raise ValueError(f"Basis state index {basis_state_index} out of range [0, {self.dimension})")

        return self._state.probability_of_basis_state(basis_state_index)

    def get_basis_probabilities(self, epsilon: float = 1e-10) -> Dict[str, float]:
        """
        Get probabilities for all basis states above threshold.

        Args:
            epsilon: Probability threshold for inclusion

        Returns:
            Dictionary mapping basis state strings to probabilities
        """
        probabilities = {}
        for i in range(self.dimension):
            prob = self.get_probability(i)
            if prob > epsilon:
                # Convert index to binary string
                basis_str = format(i, f'0{self._qubit_count}b')
                probabilities[basis_str] = prob

        return probabilities

    def print_state(self, epsilon: float = 1e-10) -> None:
        """
        Print the quantum state (amplitudes above epsilon threshold).

        Args:
            epsilon: Amplitude threshold for display
        """
        self._state.print_state(epsilon)

    def get_snapshot(self) -> StateSnapshot:
        """
        Get a snapshot of the current quantum state.

        Returns:
            StateSnapshot with amplitudes and probabilities
        """
        return StateSnapshot(
            qubit_count=self._qubit_count,
            amplitudes=self.get_amplitudes(),
            basis_probabilities=self.get_basis_probabilities(),
        )

    def __repr__(self) -> str:
        """String representation of the quantum state."""
        return f"QuantumStateWrapper(qubits={self._qubit_count}, dimension={self.dimension})"


__all__ = [
    "QuantumStateWrapper",
    "MeasurementResult",
    "StateSnapshot",
]
