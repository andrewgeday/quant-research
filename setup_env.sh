#!/bin/bash

# Allow overriding paths via environment variables
MARKET_DATA_PATH=${MARKET_DATA_PATH:-~/git/market-data-pipeline}
BACKTEST_ENGINE_PATH=${BACKTEST_ENGINE_PATH:-~/git/backtesting-engine}

# Check if required directories exist
if [ ! -d "$MARKET_DATA_PATH" ]; then
    echo "Error: Market data pipeline not found at $MARKET_DATA_PATH"
    echo "Please set MARKET_DATA_PATH to the correct path or clone the repository."
    exit 1
fi

if [ ! -d "$BACKTEST_ENGINE_PATH" ]; then
    echo "Error: Backtesting engine not found at $BACKTEST_ENGINE_PATH"
    echo "Please set BACKTEST_ENGINE_PATH to the correct path or clone the repository."
    exit 1
fi

# Install dependencies
pip install -e "$MARKET_DATA_PATH"
pip install -e "$BACKTEST_ENGINE_PATH"
pip install -e .[dev]