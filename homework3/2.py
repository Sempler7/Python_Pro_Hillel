"""Numeric-like"""

import math
from functools import total_ordering


@total_ordering
class Vector:
    """Клас Vector реалізує двовимірний вектор з базовими
    арифметичними та порівняльними операціями
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        """Додавання двох векторів"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        """Віднімання двох векторів"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        """Множення вектора на число"""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other: object) -> bool:
        """Перевірка рівності за довжиною"""
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.length(), other.length())

    def __lt__(self, other: "Vector") -> bool:
        """Порівняння за довжиною (менше)"""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.length() < other.length()

    def length(self) -> float:
        """Обчислення довжини вектора"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)
print(v1 - v2)
print(v1 * 3)

print(v1.length())
print(v2.length())

print(v1 == v2)
print(v1 < v2)
print(v2 < v1)
