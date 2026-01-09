"""Автоматична генерація методів для полів класу (опціонально)"""

from typing import Any


class AutoMethodMeta(type):
    """Метаклас, який автоматично створює методи
    get_<attribute>() та set_<attribute>(value)
    для кожного атрибута класу.
    """

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        """Створює новий клас і автоматично генерує методи геттера та сеттера
        для кожного атрибута, визначеного у просторі імен класу
        """
        cls = super().__new__(mcs, name, bases, dict(namespace))

        for attr in namespace:
            if attr.startswith("__"):
                continue

            def getter(self, attr1=attr) -> Any:
                """Автоматично згенерований геттер."""
                return getattr(self, attr1)

            def setter(self, value: Any, attr1=attr) -> None:
                """Автоматично згенерований сеттер."""
                setattr(self, attr1, value)

            setattr(cls, f"get_{attr}", getter)
            setattr(cls, f"set_{attr}", setter)

        return cls


class Person(metaclass=AutoMethodMeta):  # pylint: disable=too-few-public-methods
    """
    Клас Person з автоматично згенерованими методами
    для доступу до атрибутів name та age.
    """
    name: str = "John"
    age: int = 30

    def __getattr__(self, item: str):
        """Пояснюємо mypy/pylint, що атрибути можуть бути динамічні"""
        raise AttributeError(f"{item} не існує")


if __name__ == "__main__":
    p = Person()
    print(p.get_name())
    p.set_age(31)
    print(p.get_age())
