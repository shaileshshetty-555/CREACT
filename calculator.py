"""Basic Python utility examples for CREACT.

This module contains beginner-friendly math helpers.
"""


def add_numbers(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract_numbers(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply_numbers(a, b):
    """Return the product of two numbers."""
    return a * b


def divide_numbers(a, b):
    """Return the division result of two numbers.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    x = 12
    y = 4

    print("Addition:", add_numbers(x, y))
    print("Subtraction:", subtract_numbers(x, y))
    print("Multiplication:", multiply_numbers(x, y))
    print("Division:", divide_numbers(x, y))
