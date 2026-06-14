"""
Configuration management for QRiskLab Pro

Handles environment variables, settings, and runtime configuration.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Base configuration class for QRiskLab."""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    SRC_ROOT = PROJECT_ROOT / "src"
    DATA_DIR = PROJECT_ROOT / "data"
    LOGS_DIR = PROJECT_ROOT / "logs"

    # Logging
    LOG_LEVEL = os.getenv("QRISKLAB_LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("QRISKLAB_LOG_FILE", str(LOGS_DIR / "qrisklab.log"))

    # API Configuration
    API_HOST = os.getenv("QRISKLAB_API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("QRISKLAB_API_PORT", "8000"))
    API_DEBUG = os.getenv("QRISKLAB_API_DEBUG", "False").lower() == "true"

    # Quantum Configuration
    QUANTUM_BACKEND = os.getenv("QRISKLAB_QUANTUM_BACKEND", "qiskit_aer")
    QUANTUM_SHOTS = int(os.getenv("QRISKLAB_QUANTUM_SHOTS", "1024"))

    # Monte Carlo Configuration
    MONTE_CARLO_PATHS = int(os.getenv("QRISKLAB_MC_PATHS", "10000"))
    MONTE_CARLO_SEED = int(os.getenv("QRISKLAB_MC_SEED", "42"))

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def to_dict(cls) -> dict:
        """Return configuration as dictionary."""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith("_") and key.isupper()
        }


# Development configuration
class DevelopmentConfig(Config):
    """Development environment configuration."""

    API_DEBUG = True
    LOG_LEVEL = "DEBUG"


# Production configuration
class ProductionConfig(Config):
    """Production environment configuration."""

    API_DEBUG = False
    LOG_LEVEL = "INFO"


# Testing configuration
class TestingConfig(Config):
    """Testing environment configuration."""

    API_DEBUG = True
    LOG_LEVEL = "DEBUG"
    MONTE_CARLO_PATHS = 100  # Reduced for faster tests
    QUANTUM_SHOTS = 256  # Reduced for faster tests


def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration object based on environment.

    Args:
        env: Environment name ('development', 'production', 'testing').
             If None, uses QRISKLAB_ENV environment variable or defaults to 'development'.

    Returns:
        Configuration object for the specified environment.
    """
    if env is None:
        env = os.getenv("QRISKLAB_ENV", "development").lower()

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_class = config_map.get(env, DevelopmentConfig)
    config_class.ensure_directories()
    return config_class()


# Default configuration instance
config = get_config()
