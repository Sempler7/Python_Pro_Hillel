"""Vector class implementation"""

from math import sqrt
from functools import total_ordering

@total_ordering
class Vector:
    """Клас, що представляє математичний вектор у n-вимірному просторі"""
    def __init__(self, *coords):
        """Ініціалізує вектор із заданими координатами"""
        self.coords = tuple(coords)
        self.n = len(coords)

    def __repr__(self):
        """Повертає рядкове представлення вектора"""
        return f"Vector{self.coords}"

    def __add__(self, other):
        """Додає два вектори однакової розмірності"""
        if self.n != other.n:
            raise ValueError("Вектори повинні мати однакову розмірність")
        return Vector(*(a + b for a, b in zip(self.coords, other.coords)))

    def __sub__(self, other):
        """Віднімає інший вектор від поточного"""
        if self.n != other.n:
            raise ValueError("Вектори повинні мати однакову розмірність")
        return Vector(*(a - b for a, b in zip(self.coords, other.coords)))

    def __mul__(self, other):
        """Виконує множення: скалярне або на число"""
        if isinstance(other, Vector):
            if self.n != other.n:
                raise ValueError("Вектори повинні мати однакову розмірність")
            return sum(a * b for a, b in zip(self.coords, other.coords))
        return Vector(*(a * other for a in self.coords))

    def length(self):
        """Обчислює довжину вектора"""
        return sqrt(sum(a * a for a in self.coords))

    def __eq__(self, other):
        """Перевіряє рівність двох векторів за їх довжиною"""
        return self.length() == other.length()

    def __lt__(self, other):
        """Порівнює два вектори за довжиною"""
        return self.length() < other.length()


v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)

print(v1 + v2)
print(v2 - v1)
print(v1 * v2)
print(v1 * 2)

print(v1.length())
print(v2.length())

print(v1 < v2)
print(v1 == v2)
