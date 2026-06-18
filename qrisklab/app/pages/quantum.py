"""
Quantum Algorithms Page

Provides interface for running quantum algorithms.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from qrisklab.quantum.algorithms import (
    QuantumAmplitudeEstimation,
    VariationalQuantumEigensolver,
    QuantumPhaseEstimation,
)
from qrisklab.quantum.backends import BackendFactory
from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)


def show():
    """Display quantum algorithms page."""
    st.header("🔬 Quantum Algorithms")
    st.markdown("Run quantum algorithms for financial analysis")
    
    # Display available backends
    show_backend_status()
    
    # Create tabs for different algorithms
    tab1, tab2, tab3 = st.tabs([
        "Amplitude Estimation",
        "Variational Quantum Eigensolver",
        "Quantum Phase Estimation"
    ])
    
    with tab1:
        show_amplitude_estimation()
    
    with tab2:
        show_vqe()
    
    with tab3:
        show_phase_estimation()


def show_backend_status():
    """Display quantum backend status."""
    st.subheader("Quantum Backends")
    
    try:
        available = BackendFactory.get_available_backends()
        default = BackendFactory.get_default_backend()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Available Backends", len(available))
        col2.metric("Default Backend", default.name if default else "None")
        col3.metric("Status", "✅ Ready" if available else "❌ No backends")
        
        if available:
            st.markdown("**Available Backends:**")
            for backend_name in available:
                st.write(f"- {backend_name}")
    
    except Exception as e:
        st.warning(f"Could not load backend information: {str(e)}")
        logger.warning(f"Backend status error: {e}")


def show_amplitude_estimation():
    """Display amplitude estimation interface."""
    st.subheader("Quantum Amplitude Estimation")
    st.markdown("Estimate amplitudes with quadratic speedup over classical methods")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_qubits = st.slider(
            "Number of Qubits",
            min_value=1,
            max_value=20,
            value=5,
            help="Number of qubits for the algorithm"
        )
        shots = st.number_input(
            "Measurement Shots",
            min_value=100,
            value=1024,
            step=100,
            help="Number of measurement shots"
        )
    
    with col2:
        precision_bits = st.slider(
            "Precision Bits",
            min_value=1,
            max_value=10,
            value=3,
            help="Bits for phase estimation precision"
        )
        backend = st.selectbox(
            "Quantum Backend",
            BackendFactory.get_available_backends() or ["qiskit_aer"],
            help="Quantum backend to use"
        )
    
    if st.button("Run Amplitude Estimation", key="ae_run"):
        try:
            with st.spinner("Running quantum algorithm..."):
                algorithm = QuantumAmplitudeEstimation(backend=backend)
                
                # Placeholder oracle
                def oracle():
                    pass
                
                result = algorithm.run(
                    oracle=oracle,
                    num_qubits=num_qubits,
                    shots=shots,
                    precision_bits=precision_bits,
                )
            
            # Display results
            col1, col2, col3 = st.columns(3)
            col1.metric("Estimated Amplitude", f"{result.estimated_amplitude:.4f}")
            col2.metric("Execution Time", f"{result.execution_time_seconds:.3f}s")
            col3.metric("Iterations", result.iterations)
            
            # Display confidence interval
            ci_low, ci_high = result.confidence_interval
            st.info(f"Confidence Interval: [{ci_low:.4f}, {ci_high:.4f}]")
            
            logger.info(f"Amplitude estimation completed: {result.estimated_amplitude:.4f}")
            
        except Exception as e:
            st.error(f"Error running amplitude estimation: {str(e)}")
            logger.error(f"Amplitude estimation error: {e}")


def show_vqe():
    """Display VQE interface."""
    st.subheader("Variational Quantum Eigensolver (VQE)")
    st.markdown("Find ground states with hybrid quantum-classical optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_qubits = st.slider(
            "Number of Qubits",
            min_value=1,
            max_value=20,
            value=5,
            key="vqe_qubits"
        )
        max_iterations = st.number_input(
            "Max Iterations",
            min_value=10,
            value=100,
            step=10,
            help="Maximum optimization iterations"
        )
    
    with col2:
        learning_rate = st.slider(
            "Learning Rate",
            min_value=0.001,
            max_value=0.1,
            value=0.01,
            step=0.001,
            help="Optimizer learning rate"
        )
        backend = st.selectbox(
            "Quantum Backend",
            BackendFactory.get_available_backends() or ["pennylane"],
            key="vqe_backend"
        )
    
    if st.button("Run VQE", key="vqe_run"):
        try:
            with st.spinner("Running VQE optimization..."):
                algorithm = VariationalQuantumEigensolver(backend=backend)
                
                # Placeholder Hamiltonian
                hamiltonian = [(1.0, "Z0"), (0.5, "X0")]
                
                result = algorithm.run(
                    hamiltonian=hamiltonian,
                    num_qubits=num_qubits,
                    max_iterations=max_iterations,
                    learning_rate=learning_rate,
                )
            
            # Display results
            col1, col2, col3 = st.columns(3)
            col1.metric("Eigenvalue", f"{result.eigenvalue:.6f}")
            col2.metric("Execution Time", f"{result.execution_time_seconds:.3f}s")
            col3.metric("Iterations", result.iterations)
            
            st.info(f"Optimization converged after {result.iterations} iterations")
            
            logger.info(f"VQE completed: eigenvalue={result.eigenvalue:.6f}")
            
        except Exception as e:
            st.error(f"Error running VQE: {str(e)}")
            logger.error(f"VQE error: {e}")


def show_phase_estimation():
    """Display quantum phase estimation interface."""
    st.subheader("Quantum Phase Estimation (QPE)")
    st.markdown("Estimate eigenvalues with exponential speedup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_qubits = st.slider(
            "Number of Qubits",
            min_value=1,
            max_value=20,
            value=5,
            key="qpe_qubits"
        )
        precision_bits = st.slider(
            "Precision Bits",
            min_value=1,
            max_value=10,
            value=5,
            key="qpe_precision"
        )
    
    with col2:
        shots = st.number_input(
            "Measurement Shots",
            min_value=100,
            value=1024,
            step=100,
            key="qpe_shots"
        )
        backend = st.selectbox(
            "Quantum Backend",
            BackendFactory.get_available_backends() or ["qiskit_aer"],
            key="qpe_backend"
        )
    
    if st.button("Run Phase Estimation", key="qpe_run"):
        try:
            with st.spinner("Running quantum phase estimation..."):
                algorithm = QuantumPhaseEstimation(backend=backend)
                
                # Placeholder unitary
                def unitary():
                    pass
                
                result = algorithm.run(
                    unitary=unitary,
                    num_qubits=num_qubits,
                    precision_bits=precision_bits,
                    shots=shots,
                )
            
            # Display results
            col1, col2, col3 = st.columns(3)
            col1.metric("Phase", f"{result.phase:.6f}")
            col2.metric("Eigenvalue", f"{result.eigenvalue:.6f}")
            col3.metric("Execution Time", f"{result.execution_time_seconds:.3f}s")
            
            st.info(f"Phase estimation precision: {result.precision_bits} bits")
            
            logger.info(f"Phase estimation completed: phase={result.phase:.6f}")
            
        except Exception as e:
            st.error(f"Error running phase estimation: {str(e)}")
            logger.error(f"Phase estimation error: {e}")
