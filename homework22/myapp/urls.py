
from django.contrib import admin  # type: ignore[import-untyped]
from django.urls import path, include  # type: ignore[import-untyped]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customization.urls')),
]
