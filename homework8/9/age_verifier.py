"""Модуль для перевірки віку користувача"""


class AgeVerifier:  # pylint: disable=too-few-public-methods
    """Клас для перевірки, чи є користувач дорослим"""

    @staticmethod
    def is_adult(age: int) -> bool:
        """Перевіряє, чи є користувач дорослим (>= 18)."""
        return age >= 18
