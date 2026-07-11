"""Reusable order placement helpers for Binance Futures Testnet."""

from __future__ import annotations

from typing import Any

from binance import Client as BinanceClient

from .exceptions import APIException
from .logger import logger


def _parse_order_response(response: dict[str, Any]) -> dict[str, Any]:
    """Normalize an order response into a consistent dictionary."""
    return {
        "order_id": response.get("orderId") or response.get("id"),
        "status": response.get("status"),
        "executed_quantity": response.get("executedQty") or response.get("executed_quantity"),
        "avg_price": response.get("avgPrice") or response.get("averagePrice"),
        "timestamp": response.get("updateTime") or response.get("transactTime"),
        "raw": response,
    }


def place_market_order(client: BinanceClient, symbol: str, side: str, quantity: str) -> dict[str, Any]:
    """Place a market order on Binance Futures Testnet."""
    try:
        logger.info("Placing market order for %s %s %s", symbol, side, quantity)
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        logger.info("Market order response: %s", response)
        return _parse_order_response(response)
    except Exception as exc:  # pragma: no cover - defensive handling
        logger.exception("Failed to place market order")
        raise APIException(f"Market order failed: {exc}") from exc


def place_limit_order(client: BinanceClient, symbol: str, side: str, quantity: str, price: str) -> dict[str, Any]:
    """Place a limit order on Binance Futures Testnet."""
    try:
        logger.info("Placing limit order for %s %s %s @ %s", symbol, side, quantity, price)
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
        logger.info("Limit order response: %s", response)
        return _parse_order_response(response)
    except Exception as exc:  # pragma: no cover - defensive handling
        logger.exception("Failed to place limit order")
        raise APIException(f"Limit order failed: {exc}") from exc
