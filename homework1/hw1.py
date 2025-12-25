import math

def calculate_circle_area(radius):
    return math.pi * radius_circle ** 2

user_input = input("Введите радиус круга: ")
radius_circle = float(user_input)
area = calculate_circle_area(radius_circle)

print(f"Площадь круга: {area:.2f}")