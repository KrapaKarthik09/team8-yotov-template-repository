"""Notifier component for sending alerts."""

class Notifier:
    """Sends alerts when results exceed thresholds."""

    def __init__(self, threshold: float) -> None:
        """Initialize the notifier with a threshold."""
        self.threshold = threshold

    def notify(self, result: float) -> str | None:
        """Send an alert if the result exceeds the threshold."""
        if result > self.threshold:
            return f"Alert: Result {result} exceeds threshold {self.threshold}"
        return None
