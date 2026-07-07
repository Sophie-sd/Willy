from django.shortcuts import redirect, render

from catalog.models import AnimalCategory, Product
from core.content_services import (
    get_contacts_page,
    get_delivery_page,
    get_faq_page,
    get_google_maps_url,
    get_map_embed_url,
    get_promotions_page,
    get_reviews,
    get_site_contacts,
)
from core.models import HeroSlide


def home(request):
    categories = AnimalCategory.objects.filter(is_active=True)
    sale_products = Product.objects.sale_active().filter(is_available=True)[:4]
    site_contacts = get_site_contacts()
    return render(request, 'core/home.html', {
        'categories': categories,
        'sale_products': sale_products,
        'hero_slides': HeroSlide.objects.filter(is_active=True).order_by('order'),
        'reviews': get_reviews(),
        'google_maps_url': site_contacts.get('google_maps_url') or get_google_maps_url(),
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
    return render(request, 'core/contacts.html', {
        'page': page,
        'map_embed_url': get_map_embed_url(),
        'map_open_url': contacts_info.get('google_maps_url') or get_google_maps_url(),
        'breadcrumbs': [{'label': page['title']}],
    })


def contacts_legacy_redirect(request):
    return redirect('contacts', permanent=False)


def reviews_redirect(request):
    return redirect('faq', permanent=True)
