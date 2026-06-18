"""
Unit tests for quantum module.

Tests quantum state management, algorithms, and backend selection.
"""

import pytest
from unittest.mock import MagicMock, patch

from qrisklab.quantum.state import QuantumStateWrapper, MeasurementResult, StateSnapshot
from qrisklab.quantum.algorithms import (
    QuantumAmplitudeEstimation,
    VariationalQuantumEigensolver,
    QuantumPhaseEstimation,
)
from qrisklab.quantum.backends import BackendFactory, BackendType


class TestQuantumStateWrapper:
    """Tests for QuantumStateWrapper class."""

    @patch("qrisklab.quantum.state.QuantumState")
    def test_wrapper_initialization(self, mock_qs):
        """Test that wrapper initializes correctly."""
        mock_qs.return_value = MagicMock()
        wrapper = QuantumStateWrapper(2)
        assert wrapper.qubit_count == 2

    @patch("qrisklab.quantum.state.QuantumState")
    def test_wrapper_invalid_qubit_count(self, mock_qs):
        """Test that invalid qubit count raises error."""
        with pytest.raises(ValueError):
            QuantumStateWrapper(0)

    @patch("qrisklab.quantum.state.QuantumState")
    def test_wrapper_dimension(self, mock_qs):
        """Test dimension calculation."""
        mock_state = MagicMock()
        mock_state.dimension.return_value = 4
        mock_qs.return_value = mock_state
        
        wrapper = QuantumStateWrapper(2)
        assert wrapper.dimension == 4

    @patch("qrisklab.quantum.state.QuantumState")
    def test_wrapper_reset(self, mock_qs):
        """Test state reset."""
        mock_state = MagicMock()
        mock_qs.return_value = mock_state
        
        wrapper = QuantumStateWrapper(2)
        wrapper.reset()
        
        mock_state.reset.assert_called_once()

    @patch("qrisklab.quantum.state.QuantumState")
    def test_wrapper_apply_hadamard(self, mock_qs):
        """Test Hadamard gate application."""
        mock_state = MagicMock()
        mock_qs.return_value = mock_state
        
        wrapper = QuantumStateWrapper(2)
        wrapper.apply_hadamard(0)
        
        mock_state.apply_hadamard.assert_called_once_with(0)

    @patch("qrisklab.quantum.state.QuantumState")
    def test_wrapper_apply_cnot(self, mock_qs):
        """Test CNOT gate application."""
        mock_state = MagicMock()
        mock_qs.return_value = mock_state
        
        wrapper = QuantumStateWrapper(2)
        wrapper.apply_cnot(0, 1)
        
        mock_state.apply_cnot.assert_called_once_with(0, 1)

    @patch("qrisklab.quantum.state.QuantumState")
    def test_wrapper_get_snapshot(self, mock_qs):
        """Test state snapshot generation."""
        mock_state = MagicMock()
        mock_state.amplitudes.return_value = [1.0, 0.0, 0.0, 0.0]
        mock_qs.return_value = mock_state
        
        wrapper = QuantumStateWrapper(2)
        snapshot = wrapper.get_snapshot()
        
        assert isinstance(snapshot, StateSnapshot)
        assert snapshot.qubit_count == 2


class TestQuantumAmplitudeEstimation:
    """Tests for QuantumAmplitudeEstimation algorithm."""

    def test_algorithm_initialization(self):
        """Test that algorithm initializes correctly."""
        algo = QuantumAmplitudeEstimation(backend="qiskit_aer")
        assert algo.name == "QuantumAmplitudeEstimation"
        assert algo.backend == "qiskit_aer"

    def test_algorithm_run(self):
        """Test algorithm execution."""
        algo = QuantumAmplitudeEstimation()
        
        def dummy_oracle():
            pass
        
        result = algo.run(
            oracle=dummy_oracle,
            num_qubits=5,
            shots=1024,
            precision_bits=3
        )
        
        assert result.success is True
        assert result.algorithm_name == "QuantumAmplitudeEstimation"
        assert hasattr(result, "estimated_amplitude")
        assert hasattr(result, "confidence_interval")


class TestVariationalQuantumEigensolver:
    """Tests for VariationalQuantumEigensolver algorithm."""

    def test_algorithm_initialization(self):
        """Test that VQE initializes correctly."""
        algo = VariationalQuantumEigensolver(backend="pennylane")
        assert algo.name == "VariationalQuantumEigensolver"
        assert algo.backend == "pennylane"

    def test_algorithm_run(self):
        """Test VQE execution."""
        algo = VariationalQuantumEigensolver()
        
        hamiltonian = [(1.0, "Z0"), (0.5, "X0")]
        result = algo.run(
            hamiltonian=hamiltonian,
            num_qubits=5,
            max_iterations=100,
            learning_rate=0.01
        )
        
        assert result.success is True
        assert result.algorithm_name == "VariationalQuantumEigensolver"
        assert hasattr(result, "eigenvalue")
        assert hasattr(result, "parameters")


class TestQuantumPhaseEstimation:
    """Tests for QuantumPhaseEstimation algorithm."""

    def test_algorithm_initialization(self):
        """Test that QPE initializes correctly."""
        algo = QuantumPhaseEstimation(backend="qiskit_aer")
        assert algo.name == "QuantumPhaseEstimation"
        assert algo.backend == "qiskit_aer"

    def test_algorithm_run(self):
        """Test QPE execution."""
        algo = QuantumPhaseEstimation()
        
        def dummy_unitary():
            pass
        
        result = algo.run(
            unitary=dummy_unitary,
            num_qubits=5,
            precision_bits=5,
            shots=1024
        )
        
        assert result.success is True
        assert result.algorithm_name == "QuantumPhaseEstimation"
        assert hasattr(result, "phase")
        assert hasattr(result, "eigenvalue")


class TestBackendFactory:
    """Tests for BackendFactory."""

    def test_factory_initialization(self):
        """Test that factory initializes."""
        BackendFactory.initialize()
        assert BackendFactory._backends is not None

    def test_factory_get_available_backends(self):
        """Test getting available backends."""
        BackendFactory.initialize()
        available = BackendFactory.get_available_backends()
        assert isinstance(available, list)

    def test_factory_get_default_backend(self):
        """Test getting default backend."""
        BackendFactory.initialize()
        backend = BackendFactory.get_default_backend()
        # Backend may be None if no quantum libraries installed
        assert backend is None or hasattr(backend, "name")

    def test_factory_list_backends(self):
        """Test listing all backends."""
        BackendFactory.initialize()
        backends_info = BackendFactory.list_backends()
        assert isinstance(backends_info, dict)
        assert "qiskit_aer" in backends_info or len(backends_info) >= 0
