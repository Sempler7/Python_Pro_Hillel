"""Метаклас для перевірки типів полів (опціонально)"""

from typing import get_type_hints


class TypeCheckedMeta(type):
    """
    Метаклас, який перевіряє типи атрибутів при їх встановленні.
    Якщо значення не відповідає типовому опису, виникає TypeError.
    """

    def __new__(mcs, name, bases, namespace):
        """Створює новий клас і перевизначає __setattr__ для перевірки типів."""
        cls = super().__new__(mcs, name, bases, namespace)

        cls.__type_hints__ = get_type_hints(cls)

        def __setattr__(self, key, value):
            """Перевіряє тип значення перед встановленням атрибута."""
            expected_types = self.__class__.__type_hints__
            if key in expected_types:
                expected_type = expected_types[key]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Для атрибута '{key}' очікується тип "
                        f"'{expected_type.__name__}', але отримано '{type(value).__name__}'."
                    )
            super().__setattr__(key, value)

        cls.__setattr__ = __setattr__
        return cls


class Person(metaclass=TypeCheckedMeta):  # pylint: disable=too-few-public-methods
    """Клас для прикладу: має атрибути name (str) та age (int).
    """
    name: str = ""
    age: int = 0


p = Person()
p.name = "John"
p.age = 30
p.age = "30"
