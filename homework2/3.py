"""Програма імітація магазину з акційними знижками
"""

from typing import Final

DISCOUNT: Final[float] = 0.1

def create_order(price: float) -> None:
    """Функція, яка вираховує кінцеву ціну зі знижкою"""
    final_price = price - price * DISCOUNT

    def apply_additional_discount(extra_discount: float = 0.0) -> None:
        """Вкладена функція для додаткової знижки (наприклад, VIP-клієнт)"""
        nonlocal final_price
        final_price -= final_price * extra_discount

    apply_additional_discount(0.05)  #  тут вказується додаткова знижка (якщо потрібно)
    print(f"Фінальна ціна замовлення: {final_price:.2f} грн")

create_order(1000)
create_order(500)
