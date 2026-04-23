import pandas as pd
import yaml
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import yfinance as yf

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.strategies.moving_average import MovingAverageStrategy
from backtesting_engine.metrics.performance import sharpe_ratio, max_drawdown

BASE_DIR = Path(__file__).resolve().parents[2]

def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def build_portfolio_returns(prices: pd.DataFrame, signals: pd.Series):
    df = prices.copy()
    df["signal"] = signals

    df["returns"] = df["close"].pct_change()

    # Strategy returns
    df["strategy_returns"] = df["returns"] * df["signal"].shift(1)

    # Aggregate across symbols
    portfolio_returns = df.groupby("date")["strategy_returns"].mean()

    return portfolio_returns.dropna()

def momentum_signal(prices, window=20):
    return (prices["close"].pct_change(window) > 0).astype(int)


def mean_reversion_signal(prices, window=20):
    rolling_mean = prices["close"].rolling(window).mean()
    return (prices["close"] < rolling_mean).astype(int)


def cumulative_returns(returns: pd.Series) -> pd.Series:
    return (1 + returns).cumprod()

def compute_alpha(strategy_returns, benchmark_returns):
    aligned = pd.concat([strategy_returns, benchmark_returns], axis=1).dropna()
    strat = aligned.iloc[:, 0]
    bench = aligned.iloc[:, 1]

    return strat.mean() - bench.mean()


def run():
    data_cfg = load_yaml(BASE_DIR / "config/data.yaml")

    # Run pipeline
    pipeline_config_path = (BASE_DIR / data_cfg["pipeline"]["config_path"]).resolve()
    output_path = run_pipeline(config_path=str(pipeline_config_path))

    prices = pd.read_csv(
        output_path,
        parse_dates=["date"],
    ).set_index("date")

    spy = yf.download("SPY", start=prices.index.min(), end=prices.index.max())
    spy_returns = plt.spy["Close"].pct_change().dropna()

    results = {}

    # --- Moving Average ---
    ma = MovingAverageStrategy(20, 50)
    ma_signals = ma.generate_signals(prices)
    ma_returns = build_portfolio_returns(prices, ma_signals)
    results["Moving Average"] = ma_returns

    # --- Momentum ---
    mom_returns = build_portfolio_returns(prices, momentum_signal(prices))
    results["Momentum"] = mom_returns

    # --- Mean Reversion ---
    mr_returns = build_portfolio_returns(prices, mean_reversion_signal(prices))
    results["Mean Reversion"] = mr_returns

    # --- Metrics ---
    print("\n=== Strategy Comparison ===")
    metrics = []

    for name, ret in results.items():
        sharpe = sharpe_ratio(ret)
        mdd = max_drawdown(ret)
        alpha = compute_alpha(ret, spy_returns)

        print(f"\n{name}")
        print("Sharpe:", round(sharpe, 2))
        print("Max DD:", round(mdd, 2))
        print("Alpha vs SPY:", round(alpha, 4))

        metrics.append({
            "strategy": name,
            "sharpe": sharpe,
            "max_drawdown": mdd,
            "alpha": alpha
        })

    metrics_df = pd.DataFrame(metrics)

    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    metrics_path = results_dir / f"metrics_{timestamp}.csv"
    metrics_df.to_csv(metrics_path, index=False)

    print(f"\nMetrics saved: {metrics_path}")

    tracking_path = BASE_DIR / "results" / "experiment_log.csv"

    run_summary = {
        "timestamp": timestamp,
        "strategy": "comparison",
        "sharpe_mean": metrics_df["sharpe"].mean(),
        "max_drawdown_min": metrics_df["max_drawdown"].min()
    }

    log_df = pd.DataFrame([run_summary])

    if tracking_path.exists():
        log_df.to_csv(tracking_path, mode="a", header=False, index=False)
    else:
        log_df.to_csv(tracking_path, index=False)


    # --- Plot ---
    plt.figure()
    for name, ret in results.items():
        plt.plot(cumulative_returns(ret), label=name)
        plt.plot(
            cumulative_returns(spy_returns),
            label="SPY (Benchmark)",
            linestyle="--"
        )

    plt.legend()
    plt.title("Strategy Comparison")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns")
    plot_path = results_dir / f"plot_{timestamp}.png"

    plt.savefig(plot_path)
    print(f"Plot saved: {plot_path}")

    plt.close()


if __name__ == "__main__":
    run()