#include "finance/MonteCarlo.h"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <random>
#include <stdexcept>

namespace qrisk::finance
{
    OptionPricingResult MonteCarlo::priceEuropeanCall(
        double spotPrice,
        double strikePrice,
        double riskFreeRate,
        double volatility,
        double maturityYears,
        std::size_t paths,
        std::uint64_t seed
    )
    {
        if (spotPrice <= 0.0 || strikePrice <= 0.0)
        {
            throw std::invalid_argument("Spot price and strike price must be positive.");
        }

        if (volatility < 0.0 || maturityYears <= 0.0 || paths == 0)
        {
            throw std::invalid_argument("Invalid Monte Carlo input.");
        }

        std::mt19937_64 rng(seed);
        std::normal_distribution<double> normal(0.0, 1.0);

        std::vector<double> discountedPayoffs;
        discountedPayoffs.reserve(paths);

        const double drift = (riskFreeRate - 0.5 * volatility * volatility) * maturityYears;
        const double diffusionScale = volatility * std::sqrt(maturityYears);
        const double discountFactor = std::exp(-riskFreeRate * maturityYears);

        for (std::size_t i = 0; i < paths; ++i)
        {
            const double z = normal(rng);
            const double terminalPrice = spotPrice * std::exp(drift + diffusionScale * z);
            const double payoff = std::max(terminalPrice - strikePrice, 0.0);
            discountedPayoffs.push_back(discountFactor * payoff);
        }

        const double sum = std::accumulate(discountedPayoffs.begin(), discountedPayoffs.end(), 0.0);
        const double mean = sum / static_cast<double>(paths);

        double variance = 0.0;

        for (double payoff : discountedPayoffs)
        {
            const double diff = payoff - mean;
            variance += diff * diff;
        }

        variance /= static_cast<double>(paths > 1 ? paths - 1 : 1);

        OptionPricingResult result;
        result.estimatedPrice = mean;
        result.standardError = std::sqrt(variance / static_cast<double>(paths));
        result.discountedPayoffs = std::move(discountedPayoffs);

        return result;
    }

    std::vector<double> MonteCarlo::simulatePortfolioLosses(
        double initialPortfolioValue,
        double expectedReturn,
        double volatility,
        double timeHorizonYears,
        std::size_t scenarios,
        std::uint64_t seed
    )
    {
        if (initialPortfolioValue <= 0.0)
        {
            throw std::invalid_argument("Initial portfolio value must be positive.");
        }

        if (volatility < 0.0 || timeHorizonYears <= 0.0 || scenarios == 0)
        {
            throw std::invalid_argument("Invalid portfolio simulation input.");
        }

        std::mt19937_64 rng(seed);
        std::normal_distribution<double> normal(0.0, 1.0);

        std::vector<double> losses;
        losses.reserve(scenarios);

        const double drift = (expectedReturn - 0.5 * volatility * volatility) * timeHorizonYears;
        const double diffusionScale = volatility * std::sqrt(timeHorizonYears);

        for (std::size_t i = 0; i < scenarios; ++i)
        {
            const double z = normal(rng);
            const double terminalValue = initialPortfolioValue * std::exp(drift + diffusionScale * z);
            const double loss = initialPortfolioValue - terminalValue;

            losses.push_back(loss);
        }

        return losses;
    }
}