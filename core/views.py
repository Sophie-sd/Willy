from django.conf import settings
from django.shortcuts import redirect, render

from catalog.models import AnimalCategory, Product
from core.hero_slides import get_hero_slides
from core.page_content import (
    CONTACTS_PAGE,
    DELIVERY_PAGE,
    FAQ_PAGE,
    PROMOTIONS_PAGE,
    REVIEWS,
)


def home(request):
    categories = AnimalCategory.objects.filter(is_active=True)
    sale_products = Product.objects.filter(is_on_sale=True, is_available=True)[:4]
    return render(request, 'core/home.html', {
        'categories': categories,
        'sale_products': sale_products,
        'hero_slides': get_hero_slides(),
        'reviews': REVIEWS,
    })


def promotions(request):
    products = Product.objects.filter(is_on_sale=True, is_available=True)
    return render(request, 'core/promotions.html', {
        'page': PROMOTIONS_PAGE,
        'products': products,
        'breadcrumbs': [{'label': PROMOTIONS_PAGE['title']}],
    })


def delivery(request):
    return render(request, 'core/delivery.html', {
        'page': DELIVERY_PAGE,
        'breadcrumbs': [{'label': DELIVERY_PAGE['title']}],
    })


def faq(request):
    return render(request, 'core/faq.html', {
        'page': FAQ_PAGE,
        'breadcrumbs': [{'label': FAQ_PAGE['title']}],
    })


def contacts(request):
    contacts_info = settings.SITE_CONTACTS
    lat = contacts_info['map_lat']
    lng = contacts_info['map_lng']
    return render(request, 'core/contacts.html', {
        'page': CONTACTS_PAGE,
        'map_embed_url': CONTACTS_PAGE['map_embed_url'],
        'map_open_url': f'https://www.google.com/maps/search/?api=1&query={lat},{lng}',
        'breadcrumbs': [{'label': CONTACTS_PAGE['title']}],
    })


def contacts_legacy_redirect(request):
    return redirect('contacts', permanent=False)


def reviews_redirect(request):
    return redirect('faq', permanent=True)
