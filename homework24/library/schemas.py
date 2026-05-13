from ninja import Schema
from typing import Optional
from datetime import date, datetime


class BookIn(Schema):
    """Схема для створення або оновлення книги"""

    title: str
    author: str
    genre: str


class BookOut(Schema):
    """Схема відповіді для книги"""

    id: int
    title: str
    author: str
    genre: str
    is_available: bool
    created_at: datetime


class RentalIn(Schema):
    """Схема для створення оренди книги"""

    due_date: date


class RentalOut(Schema):
    """Схема відповіді для оренди книги"""

    id: int
    book_id: int
    user_id: int
    rented_at: datetime
    due_date: date
    returned_at: Optional[datetime]