from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import ContentPage, FaqItem, Review, SiteSettings
from core.page_content import (
    CONTACTS_PAGE,
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
                'map_embed_url': CONTACTS_PAGE['map_embed_url'],
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

        self.stdout.write(self.style.SUCCESS('Done.'))
