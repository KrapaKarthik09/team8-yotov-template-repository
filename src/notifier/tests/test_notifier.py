"""Unit tests for the Notifier component."""

from unittest.mock import MagicMock

import pytest
from notifier import Notifier, NotificationType, NotificationChannel


class MockChannel:
    """Mock notification channel for testing."""

    def __init__(self, should_succeed: bool = True) -> None:
        """Initialize mock channel.

        Args:
            should_succeed: Whether send operations should succeed
        """
        self.should_succeed = should_succeed
        self.messages = []

    def send(self, message: str, notification_type: NotificationType) -> bool:
        """Record message and return success indicator.

        Args:
            message: The notification message
            notification_type: The type/severity of the notification

        Returns:
            True if should_succeed is True, False otherwise
        """
        self.messages.append((message, notification_type))
        return self.should_succeed


class TestNotifier:
    """Test suite for Notifier component."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.mock_channel = MockChannel()
        self.notifier = Notifier(default_channel=self.mock_channel)

    def test_set_threshold(self) -> None:
        """Test setting thresholds."""
        self.notifier.set_threshold("test", 100)
        
        # Threshold not exceeded
        result = self.notifier.check_threshold("test", 50)
        assert result is False
        assert len(self.mock_channel.messages) == 0
        
        # Threshold exceeded
        result = self.notifier.check_threshold("test", 150)
        assert result is True
        assert len(self.mock_channel.messages) == 1
        assert "test threshold exceeded: 150 > 100" in self.mock_channel.messages[0][0]

    def test_custom_message_template(self) -> None:
        """Test using a custom message template."""
        custom_template = "ALERT: {actual_value} has gone above {threshold_value}!"
        self.notifier.set_threshold(
            "custom", 
            75, 
            message_template=custom_template
        )
        
        self.notifier.check_threshold("custom", 80)
        assert "ALERT: 80 has gone above 75!" in self.mock_channel.messages[0][0]

    def test_notification_types(self) -> None:
        """Test different notification types."""
        self.notifier.set_threshold(
            "info_threshold", 
            10, 
            notification_type=NotificationType.INFO
        )
        self.notifier.set_threshold(
            "warning_threshold", 
            20, 
            notification_type=NotificationType.WARNING
        )
        
        self.notifier.check_threshold("info_threshold", 15)
        assert self.mock_channel.messages[0][1] == NotificationType.INFO
        
        self.notifier.check_threshold("warning_threshold", 25)
        assert self.mock_channel.messages[1][1] == NotificationType.WARNING

    def test_multiple_channels(self) -> None:
        """Test notifications going to multiple channels."""
        second_channel = MockChannel()
        self.notifier.add_channel(second_channel)
        
        self.notifier.set_threshold("multi", 50)
        self.notifier.check_threshold("multi", 100)
        
        assert len(self.mock_channel.messages) == 1
        assert len(second_channel.messages) == 1
        assert self.mock_channel.messages[0][0] == second_channel.messages[0][0]

    def test_channel_failure(self) -> None:
        """Test handling of channel failures."""
        failing_channel = MockChannel(should_succeed=False)
        self.notifier.add_channel(failing_channel)
        
        self.notifier.set_threshold("test", 10)
        result = self.notifier.check_threshold("test", 20)
        
        # Should still be True because at least one channel succeeded
        assert result is True
        assert len(self.mock_channel.messages) == 1
        assert len(failing_channel.messages) == 1

    def test_all_channels_failing(self) -> None:
        """Test when all channels fail."""
        self.notifier = Notifier()  # Start fresh
        
        # Clear the default console channel
        self.notifier._channels.clear()
        
        failing_channel1 = MockChannel(should_succeed=False)
        failing_channel2 = MockChannel(should_succeed=False)
        
        self.notifier.add_channel(failing_channel1)
        self.notifier.add_channel(failing_channel2)
        
        self.notifier.set_threshold("test", 10)
        result = self.notifier.check_threshold("test", 20)
        
        # Should be False because all channels failed
        assert result is False

    def test_nonexistent_threshold(self) -> None:
        """Test checking a threshold that doesn't exist."""
        with pytest.raises(KeyError):
            self.notifier.check_threshold("nonexistent", 100)

    def test_manual_notification(self) -> None:
        """Test sending a manual notification."""
        result = self.notifier.notify(
            "This is a test message", 
            NotificationType.WARNING
        )
        
        assert result is True
        assert len(self.mock_channel.messages) == 1
        assert "This is a test message" in self.mock_channel.messages[0][0]
        assert self.mock_channel.messages[0][1] == NotificationType.WARNING