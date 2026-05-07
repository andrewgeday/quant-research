import logging
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.metrics.performance import sharpe_ratio, max_drawdown, sortino_ratio

from quant_research.strategies import MomentumStrategy
from quant_research.utils import configure_logging, load_yaml, validate_config

logger = configure_logging(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Args:
        path: Path to the YAML file.

    Returns:
        Dictionary containing the parsed YAML data.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the YAML is malformed.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {path}: {e}")
        raise


def run() -> None:
    """
    Run the momentum strategy experiment.

    This function loads configuration, runs the data pipeline, generates momentum signals,
    performs backtesting, and logs performance metrics.
    """
    try:
        data_cfg = load_yaml(BASE_DIR / "config" / "data.yaml")
        bt_cfg = load_yaml(BASE_DIR / "config" / "backtest.yaml")

        # Run pipeline
        run_pipeline(config_path=data_cfg["pipeline"]["config_path"])

        # Load prices
        prices_path = BASE_DIR / data_cfg["output"]["prices_path"]
        prices = pd.read_csv(
            prices_path,
            parse_dates=["date"],
        ).set_index("date")

        # Signals
        strat = MomentumStrategy(window=20)
        signals = strat.generate_signals(prices)

        # Backtest
        returns = run_backtest(
            prices,
            signals,
            transaction_cost=bt_cfg["backtest"]["transaction_cost"],
        )

        # Metrics
        sharpe = sharpe_ratio(returns)
        max_dd = max_drawdown(returns)
        sortino = sortino_ratio(returns)
        logger.info("Momentum Strategy")
        logger.info(f"Sharpe: {sharpe:.2f}")
        logger.info(f"Max DD: {max_dd:.2f}")
        logger.info(f"Sortino: {sortino:.2f}")

    except Exception as e:
        logger.error(f"Error running momentum experiment: {e}")
        raise


def main() -> None:
    """Entry point for CLI."""
    run()


if __name__ == "__main__":
    main()