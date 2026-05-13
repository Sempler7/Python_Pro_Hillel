from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """Модель книги"""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення книги"""
        return self.title


class Rental(models.Model):
    """Модель оренди книги"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    rented_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення оренди"""
        return f"{self.user.username} — {self.book.title}"