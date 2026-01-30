"""Тестування модуля age_verifier.py з використанням pytest"""

import pytest
from age_verifier import AgeVerifier


@pytest.mark.parametrize("age,expected", [
    (0, False),
    (5, False),
    (17, False),
    (18, True),
    (25, True),
    (120, True),  # формально дорослий, але граничне значення
])
def test_is_adult(age, expected):
    """Тестування методу is_adult з різними значеннями віку"""
    assert AgeVerifier.is_adult(age) == expected


@pytest.mark.skip(reason="Некоректне значення віку (менше 0)")
def test_negative_age():
    """Тестування з від'ємним значенням віку"""
    age = -5
    assert AgeVerifier.is_adult(age) is False


# Умовний скіп, якщо вік > 120
MAX_TEST_AGE = 121


@pytest.mark.skipif(MAX_TEST_AGE > 120, reason="Неправильне значення віку")
def test_age_too_high():
    """Тестування з віком понад 120"""
    assert AgeVerifier.is_adult(MAX_TEST_AGE) is False
