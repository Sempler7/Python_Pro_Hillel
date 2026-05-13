from django.urls import path
from library import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/unoptimized/", views.unoptimized_books, name="unoptimized_books"),
    path("books/optimized/", views.optimized_books, name="optimized_books"),
    path("stats/", views.stats_view, name="stats"),
    path("raw-sql/", views.raw_sql_view, name="raw_sql"),
    path("import/", views.import_books_view, name="import_books"),
    path("task/<str:task_id>/", views.task_status_view, name="task_status"),
    path("index-test/", views.indexed_query_test, name="indexed_query_test"),
]
