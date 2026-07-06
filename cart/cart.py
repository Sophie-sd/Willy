from decimal import Decimal

from catalog.models import Product
from catalog.product_images import get_product_image_data


CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            image_data = get_product_image_data(product)
            self.cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 0,
                'slug': product.slug,
                'image': image_data['image'],
                'image_static': image_data['image_static'],
            }
        self.cart[product_id]['quantity'] += quantity
        self._save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self._save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                del self.cart[product_id]
            self._save()

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self._save()

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def items(self):
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = {
            p.id: p
            for p in Product.objects.filter(id__in=product_ids).select_related('category')
        }

        result = []
        for pid, data in self.cart.items():
            product = products.get(int(pid))
            image = data.get('image') or ''
            image_static = data.get('image_static') or ''

            if product and not image and not image_static:
                image_data = get_product_image_data(product)
                image = image_data['image']
                image_static = image_data['image_static']

            result.append({
                'product_id': pid,
                'name': data['name'],
                'price': Decimal(data['price']),
                'quantity': data['quantity'],
                'slug': data['slug'],
                'image': image,
                'image_static': image_static,
                'subtotal': Decimal(data['price']) * data['quantity'],
            })
        return result

    def _save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        return iter(self.items())
