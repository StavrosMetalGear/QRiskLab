#pragma once

#include <fstream>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>

namespace qrisk::utils
{
    enum class LogLevel
    {
        Trace,
        Debug,
        Info,
        Warning,
        Error,
        Critical
    };

    class Logger
    {
    public:
        static Logger& instance();

        Logger(const Logger&) = delete;
        Logger& operator=(const Logger&) = delete;

        void setMinimumLevel(LogLevel level);
        void enableConsole(bool enabled);
        void enableFileLogging(const std::string& filePath);
        void disableFileLogging();

        void log(LogLevel level, const std::string& message);

        void trace(const std::string& message);
        void debug(const std::string& message);
        void info(const std::string& message);
        void warning(const std::string& message);
        void error(const std::string& message);
        void critical(const std::string& message);

    private:
        Logger() = default;
        ~Logger();

        static std::string levelToString(LogLevel level);
        static bool shouldLog(LogLevel messageLevel, LogLevel minimumLevel);
        static std::string currentTimestamp();

        std::mutex m_mutex;
        LogLevel m_minimumLevel = LogLevel::Info;
        bool m_consoleEnabled = true;
        std::ofstream m_file;
    };
}

#define QRISK_LOG_TRACE(message)    ::qrisk::utils::Logger::instance().trace(message)
#define QRISK_LOG_DEBUG(message)    ::qrisk::utils::Logger::instance().debug(message)
#define QRISK_LOG_INFO(message)     ::qrisk::utils::Logger::instance().info(message)
#define QRISK_LOG_WARNING(message)  ::qrisk::utils::Logger::instance().warning(message)
#define QRISK_LOG_ERROR(message)    ::qrisk::utils::Logger::instance().error(message)
#define QRISK_LOG_CRITICAL(message) ::qrisk::utils::Logger::instance().critical(message)
