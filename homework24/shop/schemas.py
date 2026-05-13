from ninja import Schema
from decimal import Decimal
from typing import List, Any
from datetime import datetime


class ProductIn(Schema):
    """Схема для створення або оновлення товару"""

    name: str
    description: str = ""
    price: Decimal
    stock: int = 0


class ProductOut(Schema):
    """Схема відповіді для товару"""

    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    created_at: datetime


class CartItemOut(Schema):
    """Схема відповіді для елемента кошика"""

    id: int
    product_id: int
    product_name: str
    quantity: int

    @staticmethod
    def resolve_product_name(obj: Any) -> str:
        """Отримує назву товару з пов'язаного об'єкта"""
        return obj.product.name


class AddToCartIn(Schema):
    """Схема для додавання товару до кошика"""

    product_id: int
    quantity: int = 1


class OrderItemOut(Schema):
    """Схема відповіді для елемента замовлення"""

    id: int
    product_id: int
    product_name: str
    quantity: int
    price: Decimal

    @staticmethod
    def resolve_product_name(obj: Any) -> str:
        """Отримує назву товару з пов'язаного об'єкта"""
        return obj.product.name


class OrderOut(Schema):
    """Схема відповіді для замовлення"""

    id: int
    status: str
    created_at: datetime
    items: List[OrderItemOut]


class OrderStatusIn(Schema):
    """Схема для оновлення статусу замовлення"""

    status: str