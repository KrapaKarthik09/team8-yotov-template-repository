"""Unit tests for the Logger component."""

from src.components.logger import Logger


def test_logger() -> None:
    """Test logging functionality."""
    logger = Logger()
    logger.log("add", 5)
    assert logger.get_logs() == ["add: 5"]
