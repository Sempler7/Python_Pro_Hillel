from django.apps import AppConfig


class PhotosConfig(AppConfig):
    """Конфігурація Django-додатку photos"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "photos"

    def ready(self) -> None:
        """Підключає сигнали після ініціалізації застосунку"""

        from . import signals  # noqa: F401
