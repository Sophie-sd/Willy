from django import template

from catalog.product_images import get_product_static_image

register = template.Library()

CATEGORY_IMAGES = {
    'cats': 'images/categories/cats.jpg',
    'dogs': 'images/categories/dogs.jpg',
    'birds': 'images/categories/birds.jpg',
    'rodents': 'images/categories/rodents.jpg',
}


@register.simple_tag
def product_image_src(product):
    if product.image:
        return product.image.url
    return get_product_static_image(product)


@register.simple_tag
def category_image_src(category):
    if category.image:
        return category.image.url
    return CATEGORY_IMAGES.get(category.slug, 'images/placeholders/product.svg')


@register.filter
def category_placeholder(slug):
    return CATEGORY_IMAGES.get(slug, 'images/placeholders/product.svg')
