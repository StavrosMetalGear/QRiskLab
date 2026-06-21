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
    if isinstance(level, str):
        level = LogLevel[level.upper()]

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
