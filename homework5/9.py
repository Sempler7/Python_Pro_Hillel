"""Динамічне додавання властивостей"""

from typing import Any, Dict


class DynamicProperties:  # pylint: disable=too-few-public-methods
    """Клас для динамічного додавання властивостей під час виконання програми.
    """

    def __init__(self) -> None:
        """Ініціалізує словник для збереження значень властивостей.
        """
        self._values: Dict[str, Any] = {}
        self.name: Any

    def add_property(self, name: str, default_value: Any = None) -> None:
        """Додає нову властивість у клас під час виконання програми.
        """
        self._values[name] = default_value

        def getter(instance: "DynamicProperties") -> Any:
            # pylint: disable=protected-access
            return instance._values[name]

        def setter(instance: "DynamicProperties", value: Any) -> None:
            # pylint: disable=protected-access
            instance._values[name] = value

        setattr(self.__class__, name, property(getter, setter))


obj = DynamicProperties()
obj.add_property('name', 'default_name')

print(obj.name)
obj.name = "Python"
print(obj.name)
