from decimal import Decimal

from catalog.models import Product
from orders.models import Order, OrderItem


def create_order_from_cart(cart, form_data):
    items = cart.items()
    if not items:
        return None

    total = Decimal(str(cart.get_total_price()))
    order = Order.objects.create(
        customer_name=form_data['customer_name'],
        phone=form_data['phone'],
        email=form_data.get('email', ''),
        delivery_method=form_data['delivery_method'],
        delivery_city=form_data['delivery_city'],
        delivery_address=form_data['delivery_address'],
        comment=form_data.get('comment', ''),
        total=total,
        status=Order.STATUS_NEW,
    )

    for item in items:
        product = Product.objects.filter(pk=int(item['product_id'])).first()
        if not product:
            continue
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=item['name'],
            quantity=item['quantity'],
            price=Decimal(str(item['price'])),
        )

    cart.clear()
    return order
