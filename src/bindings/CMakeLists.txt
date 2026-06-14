# pybind11 bindings for QRiskLab C++ modules
# Exposes QuantumState, MonteCarlo, and RiskMetrics to Python

# Find pybind11
find_package(pybind11 CONFIG REQUIRED)

# Create the Python extension module
pybind11_add_module(_qrisklab_core
    bindings.cpp
)

# Link against core libraries
target_link_libraries(_qrisklab_core PRIVATE
    qrisklab_core
    qrisklab_finance
    qrisklab_utils
)

# Set C++ standard
target_compile_features(_qrisklab_core PRIVATE cxx_std_17)

# Add include directories
target_include_directories(_qrisklab_core PRIVATE
    ${CMAKE_SOURCE_DIR}/src
)
