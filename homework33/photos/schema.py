import base64
import uuid

import graphene
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from graphene_django import DjangoObjectType

from .models import Photo
from .search import search_photo_ids
from .services import create_photo, toggle_like, update_photo

User = get_user_model()


class PhotoType(DjangoObjectType):
    """GraphQL-тип для фотографії"""

    image = graphene.String()
    tags = graphene.List(graphene.String)
    metadata = graphene.JSONString()
    likes_count = graphene.Int(name="likesCount")

    class Meta:
        model = Photo
        fields = (
            "id",
            "author",
            "image",
            "caption",
            "tags",
            "metadata",
            "likes_count",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def resolve_image(root, info) -> str | None:
        """Повертає URL зображення"""

        if root.image:
            return root.image.url
        return None

    @staticmethod
    def resolve_tags(root, info) -> list[str]:
        """Повертає список тегів"""

        if isinstance(root.tags, list):
            return root.tags
        return []

    @staticmethod
    def resolve_likes_count(root, info) -> int:
        """Повертає кількість лайків"""

        return root.likes_count


class Query(graphene.ObjectType):
    """GraphQL-запити для фотографій"""

    photos = graphene.List(PhotoType)

    search_photos = graphene.List(
        PhotoType,
        query=graphene.String(required=True),
    )

    @staticmethod
    def resolve_photos(root, info) -> list[Photo]:
        """Повертає всі фотографії"""

        return list(Photo.objects.select_related("author").all())

    @staticmethod
    def resolve_search_photos(root, info, query: str) -> list[Photo]:
        """Повертає результати пошуку фотографій"""

        photo_ids = search_photo_ids(query)
        return list(Photo.objects.filter(id__in=photo_ids))


class CreatePhoto(graphene.Mutation):
    """Мутація для створення фотографії"""

    class Arguments:
        caption = graphene.String()
        tags = graphene.List(graphene.String)
        image_base64 = graphene.String()

    photo = graphene.Field(PhotoType)

    @classmethod
    def mutate(cls, root, info, caption="", tags=None, image_base64=None) -> "CreatePhoto":
        """Створює нову фотографію"""

        user = info.context.user

        if user.is_anonymous:
            user, _ = User.objects.get_or_create(username="demo")

        photo = create_photo(
            author=user,
            caption=caption or "",
            tags=tags or [],
        )

        if image_base64 and ";base64," in image_base64:
            format_part, imgstr = image_base64.split(";base64,")
            ext = format_part.split("/")[-1]
            filename = f"{uuid.uuid4()}.{ext}"

            photo.image.save(
                filename,
                ContentFile(base64.b64decode(imgstr)),
                save=True,
            )

        result = cls()
        result.photo = photo
        return result


class UpdatePhoto(graphene.Mutation):
    """Мутація для редагування фотографії"""

    class Arguments:
        photo_id = graphene.ID(required=True)
        caption = graphene.String()
        tags = graphene.List(graphene.String)

    photo = graphene.Field(PhotoType)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        photo_id: str,
        caption: str | None = None,
        tags: list[str] | None = None,
    ) -> "UpdatePhoto":
        """Оновлює фотографію"""

        photo = Photo.objects.get(pk=int(photo_id))

        updated_photo = update_photo(
            photo=photo,
            caption=caption,
            tags=tags,
        )

        result = cls()
        result.photo = updated_photo
        return result


class ToggleLike(graphene.Mutation):
    """Мутація для додавання або скасування лайку"""

    class Arguments:
        photo_id = graphene.ID(required=True)

    photo = graphene.Field(PhotoType)

    @classmethod
    def mutate(cls, root, info, photo_id: str) -> "ToggleLike":
        """Перемикає лайк для фотографії"""

        user = info.context.user

        if user.is_anonymous:
            user, _ = User.objects.get_or_create(username="demo")

        photo = Photo.objects.get(pk=int(photo_id))
        liked_photo = toggle_like(photo=photo, user=user)

        result = cls()
        result.photo = liked_photo
        return result


class Mutation(graphene.ObjectType):
    """GraphQL-мутації для фотографій"""

    create_photo = CreatePhoto.Field()
    update_photo = UpdatePhoto.Field()
    toggle_like = ToggleLike.Field()