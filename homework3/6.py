"""Access-like"""

import re

class User:
    """Клас User, що моделює запис користувача з перевіркою формату email"""
    def __init__(self, first_name: str, last_name: str, email: str):
        """Ініціалізує новий об'єкт користувача"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @property
    def first_name(self) -> str:
        """Повертає ім'я користувача"""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """Встановлює ім'я користувача"""
        self._first_name = value

    @property
    def last_name(self) -> str:
        """Повертає прізвище користувача"""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """Встановлює прізвище користувача"""
        self._last_name = value

    @property
    def email(self) -> str:
        """Повертає email користувача"""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Встановлює email користувача з перевіркою формату"""
        if not self.is_valid_email(value):
            raise ValueError("Некорректный формат email")
        self._email = value

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Перевіряє правильність формату email за допомогою регулярного виразу"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def __str__(self) -> str:
        """Повертає рядкове представлення об'єкта"""
        return f"""[
        '{self.first_name}',
        '{self.last_name}',
        '{self.email}'
    ]"""


user = User("John", "Smith", "John@example.com")

print(user.first_name)
print(user.last_name)
print(user.email)

user.first_name = "Vit"
user.last_name = "Erenkov"
user.email = "vit@domain.com"

print(user)

user.email = "new@mail.com"
user.email = "wrong-email"
