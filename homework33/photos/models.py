from django.conf import settings
from django.db import models


class Photo(models.Model):
    """Модель фотографії, яку користувач публікує на платформі."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(upload_to="photos/", blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_photos",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def likes_count(self) -> int:
        """Повертає кількість "подобається"
        (лайків) для фотографії."""

        return self.likes.count()

    def __str__(self) -> str:
        """Повертає читабельний опис фотографії."""

        return f"Photo #{self.pk}: {self.caption[:30]}"
