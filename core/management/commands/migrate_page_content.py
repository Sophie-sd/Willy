from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import ContentPage, FaqItem, HeroSlide, Review, SiteSettings
from core.page_content import (
    CONTACTS_PAGE,
    DEFAULT_GOOGLE_MAPS_URL,
    DEFAULT_MAP_EMBED_URL,
    DELIVERY_PAGE,
    FAQ_PAGE,
    PROMOTIONS_PAGE,
    REVIEWS,
)


class Command(BaseCommand):
    help = 'Імпорт контенту з page_content.py та SITE_CONTACTS у БД'

    def handle(self, *args, **options):
        contacts = settings.SITE_CONTACTS
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                'phone': contacts['phone'],
                'phone_intl': contacts['phone_intl'],
                'phone_href': contacts['phone_href'],
                'email': contacts['email'],
                'address': contacts['address'],
                'hours': contacts['hours'],
                'name': contacts['name'],
                'map_lat': contacts['map_lat'],
                'map_lng': contacts['map_lng'],
                'map_embed_url': DEFAULT_MAP_EMBED_URL,
                'google_maps_url': DEFAULT_GOOGLE_MAPS_URL,
            },
        )
        self.stdout.write(self.style.SUCCESS('SiteSettings — ok'))

        if not FaqItem.objects.exists():
            for index, item in enumerate(FAQ_PAGE['items'], start=1):
                FaqItem.objects.create(
                    question=item['question'],
                    answer=item['answer'],
                    order=index,
                    is_active=True,
                )
            self.stdout.write(self.style.SUCCESS(f'FAQ — {len(FAQ_PAGE["items"])} items'))
        else:
            self.stdout.write('FAQ — already exists, skipped')

        if not Review.objects.exists():
            for item in REVIEWS:
                Review.objects.create(
                    text=item['text'],
                    author=item['author'],
                    is_published=True,
                )
            self.stdout.write(self.style.SUCCESS(f'Reviews — {len(REVIEWS)} items'))
        else:
            self.stdout.write('Reviews — already exists, skipped')

        pages = [
            ('promotions', PROMOTIONS_PAGE, {'empty_text': PROMOTIONS_PAGE['empty_text']}),
            ('delivery', DELIVERY_PAGE, {'sections': DELIVERY_PAGE['sections']}),
            ('faq', FAQ_PAGE, {'note': FAQ_PAGE['note']}),
            ('contacts', CONTACTS_PAGE, {
                'cards': CONTACTS_PAGE['cards'],
                'map_embed_url': DEFAULT_MAP_EMBED_URL,
            }),
        ]

        for slug, source, extra in pages:
            ContentPage.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': source['title'],
                    'eyebrow': source.get('eyebrow', ''),
                    'lead': source.get('lead', ''),
                    'body': '',
                    'extra_data': extra,
                },
            )
            self.stdout.write(self.style.SUCCESS(f'ContentPage "{slug}" — ok'))

        if not HeroSlide.objects.exists():
            hero_seed = [
                {
                    'title': 'Все для вашого улюбленця',
                    'subtitle': 'Корм, іграшки та аксесуари для котів, собак, птахів і гризунів',
                    'cta_text': 'До каталогу',
                    'cta_url': '/catalog/',
                    'image': 'images/hero/hero-wide.webp',
                    'object_position': '66% 54%',
                    'order': 1,
                },
                {
                    'title': 'Акційні пропозиції',
                    'subtitle': 'Знижки на корм, іграшки та аксесуари — щотижня нові пропозиції',
                    'cta_text': 'Дивитись акції',
                    'cta_url': '/promotions/',
                    'image': 'images/hero/slide-sale-wide.jpg',
                    'object_position': '58% center',
                    'order': 2,
                },
                {
                    'title': 'Доставка по Україні',
                    'subtitle': 'Нова Пошта та Укрпошта. Відправляємо щодня з 8:00 до 19:00',
                    'cta_text': 'Детальніше',
                    'cta_url': '/delivery/',
                    'image': 'images/hero/slide-delivery-wide.jpg',
                    'object_position': '62% center',
                    'order': 3,
                },
            ]
            for item in hero_seed:
                slide = HeroSlide(
                    title=item['title'],
                    subtitle=item['subtitle'],
                    cta_text=item['cta_text'],
                    cta_url=item['cta_url'],
                    object_position=item['object_position'],
                    order=item['order'],
                    is_active=True,
                )
                image_path = settings.BASE_DIR / 'static' / item['image']
                if image_path.exists():
                    with image_path.open('rb') as image_file:
                        slide.image.save(image_path.name, File(image_file), save=False)
                slide.save()
            self.stdout.write(self.style.SUCCESS(f'HeroSlide — {len(hero_seed)} items'))
        else:
            self.stdout.write('HeroSlide — already exists, skipped')

        self.stdout.write(self.style.SUCCESS('Done.'))
