from event_bus import EventBus


def email_sender(event_name, data) -> None:
    """Обробляє подію реєстрації користувача та імітує відправку email"""

    print(f"Email sender отримав подію: {event_name}")
    print(f"Дані: {data}")


def logger(event_name, data) -> None:
    """Логує отримані події"""

    print(f"Logger записав подію: {event_name}")
    print(f"Дані: {data}")


def analytics(event_name, data) -> None:
    """Обробляє аналітичні події"""

    print(f"Analytics обробив подію: {event_name}")
    print(f"Дані: {data}")


bus = EventBus()

bus.subscribe("user.registered", email_sender)
bus.subscribe("user.*", logger)
bus.subscribe("order.created", analytics)
bus.subscribe("order.*", logger)

bus.emit("user.registered", {
    "id": 1,
    "name": "Vit",
    "email": "Vit@example.com"
})

print()

bus.emit("user.deleted", {
    "id": 1,
    "reason": "Користувач видалив акаунт"
})

print()

bus.emit("order.created", {
    "order_id": 101,
    "user_id": 1,
    "total": 1000
})

print()

print("Журнал подій:")
print(bus.get_event_log())

print()

bus.unsubscribe("user.*", logger)

bus.emit("user.deleted", {
    "id": 2,
    "reason": "Перевірка unsubscribe"
})
