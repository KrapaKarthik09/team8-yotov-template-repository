"""Tests for calculator module."""

import pytest
from .calculator import add, subtract, multiply, divide, square

def test_add():
    """Test add function."""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0

def test_subtract():
    """Test subtract function."""
    assert subtract(3, 2) == 1
    assert subtract(5, 5) == 0

def test_multiply():
    """Test multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(5, 0) == 0

def test_divide():
    """Test divide function."""
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    
    with pytest.raises(ValueError):
        divide(1, 0)

def test_square():
    """Test square function."""
    assert square(2) == 4
    assert square(-3) == 9

# Note: No test for cube function, which will show up as uncovered
