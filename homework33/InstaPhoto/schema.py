import graphene

import comments.schema
import photos.schema


class Query(photos.schema.Query, comments.schema.Query, graphene.ObjectType):
    """Кореневі GraphQL-запити проєкту."""


class Mutation(
    photos.schema.Mutation,
    comments.schema.Mutation,
    graphene.ObjectType,
):
    """Кореневі GraphQL-мутації проєкту."""


schema = graphene.Schema(query=Query, mutation=Mutation)
