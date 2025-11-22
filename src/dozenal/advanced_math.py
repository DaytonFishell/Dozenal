"""Advanced mathematical operations using NumPy for dozenal calculations.

This module provides additional mathematical functionality including:
- Polynomial operations
- Trigonometric functions
- Advanced statistical functions
- Linear algebra operations
"""

from __future__ import annotations

from decimal import Decimal
from typing import List

import numpy as np

from .dozenal_decimal_converter import decimal_to_dozenal, dozenal_to_decimal

__all__ = [
    "polynomial_eval",
    "trigonometric_functions",
    "linear_regression",
    "eigenvalues",
]


def polynomial_eval(coefficients: List[float], x: float, frac_precision: int = 12) -> dict[str, str]:
    """Evaluate a polynomial at a given point.
    
    Args:
        coefficients: List of polynomial coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ...
        x: Point at which to evaluate
        frac_precision: Fractional precision for dozenal conversion
    
    Returns:
        Dictionary with decimal and dozenal results
    """
    poly = np.poly1d(coefficients[::-1])  # poly1d expects highest degree first
    result = float(poly(x))
    
    return {
        "decimal": str(result),
        "dozenal": decimal_to_dozenal(result, frac_precision=frac_precision)
    }


def trigonometric_functions(value: float, frac_precision: int = 12) -> dict[str, dict[str, str]]:
    """Calculate trigonometric functions for a value (in radians).
    
    Args:
        value: Input value in radians
        frac_precision: Fractional precision for dozenal conversion
    
    Returns:
        Dictionary of trigonometric function results in decimal and dozenal
    """
    results = {
        "sin": float(np.sin(value)),
        "cos": float(np.cos(value)),
        "tan": float(np.tan(value)),
    }
    
    return {
        func: {
            "decimal": str(val),
            "dozenal": decimal_to_dozenal(val, frac_precision=frac_precision)
        }
        for func, val in results.items()
    }


def linear_regression(x_values: List[float], y_values: List[float], frac_precision: int = 12) -> dict[str, dict[str, str]]:
    """Perform linear regression on data points.
    
    Args:
        x_values: List of x coordinates
        y_values: List of y coordinates
        frac_precision: Fractional precision for dozenal conversion
    
    Returns:
        Dictionary with slope and intercept in decimal and dozenal
    """
    if len(x_values) != len(y_values):
        raise ValueError("x and y must have the same length")
    
    x_arr = np.array(x_values)
    y_arr = np.array(y_values)
    
    # Calculate slope and intercept
    coeffs = np.polyfit(x_arr, y_arr, 1)
    slope = float(coeffs[0])
    intercept = float(coeffs[1])
    
    # Calculate R-squared
    y_pred = slope * x_arr + intercept
    ss_res = np.sum((y_arr - y_pred) ** 2)
    ss_tot = np.sum((y_arr - np.mean(y_arr)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return {
        "slope": {
            "decimal": str(slope),
            "dozenal": decimal_to_dozenal(slope, frac_precision=frac_precision)
        },
        "intercept": {
            "decimal": str(intercept),
            "dozenal": decimal_to_dozenal(intercept, frac_precision=frac_precision)
        },
        "r_squared": {
            "decimal": str(r_squared),
            "dozenal": decimal_to_dozenal(r_squared, frac_precision=frac_precision)
        }
    }


def eigenvalues(matrix: List[List[float]], frac_precision: int = 12) -> dict[str, List[dict[str, str]]]:
    """Calculate eigenvalues of a square matrix.
    
    Args:
        matrix: Square matrix as list of lists
        frac_precision: Fractional precision for dozenal conversion
    
    Returns:
        Dictionary with eigenvalues and eigenvectors
    """
    mat = np.array(matrix)
    
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("Matrix must be square")
    
    eigenvals, eigenvecs = np.linalg.eig(mat)
    
    return {
        "eigenvalues": [
            {
                "decimal": str(float(val.real)),
                "dozenal": decimal_to_dozenal(float(val.real), frac_precision=frac_precision)
            }
            for val in eigenvals
        ]
    }


def compute_fft(values: List[float], frac_precision: int = 12) -> dict[str, List[dict[str, str]]]:
    """Compute Fast Fourier Transform of a sequence.
    
    Args:
        values: List of values to transform
        frac_precision: Fractional precision for dozenal conversion
    
    Returns:
        Dictionary with FFT magnitudes
    """
    arr = np.array(values)
    fft_result = np.fft.fft(arr)
    magnitudes = np.abs(fft_result)
    
    return {
        "magnitudes": [
            {
                "decimal": str(float(mag)),
                "dozenal": decimal_to_dozenal(float(mag), frac_precision=frac_precision)
            }
            for mag in magnitudes
        ]
    }
