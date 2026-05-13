from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("greeting/", views.greeting_view, name="greeting"),
    path("logout/", views.logout_view, name="logout"),
]