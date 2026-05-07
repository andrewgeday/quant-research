"""
Strategy base classes and implementations for quantitative trading.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd


class Strategy(ABC):
    """
    Abstract base class for trading strategies.

    Strategies generate buy/sell signals based on price data.
    """

    def __init__(self, **params: Any) -> None:
        """
        Initialize strategy with parameters.

        Args:
            **params: Strategy-specific parameters.
        """
        self.params = params

    @abstractmethod
    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals from price data.

        Args:
            prices: DataFrame with price data, must contain 'close' column.

        Returns:
            Series of signals (0 for sell/short, 1 for buy/long).
        """
        pass

    def get_params(self) -> Dict[str, Any]:
        """Get strategy parameters."""
        return self.params.copy()


class MovingAverageStrategy(Strategy):
    """
    Moving Average Crossover Strategy.

    Generates signals based on short and long moving average crossovers.
    """

    def __init__(self, short_window: int = 20, long_window: int = 50) -> None:
        super().__init__(short_window=short_window, long_window=long_window)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        """
        Generate signals using moving average crossover.

        Args:
            prices: DataFrame with 'close' column.

        Returns:
            Series of signals (1 when short MA > long MA, 0 otherwise).
        """
        short_ma = prices["close"].rolling(self.short_window).mean()
        long_ma = prices["close"].rolling(self.long_window).mean()
        signals = (short_ma > long_ma).astype(int)
        return signals


class MomentumStrategy(Strategy):
    """
    Momentum Strategy.

    Generates signals based on past return momentum.
    """

    def __init__(self, window: int = 20) -> None:
        super().__init__(window=window)
        self.window = window

    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        """
        Generate signals based on momentum.

        Args:
            prices: DataFrame with 'close' column.

        Returns:
            Series of signals (1 when past return > 0, 0 otherwise).
        """
        momentum = prices["close"].pct_change(self.window)
        signals = (momentum > 0).astype(int)
        return signals


class MeanReversionStrategy(Strategy):
    """
    Mean Reversion Strategy.

    Generates signals based on deviation from rolling mean.
    """

    def __init__(self, window: int = 20) -> None:
        super().__init__(window=window)
        self.window = window

    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        """
        Generate signals for mean reversion.

        Args:
            prices: DataFrame with 'close' column.

        Returns:
            Series of signals (1 when price < rolling mean, 0 otherwise).
        """
        rolling_mean = prices["close"].rolling(self.window).mean()
        signals = (prices["close"] < rolling_mean).astype(int)
        return signals