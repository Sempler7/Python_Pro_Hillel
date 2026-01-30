"""Приклад комплексного тестування банківського рахунку"""


class BankAccount:
    """Клас для роботи з банківським рахунком."""

    def __init__(self, initial_balance: float = 0.0) -> None:
        self._balance = initial_balance

    def deposit(self, amount: float) -> None:
        """Метод для поповнення рахунку."""
        if amount <= 0:
            raise ValueError("Сума поповнення має бути додатною")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Метод для зняття коштів з рахунку."""
        if amount <= 0:
            raise ValueError("Сума зняття має бути додатною")
        if amount > self._balance:
            raise ValueError("Недостатньо коштів на рахунку")
        self._balance -= amount

    def get_balance(self) -> float:
        """Метод для отримання поточного балансу рахунку."""
        return self._balance
