"""Модуль для демонстрації динамічної модифікації атрибутів об'єкта.
"""

from typing import Any


class MutableClass:
    """Клас, що дозволяє динамічно додавати та видаляти атрибути"""

    def add_attribute(self, name: str, value: Any) -> None:
        """Додає новий атрибут до об'єкта"""
        setattr(self, name, value)

    def remove_attribute(self, name: str) -> None:
        """Видаляє атрибут з об'єкта"""
        if hasattr(self, name):
            delattr(self, name)
        else:
            raise AttributeError(f"Атрибут '{name}' не існує")


if __name__ == "__main__":
    obj: Any = MutableClass()

    obj.add_attribute("name", "Python")
    print(obj.name)  # pylint: disable=no-member

    obj.remove_attribute("name")
    print(obj.name)  # pylint: disable=no-member
