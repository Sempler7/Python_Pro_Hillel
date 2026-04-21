from django.conf import settings 
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_ratelimit.exceptions import Ratelimited


def home(request):
    return render(request, "home.html")


from django.shortcuts import render

# Простий генератор (як був)
packing_lists = {
    "пляж": {
        "літо": ["Купальник", "Сонцезахисний крем", "Капелюх", "Шльопанці"],
        "зима": ["Теплі речі", "Аптечка", "Універсальний адаптер"]
    },
    "гори": {
        "літо": ["Трекінгові черевики", "Репелент", "Палатка"],
        "зима": ["Термобілизна", "Лижі", "Аптечка"]
    }
}

# def packing_generator(request):
#     items = []
#     if request.method == "POST":
#         destination = request.POST.get("destination_type")
#         season = request.POST.get("season")
#         items = packing_lists.get(destination, {}).get(season, [])
#     return render(request, "packing.html", {"items": items})


# Розширений генератор
def packing_list_view(request):
    packing_list = {}
    selected = {}

    if request.method == "POST":
        trip_type = request.POST.get("trip_type")
        weather = request.POST.get("weather")
        duration = request.POST.get("duration")

        selected = {
            "trip_type": trip_type,
            "weather": weather,
            "duration": duration,
        }

        packing_list = {
            "Документи": [
                "Паспорт або ID",
                "Банківська картка",
                "Готівка",
                "Квитки / бронювання",
                "Страхування",
            ],
            "Гігієна": [
                "Зубна щітка",
                "Зубна паста",
                "Дезодорант",
                "Шампунь",
                "Сонцезахисний крем",
            ],
            "Електроніка": [
                "Телефон",
                "Зарядка для телефону",
                "Павербанк",
                "Навушники",
            ],
            "Здоров’я": [
                "Особисті ліки",
                "Знеболювальне",
                "Антисептик",
                "Міні-аптечка",
            ],
            "Одяг": [
                "Нижня білизна",
                "Шкарпетки",
                "Футболки",
                "Зручне взуття",
                "Одяг для сну",
            ],
            "Додатково": [
                "Пляшка для води",
                "Невелика сумка або рюкзак",
            ],
        }

        # Логіка залежно від типу подорожі
        if trip_type == "beach":
            packing_list["Одяг"] += ["Купальник або плавки", "Сандалі", "Капелюх"]
            packing_list["Додатково"] += ["Пляжний рушник", "Сонцезахисні окуляри"]

        elif trip_type == "city":
            packing_list["Одяг"] += ["Легка куртка", "Повсякденний одяг"]
            packing_list["Додатково"] += ["Міська карта або путівник", "Компактна сумка"]

        elif trip_type == "hiking":
            packing_list["Одяг"] += ["Трекінгове взуття", "Термобілизна", "Дощовик"]
            packing_list["Додатково"] += ["Рюкзак", "Ліхтарик", "Контейнер для перекусу"]

        elif trip_type == "business":
            packing_list["Одяг"] += ["Діловий одяг", "Класичне взуття"]
            packing_list["Електроніка"] += ["Ноутбук", "Зарядка для ноутбука"]
            packing_list["Документи"] += ["Робочі документи"]

        # Логіка залежно від погоди
        if weather == "hot":
            packing_list["Одяг"] += ["Шорти", "Легкий одяг"]
            packing_list["Гігієна"] += ["Крем після сонця"]

        elif weather == "cold":
            packing_list["Одяг"] += ["Теплий светр", "Куртка", "Рукавички", "Шарф"]

        elif weather == "rain":
            packing_list["Одяг"] += ["Водонепроникна куртка"]
            packing_list["Додатково"] += ["Парасолька"]

        # Логіка залежно від тривалості
        if duration == "short":
            packing_list["Одяг"] += ["Одяг на 2–3 дні"]

        elif duration == "medium":
            packing_list["Одяг"] += ["Одяг на 4–7 днів"]

        elif duration == "long":
            packing_list["Одяг"] += ["Одяг на 8+ днів", "Мішок для брудних речей"]

    return render(
        request,
        "packing_list.html",
        {
            "packing_list": packing_list,
            "selected": selected,
        }
    )


def rate_limiter_view(request, *args, **kwargs):
    return render(request, 'ratelimit.html', status=429)


def view_404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler_403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('Sorry too many requests, please wait', status=429)
    return HttpResponseForbidden('Forbidden')


def home_view(request):
    return render(request, 'home.html', status=200)
