"""Тестування класу BankAccount з використанням фікстур, pytest та моків"""

from unittest.mock import patch
from bank_account import BankAccount
import pytest


# pylint: disable=redefined-outer-name

@pytest.fixture
def account():
    """Фікстура для створення банківського рахунку з початковим балансом 100.0"""
    return BankAccount(initial_balance=100.0)


@pytest.mark.parametrize("deposit_amount, expected_balance", [
    (50, 150.0),
    (100, 200.0),
    (200.5, 300.5),
])
def test_deposit(account, deposit_amount, expected_balance):
    """Тестування методу поповнення рахунку з різними сумами."""
    account.deposit(deposit_amount)
    assert account.get_balance() == expected_balance


@pytest.mark.parametrize("withdraw_amount, expected_balance", [
    (50, 50.0),
    (100, 0.0),
])
def test_withdraw(account, withdraw_amount, expected_balance):
    """Тестування методу зняття коштів з рахунку з різними сумами."""
    account.withdraw(withdraw_amount)
    assert account.get_balance() == expected_balance


def test_withdraw_skip_if_empty():
    """Тестування зняття коштів з порожнього рахунку з пропуском тесту."""
    empty_account = BankAccount(initial_balance=0.0)
    if empty_account.get_balance() == 0.0:
        pytest.skip("Рахунок порожній, тест пропущено")
    empty_account.withdraw(10)


def test_external_api_mock(account):
    """Тестування з використанням моків для зовнішнього API."""
    with patch("bank_account.BankAccount.get_balance", return_value=999.99):
        balance = account.get_balance()
        assert balance == 999.99
