"""Custom exceptions for the trading bot."""


class TradingBotException(Exception):
    """Base exception for the trading bot."""


class ValidationException(TradingBotException):
    """Raised when user input validation fails."""


class ConfigurationException(TradingBotException):
    """Raised when application configuration is invalid."""


class APIException(TradingBotException):
    """Raised when Binance API requests fail."""
