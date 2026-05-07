.PHONY: help install install-dev test lint format type-check clean docs

help:
	@echo "Quant Research - Available Commands"
	@echo "===================================="
	@echo "make install        Install the package"
	@echo "make install-dev    Install with dev dependencies"
	@echo "make test           Run tests"
	@echo "make lint           Run flake8 linter"
	@echo "make format         Format code with black"
	@echo "make type-check     Run mypy type checker"
	@echo "make clean          Remove build artifacts"
	@echo "make pre-commit-install  Setup pre-commit hooks"
	@echo "make experiments    Show available experiments"

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

test:
	pytest --verbose --tb=short

test-cov:
	pytest --verbose --cov=quant_research --cov-report=html

lint:
	flake8 quant_research/ tests/

format:
	black quant_research/ tests/

type-check:
	mypy quant_research/

quality: format lint type-check test

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/

pre-commit-install:
	pre-commit install
	pre-commit run --all-files

experiments:
	@echo "Available experiments:"
	@echo "  quant-baseline          Baseline moving average strategy"
	@echo "  quant-momentum          Momentum strategy"
	@echo "  quant-mean-reversion    Mean reversion strategy"
	@echo "  quant-parameter-sweep   Parameter sweep"
	@echo "  quant-compare           Strategy comparison"