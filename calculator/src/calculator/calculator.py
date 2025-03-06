"""Calculator module for basic arithmetic operations."""

from typing import Union

Number = Union[int, float]


class Calculator:
    """Performs basic arithmetic operations."""
    
    def add(self, a: Number, b: Number) -> Number:
        """Add two numbers.
        
        Args:
            a: First number
            b: Second number
        
        Returns:
            Sum of a and b
        """
        return a + b
    
    def subtract(self, a: Number, b: Number) -> Number:
        """Subtract b from a.
        
        Args:
            a: First number
            b: Second number
        
        Returns:
            Difference of a and b
        """
        return a - b
    
    def multiply(self, a: Number, b: Number) -> Number:
        """Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
        
        Returns:
            Product of a and b
        """
        return a * b
    
    def divide(self, a: Number, b: Number) -> Number:
        """Divide a by b.
        
        Args:
            a: First number
            b: Second number
        
        Returns:
            Quotient of a and b
        
        Raises:
            ZeroDivisionError: If b is zero
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

