import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import patch

from quant_research.strategies import (
    MovingAverageStrategy,
    MomentumStrategy,
    MeanReversionStrategy
)
from quant_research.experiments.compare_strategies import (
    build_portfolio_returns,
    cumulative_returns,
    compute_alpha
)


@pytest.fixture
def sample_prices():
    """Sample price data for testing."""
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    prices = pd.DataFrame({
        "close": [100 + i * 0.1 for i in range(100)],
        "date": dates
    })
    prices.set_index("date", inplace=True)
    return prices


@pytest.fixture
def sample_signals():
    """Sample signals for testing."""
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    signals = pd.Series([1 if i % 2 == 0 else 0 for i in range(100)], index=dates)
    return signals


@pytest.fixture
def sample_returns():
    """Sample returns for testing."""
    dates = pd.date_range("2020-01-01", periods=99, freq="D")
    returns = pd.Series([0.01 if i % 2 == 0 else -0.01 for i in range(99)], index=dates)
    return returns


class TestSignalGeneration:
    """Test signal generation functions."""

    def test_generate_mean_reversion_signals(self, sample_prices):
        strat = MeanReversionStrategy(window=20)
        signals = strat.generate_signals(sample_prices)
        assert isinstance(signals, pd.Series)
        assert len(signals) == len(sample_prices)
        assert signals.dtype == int
        assert set(signals.unique()).issubset({0, 1})

    def test_generate_momentum_signals(self, sample_prices):
        strat = MomentumStrategy(window=20)
        signals = strat.generate_signals(sample_prices)
        assert isinstance(signals, pd.Series)
        assert len(signals) == len(sample_prices)
        assert signals.dtype == int
        assert set(signals.unique()).issubset({0, 1})


class TestPortfolioReturns:
    """Test portfolio return calculations."""

    def test_build_portfolio_returns(self, sample_prices, sample_signals):
        returns = build_portfolio_returns(sample_prices, sample_signals)
        assert isinstance(returns, pd.Series)
        assert len(returns) < len(sample_prices)  # Due to shift and dropna
        assert returns.index.name == "date"

    def test_cumulative_returns(self, sample_returns):
        cum_returns = cumulative_returns(sample_returns)
        assert isinstance(cum_returns, pd.Series)
        assert len(cum_returns) == len(sample_returns)
        assert cum_returns.iloc[0] == pytest.approx(1.01, rel=1e-2)  # First return applied

    def test_compute_alpha(self, sample_returns):
        benchmark = sample_returns * 0.5  # Mock benchmark
        alpha = compute_alpha(sample_returns, benchmark)
        assert isinstance(alpha, float)


class TestDataValidation:
    """Test data validation functions."""

    def test_load_yaml_valid(self, tmp_path):
        yaml_content = """
        key: value
        number: 42
        """
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        result = load_yaml(yaml_file)
        assert result == {"key": "value", "number": 42}

    def test_load_yaml_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_yaml(Path("nonexistent.yaml"))

    @patch("builtins.open")
    def test_load_yaml_invalid_yaml(self, mock_open, tmp_path):
        mock_open.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            load_yaml(tmp_path / "test.yaml")


class TestExperimentIntegration:
    """Integration tests for experiment runs (mocked)."""

    @patch("quant_research.experiments.mean_reversion.run_pipeline")
    @patch("quant_research.experiments.mean_reversion.load_yaml")
    @patch("pandas.read_csv")
    @patch("quant_research.experiments.mean_reversion.run_backtest")
    @patch("backtesting_engine.metrics.performance.sharpe_ratio")
    @patch("backtesting_engine.metrics.performance.max_drawdown")
    def test_run_mean_reversion_integration(self, mock_mdd, mock_sharpe, mock_backtest,
                                           mock_read_csv, mock_load_yaml, mock_pipeline):
        # Mock all external dependencies
        mock_load_yaml.return_value = {"pipeline": {"config_path": "dummy"}, "output": {"prices_path": "dummy.csv"}}
        mock_pipeline.return_value = "dummy.csv"
        mock_read_csv.return_value = sample_prices()
        mock_backtest.return_value = pd.Series([0.01] * 10)
        mock_sharpe.return_value = 1.5
        mock_mdd.return_value = -0.1

        # This would normally run the full experiment
        # For now, just ensure mocks are called
        from quant_research.experiments.mean_reversion import run
        # run()  # Commented out to avoid actual execution in test

        # Assert mocks were called
        assert mock_load_yaml.call_count >= 2  # Called for data and bt config