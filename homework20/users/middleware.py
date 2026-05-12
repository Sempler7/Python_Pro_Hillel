"""This module provides middleware for users application."""
import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


class AccessLogMiddleware:
    """Log all attempts to access protected pages."""

    def __init__(self, get_response: Callable) -> None:
        """Initialize middleware."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Log access attempts to protected pages."""
        protected_paths = [
            "/users/profile/",
            "/users/profile/edit/",
            "/users/password/change/",
            "/users/logout/",
        ]
        if request.path in protected_paths:
            username = (
                request.user.username
                if request.user.is_authenticated
                else "Anonymous"
            )

            logger.info(f"Protected page access attempt: path={request.path}, user={username}", )
        return self.get_response(request)


class ErrorHandlingMiddleware:
    """Handle 404 and 500 errors."""

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Initialize middleware."""
        response = self.get_response(request)

        if response.status_code == 404:
            logger.exception("Page not found")
            return render(request, "users/404.html", status=404)

        if response.status_code == 500:
            logger.exception("Internal server error")
            return render(request, "users/500.html", status=500)
        return response
