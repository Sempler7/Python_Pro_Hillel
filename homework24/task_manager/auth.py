from typing import Optional

from ninja.security import HttpBearer
from django.contrib.auth.models import User


class AuthBearer(HttpBearer):
    """Кастомна схема автентифікації через Bearer-токен"""

    def authenticate(self, request, token: str) -> Optional[User]:
        """Аутентифікує користувача за токеном"""
        try:
            user = User.objects.get(username=token)
            request.user = user
            return user
        except User.DoesNotExist:
            return None