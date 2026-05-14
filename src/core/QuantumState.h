#pragma once

#include <complex>
#include <cstddef>
#include <cstdint>
#include <random>
#include <vector>

namespace qrisk::core
{
    using Complex = std::complex<double>;

    class QuantumState
    {
    public:
        explicit QuantumState(std::size_t qubitCount);

        std::size_t qubitCount() const;
        std::size_t dimension() const;

        void reset();

        void applyX(std::size_t target);
        void applyZ(std::size_t target);
        void applyHadamard(std::size_t target);
        void applyCNOT(std::size_t control, std::size_t target);

        int measure(std::size_t target, std::mt19937_64& rng);

        const std::vector<Complex>& amplitudes() const;

        double probabilityOfBasisState(std::size_t index) const;
        void printState(double epsilon = 1e-10) const;

    private:
        std::size_t m_qubitCount;
        std::vector<Complex> m_state;

        void validateQubit(std::size_t qubit) const;
    };
}
