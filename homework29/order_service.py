class OrderService:
    """Сервіс для роботи із замовленнями та генерації подій"""

    def __init__(self, event_bus) -> None:
        """Ініціалізує сервіс замовлень"""

        self.event_bus = event_bus

    def create_order_data(self, order_id, user_email, user_phone, total) -> dict:
        """Формує словник даних замовлення"""

        return {
            "order_id": order_id,
            "user_email": user_email,
            "user_phone": user_phone,
            "total": total
        }

    def create_order(self, order_id, user_email, user_phone, total) -> None:
        """Створює замовлення та генерує відповідну подію"""

        order_data = self.create_order_data(order_id, user_email, user_phone, total)

        print(f"Створено замовлення #{order_id}")

        self.event_bus.emit("order.created", order_data)

    def pay_order(self, order_id, user_email, user_phone, total) -> None:
        """Обробляє оплату замовлення та генерує подію оплати"""

        payment_data = self.create_order_data(order_id, user_email, user_phone, total)

        print(f"Оплачено замовлення #{order_id}")

        self.event_bus.emit("order.paid", payment_data)
