import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from market_data_pipeline.pipeline import run_pipeline
from backtesting_engine.engine.backtest import run_backtest
from backtesting_engine.strategies.moving_average import MovingAverageStrategy
from backtesting_engine.metrics.performance import sharpe_ratio, max_drawdown, sortino_ratio

from quant_research.strategies import MomentumStrategy, MeanReversionStrategy
from quant_research.utils import configure_logging, load_yaml, validate_config

logger = configure_logging(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]


def build_portfolio_returns(prices: pd.DataFrame, signals: pd.Series) -> pd.Series:
    """
    Build portfolio returns from price data and signals.

    Args:
        prices: DataFrame with price data, must contain 'close' column.
        signals: Series of trading signals (0 or 1).

    Returns:
        Series of portfolio returns.
    """
    df = prices.copy()
    df["signal"] = signals
    df["returns"] = df["close"].pct_change()
    df["strategy_returns"] = df["returns"] * df["signal"].shift(1)
    portfolio_returns = df.groupby("date")["strategy_returns"].mean()
    return portfolio_returns.dropna()


def cumulative_returns(returns: pd.Series) -> pd.Series:
    """
    Calculate cumulative returns.

    Args:
        returns: Series of periodic returns.

    Returns:
        Series of cumulative returns.
    """
    return (1 + returns).cumprod()


def compute_alpha(strategy_returns: pd.Series, benchmark_returns: pd.Series) -> float:
    """
    Compute alpha as the difference in mean returns vs benchmark.

    Args:
        strategy_returns: Series of strategy returns.
        benchmark_returns: Series of benchmark returns.

    Returns:
        Alpha value.
    """
    aligned = pd.concat([strategy_returns, benchmark_returns], axis=1).dropna()
    strat = aligned.iloc[:, 0]
    bench = aligned.iloc[:, 1]
    return strat.mean() - bench.mean()


def run() -> None:
    """
    Run strategy comparison experiment.

    Compares moving average, momentum, and mean reversion strategies,
    computes metrics, saves results, and generates plots.
    """
    try:
        data_cfg = load_yaml(BASE_DIR / "config" / "data.yaml")

        # Run pipeline
        pipeline_config_path = (BASE_DIR / data_cfg["pipeline"]["config_path"]).resolve()
        output_path = run_pipeline(config_path=str(pipeline_config_path))

        prices = pd.read_csv(
            output_path,
            parse_dates=["date"],
        ).set_index("date")

        spy = yf.download("SPY", start=prices.index.min(), end=prices.index.max())
        spy_returns = spy["Close"].pct_change().dropna()

        results: Dict[str, pd.Series] = {}

        # --- Moving Average ---
        ma = MovingAverageStrategy(20, 50)
        ma_signals = ma.generate_signals(prices)
        ma_returns = build_portfolio_returns(prices, ma_signals)
        results["Moving Average"] = ma_returns

        # --- Momentum ---
        mom_strat = MomentumStrategy(window=20)
        mom_signals = mom_strat.generate_signals(prices)
        mom_returns = build_portfolio_returns(prices, mom_signals)
        results["Momentum"] = mom_returns

        # --- Mean Reversion ---
        mr_strat = MeanReversionStrategy(window=20)
        mr_signals = mr_strat.generate_signals(prices)
        mr_returns = build_portfolio_returns(prices, mr_signals)
        results["Mean Reversion"] = mr_returns

        # --- Metrics ---
        logger.info("=== Strategy Comparison ===")
        metrics: List[Dict[str, Any]] = []

        for name, ret in results.items():
            sharpe = sharpe_ratio(ret)
            mdd = max_drawdown(ret)
            sortino = sortino_ratio(ret)
            alpha = compute_alpha(ret, spy_returns)

            logger.info(f"\n{name}")
            logger.info(f"Sharpe: {sharpe:.2f}")
            logger.info(f"Max DD: {mdd:.2f}")
            logger.info(f"Sortino: {sortino:.2f}")
            logger.info(f"Alpha vs SPY: {alpha:.4f}")

            metrics.append({
                "strategy": name,
                "sharpe": sharpe,
                "max_drawdown": mdd,
                "sortino": sortino,
                "alpha": alpha
            })

        metrics_df = pd.DataFrame(metrics)

        results_dir = BASE_DIR / "results"
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        metrics_path = results_dir / f"metrics_{timestamp}.csv"
        metrics_df.to_csv(metrics_path, index=False)

        logger.info(f"Metrics saved: {metrics_path}")

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
        plt.figure(figsize=(12, 8))
        colors = ['blue', 'green', 'red', 'orange']
        for i, (name, ret) in enumerate(results.items()):
            plt.plot(cumulative_returns(ret), label=name, color=colors[i], linewidth=2)
        plt.plot(
            cumulative_returns(spy_returns),
            label="SPY (Benchmark)",
            linestyle="--",
            color="black",
            linewidth=2
        )

        plt.legend()
        plt.title("Strategy Comparison - Cumulative Returns", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Cumulative Returns", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plot_path = results_dir / f"plot_{timestamp}.png"

        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Plot saved: {plot_path}")

    except Exception as e:
        logger.error(f"Error running strategy comparison: {e}")
        raise
    print(f"Plot saved: {plot_path}")

    plt.close()


def main() -> None:
    """Entry point for CLI."""
    run()


if __name__ == "__main__":
    main()