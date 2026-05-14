import json


class EventBus:
    """Шина подій для підписки, публікації та повторного відтворення подій"""

    def __init__(self) -> None:
        """Ініціалізує шину подій"""

        self.listeners = {}
        self.event_log = []

    def subscribe(self, event_name, callback) -> None:
        """Підписує callback-функцію на подію"""

        if event_name not in self.listeners:
            self.listeners[event_name] = []

        if callback not in self.listeners[event_name]:
            self.listeners[event_name].append(callback)

    def unsubscribe(self, event_name, callback) -> None:
        """Відписує callback-функцію від події"""

        if event_name in self.listeners:
            if callback in self.listeners[event_name]:
                self.listeners[event_name].remove(callback)

            if len(self.listeners[event_name]) == 0:
                del self.listeners[event_name]

    def emit(self, event_name, data) -> None:
        """Публікує подію, зберігає її у файл і викликає підписників"""

        event = {
            "event_name": event_name,
            "data": data
        }

        self.event_log.append(event)
        self.save_event_to_file(event)

        for listener_event, callbacks in self.listeners.items():
            if self._matches(listener_event, event_name):
                for callback in callbacks:
                    try:
                        callback(event_name, data)
                    except Exception as error:
                        print(f"Помилка listener-а для події {event_name}: {error}")

    def emit_without_saving(self, event_name, data) -> None:
        """Публікує подію без збереження у файл"""

        self.event_log.append({
            "event_name": event_name,
            "data": data
        })

        for listener_event, callbacks in self.listeners.items():
            if self._matches(listener_event, event_name):
                for callback in callbacks:
                    try:
                        callback(event_name, data)
                    except Exception as error:
                        print(f"Помилка listener-а для події {event_name}: {error}")

    def save_event_to_file(self, event) -> None:
        """Зберігає подію у файл журналу"""

        with open("events.log", "a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

    def replay_from_file(self, filename) -> None:
        """Відтворює події з файлу журналу"""

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                event = json.loads(line)
                self.emit_without_saving(event["event_name"], event["data"])

    def _matches(self, listener_event, emitted_event) -> bool:
        """Перевіряє, чи відповідає подія підписці"""

        if listener_event == emitted_event:
            return True

        if listener_event.endswith("*"):
            prefix = listener_event[:-1]
            return emitted_event.startswith(prefix)

        return False

    def get_event_log(self):
        """Повертає журнал подій"""

        return self.event_log
