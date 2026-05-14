from event_bus import EventBus
from notification_service import NotificationService
from analytics_service import AnalyticsService

bus = EventBus()

notification_service = NotificationService(bus)
analytics_service = AnalyticsService(bus)

print("Replay подій з файлу events.log")
print()

bus.replay_from_file("events.log")

print()
analytics_service.show_statistics()
