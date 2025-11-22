from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from typing import Tuple

from .dozenal_decimal_converter import (
    _DOZENAL_DIGITS,
    decimal_to_dozenal,
    dozenal_to_decimal,
)

__all__ = ["CalculatorResult", "calculate"]

_ALLOWED_DIGITS = set(_DOZENAL_DIGITS)
_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}

Token = Tuple[str, str]
ConvertedToken = Tuple[str, Decimal | str]


@dataclass(frozen=True)
class CalculatorResult:
    decimal: Decimal
    dozenal: str


def calculate(expression: str, frac_precision: int = 12) -> CalculatorResult:
    """Evaluate a dozenal expression and return decimal + dozenal output."""
    expr = expression.strip().upper()
    if not expr:
        raise ValueError("expression is empty")
    if frac_precision < 0:
        raise ValueError("frac_precision must be non-negative")

    getcontext().prec = max(28, frac_precision * 3)
    tokens = _convert_numbers(_tokenize(expr))
    postfix = _to_postfix(tokens)
    result = _evaluate_postfix(postfix)
    dozenal_value = decimal_to_dozenal(result, frac_precision=frac_precision)
    return CalculatorResult(decimal=result, dozenal=dozenal_value)


def _tokenize(expression: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    can_start_number = True
    length = len(expression)

    while i < length:
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue

        if ch in "+-" and can_start_number:
            next_char = expression[i + 1] if i + 1 < length else ""
            if next_char == "(":
                tokens.append(("number", "0"))
                tokens.append(("operator", ch))
                i += 1
                can_start_number = True
                continue
            token, i = _parse_number(expression, i)
            tokens.append(("number", token))
            can_start_number = False
            continue

        if ch in "+-*/":
            tokens.append(("operator", ch))
            i += 1
            can_start_number = True
            continue

        if ch == "(":
            tokens.append(("lparen", ch))
            i += 1
            can_start_number = True
            continue

        if ch == ")":
            tokens.append(("rparen", ch))
            i += 1
            can_start_number = False
            continue

        if ch in _ALLOWED_DIGITS:
            token, i = _parse_number(expression, i)
            tokens.append(("number", token))
            can_start_number = False
            continue

        raise ValueError(f"unexpected character {ch!r} in expression")

    return tokens


def _parse_number(expression: str, start: int) -> Tuple[str, int]:
    i = start
    if expression[i] in "+-":
        i += 1
    digits_seen = False

    while i < len(expression) and expression[i] in _ALLOWED_DIGITS:
        digits_seen = True
        i += 1

    if i < len(expression) and expression[i] == ".":
        i += 1
        fractional_seen = False
        while i < len(expression) and expression[i] in _ALLOWED_DIGITS:
            fractional_seen = True
            i += 1
        digits_seen = digits_seen or fractional_seen

    if not digits_seen:
        raise ValueError("invalid dozenal number in expression")

    return expression[start:i], i


def _convert_numbers(tokens: list[Token]) -> list[ConvertedToken]:
    converted: list[ConvertedToken] = []
    for kind, value in tokens:
        if kind == "number":
            converted.append(("number", _dozenal_number_to_decimal(value)))
        else:
            converted.append((kind, value))
    return converted


def _dozenal_number_to_decimal(value: str) -> Decimal:
    raw = dozenal_to_decimal(value)
    if isinstance(raw, Decimal):
        return raw
    if isinstance(raw, float):
        return Decimal(str(raw))
    return Decimal(raw)


def _to_postfix(tokens: list[ConvertedToken]) -> list[ConvertedToken]:
    output: list[ConvertedToken] = []
    operators: list[Tuple[str, str]] = []

    for kind, value in tokens:
        if kind == "number":
            output.append((kind, value))
            continue

        if kind == "operator":
            assert isinstance(value, str)
            while operators and operators[-1][0] == "operator":
                top = operators[-1][1]
                if _PRECEDENCE[top] >= _PRECEDENCE[value]:
                    output.append(operators.pop())
                    continue
                break
            operators.append((kind, value))
            continue

        if kind == "lparen":
            assert isinstance(value, str)
            operators.append((kind, value))
            continue

        if kind == "rparen":
            while operators and operators[-1][0] != "lparen":
                output.append(operators.pop())
            if not operators:
                raise ValueError("mismatched parentheses")
            operators.pop()
            continue

        raise ValueError(f"unexpected token kind {kind!r}")

    while operators:
        kind, value = operators.pop()
        if kind in ("lparen", "rparen"):
            raise ValueError("mismatched parentheses")
        output.append((kind, value))

    return output


def _evaluate_postfix(postfix: list[ConvertedToken]) -> Decimal:
    stack: list[Decimal] = []

    for kind, value in postfix:
        if kind == "number":
            assert isinstance(value, Decimal)
            stack.append(value)
            continue

        if len(stack) < 2:
            raise ValueError("incomplete expression")

        right = stack.pop()
        left = stack.pop()

        assert isinstance(value, str)
        if value == "+":
            stack.append(left + right)
        elif value == "-":
            stack.append(left - right)
        elif value == "*":
            stack.append(left * right)
        elif value == "/":
            stack.append(left / right)
        else:
            raise ValueError(f"unsupported operator {value!r}")

    if len(stack) != 1:
        raise ValueError("expression did not reduce to single value")

    return stack[0]
