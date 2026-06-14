"""
Timing utilities for QRiskLab.

Provides decorators and context managers for performance measurement.
"""

import time
import functools
from contextlib import contextmanager
from typing import Callable, Any, Generator, Optional

from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)


def timer(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.

    Args:
        func: Function to time

    Returns:
        Wrapped function that logs execution time
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed_time = time.perf_counter() - start_time
            logger.debug(
                f"{func.__name__} executed in {elapsed_time:.4f} seconds"
            )
    return wrapper


@contextmanager
def timed_block(
    block_name: str,
    log_level: str = "debug",
) -> Generator[None, None, None]:
    """
    Context manager to measure execution time of a code block.

    Args:
        block_name: Name of the code block for logging
        log_level: Logging level ('debug', 'info', 'warning', 'error')

    Yields:
        None
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed_time = time.perf_counter() - start_time
        message = f"{block_name} completed in {elapsed_time:.4f} seconds"

        log_func = getattr(logger, log_level.lower(), logger.debug)
        log_func(message)


class Timer:
    """Simple timer for measuring elapsed time."""

    def __init__(self) -> None:
        """Initialize timer."""
        self.start_time = time.perf_counter()

    def elapsed_seconds(self) -> float:
        """Get elapsed time in seconds."""
        return time.perf_counter() - self.start_time

    def elapsed_milliseconds(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.elapsed_seconds() * 1000

    def elapsed_microseconds(self) -> int:
        """Get elapsed time in microseconds."""
        return int(self.elapsed_seconds() * 1_000_000)

    def reset(self) -> None:
        """Reset the timer."""
        self.start_time = time.perf_counter()

    def __str__(self) -> str:
        """Return string representation of elapsed time."""
        elapsed_ms = self.elapsed_milliseconds()
        return f"{elapsed_ms:.2f}ms"


__all__ = [
    "timer",
    "timed_block",
    "Timer",
]
