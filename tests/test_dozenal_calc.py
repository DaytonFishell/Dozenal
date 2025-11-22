import pytest
from decimal import Decimal

from dozenal.dozenal_calc import calculate


@pytest.mark.parametrize(
    "expr,decimal_expected,dozenal_expected",
    [
        ("1+2", Decimal(3), "3"),
        ("1+2*3", Decimal(7), "7"),
        ("(1+2)*3", Decimal(9), "9"),
        ("-T+2", Decimal(-8), "-8"),
        ("E/2", Decimal("5.5"), "5.6"),
    ],
)
def test_basic_calculator(expr: str, decimal_expected: Decimal, dozenal_expected: str) -> None:
    result = calculate(expr)
    assert result.decimal == decimal_expected
    assert result.dozenal == dozenal_expected


def test_unary_minus_before_parentheses() -> None:
    result = calculate("-(1+1)")
    assert result.decimal == Decimal(-2)
    assert result.dozenal == "-2"


def test_fractional_precision_controls_output() -> None:
    result = calculate("0.6+0.6", frac_precision=2)
    assert result.decimal == Decimal(1)
    assert result.dozenal == "1"


def test_invalid_expression_raises() -> None:
    with pytest.raises(ValueError):
        calculate("1++2")


def test_mismatched_parentheses() -> None:
    with pytest.raises(ValueError):
        calculate("(1+2")
