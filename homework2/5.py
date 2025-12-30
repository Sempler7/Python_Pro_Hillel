#Pylint ругается на Global, но, так как она нужна по заданию, то я ее оставил

"""Календар подій"""

from typing import Callable

events: list[str] = []

def event_calendar() -> tuple[Callable[[str], None], Callable[[str], None], Callable[[], None]]:

    """
    Замикання, яке повертає функції для роботи з календарем:
    - додавання подій
    - видалення подій
    - перегляд майбутніх подій
    """

    def add_event_inner(event: str) -> None:
        """Функція, яка додає нову подію"""
        global events
        events.append(event)
        print(f"Подія '{event}' додана.")

    def remove_event_inner(event: str) -> None:
        """Функція, яка видаляє подію"""
        global events
        if event in events:
            events.remove(event)
            print(f"Подія '{event}' видалена.")
        else:
            print(f"Подія '{event}' не знайдена.")

    def view_events_inner() -> None:
        """Функція, яка переглядає всі майбутні події"""
        global events
        if events:
            print("Майбутні події:")
            for i, e in enumerate(events, start=1):
                print(f"{i}. {e}")
        else:
            print("Немає запланованих подій.")

    return add_event_inner, remove_event_inner, view_events_inner


add_event, remove_event, view_events = event_calendar()

add_event("Зустріч з командою")
add_event("День народження друга")
add_event("Співбесіда")

view_events()

remove_event("Зустріч з командою")
remove_event("Сінк")

view_events()
