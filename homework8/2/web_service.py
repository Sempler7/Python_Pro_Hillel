"""Мокування за допомогою unittest.mock"""

from typing import Dict
import requests


class WebService:  # pylint: disable=too-few-public-methods
    """Сервіс для отримання даних з вебсайту."""

    @staticmethod
    def get_data(url: str) -> Dict:
        """Виконує GET-запит до вказаного URL та повертає JSON-відповідь"""
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
