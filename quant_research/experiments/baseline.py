import pandas as pd
import yaml
from pathlib import Path

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.strategies.moving_average import MovingAverageStrategy
from backtesting_engine.metrics.performance import sharpe_ratio, max_drawdown

BASE_DIR = Path(__file__).resolve().parents[2]

def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run():
    data_cfg = load_yaml(BASE_DIR / "config/data.yaml")
    bt_cfg = load_yaml(BASE_DIR / "config/backtest.yaml")

    # Run data pipeline
    run_pipeline(config_path=data_cfg["pipeline"]["config_path"])

    # Load clean prices
    prices = pd.read_csv(
        BASE_DIR / data_cfg["output"]["prices_path"],
        parse_dates=["date"],
    ).set_index("date")

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
    print("Sharpe:", round(sharpe_ratio(returns), 2))
    print("Max DD:", round(max_drawdown(returns), 2))


if __name__ == "__main__":
    run()