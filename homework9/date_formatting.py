"""Модуль для перетворення дати з формату DD/MM/YYYY у формат YYYY-MM-DD"""

from datetime import datetime


def convert_date(date_str: str) -> str:
    """Перетворює дату з формату DD/MM/YYYY у формат YYYY-MM-DD"""
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Неправильний формат дати. Використовуйте DD/MM/YYYY.")  from exc


print(convert_date("30/01/2026"))
