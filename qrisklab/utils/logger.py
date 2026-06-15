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
"""
Logging utilities for QRiskLab.

Provides a unified logging interface with support for file and console output,
configurable log levels, and integration with the C++ Logger (when available).
"""

import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Optional


class LogLevel(Enum):
    """Log level enumeration."""

    TRACE = logging.DEBUG - 1
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def setup_logging(
    level: LogLevel = LogLevel.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True,
) -> None:
    """
    Configure logging for QRiskLab.

    Args:
        level: Minimum log level to display
        log_file: Optional path to log file. If provided, logs are written to file.
        console_output: Whether to output logs to console (default: True)

    Example:
        >>> from qrisklab.utils.logger import setup_logging, LogLevel
        >>> setup_logging(level=LogLevel.DEBUG, log_file="qrisklab.log")
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level.value)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level.value)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level.value)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance

    Example:
        >>> from qrisklab.utils.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return logging.getLogger(name)
