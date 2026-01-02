"""Програма для управління товарами в онлайн-магазині (з використанням карируваної функції.
"""

from typing import Callable, Dict, Tuple


def create_product(name: str) -> Callable[[float], Callable[[int],
        Tuple[Dict[str, object], Callable[[float], Dict[str, object]]]]]:
    """
    Функція, яка створює товар за допомогою карирування
    """


    def with_price(
        price: float
    ) -> Callable[[int], Tuple[Dict[str, object], Callable[[float], Dict[str, object]]]]:
        """Функція, яка додає ціну до товару"""


        def with_quantity(
            quantity: int
        ) -> Tuple[Dict[str, object], Callable[[float], Dict[str, object]]]:
            """Функція, яка додає кількість та створює замикання для зміни ціни"""

            product_data: Dict[str, object] = {
                "name": name,
                "price": price,
                "quantity": quantity
            }


            def set_price(new_price: float) -> Dict[str, object]:
                """Замикання для зміни ціни товару."""
                product_data["price"] = new_price
                return product_data

            return product_data, set_price

        return with_quantity

    return with_price


product_info, change_price = create_product("Ноутбук")(25000)(10)

print("Початковий товар:", product_info)

change_price(22000)
print("Після зміни ціни:", product_info)
