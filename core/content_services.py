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
        Review.objects.filter(is_published=True).values('text', 'author'),
    )
    if reviews:
        return reviews
    return REVIEWS


def get_promotions_page():
    return get_content_page('promotions', PROMOTIONS_PAGE)


def get_delivery_page():
    return get_content_page('delivery', DELIVERY_PAGE)


def get_contacts_page():
    return get_content_page('contacts', CONTACTS_PAGE)
