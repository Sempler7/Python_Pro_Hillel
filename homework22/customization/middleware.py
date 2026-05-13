import logging
from typing import Callable
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger('custom_logger')


class CustomHeaderMiddleware:
    """Middleware, який додає кастомний HTTP-заголовок до кожної відповіді."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Ініціалізує middleware"""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Обробляє запит та додає кастомний заголовок до відповіді"""
        response = self.get_response(request)
        if response:
            response['X-Custom-Header'] = 'CustomAppHeader'
        return response


class RequestCountMiddleware:
    """Middleware для підрахунку кількості запитів до сервера."""
    request_count = 0

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Ініціалізує middleware"""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Обробляє запит, рахує кількість запитів та додає заголовок з їх кількістю"""
        RequestCountMiddleware.request_count += 1

        logger.info(
            f'Request #{RequestCountMiddleware.request_count}: '
            f'{request.method} {request.path} by {request.user}'
        )

        response = self.get_response(request)
        response['X-Request-Count'] = str(RequestCountMiddleware.request_count)
        return response