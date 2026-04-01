from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                # головна сторінка
    path('about/', views.about, name='about'),        # сторінка "Про нас"
    path('contact/', views.ContactView.as_view(), name='contact'),  # сторінка "Контакти"
    path('services/', views.ServiceView.as_view(), name='services'), # сторінка "Послуги"
]
