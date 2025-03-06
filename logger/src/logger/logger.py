"""Logger module for recording operations and their results."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


@dataclass
class LogEntry:
    """Represents a single log entry."""

    timestamp: datetime
    operation: str
    parameters: Dict[str, Any]
    result: Optional[Union[int, float, str, bool, List[Any], Dict[str, Any]]]
    metadata: Optional[Dict[str, Any]] = None


class Logger:
    """Records operations and their results for later retrieval."""

    def __init__(self) -> None:
        """Initialize a new logger instance."""
        self._logs: List[LogEntry] = []

    def log_operation(
        self,
        operation: str,
        parameters: Dict[str, Any],
        result: Optional[Union[int, float, str, bool, List[Any], Dict[str, Any]]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an operation and its result.

        Args:
            operation: The name of the operation performed
            parameters: Dictionary of parameters used in the operation
            result: The result of the operation
            metadata: Optional additional information about the operation

        """
        entry = LogEntry(
            timestamp=datetime.now(),
            operation=operation,
            parameters=parameters,
            result=result,
            metadata=metadata,
        )
        self._logs.append(entry)

    def get_logs(self, operation: Optional[str] = None) -> List[LogEntry]:
        """Retrieve logs, optionally filtered by operation.

        Args:
            operation: If provided, only logs for this operation will be returned

        Returns:
            A list of log entries matching the filter criteria

        """
        if operation is None:
            return self._logs.copy()

        return [log for log in self._logs if log.operation == operation]

    def clear_logs(self) -> None:
        """Clear all logs from the logger."""
        self._logs.clear()

    def count_logs(self, operation: Optional[str] = None) -> int:
        """Count the number of log entries, optionally filtered by operation.

        Args:
            operation: If provided, only logs for this operation will be counted

        Returns:
            The number of log entries matching the filter criteria

        """
        return len(self.get_logs(operation))
