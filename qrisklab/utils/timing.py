"""
Timing utilities for QRiskLab.

Provides decorators and context managers for measuring execution time
and performance profiling.
"""

import functools
import logging
import time
from contextlib import contextmanager
from typing import Any, Callable, Generator, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """
    Decorator to measure function execution time.

    Logs the execution time at INFO level. Useful for performance profiling.

    Args:
        func: Function to decorate

    Returns:
        Decorated function

    Example:
        >>> from qrisklab.utils.timing import timer
        >>> @timer
        ... def expensive_operation():
        ...     time.sleep(1)
        >>> expensive_operation()  # Logs: "expensive_operation completed in 1.000 seconds"
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = logging.getLogger(func.__module__)
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start_time
            logger.info(f"{func.__name__} completed in {elapsed:.3f} seconds")

    return wrapper  # type: ignore


@contextmanager
def timed_block(
    block_name: str,
    log_level: str = "debug",
) -> Generator[None, None, None]:
    """
    Context manager to measure execution time of a code block.

    Args:
        block_name: Name of the code block for logging
        log_level: Logging level ("debug", "info", "warning", "error", "critical")

    Yields:
        None

    Example:
        >>> from qrisklab.utils.timing import timed_block
        >>> with timed_block("data processing"):
        ...     # expensive operation
        ...     pass
        >>> # Logs: "data processing completed in X.XXX seconds"
    """
    logger = logging.getLogger()
    log_func = getattr(logger, log_level.lower(), logger.debug)

    start_time = time.perf_counter()
    log_func(f"Started: {block_name}")

    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        log_func(f"{block_name} completed in {elapsed:.3f} seconds")


class Timer:
    """
    Simple timer for measuring elapsed time.

    Useful for manual timing of operations without logging.

    Example:
        >>> from qrisklab.utils.timing import Timer
        >>> timer = Timer()
        >>> time.sleep(0.5)
        >>> print(f"Elapsed: {timer.elapsed_seconds():.2f}s")
        Elapsed: 0.50s
    """

    def __init__(self) -> None:
        """Initialize timer."""
        self._start_time = time.perf_counter()

    def elapsed_seconds(self) -> float:
        """Get elapsed time in seconds."""
        return time.perf_counter() - self._start_time

    def elapsed_milliseconds(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.elapsed_seconds() * 1000.0

    def reset(self) -> None:
        """Reset the timer."""
        self._start_time = time.perf_counter()
"""
Timing utilities for QRiskLab.

Provides decorators and context managers for measuring execution time
and performance profiling.
"""

import functools
import logging
import time
from contextlib import contextmanager
from typing import Any, Callable, Generator, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """
    Decorator to measure function execution time.

    Logs the execution time at INFO level. Useful for performance profiling.

    Args:
        func: Function to decorate

    Returns:
        Decorated function

    Example:
        >>> from qrisklab.utils.timing import timer
        >>> @timer
        ... def expensive_operation():
        ...     time.sleep(1)
        >>> expensive_operation()  # Logs: "expensive_operation completed in 1.000 seconds"
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = logging.getLogger(func.__module__)
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start_time
            logger.info(f"{func.__name__} completed in {elapsed:.3f} seconds")

    return wrapper  # type: ignore


@contextmanager
def timed_block(
    block_name: str,
    log_level: str = "debug",
) -> Generator[None, None, None]:
    """
    Context manager to measure execution time of a code block.

    Args:
        block_name: Name of the code block for logging
        log_level: Logging level ("debug", "info", "warning", "error", "critical")

    Yields:
        None

    Example:
        >>> from qrisklab.utils.timing import timed_block
        >>> with timed_block("data processing"):
        ...     # expensive operation
        ...     pass
        >>> # Logs: "data processing completed in X.XXX seconds"
    """
    logger = logging.getLogger()
    log_func = getattr(logger, log_level.lower(), logger.debug)

    start_time = time.perf_counter()
    log_func(f"Started: {block_name}")

    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        log_func(f"{block_name} completed in {elapsed:.3f} seconds")


class Timer:
    """
    Simple timer for measuring elapsed time.

    Useful for manual timing of operations without logging.

    Example:
        >>> from qrisklab.utils.timing import Timer
        >>> timer = Timer()
        >>> time.sleep(0.5)
        >>> print(f"Elapsed: {timer.elapsed_seconds():.2f}s")
        Elapsed: 0.50s
    """

    def __init__(self) -> None:
        """Initialize timer."""
        self._start_time = time.perf_counter()

    def elapsed_seconds(self) -> float:
        """Get elapsed time in seconds."""
        return time.perf_counter() - self._start_time

    def elapsed_milliseconds(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.elapsed_seconds() * 1000.0

    def reset(self) -> None:
        """Reset the timer."""
        self._start_time = time.perf_counter()
