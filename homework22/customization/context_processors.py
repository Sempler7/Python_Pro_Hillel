from typing import Dict, Any
from django.http import HttpRequest

from .models import Category


def global_data(request: HttpRequest) -> Dict[str, Any]:
    """Додає глобальні дані до контексту шаблонів"""
    return {
        'site_title': 'Customization',
        'all_categories': Category.objects.values('id', 'name')[:10],
    }