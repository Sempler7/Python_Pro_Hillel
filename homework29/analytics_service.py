class AnalyticsService:
    """Сервіс аналітики для підрахунку подій замовлень та оплат"""

    def __init__(self, event_bus) -> None:
        """Ініціалізує сервіс аналітики та підписується на події"""

        self.event_bus = event_bus
        self.orders_count = 0
        self.payments_count = 0

        self.event_bus.subscribe("order.created", self.count_orders)
        self.event_bus.subscribe("order.paid", self.count_payments)

    def count_orders(self, event_name, data) -> None:
        """Обробляє подію створення замовлення"""

        self.orders_count += 1
        print(f"Analytics: кількість створених замовлень = {self.orders_count}")

    def count_payments(self, event_name, data) -> None:
        """Обробляє подію оплати замовлення"""

        self.payments_count += 1
        print(f"Analytics: кількість оплат = {self.payments_count}")

    def show_statistics(self) -> None:
        """Виводить статистику замовлень та оплат"""

        print("Статистика:")
        print(f"Створено замовлень: {self.orders_count}")
        print(f"Оплачено замовлень: {self.payments_count}")
