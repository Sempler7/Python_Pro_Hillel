"""
Модуль для демонстрації динамічного створення класів у Python.
"""

from typing import Callable, Dict, Type, Any


def create_class(class_name: str, methods: Dict[str, Callable]) -> Type[object]:
    """
    Створює клас динамічно з заданим ім'ям та методами.

    Args:
        class_name (str): Назва класу.
        methods (dict[str, Callable]): Словник {назва_методу: функція}.

    Returns:
        type: Новий клас.
    """
    return type(class_name, (object,), methods)


def greet(_self: object, name: str) -> str:
    """Повертає привітання з ім'ям."""
    return f"Привіт, {name}!"


def square(_self: object, x: int) -> str:
    """Обчислює квадрат числа."""
    return f"Квадрат числа {x} дорівнює {x ** 2}"


def is_even(_self: object, x: int) -> str:
    """Перевіряє, чи є число парним."""
    return f"Число {x} парне" if x % 2 == 0 else f"Число {x} непарне"


all_methods: Dict[str, Callable] = {
    "greet": greet,
    "square": square,
    "is_even": is_even
}

MathHelper = create_class("MathHelper", all_methods)

if __name__ == "__main__":
    obj: Any = MathHelper()

    print(obj.greet("Віталій"), obj.square(7), obj.is_even(10), obj.is_even(13), sep="\n")
