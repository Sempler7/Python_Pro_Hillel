import time
from django.http import HttpRequest, JsonResponse

from library.models import Book
from nosql_app.mongo import books_collection


def mongo_books_view(request: HttpRequest) -> JsonResponse:
    """Відображає дані книг з MongoDB та реляційної бази даних
    і порівнює продуктивність їх отримання"""
    if books_collection.count_documents({}) == 0:
        data = []

        books = Book.objects.select_related("author").prefetch_related("reviews")

        for book in books:
            data.append({
                "title": book.title,
                "author": book.author.name,
                "published_year": book.published_year,
                "reviews": [review.rating for review in book.reviews.all()],
            })

        if data:
            books_collection.insert_many(data)

    start = time.perf_counter()
    mongo_books = list(books_collection.find({}, {"_id": 0}))
    mongo_time = time.perf_counter() - start

    start = time.perf_counter()
    relational_books = list(
        Book.objects.select_related("author").prefetch_related("reviews")
    )
    relational_time = time.perf_counter() - start

    return JsonResponse({
        "mongo_time": mongo_time,
        "relational_time": relational_time,
        "mongo_books_count": len(mongo_books),
        "relational_books_count": len(relational_books),
        "mongo_books": mongo_books[:10],
    })