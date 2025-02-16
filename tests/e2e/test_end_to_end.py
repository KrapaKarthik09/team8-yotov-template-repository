"""End-to-end test for Calculator, Logger, and Notifier integration."""

from src.components.calculator import Calculator
from src.components.logger import Logger
from src.components.notifier import Notifier


def test_end_to_end() -> None:
    """Test end-to-end functionality."""
    calculator = Calculator()
    logger = Logger()
    notifier = Notifier(threshold=10)

    result = calculator.add(5, 6)
    logger.log("add", result)
    alert = notifier.notify(result)

    assert logger.get_logs() == ["add: 11"]
    assert alert == "Alert: Result 11 exceeds threshold 10"
