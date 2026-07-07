from django.core.management.base import BaseCommand

from core.google_places import fetch_place_reviews, find_place_id
from core.models import Review, SiteSettings


class Command(BaseCommand):
    help = 'Імпорт відгуків з Google Maps через Places API (потрібен GOOGLE_PLACES_API_KEY)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--place-id',
            help='Google Place ID (якщо не вказано — пошук за адресою магазину)',
        )
        parser.add_argument(
            '--unpublish-manual',
            action='store_true',
            help='Приховати старі ручні відгуки з головної після імпорту Google',
        )

    def handle(self, *args, **options):
        settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
        place_id = options.get('place_id') or settings_obj.google_place_id

        if not place_id:
            place_id, error = find_place_id()
            if error:
                self.stderr.write(self.style.ERROR(error))
                return
            settings_obj.google_place_id = place_id
            settings_obj.save(update_fields=['google_place_id'])
            self.stdout.write(self.style.SUCCESS(f'Place ID: {place_id}'))

        data, error = fetch_place_reviews(place_id)
        if error:
            self.stderr.write(self.style.ERROR(error))
            return

        imported = 0
        for item in data['reviews']:
            _, created = Review.objects.update_or_create(
                google_review_id=item['google_review_id'],
                defaults={
                    'text': item['text'],
                    'author': item['author'],
                    'rating': item['rating'],
                    'source': Review.SOURCE_GOOGLE,
                    'is_published': True,
                    'show_on_homepage': True,
                },
            )
            if created:
                imported += 1

        if options['unpublish_manual']:
            updated = Review.objects.filter(
                source=Review.SOURCE_MANUAL,
                show_on_homepage=True,
            ).update(show_on_homepage=False)
            self.stdout.write(f'Приховано ручних відгуків на головній: {updated}')

        total = Review.objects.filter(source=Review.SOURCE_GOOGLE, is_published=True).count()
        self.stdout.write(self.style.SUCCESS(
            f'Google відгуки: {len(data["reviews"])} отримано, {imported} нових. '
            f'Опубліковано всього: {total}. '
            f'Рейтинг Google: {data.get("rating")} ({data.get("user_rating_count")} оцінок)',
        ))
