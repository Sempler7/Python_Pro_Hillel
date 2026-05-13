from rest_framework import serializers
from .models import Article, Comment, Category


class CommentSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі коментаря."""

    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі категорії."""

    class Meta:
        model = Category
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі статті з вкладеними коментарями та категорією."""

    comments = CommentSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'metadata', 'status',
            'views', 'rating', 'author', 'category', 'category_id',
            'comments', 'created_at'
        ]