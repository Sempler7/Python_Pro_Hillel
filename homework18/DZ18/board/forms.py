from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Підтвердження паролю")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Користувач з таким ім'ям вже існує.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Користувач з такою електронною поштою вже існує.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Паролі не співпадають.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "birth_date", "location", "avatar"]

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            # Перевірка розміру файлу (макс. 2 МБ)
            if avatar.size > 2 * 1024 * 1024:  # 2 МБ
                raise ValidationError("Розмір зображення не може перевищувати 2 МБ.")
        return avatar


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Поточний пароль"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Новий пароль"
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Підтвердження нового паролю"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # передаємо поточного користувача у форму

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise ValidationError("Поточний пароль введено неправильно.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        current_password = cleaned_data.get("current_password")

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise ValidationError("Нові паролі не співпадають.")
            if current_password and new_password == current_password:
                raise ValidationError("Новий пароль не може співпадати з поточним.")
        return cleaned_data


