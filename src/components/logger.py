"""Logger component for recording operations."""

class Logger:
    """Logs operations performed by components."""

    def __init__(self) -> None:
        """Initialize the logger."""
        self.logs = []

    def log(self, operation: str, result: float) -> None:
        """Log an operation and its result."""
        self.logs.append(f"{operation}: {result}")

    def get_logs(self) -> list[str]:
        """Retrieve all logged operations."""
        return self.logs
