from django.conf import settings

from core.models import ContentPage, FaqItem, Review, SiteSettings
from core.page_content import (
    CONTACTS_PAGE,
    DELIVERY_PAGE,
    FAQ_PAGE,
    PROMOTIONS_PAGE,
    REVIEWS,
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
        return page.as_dict()
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
    reviews = list(
        Review.objects.filter(
            is_published=True,
            show_on_homepage=True,
            source=Review.SOURCE_GOOGLE,
        ).order_by('-created_at').values('text', 'author', 'rating'),
    )
    if reviews:
        return reviews

    reviews = list(
        Review.objects.filter(
            is_published=True,
            show_on_homepage=True,
        ).order_by('-created_at').values('text', 'author', 'rating'),
    )
    if reviews:
        return reviews

    return [{**item, 'rating': 5} for item in REVIEWS]


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
