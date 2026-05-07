# Quant Research

This repository demonstrates an end-to-end quantitative research workflow, built on reusable data ingestion and backtesting packages.

## Prerequisites

Before running this project, ensure you have the following dependencies installed locally:

- `market-data-pipeline`: Data ingestion and validation package
- `backtesting-engine`: Backtesting and risk evaluation package

Clone these repositories to `~/git/` or update `MARKET_DATA_PATH` and `BACKTEST_ENGINE_PATH` in `setup_env.sh`.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/andrewgeday/quant-research.git
   cd quant-research
   ```

2. Set up the environment:
   ```bash
   # Install dependencies (adjust paths if needed)
   ./setup_env.sh
   ```

3. Install development dependencies (optional):
   ```bash
   pip install -e .[dev]
   ```

## Usage

### Running Experiments

You can run experiments either as Python modules or using the installed CLI commands:

**Using CLI (after installation):**

```bash
quant-baseline          # Baseline moving average strategy
quant-momentum          # Momentum strategy
quant-mean-reversion    # Mean reversion strategy
quant-parameter-sweep   # Parameter sweep for moving average
quant-compare           # Strategy comparison
```

**Using Python modules:**

```bash
python -m quant_research.experiments.baseline
python -m quant_research.experiments.momentum
python -m quant_research.experiments.mean_reversion
python -m quant_research.experiments.parameter_sweep
python -m quant_research.experiments.compare_strategies
```

### Configuration

Modify parameters in `config/`:

- `backtest.yaml`: Backtesting settings (transaction costs, strategy parameters)
- `data.yaml`: Data pipeline configuration

### Using as a Python Library

```python
from quant_research import MovingAverageStrategy, load_yaml
import pandas as pd

# Load config
config = load_yaml("config/backtest.yaml")

# Create and use a strategy
strategy = MovingAverageStrategy(short_window=20, long_window=50)
prices = pd.read_csv("data.csv", parse_dates=["date"]).set_index("date")
signals = strategy.generate_signals(prices)
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black .
flake8 quant_research/
mypy quant_research/
```

## Project Structure

- `quant_research/`: Main package
  - `strategies.py`: Strategy implementations
  - `experiments/`: Experiment scripts
  - `notebooks/`: Jupyter notebooks
- `config/`: Configuration files
- `results/`: Experiment outputs
- `tests/`: Unit tests

## Purpose

This repository focuses on research orchestration and experimentation, not infrastructure reimplementation.

## Results

We evaluate three simple strategies:

- **Moving Average** (trend-following)
- **Momentum** (return-based signal)
- **Mean Reversion** (contrarian)

### Key Observations

- Trend-following strategies perform better in sustained directional markets
- Mean reversion performs better in range-bound conditions
- Strategy performance is sensitive to parameter choices

### Notes

These results are illustrative and not indicative of real trading performance. The goal is to demonstrate research workflow and evaluation methodology.

## Outputs

Each pipeline run generates:

- Versioned dataset (CSV)
- Metadata (JSON)
- Strategy performance metrics
- Cumulative return plots

This ensures reproducibility and traceability of results.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run `black`, `flake8`, and `mypy`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

This project is intended for demonstration and educational purposes.