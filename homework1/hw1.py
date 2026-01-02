"""Программа для вычисления площади круга по заданному радиусу."""

import math


def calculate_circle_area(radius: float) -> float:
    """Вычисляет площадь круга по заданному радиусу."""
    return math.pi * radius ** 2


user_input: str = input("Введите радиус круга: ")
radius_circle: float = float(user_input)
area: float = calculate_circle_area(radius_circle)

print(f"Площадь круга: {area:.2f}")
