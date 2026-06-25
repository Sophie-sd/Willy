from django import template

register = template.Library()

CATEGORY_IMAGES = {
    'cats': 'images/categories/cats.jpg',
    'dogs': 'images/categories/dogs.jpg',
    'birds': 'images/categories/birds.jpg',
    'rodents': 'images/categories/rodents.jpg',
}

PRODUCT_IMAGES = {
    'royal-canin-mini-adult': 'images/products/dog-food.jpg',
    'whiskas-losos': 'images/products/whiskas-losos.jpg',
    'igrashka-kanat-dogs': 'images/products/dog-toy.jpg',
    'vitakraft-homyak': 'images/products/rodent-food.jpg',
    'pro-plan-cats': 'images/products/cat-food.jpg',
    'lezhak-myakyi': 'images/products/dog-bed.jpg',
    'hills-science-dog': 'images/products/dog-food.jpg',
    'dzerkalo-ptahy': 'images/products/bird-mirror.jpg',
    'koleso-gryzun': 'images/products/rodent-wheel.jpg',
    'nashynnyk-shkiryany': 'images/products/dog-collar.jpg',
}

CATEGORY_PRODUCT_FALLBACK = {
    'cats': 'images/products/cat-food.jpg',
    'dogs': 'images/products/dog-food.jpg',
    'birds': 'images/products/bird-food.jpg',
    'rodents': 'images/products/rodent-food.jpg',
}


@register.simple_tag
def product_image_src(product):
    if product.image:
        return product.image.url
    if product.slug in PRODUCT_IMAGES:
        return PRODUCT_IMAGES[product.slug]
    return CATEGORY_PRODUCT_FALLBACK.get(
        product.category.slug,
        'images/products/general-pet.jpg',
    )


@register.simple_tag
def category_image_src(category):
    if category.image:
        return category.image.url
    return CATEGORY_IMAGES.get(category.slug, 'images/placeholders/product.svg')


@register.filter
def category_placeholder(slug):
    return CATEGORY_IMAGES.get(slug, 'images/placeholders/product.svg')
