#pragma once

#include <chrono>
#include <cstdint>
#include <string>

namespace qrisk::utils
{
    class Timer
    {
    public:
        Timer();

        void reset();

        double elapsedSeconds() const;
        double elapsedMilliseconds() const;
        std::int64_t elapsedMicroseconds() const;

        std::string elapsedMillisecondsString() const;

    private:
        using Clock = std::chrono::high_resolution_clock;
        Clock::time_point m_start;
    };

    class ScopedTimer
    {
    public:
        explicit ScopedTimer(std::string operationName);
        ~ScopedTimer();

        ScopedTimer(const ScopedTimer&) = delete;
        ScopedTimer& operator=(const ScopedTimer&) = delete;

    private:
        std::string m_operationName;
        Timer m_timer;
    };
}