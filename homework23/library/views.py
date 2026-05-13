import time

from celery.result import AsyncResult
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.db import connection
from django.db.models import Avg, Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from library.models import Author, Book, Review
from library.tasks import import_books_from_csv


def unoptimized_books(request: HttpRequest) -> JsonResponse:
    """Виконує запит без ORM-оптимізації"""
    start = time.perf_counter()

    books = Book.objects.all()

    data = []
    for book in books:
        data.append({
            "title": book.title,
            "author": book.author.name,
            "reviews": [review.rating for review in book.reviews.all()],
        })

    duration = time.perf_counter() - start

    return JsonResponse({
        "type": "without optimization",
        "time": duration,
        "queries": len(connection.queries),
        "items": len(data),
    })


def optimized_books(request: HttpRequest) -> JsonResponse:
    """Виконує оптимізований ORM-запит"""
    start = time.perf_counter()

    books = (
        Book.objects
        .select_related("author")
        .prefetch_related("reviews")
    )

    data = []
    for book in books:
        data.append({
            "title": book.title,
            "author": book.author.name,
            "reviews": [review.rating for review in book.reviews.all()],
        })

    duration = time.perf_counter() - start

    return JsonResponse({
        "type": "with select_related and prefetch_related",
        "time": duration,
        "queries": len(connection.queries),
        "items": len(data),
    })


def book_list(request: HttpRequest) -> HttpResponse:
    """Відображає список книг з авторами"""
    cached_books = cache.get("book_list")

    if cached_books is None:
        books = (
            Book.objects
            .select_related("author")
            .values(
                "title",
                "author__name",
            )
        )

        cached_books = list(books)
        cache.set("book_list", cached_books, 60 * 5)

    return render(request, "library/book_list.html", {
        "books": cached_books
    })


def stats_view(request: HttpRequest) -> HttpResponse:
    """Відображає статистику книг та авторів"""
    books = (
        Book.objects
        .select_related("author")
        .annotate(
            reviews_count=Count("reviews"),
            avg_rating=Avg("reviews__rating"),
        )
        .order_by("-reviews_count", "-avg_rating")
    )

    authors = (
        Author.objects
        .annotate(avg_book_rating=Avg("books__reviews__rating"))
        .order_by("-avg_book_rating")
    )

    return render(request, "library/stats.html", {
        "books": books,
        "authors": authors,
    })


def raw_sql_view(request: HttpRequest) -> JsonResponse:
    """Виконує raw SQL-запити до бази даних"""
    min_reviews = int(request.GET.get("min_reviews", 10))

    # Захист від SQL injection: параметри передаємо окремо, не через f-string.
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT a.id, a.name, COUNT(r.id) AS total_reviews
            FROM library_author a
                     JOIN library_book b ON b.author_id = a.id
                     JOIN library_review r ON r.book_id = b.id
            GROUP BY a.id, a.name
            HAVING COUNT(r.id) > %s
            """,
            [min_reviews],
        )
        authors = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM library_book
            """
        )
        total_books = cursor.fetchone()[0]

    return JsonResponse({
        "authors_with_many_reviews": authors,
        "total_books": total_books,
    })


def import_books_view(request: HttpRequest) -> HttpResponse:
    """Обробляє імпорт книг із CSV-файлу"""
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        email = request.POST["email"]

        file_path = default_storage.save(f"imports/{csv_file.name}", csv_file)

        task = import_books_from_csv.delay(file_path, email)

        return redirect("task_status", task_id=task.id)

    return render(request, "library/import.html")


def task_status_view(request: HttpRequest, task_id: str) -> HttpResponse:
    """Відображає статус Celery-завдання"""
    task = AsyncResult(task_id)

    return render(request, "library/task_status.html", {
        "task_id": task_id,
        "status": task.status,
        "result": task.result,
    })


def indexed_query_test(request: HttpRequest) -> JsonResponse:
    """Виконує тест продуктивності запиту з індексами"""
    runs = int(request.GET.get("runs", 5))

    times = []

    for _ in range(runs):
        start = time.perf_counter()

        list(
            Review.objects
            .filter(rating=5)
            .select_related("book")
        )

        duration = time.perf_counter() - start
        times.append(duration)

    avg_time = sum(times) / len(times)

    return JsonResponse({
        "runs": runs,
        "times": times,
        "avg_time": avg_time,
        "min_time": min(times),
        "max_time": max(times),
        "queries": len(connection.queries),
    })
