from django.shortcuts import render, redirect
from django.utils import timezone
from urllib.parse import quote, unquote
from django.http import HttpRequest, HttpResponse

COOKIE_NAME = "username"
COOKIE_MAX_AGE = 60 * 60 * 24 * 7


def login_view(request: HttpRequest) -> HttpResponse:
    """Обробляє сторінку входу користувача"""
    if request.method == "POST":
        username = request.POST.get("username")
        age = request.POST.get("age")

        if not username or not age:
            return render(request, "accounts/login.html", {
                "error": "Введіть ім'я та вік."
            })

        response = redirect("greeting")

        response.set_cookie(
            COOKIE_NAME,
            quote(username),
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite="Lax",
        )

        request.session["age"] = age
        request.session["last_activity"] = timezone.now().isoformat()

        return response

    return render(request, "accounts/login.html")


def greeting_view(request: HttpRequest) -> HttpResponse:
    """Відображає сторінку привітання користувача"""
    username_cookie = request.COOKIES.get(COOKIE_NAME)
    age = request.session.get("age")

    if not username_cookie or not age:
        return redirect("login")

    if not username_cookie:
        return redirect("login")

    username = unquote(username_cookie)

    request.session["last_activity"] = timezone.now().isoformat()

    response = render(request, "accounts/greeting.html", {
        "username": username,
        "age": age,
    })

    response.set_cookie(
        COOKIE_NAME,
        quote(username),
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="Lax",
    )

    return response


def logout_view(request: HttpRequest) -> HttpResponse:
    """Виконує вихід користувача з системи"""
    request.session.flush()

    response = redirect("login")
    response.delete_cookie(COOKIE_NAME)

    return response
