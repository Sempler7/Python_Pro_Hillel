from typing import Any, Optional
from django.db import models


class UpperCaseCharField(models.CharField):
    """Кастомне поле, яке автоматично зберігає текст у верхньому регістрі."""

    def to_python(self, value: Any) -> Optional[str]:
        """Перетворює значення у Python-тип і приводить рядок до верхнього регістру"""
        value = super().to_python(value)
        if isinstance(value, str):
            return value.upper()
        return value

    def get_prep_value(self, value: Any) -> Optional[str]:
        """Готує значення перед збереженням у базу даних"""
        value = super().get_prep_value(value)
        if isinstance(value, str):
            return value.upper()
        return value