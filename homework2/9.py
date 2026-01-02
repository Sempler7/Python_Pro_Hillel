"""Програма для кешування результатів функції"""

from typing import Callable, Dict, Tuple, Any


def memoize(func: Callable) -> Callable:
    """
    Декоратор для кешування результатів виклику функції.
    Зберігає результати у словнику cache, щоб уникнути повторних обчислень.
    """
    cache: Dict[Tuple[Any, ...], Any] = {}

    def wrapper(*args: Any) -> Any:
        """
        Обгортка, яка перевіряє наявність результату у кеші.
        Якщо результат є — повертає його, інакше обчислює та додає у кеш.
        """
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def factorial(n: int) -> int:
    """
    Обчислює факторіал числа n рекурсивно.
    Використовує кешування для оптимізації.
    """
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)


@memoize
def fibonacci(n: int) -> int:
    """
    Обчислює n-те число Фібоначчі рекурсивно.
    Використовує кешування для оптимізації.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


print("Факторіал(10):", factorial(10))
print("Фібоначчі(30):", fibonacci(30))
