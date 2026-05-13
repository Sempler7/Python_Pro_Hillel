from django import template
from django.forms import BoundField

register = template.Library()


@register.filter
def cut_chars(value: str, count: int = 50) -> str:
    """Обрізає рядок до заданої кількості символів"""
    value = str(value)
    count = int(count)
    return value[:count] + ('...' if len(value) > count else '')


@register.simple_tag
def app_name() -> str:
    """Повертає назву застосунку"""
    return 'Customization'


@register.filter(name='add_class')
def add_class(field: BoundField, css: str) -> str:
    """Додає CSS-клас до віджета поля форми"""
    return field.as_widget(attrs={"class": css})