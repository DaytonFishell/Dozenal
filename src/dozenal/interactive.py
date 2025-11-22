"""Interactive REPL interface for dozenal operations.

Provides a user-friendly interface for exploring dozenal math with:
- Conversion between decimal and dozenal
- Expression evaluation
- Visualization tools (multiplication tables, sequences, etc.)
- NumPy-powered advanced operations
"""

from __future__ import annotations

import sys
from decimal import Decimal
from typing import Callable

import numpy as np

from .advanced_math import polynomial_eval, trigonometric_functions, linear_regression
from .dozenal_calc import calculate
from .dozenal_decimal_converter import decimal_to_dozenal, dozenal_to_decimal

__all__ = ["run_interactive"]


def _print_banner() -> None:
    """Display welcome banner."""
    print("\n" + "=" * 60)
    print("  Welcome to the Dozenal Interactive Calculator")
    print("  Base-12 Mathematics and Conversion Tools")
    print("=" * 60)
    print("\nType 'help' for commands or 'quit' to exit.\n")


def _print_help() -> None:
    """Display help information."""
    print("\nAvailable Commands:")
    print("  convert     - Convert between decimal and dozenal")
    print("  calc        - Evaluate dozenal expressions")
    print("  table       - Display multiplication table")
    print("  sequence    - Generate number sequences")
    print("  compare     - Compare number representations")
    print("  matrix      - Matrix operations (NumPy powered)")
    print("  stats       - Statistical operations")
    print("  trig        - Trigonometric functions")
    print("  poly        - Polynomial evaluation")
    print("  regression  - Linear regression")
    print("  help        - Show this help message")
    print("  quit/exit   - Exit the interactive mode")
    print()


def _handle_convert(frac_precision: int = 12) -> None:
    """Handle interactive conversion."""
    print("\nConversion Mode")
    print("Enter 'd' for decimal->dozenal or 'z' for dozenal->decimal")
    choice = input("Choice (d/z): ").strip().lower()
    
    if choice == 'd':
        value_str = input("Enter decimal number: ").strip()
        try:
            if "." in value_str or "e" in value_str.lower():
                value = Decimal(value_str)
            else:
                value = int(value_str)
            result = decimal_to_dozenal(value, frac_precision=frac_precision)
            print(f"Decimal {value} = Dozenal {result}")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == 'z':
        value_str = input("Enter dozenal number: ").strip()
        try:
            result = dozenal_to_decimal(value_str)
            print(f"Dozenal {value_str} = Decimal {result}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice. Use 'd' or 'z'.")


def _handle_calc(frac_precision: int = 12) -> None:
    """Handle interactive calculation."""
    print("\nCalculator Mode")
    expr = input("Enter dozenal expression (e.g., '1+2*3'): ").strip()
    if not expr:
        print("No expression entered.")
        return
    
    try:
        result = calculate(expr, frac_precision=frac_precision)
        print(f"Decimal result: {result.decimal}")
        print(f"Dozenal result: {result.dozenal}")
    except Exception as e:
        print(f"Error: {e}")


def _handle_table() -> None:
    """Display multiplication table in dozenal."""
    print("\nDozenal Multiplication Table (1-12)")
    print("-" * 70)
    
    # Header
    print("   |", end="")
    for i in range(1, 13):
        doz = decimal_to_dozenal(i)
        print(f"{doz:>5}", end="")
    print()
    print("-" * 70)
    
    # Rows
    for i in range(1, 13):
        doz_i = decimal_to_dozenal(i)
        print(f"{doz_i:>3}|", end="")
        for j in range(1, 13):
            product = i * j
            doz_product = decimal_to_dozenal(product)
            print(f"{doz_product:>5}", end="")
        print()
    print()


def _handle_sequence() -> None:
    """Generate and display number sequences."""
    print("\nSequence Generator")
    print("Available sequences:")
    print("  1. Count sequence (1, 2, 3, ...)")
    print("  2. Powers of 12 (1, 12, 144, ...)")
    print("  3. Squares (1, 4, 9, ...)")
    print("  4. Cubes (1, 8, 27, ...)")
    
    choice = input("Choose sequence (1-4): ").strip()
    try:
        count = int(input("How many terms? ").strip())
        count = min(count, 20)  # Limit to 20 terms
    except ValueError:
        print("Invalid number.")
        return
    
    print("\nDecimal | Dozenal")
    print("-" * 25)
    
    if choice == "1":
        for i in range(1, count + 1):
            doz = decimal_to_dozenal(i)
            print(f"{i:7} | {doz}")
    elif choice == "2":
        for i in range(count):
            value = 12 ** i
            doz = decimal_to_dozenal(value)
            print(f"{value:7} | {doz}")
    elif choice == "3":
        for i in range(1, count + 1):
            value = i * i
            doz = decimal_to_dozenal(value)
            print(f"{value:7} | {doz}")
    elif choice == "4":
        for i in range(1, count + 1):
            value = i * i * i
            doz = decimal_to_dozenal(value)
            print(f"{value:7} | {doz}")
    else:
        print("Invalid choice.")
    print()


