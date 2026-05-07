# Results

This directory contains outputs from quantitative research experiments.

## File Naming Convention

- `metrics_YYYYMMDD_HHMMSS.csv`: Performance metrics for strategy comparisons
- `sweep_YYYYMMDD_HHMMSS.csv`: Parameter sweep results
- `plot_YYYYMMDD_HHMMSS.png`: Performance plots
- `experiment_log.csv`: Log of all experiment runs

## Metrics Explanation

- **Sharpe Ratio**: Risk-adjusted return measure (higher is better)
- **Sortino Ratio**: Risk-adjusted return focusing on downside volatility (higher is better)
- **Max Drawdown**: Maximum peak-to-trough decline (lower is better)
- **Alpha**: Excess return vs benchmark (higher is better)

## Notes

- Results are timestamped for reproducibility
- All files are generated automatically by experiment scripts
- Sensitive data should not be committed to version control