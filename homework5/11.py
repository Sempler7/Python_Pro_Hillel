"""Метаклас для обмеження кількості атрибутів (опціонально)"""

from __future__ import annotations
from typing import Any, Dict, Tuple


def _is_data_attribute(name: str, value: Any) -> bool:
    """Визначає, чи є елемент словника класу «даним» атрибутом, який слід рахувати"""
    if name.startswith("__") and name.endswith("__"):
        return False
    if isinstance(value, (staticmethod, classmethod, property)):
        return False
    if callable(value):
        return False
    return True


def _count_data_attributes(namespace: Dict[str, Any]) -> int:
    """Підраховує кількість «даних» атрибутів у словнику класу"""
    return sum(1 for k, v in namespace.items() if _is_data_attribute(k, v))


class LimitedAttributesMeta(type):
    """Метаклас, який обмежує кількість «даних» атрибутів у класі"""
    DEFAULT_MAX: int = 3

    def __new__(
        mcs: type["LimitedAttributesMeta"],
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        """Створює новий клас і перевіряє кількість атрибутів у його просторі імен"""
        raw_value = namespace.get("__max_class_attrs__", LimitedAttributesMeta.DEFAULT_MAX)
        if not isinstance(raw_value, int):
            raise TypeError("__max_class_attrs__ має бути цілим числом")
        max_attrs: int = raw_value

        data_attr_count = _count_data_attributes(namespace)
        if data_attr_count > max_attrs:
            raise TypeError(
                f"Клас {name} не може мати більше {max_attrs} атрибутів."
            )

        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls.__max_class_attrs__ = max_attrs
        cls.__current_data_attr_count__ = data_attr_count
        return cls

    def __setattr__(cls, key: str, value: Any) -> None:
        """Перевизначає встановлення атрибутів на рівні класу, щоб не перевищити ліміт"""
        if key in {"__max_class_attrs__", "__current_data_attr_count__"}:
            super().__setattr__(key, value)
            return

        counts_as_data = _is_data_attribute(key, value)
        exists = hasattr(cls, key)

        if counts_as_data and not exists:
            current = getattr(cls, "__current_data_attr_count__", 0)
            max_attrs = getattr(cls, "__max_class_attrs__", LimitedAttributesMeta.DEFAULT_MAX)
            if current + 1 > max_attrs:
                raise TypeError(
                    f"Клас {cls.__name__} не може мати більше {max_attrs} атрибутів."
                )
            super().__setattr__(key, value)
            super().__setattr__("__current_data_attr_count__", current + 1)
        else:
            super().__setattr__(key, value)


class LimitedClass(metaclass=LimitedAttributesMeta):  # pylint: disable=too-few-public-methods
    """Клас з обмеженою кількістю атрибутів"""
    # __max_class_attrs__ = 3  # Необов'язково: перевизначення ліміту (за замовчуванням 3)
    attr1 = 1
    attr2 = 2
    attr3 = 3
    attr4 = 4


obj = LimitedClass()
