import pytest
from decimal import Decimal

from dozenal.dozenal_decimal_converter import (
    decimal_to_dozenal,
    dozenal_to_decimal,
)


def test_integer_roundtrips():
    cases = [0, 1, 5, 9, 10, 11, 12, 23, 144, -1, -14]
    for n in cases:
        s = decimal_to_dozenal(n)
        # convert back
        val = dozenal_to_decimal(s)
        assert isinstance(val, (int, Decimal))
        # For negative numbers, Decimal may be used; compare as int
        assert int(val) == int(n)


def test_fractional_conversion():
    # 0.5 decimal is 6/12 = 0.6 in dozenal
    assert decimal_to_dozenal(0.5, frac_precision=6) == "0.6"
    # 0.25 decimal is 3/12 = 0.3
    assert decimal_to_dozenal(0.25, frac_precision=6) == "0.3"
    # 1/12 decimal is 0.1 in dozenal
    assert decimal_to_dozenal(1/12, frac_precision=6) == "0.1"


def test_dozenal_to_decimal_fractions():
    assert float(dozenal_to_decimal("0.6")) == pytest.approx(0.5)
    assert float(dozenal_to_decimal("0.3")) == pytest.approx(0.25)
    # T is 10 (decimal) -> 10.0
    assert float(dozenal_to_decimal("T")) == pytest.approx(10.0)
    assert float(dozenal_to_decimal("E")) == pytest.approx(11.0)


def test_invalid_strings():
    with pytest.raises(ValueError):
        dozenal_to_decimal("G")
    with pytest.raises(ValueError):
        dozenal_to_decimal("1.2.3")


def test_negative_values():
    assert decimal_to_dozenal(-14) == "-12"
    assert int(dozenal_to_decimal("-12")) == -14
