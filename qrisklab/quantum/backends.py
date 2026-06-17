"""
Quantum backend selection and factory.

Provides backend factory for selecting and configuring quantum computing
backends (Qiskit, PennyLane, Cirq, etc.) with graceful fallbacks.
"""

from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from enum import Enum
import logging

from qrisklab.utils.logger import get_logger
from qrisklab.config import config

logger = get_logger(__name__)


class BackendType(Enum):
    """Supported quantum backends."""
    QISKIT_AER = "qiskit_aer"
    QISKIT_IBMQ = "qiskit_ibmq"
    PENNYLANE = "pennylane"
    CIRQ = "cirq"
    AMAZON_BRAKET = "amazon_braket"


class QuantumBackend(ABC):
    """Abstract base class for quantum backends."""

    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize quantum backend.

        Args:
            name: Backend name
            config: Backend configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.is_available = self._check_availability()
        logger.debug(f"Initialized {name} backend (available={self.is_available})")

    @abstractmethod
    def _check_availability(self) -> bool:
        """Check if backend is available."""
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Get backend information."""
        pass


class QiskitAerBackend(QuantumBackend):
    """Qiskit Aer simulator backend."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize Qiskit Aer backend."""
        super().__init__("qiskit_aer", config)

    def _check_availability(self) -> bool:
        """Check if Qiskit is installed."""
        try:
            import qiskit
            import qiskit_aer
            return True
        except ImportError:
            logger.warning("Qiskit/Qiskit-Aer not installed. Install with: pip install qiskit qiskit-aer")
            return False

    def get_info(self) -> Dict[str, Any]:
        """Get Qiskit Aer backend information."""
        if not self.is_available:
            return {"status": "unavailable", "reason": "qiskit not installed"}

        try:
            import qiskit
            return {
                "name": "qiskit_aer",
                "version": qiskit.__version__,
                "type": "simulator",
                "status": "available",
            }
        except Exception as e:
            logger.error(f"Error getting Qiskit info: {e}")
            return {"status": "error", "reason": str(e)}


class PennyLaneBackend(QuantumBackend):
    """PennyLane quantum backend."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize PennyLane backend."""
        super().__init__("pennylane", config)

    def _check_availability(self) -> bool:
        """Check if PennyLane is installed."""
        try:
            import pennylane
            return True
        except ImportError:
            logger.warning("PennyLane not installed. Install with: pip install pennylane")
            return False

    def get_info(self) -> Dict[str, Any]:
        """Get PennyLane backend information."""
        if not self.is_available:
            return {"status": "unavailable", "reason": "pennylane not installed"}

        try:
            import pennylane
            return {
                "name": "pennylane",
                "version": pennylane.__version__,
                "type": "hybrid",
                "status": "available",
            }
        except Exception as e:
            logger.error(f"Error getting PennyLane info: {e}")
            return {"status": "error", "reason": str(e)}


class CirqBackend(QuantumBackend):
    """Google Cirq quantum backend."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize Cirq backend."""
        super().__init__("cirq", config)

    def _check_availability(self) -> bool:
        """Check if Cirq is installed."""
        try:
            import cirq
            return True
        except ImportError:
            logger.warning("Cirq not installed. Install with: pip install cirq")
            return False

    def get_info(self) -> Dict[str, Any]:
        """Get Cirq backend information."""
        if not self.is_available:
            return {"status": "unavailable", "reason": "cirq not installed"}

        try:
            import cirq
            return {
                "name": "cirq",
                "version": cirq.__version__,
                "type": "simulator",
                "status": "available",
            }
        except Exception as e:
            logger.error(f"Error getting Cirq info: {e}")
            return {"status": "error", "reason": str(e)}


