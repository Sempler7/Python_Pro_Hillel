from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Адмін-інтерфейс для моделі Photo.

        Attributes:
            list_display: Поля, що відображаються у списку.
            list_filter: Поля для фільтрації.
            search_fields: Поля для пошуку.
    """

    list_display = ("id", "author", "caption", "created_at")
    list_filter = ("created_at",)
    search_fields = ("caption", "author__username")