def _handle_compare() -> None:
    """Compare number representations across bases."""
    print("\nBase Comparison")
    value_str = input("Enter a decimal number: ").strip()
    try:
        value = int(value_str)
    except ValueError:
        print("Invalid number.")
        return
    
    print(f"\nRepresentations of {value}:")
    print(f"  Binary (base-2):  {bin(value)}")
    print(f"  Octal (base-8):   {oct(value)}")
    print(f"  Decimal (base-10): {value}")
    print(f"  Dozenal (base-12): {decimal_to_dozenal(value)}")
    print(f"  Hex (base-16):    {hex(value)}")
    print()


def _handle_matrix(frac_precision: int = 12) -> None:
    """Handle matrix operations using NumPy."""
    print("\nMatrix Operations (NumPy powered)")
    print("Available operations:")
    print("  1. Matrix addition")
    print("  2. Matrix multiplication")
    print("  3. Determinant")
    print("  4. Matrix inverse")
    
    choice = input("Choose operation (1-4): ").strip()
    
    try:
        if choice in ["1", "2"]:
            print("\nEnter first 2x2 matrix (decimal values):")
            a11 = float(input("  [0,0]: "))
            a12 = float(input("  [0,1]: "))
            a21 = float(input("  [1,0]: "))
            a22 = float(input("  [1,1]: "))
            mat1 = np.array([[a11, a12], [a21, a22]])
            
            print("\nEnter second 2x2 matrix (decimal values):")
            b11 = float(input("  [0,0]: "))
            b12 = float(input("  [0,1]: "))
            b21 = float(input("  [1,0]: "))
            b22 = float(input("  [1,1]: "))
            mat2 = np.array([[b11, b12], [b21, b22]])
            
            if choice == "1":
                result = mat1 + mat2
                print("\nResult (addition):")
            else:
                result = mat1 @ mat2
                print("\nResult (multiplication):")
            
            _print_matrix_dozenal(result, frac_precision)
            
        elif choice in ["3", "4"]:
            print("\nEnter 2x2 matrix (decimal values):")
            a11 = float(input("  [0,0]: "))
            a12 = float(input("  [0,1]: "))
            a21 = float(input("  [1,0]: "))
            a22 = float(input("  [1,1]: "))
            mat = np.array([[a11, a12], [a21, a22]])
            
            if choice == "3":
                det = np.linalg.det(mat)
                print(f"\nDeterminant (decimal): {det}")
                print(f"Determinant (dozenal): {decimal_to_dozenal(det, frac_precision=frac_precision)}")
            else:
                inv = np.linalg.inv(mat)
                print("\nInverse matrix:")
                _print_matrix_dozenal(inv, frac_precision)
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"Error: {e}")
    print()


def _print_matrix_dozenal(matrix: np.ndarray, frac_precision: int) -> None:
    """Print a matrix with both decimal and dozenal representations."""
    print("Decimal:")
    for row in matrix:
        print("  [", end="")
        for i, val in enumerate(row):
            if i > 0:
                print(", ", end="")
            print(f"{val:8.4f}", end="")
        print("]")
    
    print("Dozenal:")
    for row in matrix:
        print("  [", end="")
        for i, val in enumerate(row):
            if i > 0:
                print(", ", end="")
            doz = decimal_to_dozenal(float(val), frac_precision=frac_precision)
            print(f"{doz:>12}", end="")
        print("]")


def _handle_stats(frac_precision: int = 12) -> None:
    """Handle statistical operations using NumPy."""
    print("\nStatistical Operations (NumPy powered)")
    print("Enter numbers separated by spaces (decimal):")
    values_str = input("Numbers: ").strip()
    
    if not values_str:
        print("No values entered.")
        return
    
    try:
        values = [float(x) for x in values_str.split()]
        arr = np.array(values)
        
        mean_val = np.mean(arr)
        median_val = np.median(arr)
        std_val = np.std(arr)
        min_val = np.min(arr)
        max_val = np.max(arr)
        sum_val = np.sum(arr)
        
        print("\nStatistics:")
        print(f"  Count:      {len(values)}")
        print(f"  Sum:        {sum_val} (decimal) = {decimal_to_dozenal(sum_val, frac_precision=frac_precision)} (dozenal)")
        print(f"  Mean:       {mean_val} (decimal) = {decimal_to_dozenal(mean_val, frac_precision=frac_precision)} (dozenal)")
        print(f"  Median:     {median_val} (decimal) = {decimal_to_dozenal(median_val, frac_precision=frac_precision)} (dozenal)")
        print(f"  Std Dev:    {std_val} (decimal) = {decimal_to_dozenal(std_val, frac_precision=frac_precision)} (dozenal)")
        print(f"  Min:        {min_val} (decimal) = {decimal_to_dozenal(min_val, frac_precision=frac_precision)} (dozenal)")
        print(f"  Max:        {max_val} (decimal) = {decimal_to_dozenal(max_val, frac_precision=frac_precision)} (dozenal)")
    except Exception as e:
        print(f"Error: {e}")
    print()


