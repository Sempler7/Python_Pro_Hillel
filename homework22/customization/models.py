from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Avg, Count, Sum
from django.urls import reverse
from typing import Any, Dict

from .fields import UpperCaseCharField

PHONE_REGEX = r'^\+380\d{9}$'


class CustomUser(AbstractUser):
    """Кастомна модель користувача з додатковим полем номера телефону."""

    phone_number = models.CharField(
        help_text='Format: +380XXXXXXXXX',
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=PHONE_REGEX,
                message='Phone number must be in format +380XXXXXXXXX.'
            )
        ],
        verbose_name='Phone number'
    )

    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self) -> str:
        """Повертає строкове представлення користувача"""
        return self.username


class Category(models.Model):
    """Модель категорії для статей."""
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        """Повертає назву категорії"""
        return self.name


class ArticleQuerySet(models.QuerySet):
    """Кастомний QuerySet для моделі Article."""

    def published(self) -> "ArticleQuerySet":
        """Повертає тільки опубліковані статті"""
        return self.filter(status='published')

    def drafts(self) -> "ArticleQuerySet":
        """Повертає тільки чернетки"""
        return self.filter(status='draft')

    def by_category(self, category_id: Any) -> "ArticleQuerySet":
        """Фільтрує статті за категорією"""
        return self.filter(category_id=category_id)

    def popular(self) -> "ArticleQuerySet":
        """Повертає популярні статті (з великою кількістю переглядів)"""
        return self.filter(views__gt=100)

    def with_related(self) -> "ArticleQuerySet":
        """Оптимізує queryset, додаючи пов'язані об'єкти"""
        return self.select_related('author', 'category').prefetch_related('comments')

    def category_statistics(self) -> models.QuerySet:
        """Обчислює статистику по категоріях"""
        return self.values('category__name').annotate(
            total_articles=Count('id'),
            average_rating=Avg('rating'),
            total_views=Sum('views')
        ).order_by('-total_articles')


class Article(models.Model):
    """Модель статті."""

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = UpperCaseCharField(max_length=255)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def get_summary(self) -> str:
        """Повертає короткий опис статті"""
        return self.content[:120] + '...' if len(self.content) > 120 else self.content

    @classmethod
    def stats(cls) -> Dict[str, Any]:
        """Обчислює загальну статистику по статтях"""
        return cls.objects.aggregate(
            total_articles=Count('id'),
            avg_rating=Avg('rating'),
            published_count=Count('id', filter=models.Q(status='published'))
        )

    def get_absolute_url(self) -> str:
        """Повертає URL сторінки статті"""
        return reverse('article-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        """Повертає назву статті"""
        return self.title


class Comment(models.Model):
    """Модель коментаря до статті."""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        """Повертає текстове представлення коментаря"""
        return f'Comment by {self.user} on {self.article}'