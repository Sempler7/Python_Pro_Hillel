from django.db import models
from django.core.cache import cache


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )
    title = models.CharField(max_length=150, db_index=True)
    published_year = models.PositiveIntegerField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["published_year"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        cache.delete("book_list")
        return result

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        cache.delete("book_list")
        return result


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    reviewer_name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["rating"]),
            models.Index(fields=["book", "rating"]),
        ]

    def __str__(self):
        return f"{self.book.title} — {self.rating}"