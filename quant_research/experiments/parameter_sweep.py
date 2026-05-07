import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.metrics.performance import sharpe_ratio

from quant_research.strategies import MovingAverageStrategy
from quant_research.utils import configure_logging, load_yaml, validate_config

logger = configure_logging(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]


def run() -> None:
    """
    Run parameter sweep for moving average strategy.

    Tests different combinations of short and long windows, computes Sharpe ratio
    for each, and saves results to CSV.
    """
    try:
        data_cfg = load_yaml(BASE_DIR / "config" / "data.yaml")
        bt_cfg = load_yaml(BASE_DIR / "config" / "backtest.yaml")

        run_pipeline(config_path=data_cfg["pipeline"]["config_path"])

        prices_path = BASE_DIR / data_cfg["output"]["prices_path"]
        prices = pd.read_csv(
            prices_path,
            parse_dates=["date"],
        ).set_index("date")

        logger.info("=== Parameter Sweep (Moving Average) ===")

        results: List[Dict[str, Any]] = []

        for short in [5, 10, 20]:
            for long in [30, 50, 100]:
                if short >= long:
                    continue

                strat = MovingAverageStrategy(short, long)
                returns = run_backtest(
                    prices,
                    strat.generate_signals(prices),
                    transaction_cost=bt_cfg["backtest"]["transaction_cost"]
                )

                sharpe = sharpe_ratio(returns)

                results.append({
                    "short_window": short,
                    "long_window": long,
                    "sharpe_ratio": sharpe,
                })

        results_df = pd.DataFrame(results)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sweep_path = BASE_DIR / "results" / f"sweep_{timestamp}.csv"
        results_df.to_csv(sweep_path, index=False)

        logger.info(f"Parameter sweep results saved: {sweep_path}")

    except Exception as e:
        logger.error(f"Error running parameter sweep: {e}")
        raise


def main() -> None:
    """Entry point for CLI."""
    run()


if __name__ == "__main__":
    main()