from typing import Dict, List, Optional

from django.http import HttpRequest
from ninja import NinjaAPI, Query
from ninja.errors import HttpError

from .models import Genre, Movie, Review
from .schemas import GenreIn, GenreOut, MovieIn, MovieOut, ReviewIn, ReviewOut
from task_manager.auth import AuthBearer

api = NinjaAPI(auth=AuthBearer(), urls_namespace="movies")


@api.post("/genres", response=GenreOut)
def create_genre(request: HttpRequest, payload: GenreIn) -> Genre:
    """Створює новий жанр"""
    genre = Genre.objects.create(**payload.dict())
    return genre


@api.get("/genres", response=List[GenreOut])
def list_genres(request: HttpRequest) -> List[Genre]:
    """Повертає список усіх жанрів"""
    return list(Genre.objects.all())


@api.delete("/genres/{genre_id}")
def delete_genre(request: HttpRequest, genre_id: int) -> Dict[str, bool]:
    """Видаляє жанр за ідентифікатором"""
    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        raise HttpError(404, "Жанр не знайдено")
    genre.delete()
    return {"success": True}


@api.post("/movies", response=MovieOut)
def create_movie(request: HttpRequest, payload: MovieIn) -> Movie:
    """Створює новий фільм"""
    data = payload.dict()
    genre_ids = data.pop("genre_ids")
    movie = Movie.objects.create(**data)
    movie.genres.set(genre_ids)
    return movie


@api.get("/movies", response=List[MovieOut])
def list_movies(
    request: HttpRequest,
    search: Optional[str] = Query(None),
    genre_id: Optional[int] = Query(None),
    min_rating: Optional[float] = Query(None),
    max_rating: Optional[float] = Query(None),
    release_date: Optional[str] = Query(None),
) -> List[Movie]:
    """Повертає список фільмів із можливістю фільтрації"""
    qs = Movie.objects.prefetch_related('genres', 'reviews').all()

    if search:
        qs = qs.filter(title__icontains=search)
    if genre_id:
        qs = qs.filter(genres__id=genre_id)
    if min_rating is not None:
        qs = qs.filter(rating__gte=min_rating)
    if max_rating is not None:
        qs = qs.filter(rating__lte=max_rating)
    if release_date:
        qs = qs.filter(release_date=release_date)

    return list(qs)


@api.get("/movies/{movie_id}", response=MovieOut)
def get_movie(request: HttpRequest, movie_id: int) -> Movie:
    """Повертає фільм за ідентифікатором"""
    try:
        return Movie.objects.prefetch_related('genres', 'reviews').get(id=movie_id)
    except Movie.DoesNotExist:
        raise HttpError(404, "Фільм не знайдено")


@api.put("/movies/{movie_id}", response=MovieOut)
def update_movie(request: HttpRequest, movie_id: int, payload: MovieIn) -> Movie:
    """Оновлює дані фільму"""
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise HttpError(404, "Фільм не знайдено")
    data = payload.dict()
    genre_ids = data.pop("genre_ids")
    for attr, value in data.items():
        setattr(movie, attr, value)
    movie.save()
    movie.genres.set(genre_ids)
    return movie


@api.delete("/movies/{movie_id}")
def delete_movie(request: HttpRequest, movie_id: int) -> Dict[str, bool]:
    """Видаляє фільм за ідентифікатором"""
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise HttpError(404, "Фільм не знайдено")
    movie.delete()
    return {"success": True}


@api.post("/movies/{movie_id}/reviews", response=ReviewOut)
def add_review(request: HttpRequest, movie_id: int, payload: ReviewIn) -> Review:
    """Додає відгук до фільму"""
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise HttpError(404, "Фільм не знайдено")
    if not (0.0 <= payload.score <= 10.0):
        raise HttpError(400, "Оцінка повинна бути від 0 до 10")
    review = Review.objects.create(movie=movie, user=request.user, **payload.dict())
    movie.update_rating()
    return review


@api.get("/movies/{movie_id}/reviews", response=List[ReviewOut])
def list_reviews(request: HttpRequest, movie_id: int) -> List[Review]:
    """Повертає список відгуків до фільму"""
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise HttpError(404, "Фільм не знайдено")
    return list(movie.reviews.all())


@api.delete("/movies/{movie_id}/reviews/{review_id}")
def delete_review(
    request: HttpRequest,
    movie_id: int,
    review_id: int,
) -> Dict[str, bool]:
    """Видаляє відгук користувача до фільму"""
    try:
        review = Review.objects.get(id=review_id, movie_id=movie_id, user=request.user)
    except Review.DoesNotExist:
        raise HttpError(404, "Відгук не знайдено")
    movie = review.movie
    review.delete()
    movie.update_rating()
    return {"success": True}