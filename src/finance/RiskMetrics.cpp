#include "finance/RiskMetrics.h"

#include <algorithm>
#include <numeric>
#include <stdexcept>

namespace qrisk::finance
{
    double RiskMetrics::valueAtRisk(std::vector<double> losses, double confidenceLevel)
    {
        if (losses.empty())
        {
            throw std::invalid_argument("Loss vector cannot be empty.");
        }

        if (confidenceLevel <= 0.0 || confidenceLevel >= 1.0)
        {
            throw std::invalid_argument("Confidence level must be between 0 and 1.");
        }

        std::sort(losses.begin(), losses.end());

        const std::size_t index = static_cast<std::size_t>(confidenceLevel * static_cast<double>(losses.size() - 1));

        return losses[index];
    }

    double RiskMetrics::conditionalValueAtRisk(std::vector<double> losses, double confidenceLevel)
    {
        if (losses.empty())
        {
            throw std::invalid_argument("Loss vector cannot be empty.");
        }

        if (confidenceLevel <= 0.0 || confidenceLevel >= 1.0)
        {
            throw std::invalid_argument("Confidence level must be between 0 and 1.");
        }

        std::sort(losses.begin(), losses.end());

        const std::size_t startIndex = static_cast<std::size_t>(confidenceLevel * static_cast<double>(losses.size() - 1));

        double tailSum = 0.0;
        std::size_t tailCount = 0;

        for (std::size_t i = startIndex; i < losses.size(); ++i)
        {
            tailSum += losses[i];
            ++tailCount;
        }

        return tailSum / static_cast<double>(tailCount);
    }
}