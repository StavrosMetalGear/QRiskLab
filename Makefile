.PHONY: help build install clean test format lint type-check docs all

# Default target
help:
	@echo "QRiskLab Pro - Development Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make build          - Build C++ extensions"
	@echo "  make install        - Install package in development mode"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make test           - Run test suite"
	@echo "  make format         - Format code with black and isort"
	@echo "  make lint           - Run linters (ruff, flake8)"
	@echo "  make type-check     - Run type checker (mypy)"
	@echo "  make docs           - Build documentation"
	@echo "  make all            - Build, install, and run tests"
	@echo ""

# Build C++ extensions
build:
	@echo "Building C++ extensions..."
	python -m pip install --upgrade pip setuptools wheel cmake
	python setup.py build_ext --inplace
	@echo "Build complete!"

# Install in development mode
install: build
	@echo "Installing QRiskLab in development mode..."
	python -m pip install -e .
	@echo "Installation complete!"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.so" -delete
	@echo "Clean complete!"

# Run tests
test:
	@echo "Running test suite..."
	pytest tests/ -v --cov=qrisklab --cov-report=html --cov-report=term-missing
	@echo "Tests complete! Coverage report: htmlcov/index.html"

# Format code
format:
	@echo "Formatting code with black and isort..."
	black qrisklab/ tests/ scripts/ --line-length=100
	isort qrisklab/ tests/ scripts/ --profile=black --line-length=100
	@echo "Formatting complete!"

# Run linters
lint:
	@echo "Running linters..."
	ruff check qrisklab/ tests/ scripts/
	flake8 qrisklab/ tests/ scripts/ --max-line-length=100 --extend-ignore=E203,W503
	@echo "Linting complete!"

# Type checking
type-check:
	@echo "Running type checker..."
	mypy qrisklab/ --ignore-missing-imports --no-error-summary 2>&1 | head -20 || true
	@echo "Type checking complete!"

# Build documentation
docs:
	@echo "Building documentation..."
	@if [ ! -d "docs" ]; then \
		echo "Documentation directory not found. Skipping."; \
	else \
		cd docs && make html && cd ..; \
		echo "Documentation built! View at: docs/_build/html/index.html"; \
	fi

# Run all checks
all: clean build install test lint type-check
	@echo ""
	@echo "All checks complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  - Run 'make docs' to build documentation"
	@echo "  - Run 'python scripts/run_api.py' to start the API server"
	@echo "  - Run 'streamlit run scripts/run_dashboard.py' to start the dashboard"
	@echo ""
