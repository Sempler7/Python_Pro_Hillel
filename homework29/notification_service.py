class NotificationService:
    """Сервіс сповіщень для відправки email та SMS на основі подій"""

    def __init__(self, event_bus) -> None:
        """Ініціалізує сервіс сповіщень та підписується на події"""

        self.event_bus = event_bus
        self.event_bus.subscribe("order.created", self.send_email)
        self.event_bus.subscribe("order.paid", self.send_sms)

    def send_email(self, event_name, data) -> None:
        """Відправляє email при створенні замовлення"""

        user_email = data.get("user_email")
        order_id = data.get("order_id")

        if user_email is None:
            print(f"Email не відправлено: немає user_email для події {event_name}")
            return

        print(f"Email відправлено на {user_email} для замовлення #{order_id}")

    def send_sms(self, event_name, data) -> None:
        """Відправляє SMS при оплаті замовлення"""

        user_phone = data.get("user_phone")
        order_id = data.get("order_id")

        if user_phone is None:
            print(f"SMS не відправлено: немає user_phone для події {event_name}")
            return

        print(f"SMS відправлено на {user_phone} для оплаченого замовлення #{order_id}")
