import pandas as pd
import yaml
from pathlib import Path

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.metrics.performance import sharpe_ratio, max_drawdown

BASE_DIR = Path(__file__).resolve().parents[2]

def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def generate_mean_reversion_signals(prices: pd.DataFrame, window: int = 20) -> pd.Series:
    """
    Long when price is below rolling mean (mean reversion).
    """
    rolling_mean = prices["close"].rolling(window).mean()

    signals = (prices["close"] < rolling_mean).astype(int)
    return signals


def run():
    data_cfg = load_yaml(BASE_DIR / "config/data.yaml")
    bt_cfg = load_yaml(BASE_DIR / "config/backtest.yaml")

    # Run pipeline
    run_pipeline(config_path=data_cfg["pipeline"]["config_path"])

    # Load prices
    prices = pd.read_csv(
        BASE_DIR / data_cfg["output"]["prices_path"],
        parse_dates=["date"],
    ).set_index("date")

    # Signals
    signals = generate_mean_reversion_signals(prices, window=20)

    # Backtest
    returns = run_backtest(
        prices,
        signals,
        transaction_cost=bt_cfg["backtest"]["transaction_cost"],
    )

    # Metrics
    print("Mean Reversion Strategy")
    print("Sharpe:", round(sharpe_ratio(returns), 2))
    print("Max DD:", round(max_drawdown(returns), 2))


if __name__ == "__main__":
    run()