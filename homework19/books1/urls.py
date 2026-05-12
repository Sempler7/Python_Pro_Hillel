"""This module defines URL patterns for books app."""
from typing import List

from django.urls import include, path, URLPattern, URLResolver
from rest_framework.routers import DefaultRouter

from .views import BookViewSet

router = DefaultRouter()
router.register("books1", BookViewSet, basename="book")

urlpatterns: List[URLPattern | URLResolver] = [
    path("", include(router.urls)),
]
