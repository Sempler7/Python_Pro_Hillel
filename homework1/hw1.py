"""Программа для вычисления площади круга по заданному радиусу."""

import math


def calculate_circle_area(radius):
    """Вычисляет площадь круга по заданному радиусу."""
    return math.pi * radius ** 2


user_input = input("Введите радиус круга: ")
radius_circle = float(user_input)
area = calculate_circle_area(radius_circle)

print(f"Площадь круга: {area:.2f}")
