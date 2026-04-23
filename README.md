# Quant Research

This repository demonstrates an end-to-end quantitative research workflow,
built on reusable data ingestion and backtesting packages.

## Structure
- `market-data-pipeline`: market data ingestion and validation
- `backtesting-engine`: backtesting and risk evaluation
- `quant-research`: research experiments built on top

## Purpose
This repository focuses on research orchestration and experimentation,
not infrastructure reimplementation.

## Notes
This project is intended for demonstration and educational purposes.

## Results

We evaluate three simple strategies:

- Moving Average (trend-following)
- Momentum (return-based signal)
- Mean Reversion (contrarian)

### Key Observations
- Trend-following strategies perform better in sustained directional markets
- Mean reversion performs better in range-bound conditions
- Strategy performance is sensitive to parameter choices

### Notes
These results are illustrative and not indicative of real trading performance.
The goal is to demonstrate research workflow and evaluation methodology.

## Outputs

Each pipeline run generates:
- Versioned dataset (CSV)
- Metadata (JSON)
- Strategy performance metrics
- Cumulative return plots

This ensures reproducibility and traceability of results.