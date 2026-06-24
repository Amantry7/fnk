import re

from django import template

register = template.Library()


@register.filter
def tel(value):
    """Превращает телефон в формат для href=tel: оставляя + и цифры."""
    if not value:
        return ''
    return re.sub(r'[^\d+]', '', str(value))
