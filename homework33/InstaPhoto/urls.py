
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
