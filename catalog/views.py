from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import AnimalCategory, Product, Subcategory

PRODUCTS_PER_PAGE = 12


def _parse_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        return None


def _get_products_queryset(request, base_qs=None):
    qs = base_qs if base_qs is not None else Product.objects.filter(is_available=True)
    qs = qs.select_related('category', 'subcategory')

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    category_slug = request.GET.get('category')
    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    subcategory_slug = request.GET.get('subcategory')
    if subcategory_slug:
        qs = qs.filter(subcategory__slug=subcategory_slug)

    on_sale = request.GET.get('on_sale')
    if on_sale == '1':
        qs = qs.filter(is_on_sale=True)
        now = timezone.now()
        qs = qs.filter(
            Q(sale_starts_at__isnull=True) | Q(sale_starts_at__lte=now),
        ).filter(
            Q(sale_ends_at__isnull=True) | Q(sale_ends_at__gte=now),
        )

    price_min = _parse_decimal(request.GET.get('price_min'))
    price_max = _parse_decimal(request.GET.get('price_max'))
    if price_min is not None:
        qs = qs.filter(price__gte=price_min)
    if price_max is not None:
        qs = qs.filter(price__lte=price_max)

    sort = request.GET.get('sort', 'newest')
    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'newest': '-created_at',
        'popular': '-is_featured',
    }
    qs = qs.order_by(sort_map.get(sort, '-created_at'))

    return qs, q


def _paginate_products(qs, page_num):
    page_num = max(1, int(page_num) if str(page_num).isdigit() else 1)
    total = qs.count()
    start = (page_num - 1) * PRODUCTS_PER_PAGE
    end = start + PRODUCTS_PER_PAGE
    products = list(qs[start:end])
    has_next = end < total
    has_prev = page_num > 1
    return products, page_num, total, has_next, has_prev


def _catalog_context(request, page_title, page_subtitle='', breadcrumbs=None, base_qs=None):
    qs, search_query = _get_products_queryset(request, base_qs)
    page_num = request.GET.get('page', 1)
    products, page, total, has_next, has_prev = _paginate_products(qs, page_num)
    categories = AnimalCategory.objects.filter(is_active=True)

    return {
        'page_title': page_title,
        'page_subtitle': page_subtitle,
        'breadcrumbs': breadcrumbs or [],
        'products': products,
        'categories': categories,
        'total_count': total,
        'page': page,
        'has_next': has_next,
        'has_prev': has_prev,
        'search_query': search_query,
        'current_sort': request.GET.get('sort', 'newest'),
        'filter_category': request.GET.get('category', ''),
        'filter_subcategory': request.GET.get('subcategory', ''),
        'filter_on_sale': request.GET.get('on_sale', ''),
        'filter_price_min': request.GET.get('price_min', ''),
        'filter_price_max': request.GET.get('price_max', ''),
    }


def _render_catalog(request, **context):
    template = (
        'catalog/partials/product_grid.html'
        if request.headers.get('HX-Request')
        else 'catalog/product_list.html'
    )
    return render(request, template, context)


def product_list(request):
    ctx = _catalog_context(
        request,
        page_title='Усі товари',
        page_subtitle='Повний асортимент магазину WILLI',
        breadcrumbs=[{'label': 'Каталог', 'url': None}],
    )
    return _render_catalog(request, **ctx)


def category_detail(request, category_slug):
    category = get_object_or_404(AnimalCategory, slug=category_slug, is_active=True)
    base_qs = Product.objects.filter(is_available=True, category=category)
    ctx = _catalog_context(
        request,
        page_title=f'Товари для {category.name.lower()}',
        page_subtitle=f'Корм, іграшки та аксесуари для {category.name.lower()}',
        breadcrumbs=[
            {'label': 'Каталог', 'url': '/catalog/'},
            {'label': category.name, 'url': None},
        ],
        base_qs=base_qs,
    )
    ctx['current_category'] = category
    ctx['filter_category'] = category.slug
    return _render_catalog(request, **ctx)


def subcategory_detail(request, category_slug, subcategory_slug):
    category = get_object_or_404(AnimalCategory, slug=category_slug, is_active=True)
    subcategory = get_object_or_404(
        Subcategory, category=category, slug=subcategory_slug, is_active=True,
    )
    base_qs = Product.objects.filter(is_available=True, subcategory=subcategory)
    ctx = _catalog_context(
        request,
        page_title=f'{subcategory.name} для {category.name.lower()}',
        page_subtitle=f'Асортимент: {subcategory.name.lower()}',
        breadcrumbs=[
            {'label': 'Каталог', 'url': '/catalog/'},
            {'label': category.name, 'url': category.get_absolute_url()},
            {'label': subcategory.name, 'url': None},
        ],
        base_qs=base_qs,
    )
    ctx['current_category'] = category
    ctx['current_subcategory'] = subcategory
    ctx['filter_category'] = category.slug
    ctx['filter_subcategory'] = subcategory.slug
    return _render_catalog(request, **ctx)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'subcategory'),
        slug=slug,
    )
    related = Product.objects.filter(
        category=product.category,
        is_available=True,
    ).exclude(pk=product.pk)[:4]

    breadcrumbs = [
        {'label': 'Каталог', 'url': '/catalog/'},
        {'label': product.category.name, 'url': product.category.get_absolute_url()},
        {'label': product.subcategory.name, 'url': product.subcategory.get_absolute_url()},
        {'label': product.name, 'url': None},
    ]

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related,
        'breadcrumbs': breadcrumbs,
    })


def search(request):
    ctx = _catalog_context(
        request,
        page_title='Результати пошуку',
        page_subtitle='',
        breadcrumbs=[{'label': 'Пошук', 'url': None}],
    )
    if not ctx['search_query']:
        ctx['page_subtitle'] = 'Введіть запит у поле пошуку'
    elif ctx['total_count'] == 0:
        ctx['page_subtitle'] = 'За вашим запитом нічого не знайдено'
    else:
        ctx['page_subtitle'] = f'Знайдено {ctx["total_count"]} товарів'
    return _render_catalog(request, **ctx)
