"""Module containing model definitions for users application."""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Model definition for UserProfile based on Django's User model.

        Fields:
            username: required and unique;
            password: required;
            bio (TextField): not required;
            birth_date (DateField): not required;
            location (CharField): not required;
            avatar (ImageField): not required;"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500,blank=True, verbose_name="Bio")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth Date")
    location = models.CharField(max_length=100, blank=True, verbose_name="Location")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Avatar")

    def __str__(self) -> str:
        """Return username as a string representation of UserProfile class."""
        return self.user.username
