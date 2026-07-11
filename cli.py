"""Interactive CLI for the Binance Futures Testnet trading bot."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from bot.client import create_client
from bot.exceptions import APIException, ConfigurationException, TradingBotException, ValidationException
from bot.logger import logger
from bot.orders import place_limit_order, place_market_order
from bot.validators import validate_order_type, validate_price, validate_quantity, validate_side, validate_symbol

console = Console()


def print_banner() -> None:
    """Print the application banner."""
    console.print(Panel.fit("[bold cyan]Binance Futures Testnet Trading Bot[/bold cyan]", border_style="cyan"))


def print_summary(symbol: str, side: str, order_type: str, quantity: str, price: str | None = None) -> None:
    """Print a formatted order summary."""
    table = Table(show_header=False, box=None)
    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Type", order_type)
    table.add_row("Quantity", quantity)
    if price:
        table.add_row("Price", price)
    console.print(Panel(table, title="Order Summary", border_style="green"))


def print_result(result: dict[str, Any]) -> None:
    """Render the response information returned by Binance."""
    table = Table(show_header=False, box=None)
    table.add_row("Order ID", str(result.get("order_id") or "N/A"))
    table.add_row("Status", str(result.get("status") or "N/A"))
    table.add_row("Executed Quantity", str(result.get("executed_quantity") or "N/A"))
    table.add_row("Average Price", str(result.get("avg_price") or "N/A"))
    table.add_row("Timestamp", str(result.get("timestamp") or "N/A"))
    console.print(Panel(table, title="Order Result", border_style="magenta"))


def save_last_summary(summary: dict[str, Any]) -> None:
    """Persist the latest order summary for convenience."""
    path = Path(__file__).resolve().parent / "logs" / "last_order.json"
    path.write_text(str(summary), encoding="utf-8")


def prompt_for_order_args() -> dict[str, str]:
    """Interactively collect the required order fields."""
    symbol = Prompt.ask("Symbol", default="BTCUSDT")
    side = Prompt.ask("Side (BUY/SELL)", default="BUY")
    order_type = Prompt.ask("Order Type (MARKET/LIMIT)", default="MARKET")
    quantity = Prompt.ask("Quantity", default="0.001")
    price = None
    if order_type.upper() == "LIMIT":
        price = Prompt.ask("Price")
    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price or "",
    }


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol")
    parser.add_argument("--side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", dest="order_type", choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity")
    parser.add_argument("--price")
    parser.add_argument("--menu", action="store_true", help="Use the menu-driven CLI")
    return parser


def run_order(args: dict[str, str]) -> None:
    """Validate, confirm, and place an order."""
    symbol = validate_symbol(args["symbol"])
    side = validate_side(args["side"])
    order_type = validate_order_type(args["order_type"])
    quantity = validate_quantity(args["quantity"])
    price = None
    if order_type == "LIMIT":
        price = validate_price(args["price"])

    print_summary(symbol, side, order_type, quantity, price)
    if not Confirm.ask("Place this order?", default=False):
        console.print("[yellow]Order cancelled.[/yellow]")
        return

    console.print("[bold]Submitting order...[/bold]")
    for _ in range(2):
        console.print("[dim]Processing[/dim]", end="")
        sys.stdout.flush()
        sleep(0.4)
        console.print("[dim].[/dim]", end="")
        sys.stdout.flush()
        sleep(0.4)
        console.print("[dim].[/dim]", end="")
        sys.stdout.flush()
        sleep(0.4)
        console.print("[dim].[/dim]")
        sys.stdout.flush()

    client = create_client()
    if order_type == "MARKET":
        result = place_market_order(client, symbol, side, quantity)
    else:
        result = place_limit_order(client, symbol, side, quantity, price or "")

    print_result(result)
    save_last_summary(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "quantity": quantity,
            "price": price,
            "result": result,
        }
    )


def run_menu() -> None:
    """Offer a menu-driven interface for common actions."""
    while True:
        console.print(Panel.fit("[bold]Menu[/bold]\n1. Place Market Order\n2. Place Limit Order\n3. Exit", border_style="blue"))
        choice = Prompt.ask("Choose an option", default="1")
        if choice == "1":
            args = {
                "symbol": Prompt.ask("Symbol", default="BTCUSDT"),
                "side": Prompt.ask("Side (BUY/SELL)", default="BUY"),
                "order_type": "MARKET",
                "quantity": Prompt.ask("Quantity", default="0.001"),
                "price": "",
            }
            try:
                run_order(args)
            except (TradingBotException, ValueError, Exception) as exc:
                console.print(f"[red]Error: {exc}[/red]")
                logger.error("Menu order failed: %s", exc)
        elif choice == "2":
            args = {
                "symbol": Prompt.ask("Symbol", default="BTCUSDT"),
                "side": Prompt.ask("Side (BUY/SELL)", default="BUY"),
                "order_type": "LIMIT",
                "quantity": Prompt.ask("Quantity", default="0.001"),
                "price": Prompt.ask("Price"),
            }
            try:
                run_order(args)
            except (TradingBotException, ValueError, Exception) as exc:
                console.print(f"[red]Error: {exc}[/red]")
                logger.error("Menu order failed: %s", exc)
        elif choice == "3":
            console.print("[green]Goodbye.[/green]")
            break
        else:
            console.print("[yellow]Invalid selection.[/yellow]")


def main() -> None:
    """Entry point for the CLI."""
    print_banner()
    parser = build_parser()
    args = parser.parse_args()

    if args.menu:
        run_menu()
        return

    if not any([args.symbol, args.side, args.order_type, args.quantity, args.price]):
        interactive_args = prompt_for_order_args()
        args = argparse.Namespace(**interactive_args)
    else:
        args = argparse.Namespace(
            symbol=args.symbol or "",
            side=args.side or "",
            order_type=args.order_type or "",
            quantity=args.quantity or "",
            price=args.price or "",
        )

    try:
        run_order(
            {
                "symbol": args.symbol,
                "side": args.side,
                "order_type": args.order_type,
                "quantity": args.quantity,
                "price": args.price,
            }
        )
    except (ValidationException, ConfigurationException, APIException) as exc:
        console.print(f"[red]Error: {exc}[/red]")
        logger.error("CLI error: %s", exc)
    except Exception as exc:  # pragma: no cover - defensive handling
        console.print(f"[red]Unexpected error: {exc}[/red]")
        logger.exception("Unexpected CLI error")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
