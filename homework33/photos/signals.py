from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Photo
from .search import delete_photo_from_index, index_photo


@receiver(post_save, sender=Photo)
def sync_photo_index(sender: type[Photo], instance: Photo, **kwargs: object) -> None:
    """Синхронізує фотографію з Elasticsearch після збереження."""

    index_photo(instance)


@receiver(post_delete, sender=Photo)
def remove_photo_index(sender: type[Photo], instance: Photo, **kwargs: object) -> None:
    """Видаляє фотографію з Elasticsearch після видалення."""

    delete_photo_from_index(instance.id)
