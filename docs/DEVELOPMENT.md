# Development Guide

Guidelines for developing QRiskLab Pro.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Code Style](#code-style)
3. [Testing](#testing)
4. [Building](#building)
5. [Contributing](#contributing)
6. [Debugging](#debugging)

## Development Setup

### Prerequisites

- Python 3.10+
- Git
- C++ compiler (MSVC, GCC, or Clang)
- CMake 3.27+
- Ninja or Make

### Initial Setup

```bash
# Clone repository
git clone https://github.com/qrisklab/qrisklab.git
cd qrisklab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### IDE Setup

**Visual Studio Code:**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

**PyCharm:**
1. Open project
2. Configure interpreter: Settings → Project → Python Interpreter
3. Select `venv/bin/python`
4. Enable code inspections

## Code Style

### Python Style Guide

Follow PEP 8 with these tools:

**Black (Code Formatting):**
```bash
# Format all Python files
black qrisklab/ tests/

# Check formatting without changes
black --check qrisklab/ tests/
```

**Ruff (Linting):**
```bash
# Check code quality
ruff check qrisklab/ tests/

# Fix issues automatically
ruff check --fix qrisklab/ tests/
```

**isort (Import Sorting):**
```bash
# Sort imports
isort qrisklab/ tests/

# Check without changes
isort --check-only qrisklab/ tests/
```

**mypy (Type Checking):**
```bash
# Check type hints
mypy qrisklab/

# Strict mode
mypy --strict qrisklab/
```

### Code Style Rules

1. **Line Length:** Maximum 100 characters
2. **Indentation:** 4 spaces (no tabs)
3. **Imports:** Group by standard library, third-party, local
4. **Docstrings:** Use Google-style docstrings
5. **Type Hints:** Use for all function signatures
6. **Comments:** Explain "why", not "what"

### Example Code

```python
"""Module docstring."""

from typing import List, Optional, Dict
import logging

from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)


class MyClass:
    """Class docstring with description."""

    def __init__(self, name: str, value: float) -> None:
        """
        Initialize the class.

        Args:
            name: Object name
            value: Object value (must be positive)

        Raises:
            ValueError: If value is not positive
        """
        if value <= 0:
            raise ValueError("Value must be positive")
        
        self.name = name
        self.value = value
        logger.debug(f"Initialized {name} with value {value}")

    def process(self, items: List[str]) -> Dict[str, int]:
        """
        Process items and return counts.

        Args:
            items: List of items to process

        Returns:
            Dictionary mapping items to their counts
        """
        result = {}
        for item in items:
            result[item] = result.get(item, 0) + 1
        
        logger.info(f"Processed {len(items)} items")
        return result
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_finance.py -v

# Run specific test
pytest tests/unit/test_finance.py::test_pricing -v

# Run with coverage
pytest tests/ --cov=qrisklab --cov-report=html

# Run with markers
pytest tests/ -m "not slow" -v
```

### Writing Tests

**Test Structure:**
```python
"""Tests for finance module."""

import pytest
from qrisklab.finance.pricing import EuropeanCallPricer


class TestEuropeanCallPricer:
    """Tests for EuropeanCallPricer class."""

    @pytest.fixture
    def pricer(self):
        """Create pricer instance."""
        return EuropeanCallPricer(default_paths=1000)

    def test_price_basic(self, pricer):
        """Test basic option pricing."""
        result = pricer.price(
            spot_price=100.0,
            strike_price=105.0,
            risk_free_rate=0.05,
            volatility=0.2,
            maturity_years=1.0
        )
        
        assert result.estimated_price > 0
        assert result.standard_error > 0

    def test_price_validation(self, pricer):
        """Test input validation."""
        with pytest.raises(ValueError):
            pricer.price(
                spot_price=-100.0,  # Invalid
                strike_price=105.0,
                risk_free_rate=0.05,
                volatility=0.2,
                maturity_years=1.0
            )

    @pytest.mark.parametrize("spot,strike", [
        (100.0, 100.0),  # ATM
        (100.0, 105.0),  # OTM
        (100.0, 95.0),   # ITM
    ])
    def test_price_moneyness(self, pricer, spot, strike):
        """Test pricing at different moneyness levels."""
        result = pricer.price(
            spot_price=spot,
            strike_price=strike,
            risk_free_rate=0.05,
            volatility=0.2,
            maturity_years=1.0
        )
        
        assert result.estimated_price > 0
```

### Test Coverage

Aim for >80% code coverage:

```bash
# Generate coverage report
pytest tests/ --cov=qrisklab --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Building

### Build C++ Extensions

```bash
# Build in development mode
pip install -e . --force-reinstall

# Build in production mode
pip install . --force-reinstall

# Clean build artifacts
rm -rf build/ dist/ *.egg-info
```

### CMake Build

```bash
# Create build directory
mkdir build
cd build

# Configure
cmake ..

# Build
cmake --build . --config Release

# Install
cmake --install .
```

## Contributing

### Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Make** changes and commit: `git commit -am 'Add feature'`
4. **Push** to branch: `git push origin feature/my-feature`
5. **Create** Pull Request

### Pull Request Checklist

- [ ] Code follows style guidelines (black, ruff, mypy)
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Commit messages are clear
- [ ] All tests pass

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add quantum amplitude estimation algorithm

- Implement QAE class with run() method
- Add backend support for Qiskit and PennyLane
- Include comprehensive tests
- Update documentation

Fixes #123
```

**Prefixes:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `chore:` - Maintenance

## Debugging

### Enable Debug Logging

```python
from qrisklab.utils.logger import setup_logging, LogLevel

# Enable debug logging
setup_logging(level=LogLevel.DEBUG, log_file="debug.log")

# Now run your code
from qrisklab.finance.pricing import EuropeanCallPricer
pricer = EuropeanCallPricer()
result = pricer.price(...)
```

### Python Debugger

```python
import pdb

# Set breakpoint
pdb.set_trace()

# Or use breakpoint() in Python 3.7+
breakpoint()
```

### VS Code Debugging

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

### Performance Profiling

```python
import cProfile
import pstats

# Profile code
profiler = cProfile.Profile()
profiler.enable()

# Your code here
from qrisklab.finance.pricing import EuropeanCallPricer
pricer = EuropeanCallPricer()
result = pricer.price(spot_price=100, strike_price=105, 
                      risk_free_rate=0.05, volatility=0.2, 
                      maturity_years=1.0)

profiler.disable()

# Print results
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## Documentation

### Building Documentation

```bash
# Install Sphinx (if not already installed)
pip install sphinx sphinx-rtd-theme

# Build HTML documentation
cd docs
make html

# View documentation
open _build/html/index.html  # macOS
```

### Writing Documentation

Use Sphinx-compatible docstrings:

```python
def calculate_var(losses: List[float], confidence_level: float) -> float:
    """
    Calculate Value at Risk.

    Args:
        losses: List of portfolio losses
        confidence_level: Confidence level (0.01 to 0.99)

    Returns:
        Value at Risk at the specified confidence level

    Raises:
        ValueError: If inputs are invalid

    Example:
        >>> losses = [-100, -50, 0, 50, 100]
        >>> var = calculate_var(losses, 0.95)
        >>> print(f"VaR: ${var:.2f}")
    """
    pass
```

## Release Process

1. Update version in `qrisklab/__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. Build distribution: `python -m build`
6. Upload to PyPI: `twine upload dist/*`

## Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)

---

**Last Updated:** 2026-06-19
