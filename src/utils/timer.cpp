#include "timer.h"
#include "logger.h"

#include <iomanip>
#include <sstream>
#include <utility>

namespace qrisk::utils
{
    Timer::Timer()
    {
        reset();
    }

    void Timer::reset()
    {
        m_start = Clock::now();
    }

    double Timer::elapsedSeconds() const
    {
        return elapsedMilliseconds() / 1000.0;
    }

    double Timer::elapsedMilliseconds() const
    {
        const auto now = Clock::now();
        const auto elapsed = std::chrono::duration<double, std::milli>(now - m_start);
        return elapsed.count();
    }

    std::int64_t Timer::elapsedMicroseconds() const
    {
        const auto now = Clock::now();
        const auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(now - m_start);
        return elapsed.count();
    }

    std::string Timer::elapsedMillisecondsString() const
    {
        std::ostringstream stream;
        stream << std::fixed << std::setprecision(3) << elapsedMilliseconds() << " ms";
        return stream.str();
    }

    ScopedTimer::ScopedTimer(std::string operationName)
        : m_operationName(std::move(operationName))
    {
        QRISK_LOG_DEBUG("Started: " + m_operationName);
    }

    ScopedTimer::~ScopedTimer()
    {
        QRISK_LOG_INFO(m_operationName + " completed in " + m_timer.elapsedMillisecondsString());
    }
}
