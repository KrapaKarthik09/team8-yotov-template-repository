"""Python template repository with multiple components."""

# Re-export components for easier imports
from calculator import Calculator
from logger import Logger, LogEntry
from notifier import Notifier, NotificationType, NotificationChannel, ConsoleChannel

__all__ = [
    "Calculator",
    "Logger",
    "LogEntry",
    "Notifier",
    "NotificationType",
    "NotificationChannel",
    "ConsoleChannel",
]