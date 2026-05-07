# Development Guide

## Architecture Overview

```
quant_research/
├── __init__.py           # Public API exports
├── strategies.py         # Strategy base class and implementations
├── utils.py              # Shared utilities (logging, config, validation)
├── experiments/          # Experiment scripts
│   ├── baseline.py
│   ├── momentum.py
│   ├── mean_reversion.py
│   ├── parameter_sweep.py
│   └── compare_strategies.py
└── notebooks/            # Jupyter notebooks
```

## Key Components

### Strategies (`strategies.py`)

Abstract `Strategy` base class with three implementations:
- `MovingAverageStrategy`: Crossover-based trend following
- `MomentumStrategy`: Return-based signal generation
- `MeanReversionStrategy`: Deviation from rolling mean

All strategies implement `generate_signals(prices)` → returns 0/1 series.

### Utilities (`utils.py`)

- `configure_logging()`: Centralized logger setup
- `load_yaml()`: YAML config loading with error handling
- `validate_config()`: Config validation

### Experiments

Each experiment:
1. Loads config files using `load_yaml()`
2. Runs data pipeline
3. Loads price data
4. Creates strategy and generates signals
5. Backtests and computes metrics
6. Saves results to `results/`

## Testing

### Running Tests

```bash
pytest                    # Run all tests
pytest -v                 # Verbose
pytest --cov              # With coverage
pytest -k test_name       # Specific test
```

### Adding Tests

1. Create test function: `test_*.py` files in `tests/`
2. Use fixtures from `conftest.py` for common data
3. Target 70%+ code coverage
4. Use mocking for external dependencies

## Code Quality

### Running Checks

```bash
black .                   # Format code
flake8 quant_research/    # Lint
mypy quant_research/      # Type check
pre-commit run --all-files  # All checks
```

### Standards

- **Type Hints**: All functions must have annotations
- **Docstrings**: Google-style for public functions
- **Line Length**: 88 characters max
- **Logging**: Use logger, not print

## Adding New Strategies

1. Inherit from `Strategy` base class in `strategies.py`
2. Implement `generate_signals(prices)` method
3. Add docstring and type hints
4. Create tests in `tests/`
5. Add experiment script if needed

Example:

```python
class MyStrategy(Strategy):
    def __init__(self, param1: int = 20) -> None:
        super().__init__(param1=param1)
        self.param1 = param1
    
    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        # Implementation
        return signals
```

## Configuration Files

### `config/backtest.yaml`

```yaml
strategy:
  short_window: 20
  long_window: 50

backtest:
  transaction_cost: 0.0005
```

### `config/data.yaml`

```yaml
pipeline:
  config_path: "../market-data-pipeline/config.yaml"

output:
  prices_path: "../market-data-pipeline/output/equities_ohlcv.csv"
```

## Version Management

Version is automatically managed by `setuptools-scm` from git tags:

```bash
git tag v0.2.0
git push origin v0.2.0
```

## CI/CD

GitHub Actions workflow runs on every push/PR:
- Linting (flake8, black)
- Type checking (mypy)
- Tests (pytest on Python 3.8-3.11)
- Pre-commit hooks

See `.github/workflows/ci.yml`

## Troubleshooting

### Import Errors

Ensure package is installed: `pip install -e .`

### Test Failures

Check that mocked dependencies are correct and fixtures have proper scope.

### Config Loading Issues

Verify YAML syntax and ensure files exist at paths specified in config.

## Contributing

See `CONTRIBUTING.md` for guidelines on making changes and submitting PRs.