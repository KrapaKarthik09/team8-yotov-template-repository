"""Integration tests for Calculator and Logger components."""

from src.components.calculator.calculator import Calculator
from src.components.logger import Logger


def test_calculator_logger_integration() -> None:
    """Test integration between Calculator and Logger."""
    calculator = Calculator()
    logger = Logger()

    result = calculator.add(3, 5)
    logger.log("add", result)

    assert logger.get_logs() == ["add: 8"]
