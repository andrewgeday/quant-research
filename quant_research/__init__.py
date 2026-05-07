"""
Quant Research: Quantitative research experiments built on reusable packages.
"""

from quant_research.strategies import (
    Strategy,
    MovingAverageStrategy,
    MomentumStrategy,
    MeanReversionStrategy,
)
from quant_research.utils import (
    configure_logging,
    load_yaml,
    validate_config,
)

__version__ = "0.1.0"

__all__ = [
    "Strategy",
    "MovingAverageStrategy",
    "MomentumStrategy",
    "MeanReversionStrategy",
    "configure_logging",
    "load_yaml",
    "validate_config",
]