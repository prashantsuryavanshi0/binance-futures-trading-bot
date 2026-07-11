# Binance Futures Testnet Trading Bot

## Project Overview

This project provides a production-quality Python application for placing market and limit orders on Binance Futures Testnet (USDT-M) using the official `python-binance` library. It includes a clean CLI, reusable modules, robust validation, custom exceptions, structured logging, and environment-based configuration.

## Features

- Connect to Binance Futures Testnet
- Place MARKET and LIMIT orders
- Support BUY and SELL orders
- Interactive and menu-driven CLI
- Colored terminal output with Rich
- Meaningful validation and error handling
- Logging to `logs/bot.log`
- Environment-based configuration with `.env`

## Folder Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── constants.py
│   ├── validators.py
│   ├── orders.py
│   ├── logger.py
│   └── exceptions.py
├── logs/
├── cli.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Create Binance Testnet Account

1. Sign up for a Binance Futures Testnet account.
2. Create API keys for the testnet environment.
3. Keep the API key and secret secure.

## How to Configure `.env`

Copy the example file and fill in your credentials:

```bash
copy .env.example .env
```

Then update `.env`:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret_key
```

## Run the Project

Start the CLI:

```bash
python cli.py
```

## Example MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## Example LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

## Screenshots Placeholder

![Screenshots Placeholder](https://via.placeholder.com/800x400)

## Future Improvements

- Add retry logic for temporary network failures
- Support more order types and parameters
- Persist order history in a database
- Add unit tests
