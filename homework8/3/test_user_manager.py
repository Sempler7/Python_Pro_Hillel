"""Тестування модуля user_manager з використанням pytest"""

import pytest
from user_manager import UserManager


# pylint: disable=redefined-outer-name
@pytest.fixture
def user_manager():
    """Фікстура для попереднього створення користувачів"""
    um = UserManager()
    um.add_user("Alice", 30)
    um.add_user("Bob", 25)
    return um


def test_add_user(user_manager):
    """Тест для додавання користувача"""
    user_manager.add_user("Charlie", 40)
    users = user_manager.get_all_users()
    assert ("Charlie", 40) in users
    assert len(users) == 3


def test_remove_user(user_manager):
    """Тест для видалення користувача"""
    user_manager.remove_user("Alice")
    users = user_manager.get_all_users()
    assert ("Alice", 30) not in users
    assert len(users) == 1


def test_get_all_users(user_manager):
    """Тест для отримання всіх користувачів"""
    users = user_manager.get_all_users()
    assert ("Alice", 30) in users
    assert ("Bob", 25) in users
    assert len(users) == 2


@pytest.mark.skipif(
    len(UserManager().get_all_users()) < 3,
    reason="Пропускаємо тест, якщо менше трьох користувачів"
)
def test_skip_condition(user_manager):
    """Тест, який пропускається, якщо менш як три користувачі"""
    # Додаємо третього користувача, щоб перевірити умову
    user_manager.add_user("Charlie", 40)
    users = user_manager.get_all_users()
    assert len(users) >= 3
