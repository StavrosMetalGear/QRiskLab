cmake_minimum_required(VERSION 3.20)

project(QRiskLab VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(QRiskLab
    src/main.cpp

    src/core/QuantumState.h
    src/core/QuantumState.cpp

    src/finance/MonteCarlo.h
    src/finance/MonteCarlo.cpp
    src/finance/RiskMetrics.h
    src/finance/RiskMetrics.cpp

    src/utils/logger.h
    src/utils/logger.cpp
)

target_include_directories(QRiskLab PRIVATE src)