"""Динамічний виклик функцій"""

from typing import Any


def call_function(obj: Any, method_name: str, *args: Any) -> Any:
    """Викликає метод об'єкта за його назвою"""
    method = getattr(obj, method_name)
    return method(*args)


class TextProcessor:
    """Клас для обробки тексту, який надає базові методи роботи з рядками.
    """

    def upper(self, text: str) -> str:
        """Перетворює рядок у верхній регістр"""
        return text.upper()

    def repeat(self, text: str, times: int) -> str:
        """Повторює рядок задану кількість разів"""
        return text * times

    def replace(self, text: str, old: str, new: str) -> str:
        """Замінює підрядок у рядку на новий"""
        return text.replace(old, new)


tp = TextProcessor()

print(call_function(tp, "upper", "hello"))
print(call_function(tp, "repeat", "Python ", 3))
print(call_function(tp, "replace", "I like Java", "Java", "Python"))
