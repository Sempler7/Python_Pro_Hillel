from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Ad
from django.db.models import Count



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