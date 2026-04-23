from datetime import datetime

import pandas as pd
import yaml
from pathlib import Path

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.strategies.moving_average import MovingAverageStrategy
from backtesting_engine.metrics.performance import sharpe_ratio

BASE_DIR = Path(__file__).resolve().parents[2]


def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run():
    data_cfg = load_yaml(BASE_DIR / "config/data.yaml")

    run_pipeline(config_path=data_cfg["pipeline"]["config_path"])

    prices = pd.read_csv(
        BASE_DIR / data_cfg["output"]["prices_path"],
        parse_dates=["date"],
    ).set_index("date")

    print("\n=== Parameter Sweep (Moving Average) ===")

    results = []

    for short in [5, 10, 20]:
        for long in [30, 50, 100]:
            if short >= long:
                continue

            strat = MovingAverageStrategy(short, long)
            returns = run_backtest(prices, strat.generate_signals(prices))

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

    print(f"Parameter sweep results saved: {sweep_path}")


if __name__ == "__main__":
    run()