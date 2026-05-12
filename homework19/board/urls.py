from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # головна сторінка
    path("ads/last-month/", views.ads_last_month, name="ads_last_month"),
    path("ads/<int:ad_id>/", views.ad_detail, name="ad_detail"),
    path("ads/last-month/", views.ads_last_month, name="ads_last_month"),

    path("register/", views.register_view, name="register_view"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile_view"),
    path("profile/change-password/", views.change_password_view, name="change_password_view"),
    path("profile/<str:username>/", views.profile_view, name="profile_view"),
]
