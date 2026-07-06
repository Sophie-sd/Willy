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


def get_product_static_image(product):
    if product.slug in PRODUCT_IMAGES:
        return PRODUCT_IMAGES[product.slug]
    return CATEGORY_PRODUCT_FALLBACK.get(
        product.category.slug,
        'images/products/general-pet.jpg',
    )


def get_product_image_data(product):
    if product.image:
        return {'image': product.image.url, 'image_static': ''}
    return {'image': '', 'image_static': get_product_static_image(product)}
