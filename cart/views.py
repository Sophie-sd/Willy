import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from catalog.models import Product

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart.items(),
        'cart_total': cart.get_total_price(),
    })


@require_POST
def add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = Cart(request)
    cart.add(product)

    count = len(cart)
    response = HttpResponse(status=200)
    response['HX-Trigger'] = json.dumps({
        'cartUpdated': {'count': count},
        'showToast': {'message': f'«{product.name}» додано в кошик'},
    })
    return response


@require_POST
def remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    count = len(cart)
    response = HttpResponse(status=200)
    response['HX-Trigger'] = json.dumps({
        'cartUpdated': {'count': count},
    })
    return response


@require_POST
def update(request, product_id):
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        return HttpResponseBadRequest()

    cart = Cart(request)
    cart.update(product_id, quantity)

    count = len(cart)
    response = HttpResponse(status=200)
    response['HX-Trigger'] = json.dumps({
        'cartUpdated': {'count': count},
        'cartPageRefresh': {},
    })
    return response
