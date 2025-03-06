"""Unit tests for the Calculator component."""

import pytest
from ..calculator import Calculator


class TestCalculator:
    """Test suite for Calculator component."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.calculator = Calculator()

    def test_add(self) -> None:
        """Test addition operation."""
        assert self.calculator.add(1, 2) == 3
        assert self.calculator.add(-1, 1) == 0
        assert self.calculator.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract(self) -> None:
        """Test subtraction operation."""
        assert self.calculator.subtract(3, 1) == 2
        assert self.calculator.subtract(1, 1) == 0
        assert self.calculator.subtract(0.3, 0.1) == pytest.approx(0.2)

    def test_multiply(self) -> None:
        """Test multiplication operation."""
        assert self.calculator.multiply(2, 3) == 6
        assert self.calculator.multiply(0, 5) == 0
        assert self.calculator.multiply(0.5, 2) == pytest.approx(1.0)

    def test_divide(self) -> None:
        """Test division operation."""
        assert self.calculator.divide(6, 2) == 3
        assert self.calculator.divide(1, 2) == 0.5
        assert self.calculator.divide(0, 5) == 0

    def test_divide_by_zero(self) -> None:
        """Test division by zero raises an exception."""
        with pytest.raises(ZeroDivisionError):
            self.calculator.divide(1, 0)