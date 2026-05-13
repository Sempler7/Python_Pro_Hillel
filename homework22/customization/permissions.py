import logging
from typing import Any
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView

logger = logging.getLogger('custom_logger')


class IsAuthorOrReadOnly(BasePermission):
    """Дозвіл: тільки автор може змінювати об'єкт, інші — лише читати."""

    message = 'You do not have permission to modify this object.'

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Any
    ) -> bool:
        """Перевіряє права доступу до об'єкта"""
        if request.method in SAFE_METHODS:
            return True

        is_author = obj.author == request.user

        if not is_author:
            logger.warning(
                f'Unauthorized edit attempt by {request.user} on object {obj}'
            )

        return is_author