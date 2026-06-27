#include "core/QuantumState.h"
#include "finance/MonteCarlo.h"
#include "finance/RiskMetrics.h"
#include "utils/logger.h"
#include "utils/timer.h"
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
        QRISK_LOG_INFO("Starting Bell state demo.");
        qrisk::utils::ScopedTimer scopedTimer("Bell state demo");
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

        QRISK_LOG_INFO("Bell state demo completed.");
    }

    void runFinanceDemo()
    {
        QRISK_LOG_INFO("Starting finance Monte Carlo demo.");

        std::cout << "[Finance Demo] Monte Carlo Option Pricing + Risk Metrics\n\n";

        const double spot = 100.0;
        const double strike = 105.0;
        const double riskFreeRate = 0.05;
        const double volatility = 0.20;
        const double maturityYears = 1.0;
        const std::size_t paths = 100000;
        const std::uint64_t seed = 2026;

        QRISK_LOG_INFO("Monte Carlo paths: " + std::to_string(paths));
        QRISK_LOG_INFO("Monte Carlo seed: " + std::to_string(seed));

        qrisk::utils::Timer timer;

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

        const double elapsedMs = timer.elapsedMilliseconds();

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

        QRISK_LOG_INFO("Finance Monte Carlo demo completed in " + std::to_string(elapsedMs) + " ms.");
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
        qrisk::utils::Logger::instance().setMinimumLevel(qrisk::utils::LogLevel::Info);
        qrisk::utils::Logger::instance().enableConsole(true);

        QRISK_LOG_INFO("QRiskLab started.");

        printHeader();

        if (argc < 2)
        {
            QRISK_LOG_WARNING("No mode provided by user.");
            printUsage();
            QRISK_LOG_INFO("QRiskLab finished.");
            return 0;
        }

        const std::string mode = argv[1];

        QRISK_LOG_INFO("Selected mode: " + mode);

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
            QRISK_LOG_ERROR("Unknown mode: " + mode);
            std::cerr << "Unknown mode: " << mode << "\n\n";
            printUsage();
            return 1;
        }

        QRISK_LOG_INFO("QRiskLab finished successfully.");
        return 0;
    }
    catch (const std::exception& ex)
    {
        QRISK_LOG_CRITICAL(std::string("Fatal error: ") + ex.what());
        return 1;
    }
}