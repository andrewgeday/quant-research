import logging
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.metrics.performance import sharpe_ratio, max_drawdown, sortino_ratio

from quant_research.strategies import MovingAverageStrategy
from quant_research.utils import configure_logging, load_yaml, validate_config

logger = configure_logging(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]


def run() -> None:
    """
    Run the baseline moving average strategy experiment.

    This function loads configuration, runs the data pipeline, generates signals
    using a moving average strategy, performs backtesting, and logs performance metrics.
    """
    try:
        data_cfg = load_yaml(BASE_DIR / "config" / "data.yaml")
        bt_cfg = load_yaml(BASE_DIR / "config" / "backtest.yaml")

        # Validate config keys
        required_data_keys = ["pipeline", "output"]
        for key in required_data_keys:
            if key not in data_cfg:
                raise ValueError(f"Missing required key '{key}' in data config")

        required_bt_keys = ["strategy", "backtest"]
        for key in required_bt_keys:
            if key not in bt_cfg:
                raise ValueError(f"Missing required key '{key}' in backtest config")

        # Run data pipeline
        run_pipeline(config_path=data_cfg["pipeline"]["config_path"])

        # Load clean prices
        prices_path = BASE_DIR / data_cfg["output"]["prices_path"]
        prices = pd.read_csv(
            prices_path,
            parse_dates=["date"],
        ).set_index("date")

        # Validate prices data
        if "close" not in prices.columns:
            raise ValueError("Prices data must contain 'close' column")
        if not isinstance(prices.index, pd.DatetimeIndex):
            raise ValueError("Prices index must be DatetimeIndex")
        if prices.empty:
            raise ValueError("Prices data is empty")

        # Generate signals
        strat = MovingAverageStrategy(
            short_window=bt_cfg["strategy"]["short_window"],
            long_window=bt_cfg["strategy"]["long_window"],
        )

        signals = strat.generate_signals(prices)

        # Backtest
        returns = run_backtest(
            prices,
            signals,
            transaction_cost=bt_cfg["backtest"]["transaction_cost"],
        )

        # Evaluate
        sharpe = sharpe_ratio(returns)
        max_dd = max_drawdown(returns)
        sortino = sortino_ratio(returns)
        logger.info(f"Sharpe: {sharpe:.2f}")
        logger.info(f"Max DD: {max_dd:.2f}")
        logger.info(f"Sortino: {sortino:.2f}")

    except Exception as e:
        logger.error(f"Error running baseline experiment: {e}")
        raise


def main() -> None:
    """Entry point for CLI."""
    run()


if __name__ == "__main__":
    main()