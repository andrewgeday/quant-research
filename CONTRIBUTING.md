# Contributing to Quant Research

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/quant-research.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up the development environment: `./setup_env.sh && pip install -e .[dev]`

## Development Workflow

### Running Tests

```bash
pytest
```

### Code Quality Checks

```bash
black quant_research/ tests/      # Format code
flake8 quant_research/ tests/     # Check style
mypy quant_research/               # Type checking
```

### Using Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Code Standards

- **Type Hints**: All functions must have type annotations
- **Docstrings**: Use Google-style docstrings for all public functions/classes
- **Testing**: Add tests for new functionality (target 70%+ coverage)
- **Logging**: Use the logging module, not print statements
- **Line Length**: Maximum 88 characters (configured in black)

## Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Test additions
- `refactor:` Code refactoring
- `style:` Code style (formatting)
- `chore:` Build, dependency updates

Example: `feat: add sortino ratio metric to experiments`

## Pull Request Process

1. Update documentation if needed
2. Add/update tests for your changes
3. Run all quality checks (`black`, `flake8`, `mypy`, `pytest`)
4. Submit PR with clear description of changes
5. Ensure CI passes

## Reporting Issues

Use GitHub Issues to report bugs. Include:

- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Relevant code/logs

## Questions?

Feel free to open an issue with the `question` label or contact the maintainers.