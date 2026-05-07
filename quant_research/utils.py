"""
Utilities module for configuration, logging, and common functions.
"""
import logging
from pathlib import Path
from typing import Any, Dict

import yaml


def configure_logging(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        name: Logger name (typically __name__).
        level: Logging level (default: INFO).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(level)
    return logger


def load_yaml(path: Path) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Args:
        path: Path to the YAML file.

    Returns:
        Dictionary containing the parsed YAML data.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the YAML is malformed.
    """
    logger = configure_logging(__name__)
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {path}: {e}")
        raise


def validate_config(config: Dict[str, Any], required_keys: list[str]) -> None:
    """
    Validate that a config dict contains all required keys.

    Args:
        config: Configuration dictionary to validate.
        required_keys: List of required top-level keys.

    Raises:
        ValueError: If required keys are missing.
    """
    logger = configure_logging(__name__)
    
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(f"Missing required config keys: {missing_keys}")
    
    logger.debug(f"Config validation passed. Keys: {required_keys}")
