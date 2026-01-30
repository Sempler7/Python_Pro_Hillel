"""Модульне тестування з використанням unittest"""


class StringProcessor:
    """Клас для обробки рядків."""

    @staticmethod
    def reverse_string(s: str) -> str:
        """Повертає перевернутий рядок."""
        return s[::-1]

    @staticmethod
    def capitalize_string(s: str) -> str:
        """Робить першу літеру рядка великою."""
        if not s:
            return s
        return s[0].upper() + s[1:]

    @staticmethod
    def count_vowels(s: str) -> int:
        """Повертає кількість голосних у рядку."""
        vowels = "aeiouAEIOU"
        return sum(1 for char in s if char in vowels)
