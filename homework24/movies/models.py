from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """Модель жанру фільмів"""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Повертає назву жанру"""
        return self.name


class Movie(models.Model):
    """Модель фільму"""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(default=0.0)
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_rating(self) -> None:
        """Оновлює середній рейтинг фільму на основі відгуків"""
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = round(sum(r.score for r in reviews) / reviews.count(), 2)
        else:
            self.rating = 0.0
        self.save()

    def __str__(self) -> str:
        """Повертає назву фільму"""
        return self.title


class Review(models.Model):
    """Модель відгуку на фільм"""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)

    def __str__(self) -> str:
        """Повертає рядкове представлення відгуку"""
        return f"Відгук на {self.movie.title} від {self.user.username}"