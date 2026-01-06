"""Механізм обробки ситуацій, коли користувач намагається завершити операцію,
для якої у нього недостатньо коштів на рахунку
"""


class InsufficientFundsException(Exception):
    """Користувацьке виключення для ситуацій, коли на рахунку недостатньо коштів
    для виконання операції
    """

    def __init__(
        self,
        required_amount,
        current_balance,
        currency="UAH",
        transaction_type="operation"
    ):
        """Ініціалізує виняток з інформацією про невдалу транзакцію"""
        self.required_amount = required_amount
        self.current_balance = current_balance
        self.currency = currency
        self.transaction_type = transaction_type
        super().__init__(self._generate_message())

    def _generate_message(self):
        """Формує текст повідомлення про помилку"""
        return (f"Недостатньо коштів для виконання транзакції '{self.transaction_type}'. "
                f"Необхідно: {self.required_amount} {self.currency}, "
                f"поточний баланс: {self.current_balance} {self.currency}.")


class BankAccount:
    """Клас, що моделює банківський рахунок з базовими операціями"""

    def __init__(self, balance=0.0, currency="UAH"):
        """Метод, який ініціалізує новий банківський рахунок"""
        self.balance = balance
        self.currency = currency

    def withdraw(self, amount):
        """Виконує операцію зняття коштів з рахунку"""
        if amount > self.balance:
            raise InsufficientFundsException(
                required_amount=amount,
                current_balance=self.balance,
                currency=self.currency,
                transaction_type="Відмова"
            )
        self.balance -= amount
        print(f"Знято {amount} {self.currency}. Новий баланс: {self.balance} {self.currency}.")

    def purchase(self, amount):
        """Виконує операцію покупки (списання коштів)"""
        if amount > self.balance:
            raise InsufficientFundsException(
                required_amount=amount,
                current_balance=self.balance,
                currency=self.currency,
                transaction_type="purchase"
            )
        self.balance -= amount
        print(f"Покупка на {amount} {self.currency} успішна. "
              f"Новий баланс: {self.balance} {self.currency}."
              )


# Використання
try:
    account = BankAccount(balance=1000, currency="UAH")
    account.withdraw(1300)  # спроба зняти більше, ніж є
except InsufficientFundsException as e:
    print(e)
