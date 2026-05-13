import logging
import re
from typing import Any, Dict

from django import forms
from django.contrib.auth.forms import UserCreationForm
from better_profanity import profanity

from .models import Article, CustomUser, PHONE_REGEX
from .widgets import CustomSelectWidget

logger = logging.getLogger('custom_logger')

profanity.load_censor_words()


def censor_text(value: str) -> str:
    """Цензурує нецензурні слова у тексті"""
    censored_value = profanity.censor(value)
    if value != censored_value:
        logger.info('Profanity was censored in submitted text')
    return censored_value


class HexColorField(forms.CharField):
    """Кастомне поле для перевірки HEX-коду кольору."""

    def validate(self, value: str) -> None:
        """Перевіряє коректність HEX-коду"""
        super().validate(value)
        if not value:
            return
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
            raise forms.ValidationError('Enter a valid HEX code, e.g. #FFAA00.')


class ArticleForm(forms.ModelForm):
    """Форма для створення та редагування статті."""
    color = HexColorField(required=False)

    class Meta:
        model = Article
        fields = ['title', 'content', 'metadata', 'category', 'status']
        widgets = {
            'category': CustomSelectWidget(),
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_title(self) -> str:
        """Очищає та цензурує заголовок"""
        title = self.cleaned_data['title']
        return censor_text(title)

    def clean_content(self) -> str:
        """Очищає та цензурує контент статті"""
        content = self.cleaned_data['content']
        return censor_text(content)

    def clean_metadata(self) -> Dict[str, Any]:
        """Перевіряє, що metadata є валідним JSON-об'єктом"""
        metadata = self.cleaned_data['metadata']
        if not isinstance(metadata, dict):
            raise forms.ValidationError('Metadata must be a valid JSON object.')
        return metadata


class PhoneNumberFormField(forms.CharField):
    """Кастомне поле для валідації номера телефону."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Ініціалізує поле та додає placeholder"""
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({
            'placeholder': '+380637770707'
        })

    def validate(self, value: str) -> None:
        """Перевіряє формат номера телефону"""
        super().validate(value)

        if not re.match(PHONE_REGEX, value):
            raise forms.ValidationError(
                'Phone number must be in format +380XXXXXXXXX.'
            )


class CustomUserRegistrationForm(UserCreationForm):
    """Форма реєстрації користувача з кастомним полем телефону."""
    phone_number = PhoneNumberFormField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')