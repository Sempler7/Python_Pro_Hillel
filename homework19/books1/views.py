"""This module defines views for books app."""
from typing import List

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission

from books1.models import Book
from books1.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for Book model."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["author", "genre", "publication_year", ]
    search_fields = ["title", ]

    def get_permissions(self) -> List[BasePermission]:
        """Returns the list of permissions"""
        if self.action == "destroy":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
