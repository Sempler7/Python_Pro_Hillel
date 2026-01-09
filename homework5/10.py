"""Метаклас для контролю створення класів"""

from typing import Dict, Type


class SingletonMeta(type):
    """
    Метаклас SingletonMeta гарантує, що клас може мати лише один екземпляр.
    """
    _instances: Dict[Type, object] = {}

    def __call__(cls, *args, **kwargs):
        """Якщо екземпляр ще не створений – створюємо його"""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):  # pylint: disable=too-few-public-methods
    """Класс-одиночка, использующий SingletonMeta.
    """

    def __init__(self):
        print("Creating instance")


obj1 = Singleton()  # Creating instance
obj2 = Singleton()  # повторний виклик, екземпляр не створюється заново
print(obj1 is obj2)