def _handle_trig(frac_precision: int = 12) -> None:
    """Handle trigonometric function calculations."""
    print("\nTrigonometric Functions")
    value_str = input("Enter angle in radians (decimal): ").strip()
    
    if not value_str:
        print("No value entered.")
        return
    
    try:
        value = float(value_str)
        results = trigonometric_functions(value, frac_precision=frac_precision)
        
        print(f"\nTrigonometric values for {value} radians:")
        for func, vals in results.items():
            print(f"  {func:5} = {vals['decimal']:12} (decimal) = {vals['dozenal']:>12} (dozenal)")
    except Exception as e:
        print(f"Error: {e}")
    print()


def _handle_poly(frac_precision: int = 12) -> None:
    """Handle polynomial evaluation."""
    print("\nPolynomial Evaluation")
    print("Enter polynomial coefficients (a0 + a1*x + a2*x^2 + ...)")
    coeff_str = input("Coefficients (space-separated, decimal): ").strip()
    x_str = input("Evaluate at x (decimal): ").strip()
    
    if not coeff_str or not x_str:
        print("Missing coefficients or x value.")
        return
    
    try:
        coeffs = [float(c) for c in coeff_str.split()]
        x = float(x_str)
        result = polynomial_eval(coeffs, x, frac_precision=frac_precision)
        
        print(f"\nPolynomial result at x={x}:")
        print(f"  Decimal: {result['decimal']}")
        print(f"  Dozenal: {result['dozenal']}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def _handle_regression(frac_precision: int = 12) -> None:
    """Handle linear regression."""
    print("\nLinear Regression")
    print("Enter data points (x and y values)")
    x_str = input("X values (space-separated, decimal): ").strip()
    y_str = input("Y values (space-separated, decimal): ").strip()
    
    if not x_str or not y_str:
        print("Missing x or y values.")
        return
    
    try:
        x_vals = [float(v) for v in x_str.split()]
        y_vals = [float(v) for v in y_str.split()]
        result = linear_regression(x_vals, y_vals, frac_precision=frac_precision)
        
        print("\nLinear Regression Results:")
        print(f"  Slope:     {result['slope']['decimal']:12} (decimal) = {result['slope']['dozenal']:>12} (dozenal)")
        print(f"  Intercept: {result['intercept']['decimal']:12} (decimal) = {result['intercept']['dozenal']:>12} (dozenal)")
        print(f"  R²:        {result['r_squared']['decimal']:12} (decimal) = {result['r_squared']['dozenal']:>12} (dozenal)")
    except Exception as e:
        print(f"Error: {e}")
    print()


def run_interactive(frac_precision: int = 12) -> int:
    """Run the interactive REPL interface.
    
    Args:
        frac_precision: Fractional precision for conversions (default 12)
    
    Returns:
        Exit code (0 for success)
    """
    _print_banner()
    
    commands: dict[str, Callable[[], None]] = {
        "help": _print_help,
        "convert": lambda: _handle_convert(frac_precision),
        "calc": lambda: _handle_calc(frac_precision),
        "table": _handle_table,
        "sequence": _handle_sequence,
        "compare": _handle_compare,
        "matrix": lambda: _handle_matrix(frac_precision),
        "stats": lambda: _handle_stats(frac_precision),
        "trig": lambda: _handle_trig(frac_precision),
        "poly": lambda: _handle_poly(frac_precision),
        "regression": lambda: _handle_regression(frac_precision),
    }
    
    while True:
        try:
            command = input("dozenal> ").strip().lower()
            
            if not command:
                continue
            
            if command in ("quit", "exit", "q"):
                print("Goodbye!")
                return 0
            
            if command in commands:
                commands[command]()
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nUse 'quit' or 'exit' to leave.")
        except EOFError:
            print("\nGoodbye!")
            return 0


if __name__ == "__main__":
    sys.exit(run_interactive())
