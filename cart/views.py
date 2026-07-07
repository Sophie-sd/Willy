import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from cart.forms import CheckoutForm
from orders.models import Order
from orders.services import create_order_from_cart

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart.items(),
        'cart_total': cart.get_total_price(),
    })


def checkout(request):
    cart = Cart(request)
    cart_items = cart.items()

    if not cart_items:
        return redirect('cart:detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = create_order_from_cart(cart, form.cleaned_data)
            if order:
                return redirect('cart:order_success', order_number=order.number)
    else:
        form = CheckoutForm()

    return render(request, 'cart/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart.get_total_price(),
    })


def order_success(request, order_number):
    order = Order.objects.filter(number=order_number).first()
    if not order:
        return redirect('cart:detail')
    return render(request, 'cart/order_success.html', {'order': order})


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
