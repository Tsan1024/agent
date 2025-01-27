import inspect

from swarm.util import function_to_json


def add(a: int, b: int = 5) -> int:
    """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int, optional): The second number. Defaults to 5.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

result = function_to_json(add)
print(result)
