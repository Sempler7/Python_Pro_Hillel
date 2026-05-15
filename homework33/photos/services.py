from django.contrib.auth import get_user_model

from .models import Photo
from .search import index_photo

User = get_user_model()


def create_photo(
        *,
        author: User,
        caption: str = "",
        tags: list[str] | None = None,
        metadata: dict[str, object] | None = None,
) -> Photo:
    """Створює фотографію та додає її до пошукового індексу."""

    photo = Photo.objects.create(
        author=author,
        caption=caption,
        tags=tags or [],
        metadata=metadata or {},
    )
    index_photo(photo)
    return photo


def update_photo(
        *,
        photo: Photo,
        caption: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, object] | None = None,
) -> Photo:
    """Оновлює дані фотографії та переіндексовує її."""

    if caption is not None:
        photo.caption = caption
    if tags is not None:
        photo.tags = tags
    if metadata is not None:
        photo.metadata = metadata
    photo.save()
    index_photo(photo)
    return photo


def toggle_like(*, photo: Photo, user: User) -> Photo:
    """Додає або прибирає "подобається"
    (лайк) користувача для фотографії.
    """

    if photo.likes.filter(id=user.id).exists():
        photo.likes.remove(user)
    else:
        photo.likes.add(user)
    return photo
