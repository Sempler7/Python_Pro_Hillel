from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from django.core.exceptions import ValidationError

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True, max_length=500)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def active_ads_count(self):
        return self.ads.filter(is_active=True).count()

def validate_positive(value):
    if value <= 0:
        raise ValidationError("Ціна повинна бути додатним числом.")


class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name='ads', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name='ads', on_delete=models.CASCADE)


    """Повертає короткий опис (до 100 символів)."""
    def short_description(self):
        return (self.description[:97] + "...") if len(self.description) > 100 else self.description


    """Деактивує оголошення, якщо минуло більше 30 днів від створення."""
    def deactivate_if_expired(self):
        if self.is_active and timezone.now() - self.created_at > timedelta(days=30):
            self.is_active = False
            self.save()

    def comments_count(self):
        return self.comments.count()


"""Через сигнал post_save"""
@receiver(post_save, sender=Ad)
def check_expiration(sender, instance, **kwargs):
        instance.deactivate_if_expired()       #Ограничение: проверка будет происходить только при сохранении объекта.

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)


@receiver(post_save, sender=Ad)
def send_email_on_create(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="Ваше оголошення створено",
            message=f"Ви створили оголошення: {instance.title}",
            from_email="noreply@mysite.com",
            recipient_list=[instance.user.email],
        )




















