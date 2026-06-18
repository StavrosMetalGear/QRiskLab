"""
Unit tests for utilities module.

Tests logging, timing, and other utility functions.
"""

import pytest
import logging
import time
from pathlib import Path

from qrisklab.utils.logger import LogLevel, setup_logging, get_logger
from qrisklab.utils.timing import Timer, timed_block, timer


class TestLogLevel:
    """Tests for LogLevel enum."""

    def test_log_level_values(self):
        """Test that LogLevel has expected values."""
        assert hasattr(LogLevel, "DEBUG")
        assert hasattr(LogLevel, "INFO")
        assert hasattr(LogLevel, "WARNING")
        assert hasattr(LogLevel, "ERROR")
        assert hasattr(LogLevel, "CRITICAL")

    def test_log_level_is_enum(self):
        """Test that LogLevel is an enum."""
        assert LogLevel.INFO.value == logging.INFO


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_console(self):
        """Test logging setup with console output."""
        setup_logging(level=LogLevel.INFO, console_output=True)
        logger = logging.getLogger()
        assert len(logger.handlers) > 0

    def test_setup_logging_file(self, tmp_path):
        """Test logging setup with file output."""
        log_file = tmp_path / "test.log"
        setup_logging(level=LogLevel.INFO, log_file=str(log_file))
        
        logger = logging.getLogger()
        logger.info("Test message")
        
        assert log_file.exists()

    def test_setup_logging_level(self):
        """Test that logging level is set correctly."""
        setup_logging(level=LogLevel.DEBUG)
        logger = logging.getLogger()
        assert logger.level == LogLevel.DEBUG.value


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_name(self):
        """Test that get_logger uses provided name."""
        logger = get_logger("test_module")
        assert logger.name == "test_module"

    def test_get_logger_multiple_calls(self):
        """Test that multiple calls return same logger."""
        logger1 = get_logger("test")
        logger2 = get_logger("test")
        assert logger1 is logger2


class TestTimer:
    """Tests for Timer class."""

    def test_timer_initialization(self):
        """Test that timer initializes."""
        t = Timer()
        assert t is not None

    def test_timer_elapsed_seconds(self):
        """Test elapsed time in seconds."""
        t = Timer()
        time.sleep(0.1)
        elapsed = t.elapsed_seconds()
        assert elapsed >= 0.1

    def test_timer_elapsed_milliseconds(self):
        """Test elapsed time in milliseconds."""
        t = Timer()
        time.sleep(0.05)
        elapsed = t.elapsed_milliseconds()
        assert elapsed >= 50

    def test_timer_reset(self):
        """Test timer reset."""
        t = Timer()
        time.sleep(0.1)
        t.reset()
        time.sleep(0.05)
        elapsed = t.elapsed_seconds()
        assert elapsed < 0.1


class TestTimedBlock:
    """Tests for timed_block context manager."""

    def test_timed_block_execution(self):
        """Test that timed_block executes code."""
        executed = False
        with timed_block("test block"):
            executed = True
        assert executed is True

    def test_timed_block_timing(self):
        """Test that timed_block measures time."""
        with timed_block("test block"):
            time.sleep(0.05)
        # If we get here without error, timing worked

    def test_timed_block_exception_handling(self):
        """Test that timed_block handles exceptions."""
        with pytest.raises(ValueError):
            with timed_block("test block"):
                raise ValueError("Test error")


class TestTimerDecorator:
    """Tests for @timer decorator."""

    def test_timer_decorator_execution(self):
        """Test that @timer decorator executes function."""
        @timer
        def test_func():
            return 42
        
        result = test_func()
        assert result == 42

    def test_timer_decorator_timing(self):
        """Test that @timer decorator measures time."""
        @timer
        def test_func():
            time.sleep(0.05)
            return 42
        
        result = test_func()
        assert result == 42

    def test_timer_decorator_with_args(self):
        """Test that @timer decorator works with arguments."""
        @timer
        def test_func(a, b):
            return a + b
        
        result = test_func(1, 2)
        assert result == 3

    def test_timer_decorator_with_kwargs(self):
        """Test that @timer decorator works with keyword arguments."""
        @timer
        def test_func(a, b=10):
            return a + b
        
        result = test_func(5, b=20)
        assert result == 25
