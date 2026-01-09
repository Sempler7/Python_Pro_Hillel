"""Інтерсепція методів класу (Proxy)"""


class Proxy:  # pylint: disable=too-few-public-methods
    """Клас Proxy інтерсептує виклики методів переданого об'єкта
    та логує їх
    """

    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        """Викликається при доступі до атрибутів, яких немає у Proxy"""
        attr = getattr(self._obj, name)

        if callable(attr):
            def wrapper(*args, **kwargs):
                """Обгортка для виклику методу з логуванням"""
                print("Calling method:")
                print(f"{name} with args: {args}, kwargs: {kwargs}")
                return attr(*args, **kwargs)

            return wrapper
        return attr


class MyClass:  # pylint: disable=too-few-public-methods
    """Демонстраційний клас для перевірки роботи Proxy"""

    @staticmethod
    def greet(name):
        """Повертає привітання для заданого імені"""
        return f"Hello, {name}!"


my_obj = MyClass()
proxy = Proxy(my_obj)

print(proxy.greet("Alice"))
