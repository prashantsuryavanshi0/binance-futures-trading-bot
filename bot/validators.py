"""Input validation helpers for order parameters."""

from decimal import Decimal, InvalidOperation
import re

from .constants import SUPPORTED_ORDER_TYPES, SUPPORTED_SIDES
from .exceptions import ValidationException


def validate_symbol(symbol: str) -> str:
    """Validate and normalize a Binance futures symbol."""
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValidationException("Symbol is required.")

    normalized = symbol.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]+", normalized):
        raise ValidationException("Invalid symbol. Use a valid Binance futures symbol such as BTCUSDT.")
    if len(normalized) < 2:
        raise ValidationException("Symbol is too short.")
    return normalized


def validate_quantity(quantity: str | int | float) -> str:
    """Validate and format a quantity value."""
    try:
        value = Decimal(str(quantity))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationException("Invalid quantity. Provide a positive decimal number.") from exc

    if value <= 0:
        raise ValidationException("Quantity must be greater than zero.")
    return format(value, "f")


def validate_price(price: str | int | float) -> str:
    """Validate and format a price value."""
    try:
        value = Decimal(str(price))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationException("Invalid price. Provide a positive decimal number.") from exc

    if value <= 0:
        raise ValidationException("Price must be greater than zero.")
    return format(value, "f")


def validate_order_type(order_type: str) -> str:
    """Validate an order type."""
    normalized = (order_type or "").strip().upper()
    if normalized not in SUPPORTED_ORDER_TYPES:
        raise ValidationException("Order type must be MARKET or LIMIT.")
    return normalized


def validate_side(side: str) -> str:
    """Validate a trade side."""
    normalized = (side or "").strip().upper()
    if normalized not in SUPPORTED_SIDES:
        raise ValidationException("Side must be BUY or SELL.")
    return normalized
