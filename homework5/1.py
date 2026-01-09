"""Модуль для аналізу об'єктів: визначення типів, атрибутів та їхніх значень"""


def analyze_object(obj):
    """
    Аналізує переданий об'єкт та виводить:
    1. Тип об'єкта.
    2. Список усіх методів та атрибутів.
    3. Тип кожного атрибуту.
    """
    print(f"Тип об'єкта: {type(obj)}\n")

    attributes = dir(obj)
    print("Список методів та атрибутів:")
    for attr in attributes:
        print(f" - {attr}")
    print("\n")

    print("Типи атрибутів:")
    for attr in attributes:
        try:
            value = getattr(obj, attr)
            print(f"{attr}: {type(value)}")
        except AttributeError as e:
            print(f"{attr}: неможливо отримати ({e})")


class MyClass:
    """Простий клас для демонстрації аналізу об'єктів."""

    def __init__(self, x):
        self.x = x

    @staticmethod
    def hello():
        """Повертає привітальне повідомлення."""
        return "Привіт!"


test_obj = MyClass(10)
analyze_object(test_obj)
