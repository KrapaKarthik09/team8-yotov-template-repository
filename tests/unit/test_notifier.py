"""Unit tests for the Notifier component."""

from src.components.notifier import Notifier


def test_notifier() -> None:
    """Test notification functionality."""
    notifier = Notifier(threshold=10)
    assert notifier.notify(5) is None
    assert notifier.notify(15) == "Alert: Result 15 exceeds threshold 10"
