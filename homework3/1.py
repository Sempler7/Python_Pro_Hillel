"""Dunder methods"""

from math import gcd

class Fraction:
    """Клас для роботи з дробами"""
    def __init__(self, numerator: int, denominator: int):
        """Ініціалізує новий об'єкт Fraction"""
        if denominator == 0:
            raise ValueError("Знаменник не може дорівнювати нулю")
        self.numerator = numerator
        self.denominator = denominator
        self._reduce()

    def _reduce(self):
        """Скорочує дріб до нескорочуваного вигляду"""
        common = gcd(self.numerator, self.denominator)
        self.numerator //= common
        self.denominator //= common

    def __add__(self, other: "Fraction") -> "Fraction":
        """Додає два дроби"""
        num = self.numerator * other.denominator + other.numerator * self.denominator
        den = self.denominator * other.denominator
        return Fraction(num, den)

    def __sub__(self, other: "Fraction") -> "Fraction":
        """Віднімає інший дріб від поточногоЄ="""
        num = self.numerator * other.denominator - other.numerator * self.denominator
        den = self.denominator * other.denominator
        return Fraction(num, den)

    def __mul__(self, other: "Fraction") -> "Fraction":
        """Множить два дроби"""
        num = self.numerator * other.numerator
        den = self.denominator * other.denominator
        return Fraction(num, den)

    def __truediv__(self, other: "Fraction") -> "Fraction":
        """Ділить поточний дріб на інший"""
        if other.numerator == 0:
            raise ZeroDivisionError("Не можна ділити на нульову дріб")
        num = self.numerator * other.denominator
        den = self.denominator * other.numerator
        return Fraction(num, den)

    def __repr__(self) -> str:
        """Повертає рядкове представлення дробу"""
        return f"{self.numerator}/{self.denominator}"


f1 = Fraction(3, 7)
f2 = Fraction(2, 3)

print(f1 + f2)
print(f1 - f2)
print(f1 * f2)
print(f1 / f2)
