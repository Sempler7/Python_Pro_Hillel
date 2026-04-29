from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Ad, Category

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Авто", description="Транспорт")

    def test_deactivate_if_expired(self):
        ad = Ad.objects.create(
            title="Test Ad",
            description="Test description",
            price=100,
            user=self.user,
            category=self.category
        )
        # штучно робимо оголошення старішим за 30 днів
        ad.created_at = ad.created_at - timedelta(days=31)
        ad.save()

        ad.deactivate_if_expired()
        self.assertFalse(ad.is_active)
