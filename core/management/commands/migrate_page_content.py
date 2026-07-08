from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import (
    ContentPage,
    DeliveryItem,
    DeliverySection,
    FaqItem,
    HeroSlide,
    HomeBlock,
    Review,
    SiteSettings,
)
from core.content_services import DEFAULT_HOME_BLOCKS
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
            ('promotions', PROMOTIONS_PAGE, {
                'empty_text': PROMOTIONS_PAGE['empty_text'],
            }),
            ('delivery', DELIVERY_PAGE, {}),
            ('faq', FAQ_PAGE, {
                'note': FAQ_PAGE['note'],
            }),
            ('contacts', CONTACTS_PAGE, {
                'cards': CONTACTS_PAGE['cards'],
                'map_embed_url': DEFAULT_MAP_EMBED_URL,
            }),
        ]

        for slug, source, extra in pages:
            page_defaults = {
                'title': source['title'],
                'eyebrow': source.get('eyebrow', ''),
                'lead': source.get('lead', ''),
                'body': '',
                'extra_data': extra,
            }
            if 'empty_text' in extra:
                page_defaults['empty_text'] = extra['empty_text']
            if 'note' in extra:
                page_defaults['note'] = extra['note']

            ContentPage.objects.update_or_create(
                slug=slug,
                defaults=page_defaults,
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

        for key, defaults in DEFAULT_HOME_BLOCKS.items():
            seed_defaults = {
                **defaults,
                'text_mode': defaults.get('text_mode', HomeBlock.TEXT_DEFAULT),
            }
            if key == HomeBlock.KEY_REVIEWS:
                seed_defaults['reviews_source'] = HomeBlock.REVIEWS_ADMIN
            _, created = HomeBlock.objects.get_or_create(
                key=key,
                defaults=seed_defaults,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'HomeBlock "{key}" — created'))
        self.stdout.write(self.style.SUCCESS(f'HomeBlock — {len(DEFAULT_HOME_BLOCKS)} items'))

        if not DeliverySection.objects.exists():
            for index, section_data in enumerate(DELIVERY_PAGE['sections'], start=1):
                section = DeliverySection.objects.create(
                    step=section_data['step'],
                    title=section_data['title'],
                    intro=section_data['intro'],
                    order=index,
                    is_active=True,
                )
                for item_index, item_data in enumerate(section_data['items'], start=1):
                    DeliveryItem.objects.create(
                        section=section,
                        label=item_data['label'],
                        text=item_data['text'],
                        order=item_index,
                    )
            self.stdout.write(self.style.SUCCESS(
                f'DeliverySection — {len(DELIVERY_PAGE["sections"])} sections',
            ))
        else:
            self.stdout.write('DeliverySection — already exists, skipped')

        self.stdout.write(self.style.SUCCESS('Done.'))
