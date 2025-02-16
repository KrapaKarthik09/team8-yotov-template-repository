"""Unit tests for the Calculator component."""

from src.components.calculator import Calculator

# Constants
EXPECTED_ADD_RESULT = 5
EXPECTED_SUBTRACT_RESULT = 2
EXPECTED_MULTIPLY_RESULT = 8


def test_add() -> None:
    """Test addition functionality."""
    calc = Calculator()
    assert calc.add(2, 3) == EXPECTED_ADD_RESULT


def test_subtract() -> None:
    """Test subtraction functionality."""
    calc = Calculator()
    assert calc.subtract(5, 3) == EXPECTED_SUBTRACT_RESULT


def test_multiply() -> None:
    """Test multiplication functionality."""
    calc = Calculator()
    assert calc.multiply(4, 2) == EXPECTED_MULTIPLY_RESULT
