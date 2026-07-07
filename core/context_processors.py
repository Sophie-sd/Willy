from core.content_services import get_site_contacts


def site_context(request):
    categories = []
    try:
        from catalog.models import AnimalCategory
        categories = AnimalCategory.objects.filter(is_active=True).prefetch_related('subcategories')
    except Exception:
        pass

    from cart.cart import Cart
    cart = Cart(request)

    return {
        'site_contacts': get_site_contacts(),
        'nav_categories': categories,
        'current_nav': _current_nav(request),
        'cart_count': len(cart),
    }


def _current_nav(request):
    if not hasattr(request, 'resolver_match') or request.resolver_match is None:
        return ''
    return request.resolver_match.url_name or ''
