from typing import Optional, Dict, Any
from django.forms.widgets import Select


class CustomSelectWidget(Select):


    def __init__(self, attrs: Optional[Dict[str, Any]] = None) -> None:
        """Ініціалізує віджет та додає кастомні CSS-класи"""
        attrs = attrs or {}
        attrs.update({'class': 'form-select custom-select'})
        super().__init__(attrs)