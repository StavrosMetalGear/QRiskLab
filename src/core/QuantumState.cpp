#include "core/QuantumState.h"

#include <cmath>
#include <iomanip>
#include <iostream>
#include <stdexcept>

namespace qrisk::core
{
    QuantumState::QuantumState(std::size_t qubitCount)
        : m_qubitCount(qubitCount),
        m_state(std::size_t{ 1 } << qubitCount, Complex{ 0.0, 0.0 })
    {
        if (qubitCount == 0)
        {
            throw std::invalid_argument("QuantumState must contain at least one qubit.");
        }

        if (qubitCount >= sizeof(std::size_t) * 8)
        {
            throw std::invalid_argument("Qubit count is too large for this platform.");
        }

        reset();
    }

    std::size_t QuantumState::qubitCount() const
    {
        return m_qubitCount;
    }

    std::size_t QuantumState::dimension() const
    {
        return m_state.size();
    }

    void QuantumState::reset()
    {
        std::fill(m_state.begin(), m_state.end(), Complex{ 0.0, 0.0 });
        m_state[0] = Complex{ 1.0, 0.0 };
    }

    void QuantumState::validateQubit(std::size_t qubit) const
    {
        if (qubit >= m_qubitCount)
        {
            throw std::out_of_range("Qubit index is out of range.");
        }
    }

    void QuantumState::applyX(std::size_t target)
    {
        validateQubit(target);

        const std::size_t mask = std::size_t{ 1 } << target;

        for (std::size_t i = 0; i < m_state.size(); ++i)
        {
            if ((i & mask) == 0)
            {
                const std::size_t j = i | mask;
                std::swap(m_state[i], m_state[j]);
            }
        }
    }

    void QuantumState::applyZ(std::size_t target)
    {
        validateQubit(target);

        const std::size_t mask = std::size_t{ 1 } << target;

        for (std::size_t i = 0; i < m_state.size(); ++i)
        {
            if ((i & mask) != 0)
            {
                m_state[i] = -m_state[i];
            }
        }
    }

    void QuantumState::applyHadamard(std::size_t target)
    {
        validateQubit(target);

        const std::size_t mask = std::size_t{ 1 } << target;
        const double invSqrt2 = 1.0 / std::sqrt(2.0);

        for (std::size_t i = 0; i < m_state.size(); ++i)
        {
            if ((i & mask) == 0)
            {
                const std::size_t j = i | mask;

                const Complex a = m_state[i];
                const Complex b = m_state[j];

                m_state[i] = (a + b) * invSqrt2;
                m_state[j] = (a - b) * invSqrt2;
            }
        }
    }

    void QuantumState::applyCNOT(std::size_t control, std::size_t target)
    {
        validateQubit(control);
        validateQubit(target);

        if (control == target)
        {
            throw std::invalid_argument("Control and target qubits must be different.");
        }

        const std::size_t controlMask = std::size_t{ 1 } << control;
        const std::size_t targetMask = std::size_t{ 1 } << target;

        for (std::size_t i = 0; i < m_state.size(); ++i)
        {
            const bool controlIsOne = (i & controlMask) != 0;
            const bool targetIsZero = (i & targetMask) == 0;

            if (controlIsOne && targetIsZero)
            {
                const std::size_t j = i | targetMask;
                std::swap(m_state[i], m_state[j]);
            }
        }
    }

    int QuantumState::measure(std::size_t target, std::mt19937_64& rng)
    {
        validateQubit(target);

        const std::size_t mask = std::size_t{ 1 } << target;

        double probabilityOne = 0.0;

        for (std::size_t i = 0; i < m_state.size(); ++i)
        {
            if ((i & mask) != 0)
            {
                probabilityOne += std::norm(m_state[i]);
            }
        }

        std::uniform_real_distribution<double> distribution(0.0, 1.0);
        const double sample = distribution(rng);

        const int result = sample < probabilityOne ? 1 : 0;
        const double selectedProbability = result == 1 ? probabilityOne : 1.0 - probabilityOne;

        if (selectedProbability <= 0.0)
        {
            throw std::runtime_error("Measurement collapse failed due to zero probability.");
        }

        const double normalization = 1.0 / std::sqrt(selectedProbability);

        for (std::size_t i = 0; i < m_state.size(); ++i)
        {
            const bool bitIsOne = (i & mask) != 0;

            if ((result == 1 && bitIsOne) || (result == 0 && !bitIsOne))
            {
                m_state[i] *= normalization;
            }
            else
            {
                m_state[i] = Complex{ 0.0, 0.0 };
            }
        }

        return result;
    }

    const std::vector<Complex>& QuantumState::amplitudes() const
    {
        return m_state;
    }

    double QuantumState::probabilityOfBasisState(std::size_t index) const
    {
        if (index >= m_state.size())
        {
            throw std::out_of_range("Basis state index is out of range.");
        }

        return std::norm(m_state[index]);
    }

    void QuantumState::printState(double epsilon) const
    {
        std::cout << std::fixed << std::setprecision(6);

        for (std::size_t i = 0; i < m_state.size(); ++i)
        {
            const double probability = std::norm(m_state[i]);

            if (probability > epsilon)
            {
                std::cout << "|";

                for (std::size_t q = 0; q < m_qubitCount; ++q)
                {
                    const std::size_t bit = (i >> (m_qubitCount - q - 1)) & 1U;
                    std::cout << bit;
                }

                std::cout << "> amplitude = "
                    << m_state[i]
                    << ", probability = "
                    << probability
                    << '\n';
            }
        }
    }
}