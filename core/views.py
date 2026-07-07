from django.shortcuts import redirect, render

from catalog.models import AnimalCategory, Product
from core.content_services import (
    get_contacts_page,
    get_delivery_page,
    get_faq_page,
    get_promotions_page,
    get_reviews,
    get_site_contacts,
)
from core.hero_slides import get_hero_slides


def home(request):
    categories = AnimalCategory.objects.filter(is_active=True)
    sale_products = Product.objects.sale_active().filter(is_available=True)[:4]
    return render(request, 'core/home.html', {
        'categories': categories,
        'sale_products': sale_products,
        'hero_slides': get_hero_slides(),
        'reviews': get_reviews(),
    })


def promotions(request):
    products = Product.objects.sale_active().filter(is_available=True)
    page = get_promotions_page()
    return render(request, 'core/promotions.html', {
        'page': page,
        'products': products,
        'breadcrumbs': [{'label': page['title']}],
    })


def delivery(request):
    page = get_delivery_page()
    return render(request, 'core/delivery.html', {
        'page': page,
        'breadcrumbs': [{'label': page['title']}],
    })


def faq(request):
    page = get_faq_page()
    return render(request, 'core/faq.html', {
        'page': page,
        'breadcrumbs': [{'label': page['title']}],
    })


def contacts(request):
    contacts_info = get_site_contacts()
    page = get_contacts_page()
    lat = contacts_info['map_lat']
    lng = contacts_info['map_lng']
    return render(request, 'core/contacts.html', {
        'page': page,
        'map_embed_url': page.get('map_embed_url', ''),
        'map_open_url': f'https://www.google.com/maps/search/?api=1&query={lat},{lng}',
        'breadcrumbs': [{'label': page['title']}],
    })


def contacts_legacy_redirect(request):
    return redirect('contacts', permanent=False)


def reviews_redirect(request):
    return redirect('faq', permanent=True)
