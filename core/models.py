from django.db import models


class SiteSettings(models.Model):
    phone = models.CharField('Телефон', max_length=32, default='066 320 28 62')
    phone_intl = models.CharField('Телефон (міжнародний)', max_length=32, default='+380 66 320 28 62')
    phone_href = models.CharField('Телефон (href)', max_length=32, default='+380663202862')
    email = models.EmailField('Email', default='oksanadaragan9@gmail.com')
    address = models.CharField('Адреса', max_length=255, default='м. Київ, просп. Палладіна Академіка, 23а')
    hours = models.CharField('Години роботи', max_length=128, default='щодня з 8:00 до 19:00')
    name = models.CharField('Назва магазину', max_length=128, default='ZOO МАГАЗИН WILLI')
    map_lat = models.DecimalField('Широта', max_digits=9, decimal_places=6, default=50.464137)
    map_lng = models.DecimalField('Довгота', max_digits=9, decimal_places=6, default=30.35462)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'phone': self.phone,
            'phone_intl': self.phone_intl,
            'phone_href': self.phone_href,
            'email': self.email,
            'address': self.address,
            'hours': self.hours,
            'name': self.name,
            'map_lat': float(self.map_lat),
            'map_lng': float(self.map_lng),
        }


class FaqItem(models.Model):
    question = models.CharField('Питання', max_length=255)
    answer = models.TextField('Відповідь')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Питання FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.question


class Review(models.Model):
    text = models.TextField('Текст відгуку')
    author = models.CharField('Автор', max_length=128)
    is_published = models.BooleanField('Опубліковано', default=False)
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']

    def __str__(self):
        return self.author


class HeroSlide(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=80,
        help_text='До 80 символів',
    )
    subtitle = models.CharField(
        'Підзаголовок',
        max_length=200,
        blank=True,
        help_text='До 200 символів',
    )
    cta_text = models.CharField(
        'Текст кнопки',
        max_length=48,
        help_text='До 48 символів, напр. «До каталогу»',
    )
    cta_url = models.CharField(
        'Посилання кнопки',
        max_length=128,
        help_text='Відносний шлях: /catalog/, /promotions/, /delivery/',
    )
    image = models.ImageField(
        'Зображення',
        upload_to='hero/',
        help_text='Рекомендовано: 1920×1080 px, JPG або WebP, до 3 МБ',
    )
    object_position = models.CharField(
        'Позиція фото',
        max_length=32,
        default='center center',
        blank=True,
        help_text='CSS object-position: top, center center, 30% 50% тощо',
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = 'Банер головної'
        verbose_name_plural = 'Банери головної'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title


class ContentPage(models.Model):
    slug = models.SlugField('Slug', unique=True)
    title = models.CharField('Заголовок', max_length=128)
    eyebrow = models.CharField('Eyebrow', max_length=128, blank=True)
    lead = models.TextField('Lead', blank=True)
    body = models.TextField('Тіло (HTML)', blank=True)
    header_image = models.ImageField(
        'Зображення заголовку сторінки',
        upload_to='pages/',
        blank=True,
        help_text='Рекомендовано: 1440×480 px, JPG або WebP, до 1.5 МБ',
    )
    extra_data = models.JSONField('Додаткові дані', default=dict, blank=True)

    class Meta:
        verbose_name = 'Сторінка контенту'
        verbose_name_plural = 'Сторінки контенту'
        ordering = ['slug']

    def __str__(self):
        return self.title

    def as_dict(self):
        data = {
            'title': self.title,
            'eyebrow': self.eyebrow,
            'lead': self.lead,
        }
        if self.header_image:
            data['header_image_url'] = self.header_image.url
        if self.extra_data:
            data.update(self.extra_data)
        return data