class AmazonBraketBackend(QuantumBackend):
    """Amazon Braket quantum backend."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize Amazon Braket backend."""
        super().__init__("amazon_braket", config)

    def _check_availability(self) -> bool:
        """Check if Amazon Braket SDK is installed."""
        try:
            import braket
            return True
        except ImportError:
            logger.warning("Amazon Braket SDK not installed. Install with: pip install amazon-braket-sdk")
            return False

    def get_info(self) -> Dict[str, Any]:
        """Get Amazon Braket backend information."""
        if not self.is_available:
            return {"status": "unavailable", "reason": "amazon-braket-sdk not installed"}

        try:
            import braket
            return {
                "name": "amazon_braket",
                "version": braket.__version__,
                "type": "cloud",
                "status": "available",
            }
        except Exception as e:
            logger.error(f"Error getting Amazon Braket info: {e}")
            return {"status": "error", "reason": str(e)}


class BackendFactory:
    """Factory for creating and managing quantum backends."""

    _backends: Dict[str, QuantumBackend] = {}
    _default_backend: Optional[str] = None

    @classmethod
    def initialize(cls) -> None:
        """Initialize all available backends."""
        logger.debug("Initializing quantum backends...")

        cls._backends = {
            "qiskit_aer": QiskitAerBackend(),
            "pennylane": PennyLaneBackend(),
            "cirq": CirqBackend(),
            "amazon_braket": AmazonBraketBackend(),
        }

        # Set default backend from config
        default = config.QUANTUM_BACKEND
        if default in cls._backends and cls._backends[default].is_available:
            cls._default_backend = default
            logger.info(f"Default quantum backend: {default}")
        else:
            # Find first available backend
            for name, backend in cls._backends.items():
                if backend.is_available:
                    cls._default_backend = name
                    logger.info(f"Default quantum backend: {name} (configured backend unavailable)")
                    break

        if cls._default_backend is None:
            logger.warning("No quantum backends available. Install qiskit, pennylane, or cirq.")

    @classmethod
    def get_backend(cls, name: Optional[str] = None) -> Optional[QuantumBackend]:
        """
        Get a quantum backend by name.

        Args:
            name: Backend name. If None, returns default backend.

        Returns:
            QuantumBackend instance or None if not available
        """
        if not cls._backends:
            cls.initialize()

        if name is None:
            name = cls._default_backend

        if name not in cls._backends:
            logger.error(f"Unknown backend: {name}")
            return None

        backend = cls._backends[name]
        if not backend.is_available:
            logger.warning(f"Backend {name} is not available")
            return None

        return backend

    @classmethod
    def list_backends(cls) -> Dict[str, Dict[str, Any]]:
        """
        List all available backends with their information.

        Returns:
            Dictionary mapping backend names to their info
        """
        if not cls._backends:
            cls.initialize()

        return {name: backend.get_info() for name, backend in cls._backends.items()}

    @classmethod
    def get_available_backends(cls) -> List[str]:
        """
        Get list of available backend names.

        Returns:
            List of available backend names
        """
        if not cls._backends:
            cls.initialize()

        return [name for name, backend in cls._backends.items() if backend.is_available]

    @classmethod
    def get_default_backend(cls) -> Optional[QuantumBackend]:
        """
        Get the default quantum backend.

        Returns:
            Default QuantumBackend or None if none available
        """
        if not cls._backends:
            cls.initialize()

        if cls._default_backend is None:
            return None

        return cls._backends[cls._default_backend]

    @classmethod
    def set_default_backend(cls, name: str) -> bool:
        """
        Set the default quantum backend.

        Args:
            name: Backend name to set as default

        Returns:
            True if successful, False otherwise
        """
        if not cls._backends:
            cls.initialize()

        if name not in cls._backends:
            logger.error(f"Unknown backend: {name}")
            return False

        if not cls._backends[name].is_available:
            logger.error(f"Backend {name} is not available")
            return False

        cls._default_backend = name
        logger.info(f"Default quantum backend set to: {name}")
        return True


# Initialize backends on module import
BackendFactory.initialize()


__all__ = [
    "BackendFactory",
    "QuantumBackend",
    "QiskitAerBackend",
    "PennyLaneBackend",
    "CirqBackend",
    "AmazonBraketBackend",
    "BackendType",
]
