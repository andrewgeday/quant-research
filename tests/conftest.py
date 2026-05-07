"""
Shared pytest configuration and fixtures.
"""
import pandas as pd
import pytest


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