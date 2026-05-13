from ninja import Schema
from typing import List, Optional
from datetime import date, datetime


class GenreIn(Schema):
    """Схема для створення жанру"""

    name: str


class GenreOut(Schema):
    """Схема відповіді для жанру"""

    id: int
    name: str


class ReviewIn(Schema):
    """Схема для створення відгуку"""

    text: str
    score: float


class ReviewOut(Schema):
    """Схема відповіді для відгуку"""

    id: int
    user_id: int
    text: str
    score: float
    created_at: datetime


class MovieIn(Schema):
    """Схема для створення або оновлення фільму"""

    title: str
    description: str = ""
    release_date: Optional[date] = None
    rating: float = 0.0
    genre_ids: List[int] = []


class MovieOut(Schema):
    """Схема відповіді для фільму"""

    id: int
    title: str
    description: str
    release_date: Optional[date]
    rating: float
    genres: List[GenreOut]
    reviews: List[ReviewOut]
    created_at: datetime