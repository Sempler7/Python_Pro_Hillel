from django.urls import path
from nosql_app import views

urlpatterns = [
    path("books/", views.mongo_books_view, name="mongo_books"),
]
