import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Article, Category, Comment, CustomUser

logger = logging.getLogger('custom_logger')


class CommentInline(admin.TabularInline):
    """Inline-конфігурація для відображення коментарів у статті."""
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('user', 'text', 'created_at')


@admin.action(description='Mark selected articles as published')
def make_published(
    modeladmin: ModelAdmin,
    request: HttpRequest,
    queryset: QuerySet[Article]
) -> None:
    """Позначає вибрані статті як опубліковані"""
    updated = queryset.update(status='published')
    logger.info(f'{request.user} marked {updated} articles as published')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Адмін-конфігурація для керування статтями."""
    list_display = ('title', 'author', 'category', 'status', 'views', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content')
    actions = [make_published]
    inlines = [CommentInline]
    list_editable = ('status',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Article]:
        """Повертає оптимізований queryset із пов'язаними об'єктами"""
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Адмін-конфігурація для категорій."""
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Адмін-конфігурація для коментарів."""
    list_display = ('user', 'article', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Адмін-конфігурація для користувачів."""
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')