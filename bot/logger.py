"""Logging configuration for the trading bot."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logger(name: str = "trading_bot") -> logging.Logger:
    """Create a reusable logger that writes to logs/bot.log."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    log_path = Path(__file__).resolve().parent.parent / "logs" / "bot.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


logger = configure_logger()
