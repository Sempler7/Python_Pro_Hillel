from typing import Dict, List, Optional

from django.http import HttpRequest
from django.utils import timezone
from ninja import NinjaAPI, Query
from ninja.errors import HttpError

from .models import Book, Rental
from .schemas import BookIn, BookOut, RentalIn, RentalOut
from task_manager.auth import AuthBearer

api = NinjaAPI(auth=AuthBearer(), urls_namespace="library")


@api.post("/books", response=BookOut)
def create_book(request: HttpRequest, payload: BookIn) -> Book:
    """Створює нову книгу"""
    book = Book.objects.create(**payload.dict())
    return book


@api.get("/books", response=List[BookOut])
def list_books(
    request: HttpRequest,
    search: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
) -> List[Book]:
    """Повертає список книг із можливістю фільтрації"""
    qs = Book.objects.all()
    if search:
        qs = qs.filter(title__icontains=search)
    if author:
        qs = qs.filter(author__icontains=author)
    if genre:
        qs = qs.filter(genre__icontains=genre)
    return list(qs)


@api.get("/books/{book_id}", response=BookOut)
def get_book(request: HttpRequest, book_id: int) -> Book:
    """Повертає книгу за ідентифікатором"""
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HttpError(404, "Книгу не знайдено")


@api.put("/books/{book_id}", response=BookOut)
def update_book(request: HttpRequest, book_id: int, payload: BookIn) -> Book:
    """Оновлює дані книги"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HttpError(404, "Книгу не знайдено")
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


@api.delete("/books/{book_id}")
def delete_book(request: HttpRequest, book_id: int) -> Dict[str, bool]:
    """Видаляє книгу за ідентифікатором"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HttpError(404, "Книгу не знайдено")
    book.delete()
    return {"success": True}


@api.post("/books/{book_id}/rent", response=RentalOut)
def rent_book(request: HttpRequest, book_id: int, payload: RentalIn) -> Rental:
    """Орендує доступну книгу для авторизованого користувача"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HttpError(404, "Книгу не знайдено")
    if not book.is_available:
        raise HttpError(400, "Книга вже орендована")
    rental = Rental.objects.create(
        book=book,
        user=request.user,
        due_date=payload.due_date
    )
    book.is_available = False
    book.save()
    return rental


@api.post("/books/{book_id}/return", response=RentalOut)
def return_book(request: HttpRequest, book_id: int) -> Rental:
    """Повертає орендовану книгу"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HttpError(404, "Книгу не знайдено")
    try:
        rental = Rental.objects.get(book=book, user=request.user, returned_at=None)
    except Rental.DoesNotExist:
        raise HttpError(404, "Активну оренду не знайдено")
    rental.returned_at = timezone.now()
    rental.save()
    book.is_available = True
    book.save()
    return rental


@api.get("/rentals", response=List[RentalOut])
def list_rentals(request: HttpRequest) -> List[Rental]:
    """Повертає список оренд авторизованого користувача"""
    return list(Rental.objects.filter(user=request.user))