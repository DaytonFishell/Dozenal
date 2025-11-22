"""Dozenal <-> Decimal converter utilities.

This module provides functions for converting from base-10 (decimal) numbers to
dozenal (base-12) and the reverse. By convention, the dozenal digits are:

0, 1, 2, 3, 4, 5, 6, 7, 8, 9, T (for ten), E (for eleven)

The functions handle integers and optionally fractional parts (base-10 floats)
when the user requests a particular precision for the fractional portion.

Example:
>>> decimal_to_dozenal(14)
'12'  # 1*12 + 2
>>> dozenal_to_decimal('12')
14
>>> decimal_to_dozenal(0.5, frac_precision=6)
'0.6'  # 0.5 decimal = 6/12 in dozenal
>>> dozenal_to_decimal('0.T')
10.0
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Union

__all__ = [
	"decimal_to_dozenal",
	"dozenal_to_decimal",
]

_DOZENAL_DIGITS = "0123456789TE"


def _int_to_base12(n: int) -> str:
	"""Convert a non-negative integer to base-12 digits as a string.

	Uses the characters in _DOZENAL_DIGITS with 'T' for 10 and 'E' for 11.
	"""
	if n == 0:
		return "0"
	digits: list[str] = []
	while n > 0:
		n, rem = divmod(n, 12)
		digits.append(_DOZENAL_DIGITS[rem])
	return "".join(reversed(digits))


def _int_from_base12(s: str) -> int:
	"""Convert a base-12 integer string (no sign) to decimal int.

	Raises ValueError for invalid digits.
	"""
	total: int = 0
	for ch in s:
		if ch not in _DOZENAL_DIGITS:
			raise ValueError(f"invalid dozenal digit: {ch!r}")
		total = total * 12 + _DOZENAL_DIGITS.index(ch)
	return total


def decimal_to_dozenal(value: Union[int, float, Decimal], frac_precision: int = 12) -> str:
	"""Convert a decimal value (int, float, Decimal) to a dozenal string.

	- For integers: returns a dozenal integer string with optional leading '-' for negatives.
	- For floats and Decimal: returns decimal with fractional base-12 digits up to `frac_precision`.

	Note: For fractional conversion, Decimal is used for precision.
	"""
	if isinstance(value, int):
		sign: str = "-" if value < 0 else ""
		return sign + _int_to_base12(abs(value))

	# For floats, attempt to convert to an exact rational using Fraction
	# so simple fractions like 1/12 yield exact dozenal results.
	if isinstance(value, float):
		frac: Fraction = Fraction(value).limit_denominator(10**9)
		getcontext().prec = max(28, frac_precision * 3)
		dec: Decimal = Decimal(frac.numerator) / Decimal(frac.denominator)
	else:
		# For Decimal, use it directly; set precision relative to frac_precision
		getcontext().prec = max(28, frac_precision * 3)
		dec = Decimal(value)
	sign = "-" if dec < 0 else ""
	dec = abs(dec)
	integer_part = int(dec // 1)
	frac_part: Decimal = dec - integer_part
	integer_digits: str = _int_to_base12(integer_part)
	if frac_precision <= 0 or frac_part == 0:
		return sign + integer_digits

	# Convert fractional part to base-12: multiply frac by 12 repeatedly
	digits: list[str] = []
	for _ in range(frac_precision):
		frac_part *= 12
		digit = int(frac_part // 1)
		digits.append(_DOZENAL_DIGITS[digit])
		frac_part -= digit
		if frac_part == 0:
			break
	return sign + integer_digits + "." + "".join(digits)


def dozenal_to_decimal(s: object) -> Union[int, float, Decimal]:
	"""Convert a dozenal string into a decimal value.

	The dozenal string may contain a leading '-' and an optional fractional part
	following a single decimal point.
	"""
	if not isinstance(s, str):
		raise TypeError("dozenal_to_decimal expects a string")
	s = s.strip().upper()
	if not s:
		raise ValueError("empty string")
	sign = 1
	if s[0] == "-":
		sign = -1
		s = s[1:]
	parts: list[str] = s.split(".")
	if len(parts) > 2:
		raise ValueError("invalid dozenal format: more than one decimal point")
	int_str = parts[0] or "0"
	integer_value = _int_from_base12(int_str)
	if len(parts) == 1:
		return sign * integer_value

	frac_str = parts[1]
	# Fractional conversion: sum digit*(12**-i) for i from 1
	frac_total = Decimal(0)
	power = Decimal(1)
	for ch in frac_str:
		if ch not in _DOZENAL_DIGITS:
			raise ValueError(f"invalid dozenal digit: {ch!r}")
		power *= Decimal(12)
		frac_total += Decimal(_DOZENAL_DIGITS.index(ch)) / power
	return sign * (Decimal(integer_value) + frac_total)


if __name__ == "__main__":
	# Minimal CLI for convenience
	import argparse
	parser = argparse.ArgumentParser(description="Convert between decimal and dozenal (base-12)")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--to-doz", type=str, help="Decimal number to convert to dozenal")
	group.add_argument("--to-dec", type=str, help="Dozenal number to convert to decimal")
	parser.add_argument("--frac-precision", type=int, default=12, help="Fractional precision for conversion to dozenal (default 12)")
	args = parser.parse_args()
	if args.to_doz:
		try:
			# Try to detect if it's an integer or float
			if "." in args.to_doz or "e" in args.to_doz.lower():
				val = Decimal(args.to_doz)
			else:
				val = int(args.to_doz)
			print(decimal_to_dozenal(val, frac_precision=args.frac_precision))
		except Exception as exc:
			raise SystemExit(f"error converting to dozenal: {exc}")
	else:
		try:
			print(dozenal_to_decimal(args.to_dec))
		except Exception as exc:
			raise SystemExit(f"error converting to decimal: {exc}")


