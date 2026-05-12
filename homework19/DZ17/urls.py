
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("board.urls")),  # підключаємо всі маршрути з додатку board

    path('books1/', include('books1.urls')),
    path("api-auth/", include("rest_framework.urls")),
    path("books1/api/", include("books1.urls")),

    path("books1/api/auth/token/", obtain_auth_token, name="api-token-auth"),
    path("books1/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("books1/api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("books1/api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

]
