"""Тестування з використанням doctest"""


def is_even(n: int) -> bool:
    """
    Перевіряє, чи є число парним.

    >>> is_even(2)
    True
    >>> is_even(3)
    False
    >>> is_even(0)
    True
    >>> is_even(-4)
    True
    >>> is_even(-5)
    False
    """
    return n % 2 == 0


def factorial(n: int) -> int:
    """
    Обчислює факторіал числа n (n!).
    Підтримує лише невід’ємні цілі числа.

    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    >>> factorial(6)
    720
    >>> factorial(3)
    6
    """
    if n < 0:
        raise ValueError("Факторіал визначений лише для невід’ємних чисел")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


# Запуск тестыв:  python -m doctest -v numbers.py


#  З цим блоком, команда: python numbers.py
if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
