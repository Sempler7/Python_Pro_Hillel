import logging
from typing import Any, Type
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article

logger = logging.getLogger('custom_logger')


@receiver(post_save, sender=Article)
def article_saved(
    sender: Type[Article],
    instance: Article,
    created: bool,
    **kwargs: Any
) -> None:
    """Обробляє сигнал після збереження статті"""

    if created:
        logger.info(f'Article created: {instance.title}')
    else:
        logger.info(f'Article updated: {instance.title}')