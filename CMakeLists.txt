cmake_minimum_required(VERSION 3.20)

project(QRiskLab VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Core library sources
set(CORE_SOURCES
    src/core/QuantumState.cpp
)

set(FINANCE_SOURCES
    src/finance/MonteCarlo.cpp
    src/finance/RiskMetrics.cpp
)

set(UTILS_SOURCES
    src/utils/logger.cpp
    src/utils/timer.cpp
)

# Create static libraries for core, finance, and utils
add_library(qrisklab_core STATIC ${CORE_SOURCES})
target_include_directories(qrisklab_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

add_library(qrisklab_finance STATIC ${FINANCE_SOURCES})
target_include_directories(qrisklab_finance PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

add_library(qrisklab_utils STATIC ${UTILS_SOURCES})
target_include_directories(qrisklab_utils PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)


# Create the main executable
add_executable(QRiskLab
    src/main.cpp
)

target_link_libraries(QRiskLab PRIVATE
    qrisklab_core
    qrisklab_finance
    qrisklab_utils
)

target_include_directories(QRiskLab PRIVATE src)

# Add bindings subdirectory for Python extension
add_subdirectory(src/bindings)
