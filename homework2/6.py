"""Калькулятор"""

from typing import Callable

def create_calculator(operator: str) -> Callable[[float, float], float | str]:
    """Функція приймає оператор ('+', '-', '*', '/')
        і повертає функцію для виконання відповідної операції.
        """
    def add(x: float, y: float) -> float:
        return x + y

    def subtract(x: float, y: float) -> float:
        return x - y

    def multiply(x: float, y: float) -> float:
        return x * y

    def divide(x: float, y: float) -> float | str:
        if y == 0:
            return "На нуль ділити не можна!"
        return x / y

    if operator == '+':
        return add
    if operator == '-':
        return subtract
    if operator == '*':
        return multiply
    if operator == '/':
        return divide
    raise ValueError("Невідомий оператор")

add_func = create_calculator('+')
sub_func = create_calculator('-')
mul_func = create_calculator('*')
div_func = create_calculator('/')

print("5 + 3 =", add_func(5, 3))
print("5 - 3 =", sub_func(5, 3))
print("5 * 3 =", mul_func(5, 3))
print("5 / 3 =", div_func(5, 3))
print("5 / 0 =", div_func(5, 0))
