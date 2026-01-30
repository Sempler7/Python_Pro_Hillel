"""Модуль для уніфікованої відправки повідомлень через SMS, Email та Push.
Реалізує патерн Adapter та централізовану систему відправки.
"""

from abc import ABC, abstractmethod


class MessageSender(ABC):  # pylint: disable=too-few-public-methods
    """Інтерфейс для відправки повідомлень незалежно від каналу."""

    @abstractmethod
    def send_message(self, message: str):
        """Відправляє повідомлення через конкретний канал"""
        raise NotImplementedError("Метод має бути реалізований у підкласі.")


class SMSService:  # pylint: disable=too-few-public-methods
    """Сервіс для відправки SMS-повідомлень."""

    @staticmethod
    def send_sms(phone_number: str, message: str):
        """Відправляє SMS на вказаний номер."""
        if not phone_number.startswith("+"):
            raise ValueError("Невірний формат номера телефону")
        print(f"Відправлено SMS на {phone_number}: {message}")


class EmailService:  # pylint: disable=too-few-public-methods
    """Сервіс для відправки Email-повідомлень."""

    @staticmethod
    def send_email(email_address: str, message: str):
        """Відправляє Email на вказану адресу."""
        if "@" not in email_address:
            raise ValueError("Невірна email-адреса")
        print(f"Відправлено Email на {email_address}: {message}")


class PushService:  # pylint: disable=too-few-public-methods
    """Сервіс для відправки Push-повідомлень."""

    @staticmethod
    def send_push(device_id: str, message: str):
        """Відправляє Push на вказаний пристрій."""
        if not device_id:
            raise ValueError("Device ID не може бути порожнім")
        print(f"Відправлено Push на пристрій {device_id}: {message}")


class SMSAdapter(MessageSender):  # pylint: disable=too-few-public-methods
    """Адаптер для використання SMSService через універсальний інтерфейс."""

    def __init__(self, service: SMSService, phone_number: str):
        self.service = service
        self.phone_number = phone_number

    def send_message(self, message: str):
        """Відправляє повідомлення через SMS-сервіс."""
        self.service.send_sms(self.phone_number, message)


class EmailAdapter(MessageSender):  # pylint: disable=too-few-public-methods
    """Адаптер для використання EmailService через універсальний інтерфейс."""

    def __init__(self, service: EmailService, email_address: str):
        self.service = service
        self.email_address = email_address

    def send_message(self, message: str):
        """Відправляє повідомлення через Email-сервіс."""
        self.service.send_email(self.email_address, message)


class PushAdapter(MessageSender):  # pylint: disable=too-few-public-methods
    """Адаптер для використання PushService через універсальний інтерфейс."""

    def __init__(self, service: PushService, device_id: str):
        self.service = service
        self.device_id = device_id

    def send_message(self, message: str):
        """Відправляє повідомлення через Push-сервіс."""
        self.service.send_push(self.device_id, message)


# --- Система масової відправки ---
class MessageDispatcher:  # pylint: disable=too-few-public-methods
    """Клас для централізованої відправки повідомлень через список адаптерів."""

    def __init__(self, senders: list[MessageSender]):
        self.senders = senders

    def broadcast(self, message: str):
        """Відправляє повідомлення через усі доступні сервіси з обробкою помилок."""
        for sender in self.senders:
            try:
                sender.send_message(message)
            except (ValueError, RuntimeError) as error:
                print(f"Помилка при відправці через {sender.__class__.__name__}: {error}")


if __name__ == "__main__":
    sms_adapter = SMSAdapter(SMSService(), "+380123456789")
    email_adapter = EmailAdapter(EmailService(), "user@example.com")
    push_adapter = PushAdapter(PushService(), "device123")

    TEST_MESSAGE = "Привіт! Це тестове повідомлення."
    sms_adapter.send_message(TEST_MESSAGE)
    email_adapter.send_message(TEST_MESSAGE)
    push_adapter.send_message(TEST_MESSAGE)

    print("\n=== Масова відправка через всі сервіси ===")
    dispatcher = MessageDispatcher([sms_adapter, email_adapter, push_adapter])
    dispatcher.broadcast("Це повідомлення відправлено через усі канали.")
