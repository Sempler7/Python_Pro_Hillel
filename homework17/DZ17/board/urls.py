from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # головна сторінка
    path("ads/last-month/", views.ads_last_month, name="ads_last_month"),
    path("ads/<int:ad_id>/", views.ad_detail, name="ad_detail"),
    path("ads/last-month/", views.ads_last_month, name="ads_last_month"),
]
