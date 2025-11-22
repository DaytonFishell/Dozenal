"""Tests for advanced mathematical operations."""

import pytest
import math
from dozenal.advanced_math import (
    polynomial_eval,
    trigonometric_functions,
    linear_regression,
    eigenvalues,
)


def test_polynomial_eval_simple():
    """Test polynomial evaluation with simple coefficients."""
    # 1 + 2*x + 3*x^2 at x=2 => 1 + 4 + 12 = 17
    result = polynomial_eval([1, 2, 3], 2)
    assert result["decimal"] == "17.0"
    assert result["dozenal"] == "15"


def test_polynomial_eval_zero():
    """Test polynomial evaluation at x=0."""
    # 5 + 3*x + 2*x^2 at x=0 => 5
    result = polynomial_eval([5, 3, 2], 0)
    assert result["decimal"] == "5.0"
    assert result["dozenal"] == "5"


def test_trigonometric_functions_pi_over_2():
    """Test trig functions at π/2."""
    result = trigonometric_functions(math.pi / 2, frac_precision=6)
    
    # sin(π/2) = 1
    assert float(result["sin"]["decimal"]) == pytest.approx(1.0, abs=1e-10)
    assert result["sin"]["dozenal"] == "1"
    
    # cos(π/2) ≈ 0
    assert float(result["cos"]["decimal"]) == pytest.approx(0.0, abs=1e-10)
    
    # tan(π/2) is very large
    assert abs(float(result["tan"]["decimal"])) > 1e10


def test_trigonometric_functions_zero():
    """Test trig functions at 0."""
    result = trigonometric_functions(0, frac_precision=6)
    
    # sin(0) = 0
    assert float(result["sin"]["decimal"]) == pytest.approx(0.0)
    assert result["sin"]["dozenal"] == "0"
    
    # cos(0) = 1
    assert float(result["cos"]["decimal"]) == pytest.approx(1.0)
    assert result["cos"]["dozenal"] == "1"
    
    # tan(0) = 0
    assert float(result["tan"]["decimal"]) == pytest.approx(0.0)


def test_linear_regression_perfect_fit():
    """Test linear regression with perfect linear data."""
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]  # y = 2x
    
    result = linear_regression(x, y, frac_precision=6)
    
    # Slope should be 2
    assert float(result["slope"]["decimal"]) == pytest.approx(2.0, abs=1e-10)
    assert result["slope"]["dozenal"] == "2"
    
    # Intercept should be 0
    assert float(result["intercept"]["decimal"]) == pytest.approx(0.0, abs=1e-10)
    
    # R² should be 1 (perfect fit)
    assert float(result["r_squared"]["decimal"]) == pytest.approx(1.0, abs=1e-10)


def test_linear_regression_with_intercept():
    """Test linear regression with non-zero intercept."""
    x = [1, 2, 3, 4, 5]
    y = [3, 5, 7, 9, 11]  # y = 2x + 1
    
    result = linear_regression(x, y, frac_precision=6)
    
    # Slope should be 2
    assert float(result["slope"]["decimal"]) == pytest.approx(2.0, abs=1e-10)
    
    # Intercept should be 1
    assert float(result["intercept"]["decimal"]) == pytest.approx(1.0, abs=1e-10)
    assert result["intercept"]["dozenal"] == "1"


def test_linear_regression_mismatched_lengths():
    """Test that mismatched array lengths raise ValueError."""
    x = [1, 2, 3]
    y = [2, 4]
    
    with pytest.raises(ValueError, match="same length"):
        linear_regression(x, y)


def test_eigenvalues_identity_matrix():
    """Test eigenvalues of identity matrix."""
    matrix = [[1, 0], [0, 1]]
    result = eigenvalues(matrix, frac_precision=6)
    
    # Identity matrix should have eigenvalues of 1
    evals = result["eigenvalues"]
    assert len(evals) == 2
    assert float(evals[0]["decimal"]) == pytest.approx(1.0)
    assert float(evals[1]["decimal"]) == pytest.approx(1.0)


def test_eigenvalues_2x2_matrix():
    """Test eigenvalues of a simple 2x2 matrix."""
    matrix = [[2, 1], [1, 2]]
    result = eigenvalues(matrix, frac_precision=6)
    
    evals = result["eigenvalues"]
    assert len(evals) == 2
    
    # Eigenvalues should be 3 and 1
    eigenvals_floats = sorted([float(e["decimal"]) for e in evals])
    assert eigenvals_floats[0] == pytest.approx(1.0)
    assert eigenvals_floats[1] == pytest.approx(3.0)


def test_eigenvalues_non_square_matrix():
    """Test that non-square matrix raises ValueError."""
    matrix = [[1, 2], [3, 4], [5, 6]]
    
    with pytest.raises(ValueError, match="square"):
        eigenvalues(matrix)
