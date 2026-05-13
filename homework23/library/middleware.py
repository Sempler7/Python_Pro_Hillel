from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from typing import Callable


class AnonymousBookListCacheMiddleware:
    """
    Middleware для кешування сторінки списку книг для анонімних користувачів
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Ініціалізує middleware"""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Обробляє HTTP-запит і виконує кешування сторінки для анонімних користувачів"""
        if (
            request.path == "/library/books/"
            and not request.user.is_authenticated
            and request.method == "GET"
        ):
            cache_key = "anonymous_book_list_page"
            cached_response = cache.get(cache_key)

            if cached_response:
                return cached_response

            response = self.get_response(request)
            cache.set(cache_key, response, 60 * 2)

            return response

        return self.get_response(request)