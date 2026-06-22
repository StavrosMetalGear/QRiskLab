"""
Quantum algorithms API endpoints.

Provides REST endpoints for quantum algorithm execution and backend management.
"""

from fastapi import APIRouter, HTTPException
import logging

from qrisklab.quantum.backends import BackendFactory
from qrisklab.quantum.algorithms import (
    QuantumAmplitudeEstimation,
    VariationalQuantumEigensolver,
    QuantumPhaseEstimation,
)
from qrisklab.api.models import (
    QuantumBackendListResponse,
    QuantumAmplitudeEstimationRequest,
    QuantumAlgorithmResponse,
    QuantumStateRequest,
    QuantumStateResponse,
    ErrorResponse,
)
from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/quantum", tags=["quantum"])


@router.get(
    "/backends",
    response_model=QuantumBackendListResponse,
    summary="List Quantum Backends",
    description="Get list of available quantum backends",
)
async def list_backends() -> QuantumBackendListResponse:
    """
    List available quantum backends.

    Returns:
        QuantumBackendListResponse with available backends and their info

    Raises:
        HTTPException: If backend listing fails
    """
    try:
        logger.info("Listing quantum backends")

        available = BackendFactory.get_available_backends()
        backend_info = BackendFactory.list_backends()
        default = BackendFactory.get_default_backend()
        default_name = None
        if default:
            default_name = getattr(default, "name", default)
            if not isinstance(default_name, str):
                default_name = str(default_name)

        return QuantumBackendListResponse(
            available_backends=available,
            default_backend=default_name,
            backend_info=backend_info,
        )

    except Exception as e:
        logger.error(f"Error listing backends: {e}")
        raise HTTPException(status_code=500, detail="Internal server error listing backends")


@router.post(
    "/amplitude-estimation",
    response_model=QuantumAlgorithmResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Quantum Amplitude Estimation",
    description="Run quantum amplitude estimation algorithm",
)
async def run_amplitude_estimation(
    request: QuantumAmplitudeEstimationRequest,
) -> QuantumAlgorithmResponse:
    """
    Run quantum amplitude estimation algorithm.

    Args:
        request: Algorithm parameters

    Returns:
        QuantumAlgorithmResponse with algorithm results

    Raises:
        HTTPException: If algorithm fails
    """
    try:
        logger.info(
            f"Running amplitude estimation: qubits={request.num_qubits}, "
            f"shots={request.shots}, backend={request.backend}"
        )

        backend = request.backend or BackendFactory.get_default_backend().name
        algorithm = QuantumAmplitudeEstimation(backend=backend)

        # Run with placeholder oracle
        def placeholder_oracle():
            pass

        result = algorithm.run(
            oracle=placeholder_oracle,
            num_qubits=request.num_qubits,
            shots=request.shots,
            precision_bits=request.precision_bits,
        )

        return QuantumAlgorithmResponse(
            algorithm_name=result.algorithm_name,
            success=result.success,
            iterations=result.iterations,
            execution_time_seconds=result.execution_time_seconds,
            result={
                "estimated_amplitude": result.estimated_amplitude,
                "confidence_interval": result.confidence_interval,
                "shots": result.shots,
            },
            metadata=result.metadata,
        )

    except ValueError as e:
        logger.error(f"Amplitude estimation validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Amplitude estimation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during amplitude estimation")


@router.post(
    "/vqe",
    response_model=QuantumAlgorithmResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Variational Quantum Eigensolver",
    description="Run variational quantum eigensolver algorithm",
)
async def run_vqe(request: QuantumAmplitudeEstimationRequest) -> QuantumAlgorithmResponse:
    """
    Run Variational Quantum Eigensolver (VQE) algorithm.

    Args:
        request: Algorithm parameters

    Returns:
        QuantumAlgorithmResponse with algorithm results

    Raises:
        HTTPException: If algorithm fails
    """
    try:
        logger.info(
            f"Running VQE: qubits={request.num_qubits}, "
            f"backend={request.backend}"
        )

        backend = request.backend or BackendFactory.get_default_backend().name
        algorithm = VariationalQuantumEigensolver(backend=backend)

        # Run with placeholder Hamiltonian
        hamiltonian = [(1.0, "Z0"), (0.5, "X0")]

        result = algorithm.run(
            hamiltonian=hamiltonian,
            num_qubits=request.num_qubits,
            max_iterations=100,
            learning_rate=0.01,
        )

        return QuantumAlgorithmResponse(
            algorithm_name=result.algorithm_name,
            success=result.success,
            iterations=result.iterations,
            execution_time_seconds=result.execution_time_seconds,
            result={
                "eigenvalue": result.eigenvalue,
                "parameters": result.parameters,
            },
            metadata=result.metadata,
        )

    except ValueError as e:
        logger.error(f"VQE validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"VQE error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during VQE")


@router.post(
    "/phase-estimation",
    response_model=QuantumAlgorithmResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Quantum Phase Estimation",
    description="Run quantum phase estimation algorithm",
)
async def run_phase_estimation(
    request: QuantumAmplitudeEstimationRequest,
) -> QuantumAlgorithmResponse:
    """
    Run quantum phase estimation algorithm.

    Args:
        request: Algorithm parameters

    Returns:
        QuantumAlgorithmResponse with algorithm results

    Raises:
        HTTPException: If algorithm fails
    """
    try:
        logger.info(
            f"Running phase estimation: qubits={request.num_qubits}, "
            f"precision_bits={request.precision_bits}, backend={request.backend}"
        )

        backend = request.backend or BackendFactory.get_default_backend().name
        algorithm = QuantumPhaseEstimation(backend=backend)

        # Run with placeholder unitary
        def placeholder_unitary():
            pass

        result = algorithm.run(
            unitary=placeholder_unitary,
            num_qubits=request.num_qubits,
            precision_bits=request.precision_bits,
            shots=request.shots,
        )

        return QuantumAlgorithmResponse(
            algorithm_name=result.algorithm_name,
            success=result.success,
            iterations=result.iterations,
            execution_time_seconds=result.execution_time_seconds,
            result={
                "phase": result.phase,
                "eigenvalue": result.eigenvalue,
                "precision_bits": result.precision_bits,
            },
            metadata=result.metadata,
        )

    except ValueError as e:
        logger.error(f"Phase estimation validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Phase estimation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during phase estimation")


__all__ = ["router"]
