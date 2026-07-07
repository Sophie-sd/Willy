from django.templatetags.static import static
from django.urls import reverse_lazy


def _admin_logo(request):
    return static('images/logo-willi.png')


UNFOLD = {
    'SITE_TITLE': 'ZOO WILLI',
    'SITE_HEADER': 'ZOO МАГАЗИН WILLI — Адмінпанель',
    'SITE_LOGO': _admin_logo,
    'THEME': 'light',
    'SHOW_VIEW_ON_SITE': True,
    'DASHBOARD_CALLBACK': 'core.dashboard.dashboard_callback',
    'COLORS': {
        'primary': {
            '50': 'oklch(98% 0.02 142)',
            '100': 'oklch(95% 0.04 142)',
            '200': 'oklch(90% 0.08 142)',
            '300': 'oklch(83% 0.12 142)',
            '400': 'oklch(72% 0.18 142)',
            '500': 'oklch(68% 0.20 142)',
            '600': 'oklch(58% 0.18 142)',
            '700': 'oklch(48% 0.16 142)',
            '800': 'oklch(40% 0.12 142)',
            '900': 'oklch(33% 0.10 142)',
            '950': 'oklch(25% 0.08 142)',
        },
        'font': {
            'subtle-light': 'oklch(55% 0.01 80)',
            'default-light': 'oklch(22% 0.02 80)',
            'important-light': 'oklch(15% 0.03 80)',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'command_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Огляд',
                'items': [
                    {
                        'title': 'Панель',
                        'icon': 'dashboard',
                        'link': reverse_lazy('admin:index'),
                    },
                ],
            },
            {
                'title': 'Каталог',
                'separator': True,
                'items': [
                    {
                        'title': 'Товари',
                        'icon': 'shopping_bag',
                        'link': reverse_lazy('admin:catalog_product_changelist'),
                    },
                    {
                        'title': 'Категорії',
                        'icon': 'category',
                        'link': reverse_lazy('admin:catalog_animalcategory_changelist'),
                    },
                    {
                        'title': 'Підкатегорії',
                        'icon': 'folder',
                        'link': reverse_lazy('admin:catalog_subcategory_changelist'),
                    },
                ],
            },
            {
                'title': 'Продажі',
                'items': [
                    {
                        'title': 'Замовлення',
                        'icon': 'receipt_long',
                        'link': reverse_lazy('admin:orders_order_changelist'),
                        'badge': 'core.dashboard.new_orders_badge',
                    },
                ],
            },
            {
                'title': 'Контент',
                'separator': True,
                'items': [
                    {
                        'title': 'FAQ',
                        'icon': 'help',
                        'link': reverse_lazy('admin:core_faqitem_changelist'),
                    },
                    {
                        'title': 'Відгуки',
                        'icon': 'reviews',
                        'link': reverse_lazy('admin:core_review_changelist'),
                        'badge': 'core.dashboard.pending_reviews_badge',
                    },
                    {
                        'title': 'Сторінки',
                        'icon': 'article',
                        'link': reverse_lazy('admin:core_contentpage_changelist'),
                    },
                    {
                        'title': 'Налаштування',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:core_sitesettings_changelist'),
                    },
                ],
            },
        ],
    },
}

TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'menubar': False,
    'plugins': 'link lists code',
    'toolbar': 'undo redo | bold italic underline | bullist numlist | link | code',
    'language': 'uk',
}
