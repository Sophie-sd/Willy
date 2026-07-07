def dashboard_callback(request, context):
    from catalog.models import Product
    from core.models import Review
    from orders.models import Order

    context['dashboard_stats'] = [
        {
            'title': 'Нові замовлення',
            'value': Order.objects.filter(status='new').count(),
            'icon': 'receipt_long',
            'link': 'admin:orders_order_changelist',
        },
        {
            'title': 'Не в наявності',
            'value': Product.objects.filter(is_available=False).count(),
            'icon': 'inventory_2',
            'link': 'admin:catalog_product_changelist',
        },
        {
            'title': 'Відгуки на модерації',
            'value': Review.objects.filter(is_published=False).count(),
            'icon': 'reviews',
            'link': 'admin:core_review_changelist',
        },
        {
            'title': 'Акційні товари',
            'value': Product.objects.sale_active().count(),
            'icon': 'local_offer',
            'link': 'admin:catalog_product_changelist',
        },
    ]
    return context


def new_orders_badge(request):
    from orders.models import Order
    count = Order.objects.filter(status='new').count()
    return str(count) if count else ''


def pending_reviews_badge(request):
    from core.models import Review
    count = Review.objects.filter(is_published=False).count()
    return str(count) if count else ''
