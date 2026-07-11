"""Binance Futures Testnet client factory."""

from __future__ import annotations

from binance import Client as BinanceClient

from .config import get_api_credentials
from .exceptions import APIException, ConfigurationException


def create_client() -> BinanceClient:
    """Create a reusable Binance futures testnet client instance."""
    try:
        api_key, secret_key = get_api_credentials()
    except ConfigurationException as exc:
        raise exc

    try:
        client = BinanceClient(api_key=api_key, api_secret=secret_key, testnet=True)
        client.futures_position_information()
        return client
    except Exception as exc:  # pragma: no cover - defensive handling
        raise APIException(f"Unable to initialize Binance client: {exc}") from exc
