"""Notifier module for sending alerts when values exceed thresholds."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable


class NotificationType(Enum):
    """Types of notifications that can be sent."""

    INFO = auto()
    WARNING = auto()
    ALERT = auto()
    ERROR = auto()


@runtime_checkable
class NotificationChannel(Protocol):
    """Protocol defining the interface for notification channels."""

    def send(self, message: str, notification_type: NotificationType) -> bool:
        """Send a notification.

        Args:
            message: The notification message
            notification_type: The type/severity of the notification

        Returns:
            True if the notification was sent successfully, False otherwise
        """
        ...


@dataclass
class ConsoleChannel:
    """Simple notification channel that prints messages to the console."""

    def send(self, message: str, notification_type: NotificationType) -> bool:
        """Send a notification to the console.

        Args:
            message: The notification message
            notification_type: The type/severity of the notification

        Returns:
            True, as console notifications always succeed
        """
        prefix = f"[{notification_type.name}]"
        print(f"{prefix} {message}")
        return True


@dataclass
class Threshold:
    """Represents a threshold that can trigger notifications."""

    name: str
    value: Union[int, float]
    notification_type: NotificationType = NotificationType.ALERT
    message_template: str = "{name} threshold exceeded: {actual_value} > {threshold_value}"


class Notifier:
    """Sends notifications when values exceed predefined thresholds."""

    def __init__(self, default_channel: Optional[NotificationChannel] = None) -> None:
        """Initialize a new notifier instance.

        Args:
            default_channel: The default channel to send notifications through
        """
        self._thresholds: Dict[str, Threshold] = {}
        self._channels: List[NotificationChannel] = []
        
        # Set up default console channel if none provided
        if default_channel is not None:
            self._channels.append(default_channel)
        else:
            self._channels.append(ConsoleChannel())

    def add_channel(self, channel: NotificationChannel) -> None:
        """Add a notification channel.

        Args:
            channel: The channel to add
        """
        if channel not in self._channels:
            self._channels.append(channel)

    def remove_channel(self, channel: NotificationChannel) -> None:
        """Remove a notification channel.

        Args:
            channel: The channel to remove
        """
        if channel in self._channels:
            self._channels.remove(channel)

    def set_threshold(
        self,
        name: str,
        value: Union[int, float],
        notification_type: NotificationType = NotificationType.ALERT,
        message_template: Optional[str] = None,
    ) -> None:
        """Set a named threshold that will trigger notifications.

        Args:
            name: A unique name for the threshold
            value: The threshold value
            notification_type: The type of notification to send when exceeded
            message_template: Optional custom message template
        """
        template = message_template
        if template is None:
            template = "{name} threshold exceeded: {actual_value} > {threshold_value}"
            
        self._thresholds[name] = Threshold(
            name=name,
            value=value,
            notification_type=notification_type,
            message_template=template,
        )

    def check_threshold(
        self, name: str, actual_value: Union[int, float]
    ) -> bool:
        """Check if a value exceeds a named threshold.

        Args:
            name: The name of the threshold to check
            actual_value: The value to check against the threshold

        Returns:
            True if the threshold was exceeded and notification sent, False otherwise

        Raises:
            KeyError: If no threshold with the given name exists
        """
        if name not in self._thresholds:
            raise KeyError(f"No threshold with name '{name}' exists")
            
        threshold = self._thresholds[name]
        
        if actual_value > threshold.value:
            message = threshold.message_template.format(
                name=threshold.name,
                actual_value=actual_value,
                threshold_value=threshold.value,
            )
            
            # Send through all channels
            success = False
            for channel in self._channels:
                if channel.send(message, threshold.notification_type):
                    success = True
                    
            return success
            
        return False

    def notify(
        self, 
        message: str, 
        notification_type: NotificationType = NotificationType.INFO
    ) -> bool:
        """Send a manual notification through all channels.

        Args:
            message: The notification message
            notification_type: The type of notification to send

        Returns:
            True if the notification was sent through at least one channel
        """
        success = False
        for channel in self._channels:
            if channel.send(message, notification_type):
                success = True
                
        return success
        
    def get_threshold(self, name: str) -> Union[int, float]:
        """Get a threshold value by name.
        
        Args:
            name: The name of the threshold
            
        Returns:
            The threshold value
            
        Raises:
            KeyError: If no threshold with the given name exists
        """
        if name not in self._thresholds:
            raise KeyError(f"No threshold with name '{name}' exists")
            
        return self._thresholds[name].value