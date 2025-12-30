"""Програма для зберігання налаштувань користувача"""

from typing import Any, Callable, Dict, Optional

def create_user_settings() -> Callable[..., Any]:
    """
    Функція, яка створює систему зберігання налаштувань користувача за допомогою замикання та
    повертає функцію, яка може зберігати, змінювати та переглядати налаштування.
    """

    settings: Dict[str, Any] = {
        "theme": "light",
        "language": "uk",
        "notifications": True,
    }

    def settings_func(action: str, key: Optional[str] = None, value: Any = None) -> Any:
        """
        Керує налаштуваннями користувача.
        """
        if action == "get":
            if key is not None:
                return settings.get(key, None)
            return settings
        if action == "set" and key:
            settings[key] = value
            return f"Налаштування '{key}' змінено на {value}"
        return "Невірна дія або ключ"

    return settings_func


if __name__ == "__main__":
    user_settings = create_user_settings()

    print(user_settings("get"))

    print("Тема:", user_settings("get", "theme"))

    print(user_settings("set", "theme", "dark"))
    print(user_settings("set", "language", "en"))

    print(user_settings("get"))
