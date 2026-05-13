from django.test import TestCase
from django.contrib.auth import get_user_model

from .forms import CustomUserRegistrationForm, ArticleForm, HexColorField
from .models import Article, Category


class CustomFieldsTests(TestCase):
    """Тести для кастомних полів форми."""

    def test_hex_color_field_valid(self) -> None:
        """Перевіряє, що валідний HEX-код проходить валідацію"""
        field = HexColorField()
        self.assertIsNone(field.validate('#FFAA00'))

    def test_hex_color_field_invalid(self) -> None:
        """Перевіряє, що невалідний HEX-код викликає помилку"""
        field = HexColorField()
        with self.assertRaises(Exception):
            field.validate('red')


class CustomUserRegistrationFormTests(TestCase):
    """Тести для форми реєстрації користувача."""

    def test_invalid_phone_number(self) -> None:
        """Перевіряє, що невалідний номер телефону не проходить валідацію"""
        form = CustomUserRegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '0637770707',
            'password1': 'Pass123!!!',
            'password2': 'Pass123!!!',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class ArticleModelTests(TestCase):
    """Тести для моделі статті."""

    def test_article_title_saved_uppercase(self) -> None:
        """Перевіряє, що заголовок статті зберігається у верхньому регістрі"""
        User = get_user_model()
        user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            phone_number='+380637770707',
            password='Pass123!!!'
        )
        category = Category.objects.create(name='Django')

        article = Article.objects.create(
            title='hello world',
            content='Some content',
            category=category,
            author=user
        )

        self.assertEqual(article.title, 'HELLO WORLD')