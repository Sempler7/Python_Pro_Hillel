"""Перевірка успадкування та методів класу"""

from typing import Type, List, Tuple
import inspect


def analyze_inheritance(cls: Type) -> None:
    """Аналізує спадкування класу та виводить усі методи,
    які він наслідує від базових класів"""
    print(f"Клас {cls.__name__} наслідує:")

    for base in cls.__bases__:
        methods: List[Tuple[str, object]] = inspect.getmembers(
            base, predicate=inspect.isfunction
        )

        for method_name, _ in methods:
            if method_name not in cls.__dict__:
                print(f"- {method_name} з {base.__name__}")


class Parent:  # pylint: disable=too-few-public-methods
    """Базовий клас для демонстрації успадкування."""

    def parent_method(self) -> None:
        """Метод батьківського класу."""


class Child(Parent):  # pylint: disable=too-few-public-methods
    """Дочірній клас, що наслідує методи Parent."""

    def child_method(self) -> None:
        """Метод дочірнього класу."""


if __name__ == "__main__":
    analyze_inheritance(Child)
