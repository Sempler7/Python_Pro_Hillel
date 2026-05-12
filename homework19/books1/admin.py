"""This module defines the configuration of the admin panel
 and the registration of models."""
from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for the Book model."""
    list_display = ("title", "author", "genre", "publication_year")
    readonly_fields = ("id", "created_at")

    list_filter = ("genre",)
    search_fields = ("title",)
    search_help_text = "Search by book title"
