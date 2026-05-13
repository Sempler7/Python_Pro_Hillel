
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('library/', include('library.urls')),
    path('nosql/', include('nosql_app.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
