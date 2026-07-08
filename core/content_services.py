from types import SimpleNamespace

from django.conf import settings

from core.models import ContentPage, DeliverySection, FaqItem, HomeBlock, Review, SiteSettings
from core.page_content import (
    CONTACTS_PAGE,
    DELIVERY_PAGE,
    FAQ_PAGE,
    PROMOTIONS_PAGE,
    REVIEWS,
)

DEFAULT_HOME_BLOCKS = {
    HomeBlock.KEY_CATEGORIES: {
        'label': 'Категорії',
        'is_visible': True,
        'reviews_source': '',
        'eyebrow': 'Що шукаєте?',
        'heading': 'Оберіть категорію',
        'subheading': '',
        'perk_1': '',
        'perk_2': '',
        'perk_3': '',
        'cta_text': '',
        'cta_url': '',
    },
    HomeBlock.KEY_SALE: {
        'label': 'Акційні товари',
        'is_visible': True,
        'reviews_source': '',
        'eyebrow': 'Акція',
        'heading': 'Акційні товари',
        'subheading': '',
        'perk_1': '',
        'perk_2': '',
        'perk_3': '',
        'cta_text': '',
        'cta_url': '',
    },
    HomeBlock.KEY_REVIEWS: {
        'label': 'Відгуки',
        'is_visible': True,
        'reviews_source': HomeBlock.REVIEWS_ADMIN,
        'eyebrow': 'Відгуки',
        'heading': 'Що кажуть клієнти',
        'subheading': '',
        'perk_1': '',
        'perk_2': '',
        'perk_3': '',
        'cta_text': '',
        'cta_url': '',
    },
    HomeBlock.KEY_CTA: {
        'label': 'CTA-блок',
        'is_visible': True,
        'reviews_source': '',
        'eyebrow': 'Доставка по всій Україні',
        'heading': 'Готові зробити замовлення?',
        'subheading': '',
        'perk_1': 'Доставка Новою Поштою та Укрпоштою',
        'perk_2': 'Перевірені бренди для ваших улюбленців',
        'perk_3': 'Магазин у Києві',
        'cta_text': 'Перейти в каталог',
        'cta_url': '/catalog/',
    },
}

TEXT_FIELD_KEYS = (
    'eyebrow', 'heading', 'subheading',
    'perk_1', 'perk_2', 'perk_3', 'cta_text', 'cta_url',
)


def get_site_contacts():
    try:
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return obj.as_dict()
    except Exception:
        return settings.SITE_CONTACTS


def get_content_page(slug, fallback):
    try:
        page = ContentPage.objects.get(slug=slug)
        data = page.as_dict()
        for key, value in fallback.items():
            if key not in data or not data[key]:
                data[key] = value
        return data
    except ContentPage.DoesNotExist:
        return fallback


def get_faq_page():
    page = get_content_page('faq', FAQ_PAGE)
    items = list(
        FaqItem.objects.filter(is_active=True).values('question', 'answer'),
    )
    if items:
        page = {**page, 'items': items}
    elif 'items' not in page:
        page['items'] = FAQ_PAGE['items']
    return page


def get_reviews():
    return get_reviews_for_block(None)


def _default_review_samples():
    return [{**item, 'rating': 5} for item in REVIEWS]


def _reviews_from_queryset(queryset):
    return list(queryset.order_by('-created_at').values('text', 'author', 'rating'))


def is_google_reviews_configured():
    import os
    from core.models import SiteSettings

    api_key = os.environ.get('GOOGLE_PLACES_API_KEY', '').strip()
    if not api_key:
        return False
    try:
        settings_obj = SiteSettings.objects.get(pk=1)
        return bool(settings_obj.google_place_id)
    except SiteSettings.DoesNotExist:
        return False


