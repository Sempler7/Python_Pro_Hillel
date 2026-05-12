"""This module provides service functions for users application."""
from typing import Tuple

from django.db import connection


def get_user_by_username(username: str) -> Tuple | None:
    """
    Gets user by username using parameterized SQL query.

    Args:
        username (str): user's username.

    Returns:
        Tuple | None: user data or None.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, username, email
            FROM auth_user
            WHERE username = %s
            """,
            [username],
        )

        return cursor.fetchone()
