"""Порівняння сеттерів/геттерів, декоратора @property та дескрипторів"""

from typing import Dict, Union


#  1. Сеттери/геттери
class ProductWithGetSet:
    """
    Клас, що демонструє використання явних геттерів та сеттерів
    для доступу до приватного атрибуту _price.
    """

    def __init__(self, name: str, price: float):
        """Ініціалізація продукту з назвою та ціною"""
        self.name = name
        self._price: float = price
        self.set_price(price)

    def get_price(self) -> float:
        """Повертає поточну ціну продукту"""
        return self._price

    def set_price(self, value: float) -> None:
        """Встановлює нову ціну продукту"""
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self._price = value


#  2. Використання @property
class ProductWithProperty: # pylint: disable=too-few-public-methods
    """Клас, що демонструє використання @property
    для інкапсуляції атрибута _price.
    """

    def __init__(self, name: str, price: float):
        """Ініціалізація продукту з назвою та ціною"""
        self.name = name
        self._price: float = price
        self.price = price

    @property
    def price(self) -> float:
        """Повертає поточну ціну продукту"""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Встановлює нову ціну продукту"""
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self._price = value


#  3. Використання дескриптора
class PriceDescriptor:
    """Дескриптор для атрибута price"""

    def __init__(self):
        """Зберігаємо значення для кожного екземпляра окремо"""
        self._values: Dict[object, float] = {}

    def __get__(self, instance, owner) -> Union[float, "PriceDescriptor"]:
        """Повертає значення атрибута price для конкретного екземпляра"""
        if instance is None:
            return self
        return self._values[instance]

    def __set__(self, instance, value: float) -> None:
        """Встановлює значення атрибута price для конкретного екземпляра"""
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self._values[instance] = value


class ProductWithDescriptor: # pylint: disable=too-few-public-methods
    """Клас, що демонструє використання дескриптора для атрибута price.
    """
    price = PriceDescriptor()

    def __init__(self, name: str, price: float):
        """Ініціалізація продукту з назвою та ціною"""
        self.name = name
        self.price = price


def test_products():
    """
        Функція для демонстрації роботи трьох підходів:
        - сеттери/геттери
        - @property
        - дескриптори
        """
    print("Тестування ProductWithGetSet")
    p1 = ProductWithGetSet("Laptop", 1500)
    print("Ціна:", p1.get_price())
    p1.set_price(2000)
    print("Нова ціна:", p1.get_price())
    try:
        p1.set_price(-100)
    except ValueError as e:
        print("Помилка:", e)

    print("\nТестування ProductWithProperty")
    p2 = ProductWithProperty("Phone", 800)
    print("Ціна:", p2.price)
    p2.price = 1000
    print("Нова ціна:", p2.price)
    try:
        p2.price = -50
    except ValueError as e:
        print("Помилка:", e)

    print("\nТестування ProductWithDescriptor")
    p3 = ProductWithDescriptor("Tablet", 500)
    print("Ціна:", p3.price)
    p3.price = 700
    print("Нова ціна:", p3.price)
    try:
        p3.price = -10
    except ValueError as e:
        print("Помилка:", e)


if __name__ == "__main__":
    test_products()
