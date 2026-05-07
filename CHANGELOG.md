# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-06

### Added

- Initial release
- Three strategy implementations: Moving Average, Momentum, Mean Reversion
- Baseline experiment with performance metrics
- Parameter sweep for strategy optimization
- Strategy comparison experiment against SPY benchmark
- Unit tests with pytest
- Type hints throughout codebase
- Pre-commit hooks for code quality
- Comprehensive documentation and README
- MIT License
- Enhanced metrics: Sharpe, Sortino, Max Drawdown, Alpha
- Improved visualization with styled plots
- Centralized utilities module for common functions
- YAML configuration support
- Security policy documentation

### Changed

- Refactored duplicate code into centralized utils module
- Improved .gitignore with comprehensive Python artifacts
- Exposed public API via package __init__.py
- Centralized logging configuration

## Future Plans

- [ ] Integration with live market data sources
- [ ] Machine learning strategy implementations
- [ ] Enhanced risk metrics (VaR, Sortino ratio improvements)
- [ ] Portfolio optimization module
- [ ] Statistical significance testing
- [ ] GitHub Actions CI/CD workflow