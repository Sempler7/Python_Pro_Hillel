from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Адмін-інтерфейс для моделі Comment"""

    list_display = ("id", "photo", "author", "created_at")
    search_fields = ("text", "author__username")
