from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Модель тегу для постів"""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Повертає назву тегу"""
        return self.name


class Post(models.Model):
    """Модель посту в блозі"""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Повертає заголовок посту"""
        return self.title


class Comment(models.Model):
    """Модель коментаря до посту"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення коментаря"""
        return f"Коментар від {self.author.username} до {self.post.title}"