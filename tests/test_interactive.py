"""Tests for the interactive REPL interface."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from dozenal.interactive import (
    _handle_table,
    _handle_sequence,
    _handle_compare,
)


def test_handle_table_output(capsys):
    """Test that multiplication table generates expected output."""
    _handle_table()
    captured = capsys.readouterr()
    
    # Check for header
    assert "Dozenal Multiplication Table" in captured.out
    assert "1" in captured.out
    assert "T" in captured.out
    assert "E" in captured.out
    
    # Check for a known product: 12 * 12 = 144 (decimal) = 100 (dozenal)
    assert "100" in captured.out


@patch('builtins.input')
def test_handle_compare(mock_input, capsys):
    """Test number comparison across bases."""
    mock_input.return_value = "144"
    
    _handle_compare()
    captured = capsys.readouterr()
    
    assert "Binary" in captured.out
    assert "Octal" in captured.out
    assert "Decimal" in captured.out
    assert "Dozenal" in captured.out
    assert "100" in captured.out  # 144 decimal = 100 dozenal


@patch('builtins.input')
def test_handle_sequence_count(mock_input, capsys):
    """Test count sequence generation."""
    mock_input.side_effect = ["1", "5"]  # Choice 1 (count), 5 terms
    
    _handle_sequence()
    captured = capsys.readouterr()
    
    assert "Sequence Generator" in captured.out
    assert "Decimal | Dozenal" in captured.out
    # Should show 1-5 in both decimal and dozenal
    assert "1" in captured.out
    assert "5" in captured.out


@patch('builtins.input')
def test_handle_sequence_powers(mock_input, capsys):
    """Test powers of 12 sequence."""
    mock_input.side_effect = ["2", "3"]  # Choice 2 (powers of 12), 3 terms
    
    _handle_sequence()
    captured = capsys.readouterr()
    
    # Should show 1, 12, 144 (decimal) = 1, 10, 100 (dozenal)
    assert "1" in captured.out
    assert "10" in captured.out
    assert "100" in captured.out
