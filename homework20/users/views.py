"""Views for the working with routing in users application.
Contains function-based views responsible for rendering pages based on template."""
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from users.forms import (
    LoginForm,
    PasswordChangeForm,
    RegistrationForm,
    UserProfileForm,
)
from users.models import UserProfile


def register_view(request: HttpRequest) -> HttpResponse:
    """Register a new user and create user profile."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("user_profile")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    """Login an existing user."""
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("user_profile")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """Log out current user."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """Display user profile."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    return render(request, "users/profile.html", {"profile": profile, }, )


@login_required
def edit_profile_view(request: HttpRequest) -> HttpResponse:
    """Edit current user's profile."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("user_profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    """Change current user's password."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_password"])
            request.user.save()

            update_session_auth_hash(request, request.user)

            messages.success(request, "Password changed successfully.")
            return redirect("user_profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})
