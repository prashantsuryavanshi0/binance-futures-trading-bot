"""Configuration helpers for Binance credentials and environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from .exceptions import ConfigurationException


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE_FILE = PROJECT_ROOT / ".env.example"

load_dotenv(ENV_FILE)


def get_api_credentials() -> tuple[str, str]:
    """Load API key pair from environment variables."""
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    secret_key = os.getenv("BINANCE_SECRET_KEY", "").strip()

    if not api_key or not secret_key:
        raise ConfigurationException(
            "Missing Binance API credentials. Set BINANCE_API_KEY and BINANCE_SECRET_KEY in your .env file."
        )

    return api_key, secret_key
