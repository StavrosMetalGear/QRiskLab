"""
Setup configuration for QRiskLab Pro.

Configures the build system for C++ extensions and Python package installation.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


class CMakeExtension(Extension):
    """Custom extension for CMake-based C++ modules."""

    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    """Custom build command that uses CMake to build extensions."""

    def build_extension(self, ext):
        if not isinstance(ext, CMakeExtension):
            super().build_extension(ext)
            return

        build_temp = Path(self.build_temp).absolute()
        build_temp.mkdir(parents=True, exist_ok=True)

        build_lib = Path(self.build_lib).absolute()

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={build_lib}",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={build_lib}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args,
            cwd=build_temp,
        )

        subprocess.check_call(
            ["cmake", "--build", ".", "--config", "Release"],
            cwd=build_temp,
        )

        expected_path = Path(self.get_ext_fullpath(ext.name)).absolute()
        if expected_path.exists():
            return

        module_name = ext.name.split(".")[-1]

        candidates = []
        for search_root in (build_lib, build_temp):
            candidates.extend(search_root.rglob(f"{module_name}*.pyd"))
            candidates.extend(search_root.rglob(f"{module_name}*.so"))
            candidates.extend(search_root.rglob(f"{module_name}*.dll"))
            candidates.extend(search_root.rglob(f"{module_name}*.dylib"))

        if not candidates:
            raise FileNotFoundError(f"Could not find built extension for {ext.name}")

        source_path = candidates[0]
        expected_path.parent.mkdir(parents=True, exist_ok=True)

        if source_path.resolve() != expected_path.resolve():
            shutil.copy2(source_path, expected_path)


# Read long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="qrisklab",
    version="0.1.0",
    author="QRiskLab Team",
    author_email="team@qrisklab.dev",
    description="Hybrid Quantum-Classical Risk Analysis Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qrisklab/qrisklab",
    project_urls={
        "Documentation": "https://qrisklab.readthedocs.io",
        "Source Code": "https://github.com/qrisklab/qrisklab",
        "Issue Tracker": "https://github.com/qrisklab/qrisklab/issues",
    },
    packages=find_packages(),
    ext_modules=[CMakeExtension("qrisklab.finance._qrisklab_core")],
    cmdclass={"build_ext": CMakeBuild},
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26",
        "scipy>=1.11",
        "pandas>=2.1",
        "polars>=0.20",
        "sympy>=1.12",
        "matplotlib>=3.8",
        "plotly>=5.18",
        "streamlit>=1.31",
        "fastapi>=0.110",
        "uvicorn[standard]>=0.27",
        "pydantic>=2.6",
        "python-dotenv>=1.0",
        "cvxpy>=1.4",
        "PyPortfolioOpt>=1.5",
        "statsmodels>=0.14",
        "arch>=6.3",
        "yfinance>=0.2",
        "QuantLib>=1.31",
        "qiskit>=1.0",
        "qiskit-aer>=0.14",
        "pennylane>=0.35",
        "qutip>=5.0",
        "cirq>=1.3",
        "openfermion>=1.6",
        "amazon-braket-sdk>=1.80",
        "torch>=2.2",
        "scikit-learn>=1.4",
        "jax>=0.4",
        "jaxlib>=0.4",
        "pybind11>=2.11",
        "nanobind>=1.9",
        "mlflow>=2.10",
        "jinja2>=3.1",
        "weasyprint>=61.0",
        "rich>=13.7",
        "tqdm>=4.66",
        "jupyterlab>=4.1",
        "ipykernel>=6.29",
        "requests>=2.31",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4",
            "pytest-cov>=4.1",
            "black>=23.12",
            "ruff>=0.1",
            "mypy>=1.7",
            "flake8>=6.1",
            "isort>=5.13",
        ],
        "docs": [
            "sphinx>=7.2",
            "sphinx-rtd-theme>=2.0",
            "sphinx-autodoc-typehints>=1.25",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    zip_safe=False,
)