"""Integration tests between Logger and Notifier components."""


from logger import Logger
from notifier import Notifier, NotificationType

class LogMonitoringChannel:
    """Notification channel that monitors logs and sends alerts."""
    
    def __init__(self, operation: str, threshold: int) -> None:
        """Initialize monitor for specific operation type and threshold.
        
        Args:
            operation: The operation to monitor
            threshold: The threshold for number of operations
        """
        self.operation = operation
        self.threshold = threshold
        self.alerts_sent = []
    
    def send(self, message: str, notification_type: NotificationType) -> bool:
        """Send a notification and record it.
        
        Args:
            message: The notification message
            notification_type: The type/severity of the notification
            
        Returns:
            True, indicating successful delivery
        """
        self.alerts_sent.append((message, notification_type))
        return True


def test_notifier_monitoring_logger():
    """Test Notifier monitoring Logger activity."""
    logger = Logger()
    notifier = Notifier()
    
    # Set up a monitoring channel for 'add' operations
    monitor = LogMonitoringChannel("add", 3)
    notifier.add_channel(monitor)
    
    # Set threshold for number of 'add' operations
    notifier.set_threshold(
        "add_operations",
        3,
        notification_type=NotificationType.WARNING
    )
    
    # Log some operations
    for i in range(5):
        logger.log_operation("add", {"a": i, "b": 1}, i + 1)
        
        # Check if we've exceeded the threshold
        if logger.count_logs("add") > 3:
            notifier.notify(
                f"Too many add operations: {logger.count_logs('add')}",
                NotificationType.WARNING
            )
    
    # Verify notification was sent
    assert len(monitor.alerts_sent) == 2
    assert "Too many add operations: 4" in monitor.alerts_sent[0][0]
    assert monitor.alerts_sent[0][1] == NotificationType.WARNING


def test_logger_recording_notifications():
    """Test Logger recording Notifier activities."""
    logger = Logger()
    notifier = Notifier()
    
    # Add some thresholds
    notifier.set_threshold("cpu_usage", 80)
    notifier.set_threshold("memory_usage", 90)
    
    # Check thresholds and log the results
    cpu_result = notifier.check_threshold("cpu_usage", 85)
    logger.log_operation(
        "check_threshold",
        {"name": "cpu_usage", "value": 85},
        cpu_result,
        metadata={"threshold": 80}
    )
    
    memory_result = notifier.check_threshold("memory_usage", 75)
    logger.log_operation(
        "check_threshold",
        {"name": "memory_usage", "value": 75},
        memory_result,
        metadata={"threshold": 90}
    )
    
    # Verify logs
    logs = logger.get_logs()
    assert len(logs) == 2
    
    # CPU usage should have exceeded threshold
    assert logs[0].operation == "check_threshold"
    assert logs[0].result is True
    assert logs[0].parameters["name"] == "cpu_usage"
    assert logs[0].parameters["value"] == 85
    
    # Memory usage should not have exceeded threshold
    assert logs[1].operation == "check_threshold"
    assert logs[1].result is False
    assert logs[1].parameters["name"] == "memory_usage"
    assert logs[1].parameters["value"] == 75


def test_notification_through_log_thresholds():
    """Test setting up notifications based on log patterns."""
    logger = Logger()
    notifier = Notifier()
    
    # Log various operations
    for i in range(10):
        if i % 2 == 0:
            logger.log_operation("even_op", {"value": i}, i)
        else:
            logger.log_operation("odd_op", {"value": i}, i)

    # Force an imbalance by adding one more even operation
    logger.log_operation("even_op", {"value": 10}, 10)

    even_count = logger.count_logs("even_op")
    odd_count = logger.count_logs("odd_op")
    
    # Check if we have too many of one type of log
    even_count = logger.count_logs("even_op")
    odd_count = logger.count_logs("odd_op")
    
    # Set up a threshold for imbalanced operations
    imbalance = abs(even_count - odd_count)
    notifier.set_threshold("log_imbalance", 0)
    
    # Check if logs are imbalanced
    result = notifier.check_threshold("log_imbalance", imbalance)
    
    # Should have triggered a notification
    assert result is True