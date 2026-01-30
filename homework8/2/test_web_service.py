"""Тестування WebService з використанням моків."""

import unittest
from unittest.mock import patch, MagicMock
import requests

from web_service import WebService


class TestWebService(unittest.TestCase):
    """Тестування WebService з використанням моків."""

    def setUp(self):
        self.service = WebService()
        self.test_url = "http://fake-url.com"

    @patch("web_service.requests.get")
    def test_get_data_success(self, mock_get):
        """Тестування успішного отримання даних"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = self.service.get_data(self.test_url)
        self.assertEqual(result, {"data": "test"})

        # Перевірка виклику з таймаутом
        mock_get.assert_called_once_with(self.test_url, timeout=5)

    @patch("web_service.requests.get")
    def test_get_data_error(self, mock_get):
        """Тестування обробки помилки при отриманні даних"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError("Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            self.service.get_data(self.test_url)

        # Перевірка виклику з таймаутом
        mock_get.assert_called_once_with(self.test_url, timeout=5)


if __name__ == "__main__":
    unittest.main()