def get_reviews_for_block(block):
    source = HomeBlock.REVIEWS_ADMIN
    if block is not None:
        source = getattr(block, 'reviews_source', None) or HomeBlock.REVIEWS_ADMIN

    if source == HomeBlock.REVIEWS_CUSTOM:
        reviews = []
        if block is not None:
            for index in range(1, 4):
                text = getattr(block, f'custom_review_{index}_text', '').strip()
                author = getattr(block, f'custom_review_{index}_author', '').strip()
                if text:
                    reviews.append({
                        'text': text,
                        'author': author or 'Клієнт',
                        'rating': 5,
                    })
        return reviews or _default_review_samples()

    if source == HomeBlock.REVIEWS_SAMPLES:
        return _default_review_samples()

    if source == HomeBlock.REVIEWS_GOOGLE:
        google_reviews = _reviews_from_queryset(
            Review.objects.filter(
                is_published=True,
                show_on_homepage=True,
                source=Review.SOURCE_GOOGLE,
            ),
        )
        if google_reviews:
            return google_reviews
        admin_reviews = _reviews_from_queryset(
            Review.objects.filter(is_published=True, show_on_homepage=True),
        )
        return admin_reviews or _default_review_samples()

    admin_reviews = _reviews_from_queryset(
        Review.objects.filter(is_published=True, show_on_homepage=True),
    )
    if admin_reviews:
        return admin_reviews

    return _default_review_samples()


def get_map_embed_url():
    contacts = get_site_contacts()
    if contacts.get('map_embed_url'):
        return contacts['map_embed_url']
    return CONTACTS_PAGE.get('map_embed_url', '')


def get_google_maps_url():
    contacts = get_site_contacts()
    if contacts.get('google_maps_url'):
        return contacts['google_maps_url']
    lat = contacts['map_lat']
    lng = contacts['map_lng']
    return f'https://www.google.com/maps/search/?api=1&query={lat},{lng}'


def get_promotions_page():
    return get_content_page('promotions', PROMOTIONS_PAGE)


def get_delivery_page():
    return get_content_page('delivery', DELIVERY_PAGE)


def get_contacts_page():
    return get_content_page('contacts', CONTACTS_PAGE)


def _home_block_fallback(key):
    defaults = DEFAULT_HOME_BLOCKS[key]
    return SimpleNamespace(
        key=key,
        image=None,
        reviews_source=defaults.get('reviews_source', ''),
        **{field: defaults.get(field, '') for field in TEXT_FIELD_KEYS},
    )


def _resolve_block_texts(block):
    defaults = DEFAULT_HOME_BLOCKS[block.key]
    return {
        field: getattr(block, field, '') or defaults.get(field, '')
        for field in TEXT_FIELD_KEYS
    }


def get_home_blocks():
    blocks = {}
    stored = {block.key: block for block in HomeBlock.objects.all()}
    for key in DEFAULT_HOME_BLOCKS:
        block = stored.get(key)
        if block:
            texts = _resolve_block_texts(block)
            blocks[key] = SimpleNamespace(
                key=block.key,
                label=block.label,
                is_visible=block.is_visible,
                reviews_source=block.reviews_source,
                image=block.image,
                **texts,
            )
        else:
            blocks[key] = _home_block_fallback(key)
    return blocks


def _delivery_sections_fallback():
    sections = []
    for section_data in DELIVERY_PAGE['sections']:
        items = [
            SimpleNamespace(label=item['label'], text=item['text'])
            for item in section_data['items']
        ]
        sections.append(SimpleNamespace(
            step=section_data['step'],
            title=section_data['title'],
            intro=section_data['intro'],
            section_id=section_data.get('id', f"step-{section_data['step']}"),
            items=items,
        ))
    return sections


def get_delivery_sections():
    queryset = (
        DeliverySection.objects
        .filter(is_active=True)
        .prefetch_related('items')
        .order_by('order', 'pk')
    )
    if queryset.exists():
        return [
            SimpleNamespace(
                step=section.step,
                title=section.title,
                intro=section.intro,
                section_id=section.section_id,
                items=list(section.items.all()),
            )
            for section in queryset
        ]
    return _delivery_sections_fallback()
