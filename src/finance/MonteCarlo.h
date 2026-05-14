#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace qrisk::finance
{
    struct OptionPricingResult
    {
        double estimatedPrice = 0.0;
        double standardError = 0.0;
        std::vector<double> discountedPayoffs;
    };

    class MonteCarlo
    {
    public:
        static OptionPricingResult priceEuropeanCall(
            double spotPrice,
            double strikePrice,
            double riskFreeRate,
            double volatility,
            double maturityYears,
            std::size_t paths,
            std::uint64_t seed
        );

        static std::vector<double> simulatePortfolioLosses(
            double initialPortfolioValue,
            double expectedReturn,
            double volatility,
            double timeHorizonYears,
            std::size_t scenarios,
            std::uint64_t seed
        );
    };
}