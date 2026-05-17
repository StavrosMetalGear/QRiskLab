#include "core/QuantumState.h"
#include "finance/MonteCarlo.h"
#include "finance/RiskMetrics.h"

#include <chrono>
#include <cstdint>
#include <exception>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>

using qrisk::core::QuantumState;
using qrisk::finance::MonteCarlo;
using qrisk::finance::RiskMetrics;

namespace
{
    void printHeader()
    {
        std::cout << "========================================\n";
        std::cout << " QRiskLab\n";
        std::cout << " C++ Quantum Risk Analysis Simulator\n";
        std::cout << "========================================\n\n";
    }

    void runBellDemo()
    {
        std::cout << "[Quantum Demo] Bell State\n\n";

        QuantumState state(2);

        state.applyHadamard(0);
        state.applyCNOT(0, 1);

        std::cout << "State after H(0) and CNOT(0, 1):\n";
        state.printState();

        std::cout << "\nExpected result: approximately 50% |00>, 50% |11>\n\n";

        constexpr int shots = 1000;
        int count00 = 0;
        int count01 = 0;
        int count10 = 0;
        int count11 = 0;

        std::mt19937_64 rng(12345);

        for (int i = 0; i < shots; ++i)
        {
            QuantumState shotState(2);
            shotState.applyHadamard(0);
            shotState.applyCNOT(0, 1);

            const int q0 = shotState.measure(0, rng);
            const int q1 = shotState.measure(1, rng);

            if (q0 == 0 && q1 == 0) ++count00;
            if (q0 == 0 && q1 == 1) ++count01;
            if (q0 == 1 && q1 == 0) ++count10;
            if (q0 == 1 && q1 == 1) ++count11;
        }

        std::cout << "Shots: " << shots << '\n';
        std::cout << "|00>: " << count00 << '\n';
        std::cout << "|01>: " << count01 << '\n';
        std::cout << "|10>: " << count10 << '\n';
        std::cout << "|11>: " << count11 << '\n';
    }

    void runFinanceDemo()
    {
        std::cout << "[Finance Demo] Monte Carlo Option Pricing + Risk Metrics\n\n";

        const double spot = 100.0;
        const double strike = 105.0;
        const double riskFreeRate = 0.05;
        const double volatility = 0.20;
        const double maturityYears = 1.0;
        const std::size_t paths = 100000;
        const std::uint64_t seed = 2026;

        const auto start = std::chrono::high_resolution_clock::now();

        const auto optionResult = MonteCarlo::priceEuropeanCall(
            spot,
            strike,
            riskFreeRate,
            volatility,
            maturityYears,
            paths,
            seed
        );

        const auto losses = MonteCarlo::simulatePortfolioLosses(
            1'000'000.0,
            0.07,
            0.18,
            1.0,
            paths,
            seed
        );

        const double var95 = RiskMetrics::valueAtRisk(losses, 0.95);
        const double cvar95 = RiskMetrics::conditionalValueAtRisk(losses, 0.95);

        const auto end = std::chrono::high_resolution_clock::now();
        const auto elapsedMs = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();

        std::cout << std::fixed << std::setprecision(6);

        std::cout << "European Call Option Inputs:\n";
        std::cout << "Spot Price:      " << spot << '\n';
        std::cout << "Strike Price:    " << strike << '\n';
        std::cout << "Risk-Free Rate:  " << riskFreeRate << '\n';
        std::cout << "Volatility:      " << volatility << '\n';
        std::cout << "Maturity:        " << maturityYears << " year(s)\n";
        std::cout << "Paths:           " << paths << "\n\n";

        std::cout << "Estimated Call Price: " << optionResult.estimatedPrice << '\n';
        std::cout << "Standard Error:       " << optionResult.standardError << "\n\n";

        std::cout << "Portfolio Risk:\n";
        std::cout << "95% VaR:  " << var95 << '\n';
        std::cout << "95% CVaR: " << cvar95 << "\n\n";

        std::cout << "Elapsed: " << elapsedMs << " ms\n";
    }

    void printUsage()
    {
        std::cout << "Usage:\n";
        std::cout << "  QRiskLab bell\n";
        std::cout << "  QRiskLab finance\n";
        std::cout << "  QRiskLab all\n";
    }
}

int main(int argc, char** argv)
{
    try
    {
        printHeader();

        if (argc < 2)
        {
            printUsage();
            return 0;
        }

        const std::string mode = argv[1];

        if (mode == "bell")
        {
            runBellDemo();
        }
        else if (mode == "finance")
        {
            runFinanceDemo();
        }
        else if (mode == "all")
        {
            runBellDemo();
            std::cout << "\n----------------------------------------\n\n";
            runFinanceDemo();
        }
        else
        {
            std::cerr << "Unknown mode: " << mode << "\n\n";
            printUsage();
            return 1;
        }

        return 0;
    }
    catch (const std::exception& ex)
    {
        std::cerr << "Error: " << ex.what() << '\n';
        return 1;
    }
}