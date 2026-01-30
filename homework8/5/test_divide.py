"""Тестування функції ділення з обробкою винятків"""

import pytest
from divide import divide


def test_divide_correct():
    """Перевірка коректного ділення"""
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0


def test_divide_zero_division():
    """Перевірка винятку ZeroDivisionError"""
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5.0),
        (9, 3, 3.0),
        (7, -1, -7.0),
        (0, 5, 0.0),
    ]
)
def test_divide_parametrized(a, b, expected):
    """Перевірка ділення з різними значеннями"""
    assert divide(a, b) == expected

# Запуск тестів можна здійснити командою:
# pytest test_divide.py
# або pytest -v
