from django.conf import settings


def site_context(request):
    categories = []
    try:
        from catalog.models import AnimalCategory
        categories = AnimalCategory.objects.filter(is_active=True).prefetch_related('subcategories')
    except Exception:
        pass

    return {
        'site_contacts': settings.SITE_CONTACTS,
        'nav_categories': categories,
        'current_nav': _current_nav(request),
    }


def _current_nav(request):
    if not hasattr(request, 'resolver_match') or request.resolver_match is None:
        return ''
    return request.resolver_match.url_name or ''
