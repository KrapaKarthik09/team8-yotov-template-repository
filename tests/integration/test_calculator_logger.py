"""Integration tests between Calculator and Logger components."""

from calculator import Calculator
from logger import Logger


def test_calculator_with_logger():
    """Test Calculator operations being logged correctly."""
    calculator = Calculator()
    logger = Logger()
    
    # Perform operations and log them
    result = calculator.add(5, 3)
    logger.log_operation("add", {"a": 5, "b": 3}, result)
    
    result = calculator.subtract(10, 4)
    logger.log_operation("subtract", {"a": 10, "b": 4}, result)
    
    # Verify logs
    logs = logger.get_logs()
    assert len(logs) == 2
    
    add_log = logs[0]
    assert add_log.operation == "add"
    assert add_log.parameters == {"a": 5, "b": 3}
    assert add_log.result == 8
    
    subtract_log = logs[1]
    assert subtract_log.operation == "subtract"
    assert subtract_log.parameters == {"a": 10, "b": 4}
    assert subtract_log.result == 6


def test_logger_recording_calculator_errors():
    """Test Logger recording Calculator errors."""
    calculator = Calculator()
    logger = Logger()
    
    # Try a division by zero operation
    try:
        result = calculator.divide(10, 0)
    except ZeroDivisionError as e:
        logger.log_operation(
            "divide", 
            {"a": 10, "b": 0}, 
            None, 
            metadata={"error": str(e)}
        )
    
    # Verify the error was logged
    logs = logger.get_logs()
    assert len(logs) == 1
    assert logs[0].operation == "divide"
    assert logs[0].parameters == {"a": 10, "b": 0}
    assert logs[0].result is None
    assert "Cannot divide by zero" in logs[0].metadata["error"]


def test_calculator_multiple_operations_logging():
    """Test logging multiple Calculator operations."""
    calculator = Calculator()
    logger = Logger()
    
    # Perform a sequence of operations
    operations = [
        ("add", 2, 3),
        ("multiply", 4, 5),
        ("subtract", 10, 3),
        ("divide", 20, 4)
    ]
    
    for op_name, a, b in operations:
        # Dynamically call the operation method on calculator
        op_method = getattr(calculator, op_name)
        result = op_method(a, b)
        
        # Log the operation
        logger.log_operation(op_name, {"a": a, "b": b}, result)
    
    # Verify all operations were logged correctly
    logs = logger.get_logs()
    assert len(logs) == 4
    
    # Verify each operation individually
    assert logs[0].operation == "add"
    assert logs[0].result == 5
    
    assert logs[1].operation == "multiply"
    assert logs[1].result == 20
    
    assert logs[2].operation == "subtract"
    assert logs[2].result == 7
    
    assert logs[3].operation == "divide"
    assert logs[3].result == 5.0