"""End-to-end tests for the complete system."""

from calculator import Calculator
from logger import Logger
from notifier import Notifier, NotificationType


class TestEndToEnd:
    """End-to-end test suite for calculator, logger, and notifier integration."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.calculator = Calculator()
        self.logger = Logger()
        self.notifier = Notifier()

        # Set up thresholds for important values
        self.notifier.set_threshold("result", 100)
        self.notifier.set_threshold("error_count", 0)

    def test_calculation_with_logging_and_notification(self) -> None:
        """Test a complete flow with calculation, logging, and notification."""
        # Perform some calculations
        operations = [
            ("add", 10, 20),
            ("multiply", 5, 30),
            ("subtract", 200, 50),
            ("divide", 100, 2)
        ]

        error_count = 0

        for op_name, a, b in operations:
            try:
                # Perform the calculation
                op_method = getattr(self.calculator, op_name)
                result = op_method(a, b)

                # Log the operation
                self.logger.log_operation(op_name, {"a": a, "b": b}, result)

                # Check if result exceeds threshold
                self.notifier.check_threshold("result", result)
            except Exception as e:
                error_count += 1
                self.logger.log_operation(
                    op_name,
                    {"a": a, "b": b},
                    None,
                    metadata={"error": str(e)}
                )

        # Check if we had errors
        self.notifier.check_threshold("error_count", error_count)

        # Verify logs
        logs = self.logger.get_logs()
        assert len(logs) == 4

        # Verify operations with large results triggered thresholds
        multiply_log = logs[1]
        assert multiply_log.operation == "multiply"
        assert multiply_log.result == 150  # 5 * 30

        subtract_log = logs[2]
        assert subtract_log.operation == "subtract"
        assert subtract_log.result == 150  # 200 - 50

    def test_error_handling_with_notification(self) -> None:
        """Test error handling with notification."""
        # Try a calculation that will produce an error
        try:
            result = self.calculator.divide(10, 0)
            self.logger.log_operation("divide", {"a": 10, "b": 0}, result)
        except ZeroDivisionError as e:
            self.logger.log_operation(
                "divide",
                {"a": 10, "b": 0},
                None,
                metadata={"error": str(e)}
            )

            # Notify about the error
            self.notifier.notify(
                f"Error in calculation: {str(e)}",
                NotificationType.ERROR
            )

        # Verify the log
        logs = self.logger.get_logs()
        assert len(logs) == 1
        assert logs[0].operation == "divide"
        assert logs[0].result is None
        assert "Cannot divide by zero" in logs[0].metadata["error"]

    def test_performance_monitoring(self) -> None:
        """Test monitoring performance of calculations."""
        # Set a threshold for operation count
        self.notifier.set_threshold("operation_count", 5)

        # Perform a series of calculations
        for i in range(10):
            result = self.calculator.add(i, i)
            self.logger.log_operation("add", {"a": i, "b": i}, result)

            # Check if we've performed too many operations
            if self.logger.count_logs() > 5:
                self.notifier.check_threshold(
                    "operation_count",
                    self.logger.count_logs()
                )

        # Verify the logs
        logs = self.logger.get_logs()
        assert len(logs) == 10

        # Last operation should have a = b = 9, result = 18
        assert logs[-1].operation == "add"
        assert logs[-1].parameters == {"a": 9, "b": 9}
        assert logs[-1].result == 18
