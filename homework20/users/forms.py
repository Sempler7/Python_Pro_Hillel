"""This module contains all forms for users application."""
from typing import Dict

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import UploadedFile

from users.models import UserProfile


class RegistrationForm(UserCreationForm):
    """Registration form for registration a new users."""
    email = forms.EmailField(label="Email")

    class Meta:
        """Metaclass for registration form."""
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self) -> str:
        """
        Validate that email is unique.


        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")
        return email

    def clean_username(self) -> str:
        """
        Validate that username is unique.

        Returns:
            str: username.
        Raises:
            ValidationError: if username is already exists.
        """
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username already exists.")
        return username


class LoginForm(forms.Form):
    """Form for logging in an existing user."""
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self) -> Dict:
        """
        Validate username and password.

        Returns:
            Dict: validated form data.

        Raises:
            ValidationError: if username and password is incorrect.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            cleaned_data["user"] = user

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile data."""

    class Meta:
        """Metaclass for editing user profile form."""
        model = UserProfile
        fields = ("bio", "birth_date", "location", "avatar")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_avatar(self) -> UploadedFile | None:
        """
        Validate avatar file size.

        Returns:
            UserProfile | None: user's avatar file.
        Raises:
            ValidationError: if avatar file size is more than 10 MB.
        """
        avatar = self.cleaned_data.get("avatar")

        if avatar and avatar.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Avatar size must not be greater than 10 MB.")

        return avatar


class PasswordChangeForm(forms.Form):
    """Form for changing user password."""

    current_password = forms.CharField(label="Current password", widget=forms.PasswordInput)
    new_password = forms.CharField(label="New password", widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs) -> None:
        """Initialize form with current user."""
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self) -> str | None:
        """
        Validate current password.

        Returns:
            str | None: current password.
        Raises:
            ValidationError: if current password is incorrect.
        """
        current_password = self.cleaned_data.get("current_password")

        if current_password and not self.user.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")

        return current_password

    def clean(self) -> Dict | None:
        """
        Validate new password confirmation and difference.

        Returns:
            Dict | None: validated form data.

        Raises:
            ValidationError: if new password is incorrect.
        """
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match.")

        if current_password and new_password and current_password == new_password:
            raise forms.ValidationError(
                "New password must be different from current password."
            )

        return cleaned_data
