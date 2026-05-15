from django.conf import settings
from django.db import models

from photos.models import Photo


class Comment(models.Model):
    """Коментар користувача під фотографією."""

    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        """Повертає короткий текст коментаря."""

        return self.text[:40]
