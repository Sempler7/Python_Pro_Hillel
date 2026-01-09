"""Модуль містить декоратор log_methods для логування викликів методів класів.
"""

import functools
from typing import Any, Callable, Type


def log_methods(cls: Type) -> Type:
    """Декоратор для класів, який обгортає всі їхні методи
    та додає логування викликів (назва методу та аргументи).
    """

    def wrap_method(method: Callable, name: str) -> Callable:
        """Обгортка для окремого методу, яка додає логування
        """

        @functools.wraps(method)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            print(f"Logging: {name} called with {args}{', ' + str(kwargs) if kwargs else ''}")
            return method(self, *args, **kwargs)

        return wrapper

    for attr_name, attr_value in list(cls.__dict__.items()):
        if callable(attr_value):
            setattr(cls, attr_name, wrap_method(attr_value, attr_name))

    return cls


@log_methods
class MyClass:
    """Клас для демонстрації роботи декоратора log_methods.
    """

    def add(self, a: int, b: int) -> int:
        """Додає два числа.
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Віднімає друге число від першого.
        """
        return a - b


if __name__ == "__main__":
    obj = MyClass()
    obj.add(5, 3)
    obj.subtract(5, 3)
