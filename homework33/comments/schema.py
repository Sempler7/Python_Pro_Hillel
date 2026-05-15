import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from photos.models import Photo
from .models import Comment

User = get_user_model()


class CommentType(DjangoObjectType):
    """GraphQL-тип для коментаря"""

    class Meta:
        model = Comment
        fields = ("id", "photo", "author", "text", "created_at")


class Query(graphene.ObjectType):
    """GraphQL-запити для роботи з коментарями"""

    comments = graphene.List(CommentType, photo_id=graphene.ID(required=True))

    def resolve_comments(self, info, photo_id: int) -> list[Comment]:
        """Повертає коментарі до вибраної фотографії"""

        return list(Comment.objects.filter(photo_id=photo_id))


class CreateComment(graphene.Mutation):
    """Мутація для створення коментаря до фотографії"""

    class Arguments:
        photo_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, photo_id: int, text: str) -> "CreateComment":
        """Створює новий коментар"""

        user = info.context.user
        if user.is_anonymous:
            user, _ = User.objects.get_or_create(username="demo")
        photo = Photo.objects.get(pk=photo_id)
        comment = Comment.objects.create(photo=photo, author=user, text=text)
        result = cls()
        result.comment = comment
        return result


class Mutation(graphene.ObjectType):
    """GraphQL-мутації для роботи з коментарями"""

    create_comment = CreateComment.Field()
