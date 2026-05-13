import logging

from django.db.models import QuerySet
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import Serializer

from .models import Article
from .permissions import IsAuthorOrReadOnly
from .serializers import ArticleSerializer

logger = logging.getLogger('custom_logger')


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    """API-представлення для отримання списку та створення статей з підтримкою фільтрації, пошуку та сортування."""
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'status']
    ordering_fields = ['created_at', 'views', 'rating']
    ordering = ['-created_at']

    def get_queryset(self) -> QuerySet[Article]:
        """Повертає відфільтрований queryset на основі параметрів статусу та категорії"""
        queryset = Article.objects.with_related()

        status = self.request.GET.get('status')
        category_id = self.request.GET.get('category')

        if status == 'published':
            queryset = queryset.published()
        elif status == 'draft':
            queryset = queryset.drafts()

        if category_id:
            queryset = queryset.by_category(category_id)

        return queryset

    def perform_create(self, serializer: Serializer) -> None:
        """Зберігає нову статтю з поточним користувачем як автором та логгує дію"""
        article = serializer.save(author=self.request.user)
        logger.info(f'Article created via API: {article.title} by {self.request.user}')


class ArticleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API-представлення для отримання, оновлення та видалення однієї статті."""
    queryset = Article.objects.with_related()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_update(self, serializer: Serializer) -> None:
        """Оновлює існуючу статтю та логгує дію"""
        article = serializer.save()
        logger.info(f'Article updated via API: {article.title} by {self.request.user}')

    def perform_destroy(self, instance: Article) -> None:
        """Видаляє статтю та логгує дію"""
        logger.info(f'Article deleted via API: {instance.title} by {self.request.user}')
        instance.delete()