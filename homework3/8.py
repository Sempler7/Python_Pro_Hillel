"""Price class discussion before the PaymentGateway implementation"""

from decimal import Decimal, ROUND_HALF_UP

class Price:
    """Клас, що представляє ціну товару з можливістю заокруглення
    до двох десяткових знаків
    """
    def __init__(self, amount):
        # Використовуємо Decimal для точності обчислень
        self.amount = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __repr__(self):
        return f"Price({self.amount})"

    def __add__(self, other):
        if isinstance(other, Price):
            return Price(self.amount + other.amount)
        raise TypeError("Can only add Price to Price")

    def __sub__(self, other):
        if isinstance(other, Price):
            return Price(self.amount - other.amount)
        raise TypeError("Can only subtract Price from Price")

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __le__(self, other):
        return self.amount <= other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __ge__(self, other):
        return self.amount >= other.amount


apple = Price(12.345)
banana = Price(8.499)
milk = Price(29.99)

total = apple + banana + milk
print("Загальна сума:", total)

order_total = Price(100.00)
discount = Price(15.50)

final_price = order_total - discount
print("До сплати:", final_price)

wallet_balance = Price(50.00)
purchase_amount = Price(49.99)

if wallet_balance >= purchase_amount:
    print("Оплата можлива")
else:
    print("Недостатньо коштів")
