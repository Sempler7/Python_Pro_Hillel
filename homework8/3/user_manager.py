"""Використання фікстур у pytest"""


class UserManager:
    """Клас для керування користувачами."""

    def __init__(self) -> None:
        self._users: dict[str, int] = {}

    def add_user(self, name: str, age: int) -> None:
        """Додає користувача з ім'ям та віком."""
        self._users[name] = age

    def remove_user(self, name: str) -> None:
        """Видаляє користувача за ім'ям."""
        if name in self._users:
            del self._users[name]

    def get_all_users(self) -> list[tuple[str, int]]:
        """Повертає список усіх користувачів у форматі (ім'я, вік)."""
        return list(self._users.items())
