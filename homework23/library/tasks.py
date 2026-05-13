import csv

from celery import shared_task
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from typing import Dict

from library.models import Author, Book, Review


@shared_task(bind=True)
def import_books_from_csv(self, file_path: str, email: str):
    """Асинхронне завдання для імпорту книг з CSV-файлу"""
    created_books = 0
    created_reviews = 0

    with default_storage.open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            author, _ = Author.objects.get_or_create(
                name=row["author"]
            )

            book, book_created = Book.objects.get_or_create(
                title=row["title"],
                author=author,
                defaults={
                    "published_year": int(row["published_year"])
                }
            )

            if book_created:
                created_books += 1

            Review.objects.create(
                book=book,
                reviewer_name="CSV Import",
                text="Imported review",
                rating=int(row["rating"])
            )

            created_reviews += 1

    send_mail(
        subject="Імпорт книг завершено",
        message=(
            f"Імпорт завершено.\n"
            f"Створено книг: {created_books}\n"
            f"Створено відгуків: {created_reviews}"
        ),
        from_email="admin@example.com",
        recipient_list=[email],
    )

    return {
        "created_books": created_books,
        "created_reviews": created_reviews,
    }