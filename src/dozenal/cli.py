from __future__ import annotations

import argparse
from collections.abc import Sequence
from decimal import Decimal
from typing import Mapping

from .dozenal_decimal_converter import decimal_to_dozenal, dozenal_to_decimal

_TOOLS: Mapping[str, str] = {
    "converter": "Dozenal decimal converter (src/dozenal/dozenal_decimal_converter.py)",
}


def _parse_decimal_source(source: str) -> int | Decimal:
    normalized = source.strip()
    if not normalized:
        raise ValueError("empty decimal value")
    if "." in normalized or "e" in normalized.lower():
        return Decimal(normalized)
    return int(normalized)


def _print_tools() -> None:
    print("Available dozenal tools:")
    for name, description in _TOOLS.items():
        print(f"  {name}: {description}")


def _run_converter(args: argparse.Namespace) -> int:
    if args.to_doz:
        try:
            value = _parse_decimal_source(args.to_doz)
        except Exception as exc:  # pragma: no cover - argparse will short-circuit invalid input
            raise SystemExit(f"invalid decimal input {args.to_doz!r}: {exc}") from exc
        print(decimal_to_dozenal(value, frac_precision=args.frac_precision))
        return 0

    print(dozenal_to_decimal(args.to_dec))
    return 0


def run_cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dozenal",
        description="Dozenal utilities (converter, future tools).",
    )
    parser.add_argument(
        "--tool",
        "-t",
        choices=list(_TOOLS),
        default="converter",
        help="Choose which tool to run (default: %(default)s).",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List available tools and exit.",
    )

    converter_group = parser.add_argument_group("dozenal_decimal_converter options")
    exclusive = converter_group.add_mutually_exclusive_group()
    exclusive.add_argument("--to-doz", type=str, help="Convert the given decimal value to dozenal.")
    exclusive.add_argument("--to-dec", type=str, help="Convert the given dozenal value to decimal.")
    parser.add_argument(
        "--frac-precision",
        type=int,
        default=12,
        help="Fractional precision when converting decimals to dozenal (default 12).",
    )

    args = parser.parse_args(argv)

    if args.list_tools:
        _print_tools()
        return 0

    if args.tool == "converter":
        if not args.to_doz and not args.to_dec:
            parser.error("--tool converter requires --to-doz or --to-dec")
        return _run_converter(args)

    _print_tools()
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
