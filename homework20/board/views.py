from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Ad
from django.db.models import Count

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistrationForm, UserProfileForm, PasswordChangeForm
from .models import UserProfile



def home(request):
    return render(request, "board/home.html")


def ads_last_month(request):
    # обчислюємо дату місяць тому
    last_month = timezone.now() - timedelta(days=30)
    # вибираємо всі оголошення, створені за цей період
    ads = Ad.objects.filter(created_at__gte=last_month)
    active_ads = Ad.objects.filter(category__name="Авто", is_active=True)

    ads_with_comments = Ad.objects.annotate(num_comments=Count("comments"))
    for ad in ads_with_comments:
        print(ad.title, ad.num_comments)

    user_ads = Ad.objects.filter(user__username="Vit")

    return render(
        request,
        "board/ads_last_month.html",
        {
            "ads": ads,
            "active_ads": active_ads,
            "ads_with_comments": ads_with_comments,
            "user_ads": user_ads,
        },
    )


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, "board/ad_detail.html", {"ad": ad})


# --- Реєстрація ---
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            # створюємо профіль для нового користувача

            login(request, user)
            return redirect("profile_view", username=user.username)
    else:
        form = RegistrationForm()
    return render(request, "board/register.html", {"form": form})


# --- Редагування профілю ---
@login_required
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль оновлено успішно.")
            return redirect("profile_view", username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "board/edit_profile.html", {"form": form})


# --- Зміна паролю ---
@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # щоб не вилогінювало
            messages.success(request, "Пароль змінено успішно.")
            return redirect("profile_view", username=request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "board/change_password.html", {"form": form})


# --- Перегляд профілю ---
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "board/profile.html", {"profile": profile, "user_obj": user})
