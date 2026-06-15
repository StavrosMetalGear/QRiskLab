/**
 * @file bindings.cpp
 * @brief pybind11 bindings for QRiskLab C++ modules
 *
 * Exposes C++ classes to Python:
 * - QuantumState: Quantum state management and operations
 * - MonteCarlo: Option pricing and portfolio simulation
 * - RiskMetrics: Risk metrics calculations (VaR, CVaR)
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>

#include "core/QuantumState.h"
#include "finance/MonteCarlo.h"
#include "finance/RiskMetrics.h"

namespace py = pybind11;
using namespace qrisk::core;
using namespace qrisk::finance;

/**
 * pybind11 module definition for _qrisklab_core
 * This module exposes the C++ quantum and finance classes to Python
 */
PYBIND11_MODULE(_qrisklab_core, m)
{
    m.doc() = "QRiskLab Core C++ Module - Quantum and Finance Bindings";

    // ========================================================================
    // QuantumState Bindings
    // ========================================================================
    py::class_<QuantumState>(m, "QuantumState",
        "Quantum state representation and operations for quantum circuits")
        .def(py::init<std::size_t>(),
            py::arg("qubit_count"),
            "Initialize a quantum state with the specified number of qubits")
        
        .def("qubit_count", &QuantumState::qubitCount,
            "Get the number of qubits in this quantum state")
        
        .def("dimension", &QuantumState::dimension,
            "Get the dimension of the state vector (2^qubit_count)")
        
        .def("reset", &QuantumState::reset,
            "Reset the quantum state to |0...0>")
        
        .def("apply_hadamard", &QuantumState::applyHadamard,
            py::arg("target"),
            "Apply Hadamard gate to target qubit")
        
        .def("apply_cnot", &QuantumState::applyCNOT,
            py::arg("control"), py::arg("target"),
            "Apply CNOT (controlled-NOT) gate")
        
        .def("apply_x", &QuantumState::applyX,
            py::arg("target"),
            "Apply Pauli-X (NOT) gate to target qubit")
        
        .def("apply_z", &QuantumState::applyZ,
            py::arg("target"),
            "Apply Pauli-Z gate to target qubit")
        
        .def("measure", &QuantumState::measure,
            py::arg("target"), py::arg("rng"),
            "Measure target qubit and collapse state (returns 0 or 1)")
        
        .def("amplitudes", &QuantumState::amplitudes,
            py::return_value_policy::reference_internal,
            "Get the state vector amplitudes")
        
        .def("probability_of_basis_state", &QuantumState::probabilityOfBasisState,
            py::arg("index"),
            "Get probability of measuring a specific basis state")
        
        .def("print_state", &QuantumState::printState,
            py::arg("epsilon") = 1e-10,
            "Print the quantum state (amplitudes above epsilon threshold)");

    // ========================================================================
    // OptionPricingResult Bindings
    // ========================================================================
    py::class_<OptionPricingResult>(m, "OptionPricingResult",
        "Result of European call option pricing")
        .def_readwrite("estimated_price", &OptionPricingResult::estimatedPrice,
            "Estimated option price from Monte Carlo")
        .def_readwrite("standard_error", &OptionPricingResult::standardError,
            "Standard error of the price estimate")
        .def_readwrite("discounted_payoffs", &OptionPricingResult::discountedPayoffs,
            "Vector of discounted payoffs from all paths");

    // ========================================================================
    // MonteCarlo Bindings
    // ========================================================================
    py::class_<MonteCarlo>(m, "MonteCarlo",
        "Monte Carlo methods for option pricing and portfolio simulation")
        
        .def_static("price_european_call",
            &MonteCarlo::priceEuropeanCall,
            py::arg("spot_price"),
            py::arg("strike_price"),
            py::arg("risk_free_rate"),
            py::arg("volatility"),
            py::arg("maturity_years"),
            py::arg("paths"),
            py::arg("seed"),
            "Price a European call option using Monte Carlo simulation\n\n"
            "Args:\n"
            "  spot_price: Current stock price\n"
            "  strike_price: Option strike price\n"
            "  risk_free_rate: Risk-free interest rate\n"
            "  volatility: Stock volatility (annualized)\n"
            "  maturity_years: Time to maturity in years\n"
            "  paths: Number of Monte Carlo paths\n"
            "  seed: Random seed for reproducibility\n\n"
            "Returns:\n"
            "  OptionPricingResult with estimated_price, standard_error, and discounted_payoffs")
        
        .def_static("simulate_portfolio_losses",
            &MonteCarlo::simulatePortfolioLosses,
            py::arg("initial_portfolio_value"),
            py::arg("expected_return"),
            py::arg("volatility"),
            py::arg("time_horizon_years"),
            py::arg("scenarios"),
            py::arg("seed"),
            "Simulate portfolio losses using Monte Carlo\n\n"
            "Args:\n"
            "  initial_portfolio_value: Starting portfolio value\n"
            "  expected_return: Expected portfolio return\n"
            "  volatility: Portfolio volatility\n"
            "  time_horizon_years: Time horizon in years\n"
            "  scenarios: Number of simulation scenarios\n"
            "  seed: Random seed for reproducibility\n\n"
            "Returns:\n"
            "  Vector of simulated portfolio losses");

    // ========================================================================
    // RiskMetrics Bindings
    // ========================================================================
    py::class_<RiskMetrics>(m, "RiskMetrics",
        "Risk metrics calculations (Value at Risk, Conditional Value at Risk)")
        
        .def_static("value_at_risk",
            &RiskMetrics::valueAtRisk,
            py::arg("losses"),
            py::arg("confidence_level"),
            "Calculate Value at Risk (VaR)\n\n"
            "Args:\n"
            "  losses: Vector of portfolio losses\n"
            "  confidence_level: Confidence level (e.g., 0.95 for 95%)\n\n"
            "Returns:\n"
            "  Value at Risk at the specified confidence level")
        
        .def_static("conditional_value_at_risk",
            &RiskMetrics::conditionalValueAtRisk,
            py::arg("losses"),
            py::arg("confidence_level"),
            "Calculate Conditional Value at Risk (CVaR / Expected Shortfall)\n\n"
            "Args:\n"
            "  losses: Vector of portfolio losses\n"
            "  confidence_level: Confidence level (e.g., 0.95 for 95%)\n\n"
            "Returns:\n"
            "  Conditional Value at Risk at the specified confidence level");
}
