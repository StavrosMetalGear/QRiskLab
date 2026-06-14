"""
Logging utilities for QRiskLab.

Provides a Python wrapper around the C++ Logger class and convenience functions
for setting up logging throughout the application.
"""

import logging
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def setup_logging(
    level: LogLevel = LogLevel.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True,
) -> logging.Logger:
    """
    Set up logging for QRiskLab.

    Args:
        level: Minimum log level to display
        log_file: Optional file path for logging output
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("qrisklab")
    logger.setLevel(level.value)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level.value)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level.value)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"qrisklab.{name}")


__all__ = [
    "LogLevel",
    "setup_logging",
    "get_logger",
]
