#include "logger.h"

#include <chrono>
#include <iomanip>
#include <stdexcept>

namespace qrisk::utils
{
    Logger& Logger::instance()
    {
        static Logger logger;
        return logger;
    }

    Logger::~Logger()
    {
        std::lock_guard<std::mutex> lock(m_mutex);

        if (m_file.is_open())
        {
            m_file.flush();
            m_file.close();
        }
    }

    void Logger::setMinimumLevel(LogLevel level)
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        m_minimumLevel = level;
    }

    void Logger::enableConsole(bool enabled)
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        m_consoleEnabled = enabled;
    }

    void Logger::enableFileLogging(const std::string& filePath)
    {
        std::lock_guard<std::mutex> lock(m_mutex);

        if (m_file.is_open())
        {
            m_file.close();
        }

        m_file.open(filePath, std::ios::out | std::ios::app);

        if (!m_file.is_open())
        {
            throw std::runtime_error("Failed to open log file: " + filePath);
        }
    }

    void Logger::disableFileLogging()
    {
        std::lock_guard<std::mutex> lock(m_mutex);

        if (m_file.is_open())
        {
            m_file.flush();
            m_file.close();
        }
    }

    void Logger::log(LogLevel level, const std::string& message)
    {
        std::lock_guard<std::mutex> lock(m_mutex);

        if (!shouldLog(level, m_minimumLevel))
        {
            return;
        }

        const std::string line =
            "[" + currentTimestamp() + "] " +
            "[" + levelToString(level) + "] " +
            message;

        if (m_consoleEnabled)
        {
            if (level == LogLevel::Error || level == LogLevel::Critical)
            {
                std::cerr << line << '\n';
            }
            else
            {
                std::cout << line << '\n';
            }
        }

        if (m_file.is_open())
        {
            m_file << line << '\n';
            m_file.flush();
        }
    }

    void Logger::trace(const std::string& message)
    {
        log(LogLevel::Trace, message);
    }

    void Logger::debug(const std::string& message)
    {
        log(LogLevel::Debug, message);
    }

    void Logger::info(const std::string& message)
    {
        log(LogLevel::Info, message);
    }

    void Logger::warning(const std::string& message)
    {
        log(LogLevel::Warning, message);
    }

    void Logger::error(const std::string& message)
    {
        log(LogLevel::Error, message);
    }

    void Logger::critical(const std::string& message)
    {
        log(LogLevel::Critical, message);
    }

    std::string Logger::levelToString(LogLevel level)
    {
        switch (level)
        {
        case LogLevel::Trace:
            return "TRACE";
        case LogLevel::Debug:
            return "DEBUG";
        case LogLevel::Info:
            return "INFO";
        case LogLevel::Warning:
            return "WARNING";
        case LogLevel::Error:
            return "ERROR";
        case LogLevel::Critical:
            return "CRITICAL";
        default:
            return "UNKNOWN";
        }
    }

    bool Logger::shouldLog(LogLevel messageLevel, LogLevel minimumLevel)
    {
        return static_cast<int>(messageLevel) >= static_cast<int>(minimumLevel);
    }

    std::string Logger::currentTimestamp()
    {
        const auto now = std::chrono::system_clock::now();
        const auto time = std::chrono::system_clock::to_time_t(now);

        std::tm localTime{};

#if defined(_WIN32)
        localtime_s(&localTime, &time);
#else
        localtime_r(&time, &localTime);
#endif

        std::ostringstream stream;
        stream << std::put_time(&localTime, "%Y-%m-%d %H:%M:%S");

        return stream.str();
    }
}