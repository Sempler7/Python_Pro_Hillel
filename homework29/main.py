from event_bus import EventBus
from order_service import OrderService
from notification_service import NotificationService
from analytics_service import AnalyticsService

bus = EventBus()

order_service = OrderService(bus)
notification_service = NotificationService(bus)
analytics_service = AnalyticsService(bus)

order_service.create_order(1, "vit@example.com", "+380637770707", 1000)
print()

order_service.pay_order(1, "vit@example.com", "+380637770707", 1000)
print()

order_service.create_order(2, "sasha@example.com", "+380688880808", 350)
print()

analytics_service.show_statistics()
print()

print("Журнал подій:")
print(bus.get_event_log())
