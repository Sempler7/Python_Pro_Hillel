"""Автоматичне логування доступу до атрибутів (опціонально)"""


class LoggingMeta(type):
    """Метаклас для автоматичного логування доступу до атрибутів екземпляра"""

    def __new__(mcs, name, bases, namespace):
        """Створює новий клас і додає методи __getattribute__ та __setattr__."""
        new_cls = super().__new__(mcs, name, bases, namespace)

        def __getattribute__(self, attr):
            """Перехоплює читання атрибутів і виводить повідомлення."""
            if attr not in {"__dict__", "__class__"}:
                print(f"Logging: accessed '{attr}'")
            return object.__getattribute__(self, attr)

        def __setattr__(self, attr, value):
            """Перехоплює зміну атрибутів і виводить повідомлення."""
            if attr not in {"__dict__", "__class__"}:
                print(f"Logging: modified '{attr}'")
            object.__setattr__(self, attr, value)

        setattr(new_cls, "__getattribute__", __getattribute__)
        setattr(new_cls, "__setattr__", __setattr__)

        return new_cls


class MyClass(metaclass=LoggingMeta):  # pylint: disable=too-few-public-methods
    """Клас для демонстрації роботи метакласу LoggingMeta."""

    def __init__(self, name: str) -> None:
        """Ініціалізує екземпляр з атрибутом name."""
        self.name = name


obj = MyClass("Python")
print(obj.name)  # Logging: accessed 'name'
obj.name = "New Python"  # Logging: modified 'name'
