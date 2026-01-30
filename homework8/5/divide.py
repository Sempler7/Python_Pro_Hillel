"""Тестування винятків у pytest"""


def divide(a: int, b: int) -> float:
    """
    Ділить два числа. Якщо знаменник дорівнює нулю,
    викидає виняток ZeroDivisionError
    """
    if b == 0:
        raise ZeroDivisionError("Знаменник не може бути нулем")
    return a / b
