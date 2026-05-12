"""This module provides tests for books app."""
from typing import Callable, Any

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Book


@pytest.fixture
def api_client() -> APIClient:
    """Fixture for api client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_book(db: Any) -> Callable:
    """Fixture for creating a book"""

    def make_book(**kwargs: Any) -> Book:
        defaults = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Test Genre",
            "publication_year": 2024
        }
        defaults.update(kwargs)
        return Book.objects.create(**defaults)

    return make_book


@pytest.fixture
def auth_client(api_client: APIClient, db: Any) -> APIClient:
    """Fixture for auth client"""
    user = User.objects.create_user(username="testuser", password="password")
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_get_books_list(auth_client: APIClient, create_book: Callable) -> None:
    """Test get books list"""
    create_book(title="Book 1")
    create_book(title="Book 2")

    url = reverse("book-list")
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2


@pytest.mark.django_db
def test_create_book_authenticated(auth_client: APIClient) -> None:
    """Test create book by authenticated user."""
    url = reverse("book-list")
    data = {
        "title": "Book title 2",
        "author": "test author 2",
        "genre": "test genre",
        "publication_year": 2008
    }
    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == 1
    assert Book.objects.get().title == "Book title 2"


@pytest.mark.django_db
def test_create_book_unauthenticated(api_client: APIClient) -> None:
    """Test create book by unauthenticated user."""
    url = reverse("book-list")
    response = api_client.post(url, {"title": "Book"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_book_search_by_title(auth_client: APIClient, create_book: Callable) -> None:
    """Test book search by title"""
    create_book(title="Test book title 1")
    create_book(title="Normal Book")

    url = reverse("book-list")
    response = auth_client.get(url, {"search": "title 1"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data["results"][0]["title"] == "Test book title 1"


@pytest.mark.django_db
def test_delete_book_as_admin(api_client: APIClient, create_book: Callable) -> None:
    """Test book delete by admin"""
    book = create_book()
    admin_user = User.objects.create_superuser(username="admin", password="pass", email="admin@test.com")
    api_client.force_authenticate(user=admin_user)

    url = reverse("book-detail", kwargs={"pk": book.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Book.objects.count() == 0
