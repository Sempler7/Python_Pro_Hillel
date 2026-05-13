import logging
from typing import Any
from django.apps import AppConfig

logger = logging.getLogger('custom_logger')


class CustomizationInDjangoConfig(AppConfig):
    """Конфігурація застосунку customization_in_django."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customization'

    def ready(self) -> None:
        """Ініціалізує сигнали застосунку при його запуску"""
        import customization.signals  # noqa: F401
        logger.info('Signals loaded for customization app')