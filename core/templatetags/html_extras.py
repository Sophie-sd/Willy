from django import template
from django.utils.safestring import mark_safe

from core.html_sanitize import sanitize_html as _sanitize_html

register = template.Library()


@register.filter(name='sanitize_html')
def sanitize_html(value):
    """Sanitize admin HTML and mark safe for template output."""
    return mark_safe(_sanitize_html(value))
