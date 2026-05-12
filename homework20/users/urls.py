"""URL configuration for users application in my_site project.
The `urlpatterns` list routes URLs to corresponding views."""
from typing import List

from django.urls import path, URLPattern, URLResolver

from users.views import (
    change_password_view,
    edit_profile_view,
    login_view,
    logout_view,
    profile_view,
    register_view,
)

urlpatterns: List[URLPattern | URLResolver] = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/edit/", edit_profile_view, name="edit_profile"),
    path("profile/", profile_view, name="user_profile"),
    path("password/change/", change_password_view, name="change_password"),
]
