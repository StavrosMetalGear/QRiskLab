"""
Unit tests for configuration module.

Tests Config class, environment variable handling, and configuration management.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch

from qrisklab.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig, get_config


class TestConfig:
    """Tests for base Config class."""

    def test_config_has_required_attributes(self):
        """Test that Config has all required attributes."""
        assert hasattr(Config, "PROJECT_ROOT")
        assert hasattr(Config, "LOG_LEVEL")
        assert hasattr(Config, "API_HOST")
        assert hasattr(Config, "API_PORT")
        assert hasattr(Config, "QUANTUM_BACKEND")

    def test_config_paths_are_pathlib_paths(self):
        """Test that path attributes are Path objects."""
        assert isinstance(Config.PROJECT_ROOT, Path)
        assert isinstance(Config.SRC_ROOT, Path)
        assert isinstance(Config.DATA_DIR, Path)
        assert isinstance(Config.LOGS_DIR, Path)

    def test_config_to_dict(self):
        """Test Config.to_dict() returns dictionary."""
        config_dict = Config.to_dict()
        assert isinstance(config_dict, dict)
        assert "LOG_LEVEL" in config_dict
        assert "API_HOST" in config_dict
        assert "QUANTUM_BACKEND" in config_dict

    def test_config_ensure_directories(self):
        """Test that ensure_directories creates required directories."""
        Config.ensure_directories()
        assert Config.DATA_DIR.exists()
        assert Config.LOGS_DIR.exists()

    def test_api_port_is_integer(self):
        """Test that API_PORT is an integer."""
        assert isinstance(Config.API_PORT, int)
        assert Config.API_PORT > 0

    def test_monte_carlo_paths_is_positive(self):
        """Test that MONTE_CARLO_PATHS is positive."""
        assert Config.MONTE_CARLO_PATHS > 0


class TestDevelopmentConfig:
    """Tests for DevelopmentConfig."""

    def test_development_config_has_debug_enabled(self):
        """Test that development config has debug enabled."""
        assert DevelopmentConfig.API_DEBUG is True

    def test_development_config_log_level_is_debug(self):
        """Test that development config uses DEBUG log level."""
        assert DevelopmentConfig.LOG_LEVEL == "DEBUG"


class TestProductionConfig:
    """Tests for ProductionConfig."""

    def test_production_config_has_debug_disabled(self):
        """Test that production config has debug disabled."""
        assert ProductionConfig.API_DEBUG is False

    def test_production_config_log_level_is_info(self):
        """Test that production config uses INFO log level."""
        assert ProductionConfig.LOG_LEVEL == "INFO"


class TestTestingConfig:
    """Tests for TestingConfig."""

    def test_testing_config_has_reduced_paths(self):
        """Test that testing config uses reduced Monte Carlo paths."""
        assert TestingConfig.MONTE_CARLO_PATHS < Config.MONTE_CARLO_PATHS

    def test_testing_config_has_reduced_shots(self):
        """Test that testing config uses reduced quantum shots."""
        assert TestingConfig.QUANTUM_SHOTS < Config.QUANTUM_SHOTS


class TestGetConfig:
    """Tests for get_config() function."""

    def test_get_config_returns_development_by_default(self):
        """Test that get_config returns DevelopmentConfig by default."""
        config = get_config("development")
        assert isinstance(config, DevelopmentConfig)

    def test_get_config_returns_production(self):
        """Test that get_config returns ProductionConfig when requested."""
        config = get_config("production")
        assert isinstance(config, ProductionConfig)

    def test_get_config_returns_testing(self):
        """Test that get_config returns TestingConfig when requested."""
        config = get_config("testing")
        assert isinstance(config, TestingConfig)

    def test_get_config_defaults_to_development(self):
        """Test that get_config defaults to development."""
        config = get_config()
        assert isinstance(config, DevelopmentConfig)

    @patch.dict(os.environ, {"QRISKLAB_ENV": "production"})
    def test_get_config_respects_environment_variable(self):
        """Test that get_config respects QRISKLAB_ENV environment variable."""
        config = get_config()
        assert isinstance(config, ProductionConfig)

    def test_get_config_creates_directories(self):
        """Test that get_config creates required directories."""
        config = get_config()
        assert config.DATA_DIR.exists()
        assert config.LOGS_DIR.exists()
