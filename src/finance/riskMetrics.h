#pragma once

#include <vector>

namespace qrisk::finance
{
    class RiskMetrics
    {
    public:
        static double valueAtRisk(std::vector<double> losses, double confidenceLevel);
        static double conditionalValueAtRisk(std::vector<double> losses, double confidenceLevel);
    };
}
