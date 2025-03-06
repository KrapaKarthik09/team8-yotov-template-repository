"""Unit tests for the Logger component."""

from datetime import datetime
from ..logger import Logger


class TestLogger:
    """Test suite for Logger component."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.logger = Logger()

    def test_log_operation(self) -> None:
        """Test that operations are logged correctly."""
        self.logger.log_operation("add", {"a": 1, "b": 2}, 3)
        logs = self.logger.get_logs()
        
        assert len(logs) == 1
        assert logs[0].operation == "add"
        assert logs[0].parameters == {"a": 1, "b": 2}
        assert logs[0].result == 3
        assert isinstance(logs[0].timestamp, datetime)

    def test_get_logs_with_filter(self) -> None:
        """Test retrieving logs filtered by operation."""
        self.logger.log_operation("add", {"a": 1, "b": 2}, 3)
        self.logger.log_operation("subtract", {"a": 5, "b": 2}, 3)
        self.logger.log_operation("add", {"a": 3, "b": 4}, 7)
        
        # Get logs for add operations
        add_logs = self.logger.get_logs("add")
        assert len(add_logs) == 2
        assert all(log.operation == "add" for log in add_logs)
        
        # Get logs for subtract operations
        subtract_logs = self.logger.get_logs("subtract")
        assert len(subtract_logs) == 1
        assert subtract_logs[0].operation == "subtract"

    def test_clear_logs(self) -> None:
        """Test clearing all logs."""
        self.logger.log_operation("add", {"a": 1, "b": 2}, 3)
        self.logger.log_operation("subtract", {"a": 5, "b": 2}, 3)
        
        assert len(self.logger.get_logs()) == 2
        
        self.logger.clear_logs()
        assert len(self.logger.get_logs()) == 0

    def test_count_logs(self) -> None:
        """Test counting logs with and without filters."""
        self.logger.log_operation("add", {"a": 1, "b": 2}, 3)
        self.logger.log_operation("subtract", {"a": 5, "b": 2}, 3)
        self.logger.log_operation("add", {"a": 3, "b": 4}, 7)
        
        assert self.logger.count_logs() == 3
        assert self.logger.count_logs("add") == 2
        assert self.logger.count_logs("subtract") == 1
        assert self.logger.count_logs("multiply") == 0

    def test_metadata(self) -> None:
        """Test that metadata is correctly stored with log entries."""
        metadata = {"source": "unit_test", "priority": "high"}
        self.logger.log_operation(
            "add", {"a": 1, "b": 2}, 3, metadata=metadata
        )
        
        logs = self.logger.get_logs()
        assert logs[0].metadata == metadata