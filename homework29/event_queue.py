import queue
import threading


class EventQueue:
    """Черга подій для асинхронної обробки через шину подій"""

    def __init__(self, event_bus) -> None:
        """Ініціалізує чергу подій"""

        self.event_bus = event_bus
        self.queue = queue.Queue()
        self.running = False

    def produce(self, event_name, data) -> None:
        """Додає подію до черги"""

        self.queue.put({
            "event_name": event_name,
            "data": data
        })

    def worker(self) -> None:
        """Обробляє події з черги та передає їх у шину подій"""

        while self.running or not self.queue.empty():
            try:
                event = self.queue.get(timeout=1)
                self.event_bus.emit(event["event_name"], event["data"])
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as error:
                print(f"Worker помилка: {error}")

    def start(self) -> None:
        """Запускає окремий потік для обробки черги подій"""

        self.running = True
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()

    def stop(self) -> None:
        """Зупиняє обробник черги подій"""

        self.running = False
        self.thread.join()
