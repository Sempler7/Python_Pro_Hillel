from event_bus import EventBus
from event_queue import EventQueue
from notification_service import NotificationService
from analytics_service import AnalyticsService

bus = EventBus()

notification_service = NotificationService(bus)
analytics_service = AnalyticsService(bus)

event_queue = EventQueue(bus)

event_queue.start()

event_queue.produce("order.created", {
    "order_id": 1,
    "user_email": "vit@example.com",
    "user_phone": "+380637770707",
    "total": 1000
})

event_queue.produce("order.paid", {
    "order_id": 1,
    "user_email": "vit@example.com",
    "user_phone": "+380637770707",
    "total": 1000
})

event_queue.produce("order.created", {
    "order_id": 2,
    "user_email": "sasha@example.com",
    "user_phone": "+380688880808",
    "total": 350
})

event_queue.stop()

print()

analytics_service.show_statistics()
print()

print("Журнал подій:")
print(bus.get_event_log())
