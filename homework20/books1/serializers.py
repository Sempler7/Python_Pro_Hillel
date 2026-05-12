"""This module contains serializers for books app."""
from rest_framework import serializers

from books1.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model."""

    class Meta:
        """Metaclass for Book model."""
        model = Book
        fields = "__all__"
        read_only_fields = ("id", "created_at")
