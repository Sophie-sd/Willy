def get_hero_slides():
    return [
        {
            'title': 'Все для вашого улюбленця',
            'subtitle': 'Корм, іграшки та аксесуари для котів, собак, птахів і гризунів',
            'cta_text': 'До каталогу',
            'cta_url_name': 'catalog:product_list',
            'image': 'images/hero/hero-wide.webp',
            'object_position': '66% 54%',
            'overlay': 'green',
        },
        {
            'title': 'Акційні пропозиції',
            'subtitle': 'Знижки на корм, іграшки та аксесуари — щотижня нові пропозиції',
            'cta_text': 'Дивитись акції',
            'cta_url_name': 'promotions',
            'image': 'images/hero/slide-sale-wide.jpg',
            'object_position': '58% center',
            'overlay': 'lime',
        },
        {
            'title': 'Доставка по Україні',
            'subtitle': 'Нова Пошта та Укрпошта. Відправляємо щодня з 8:00 до 19:00',
            'cta_text': 'Детальніше',
            'cta_url_name': 'delivery',
            'image': 'images/hero/slide-delivery-wide.jpg',
            'object_position': '62% center',
            'overlay': 'dark',
        },
    ]
