from django.db import migrations

TEXT_FIELD_KEYS = (
    'eyebrow', 'heading', 'subheading',
    'perk_1', 'perk_2', 'perk_3', 'cta_text', 'cta_url',
)

DEFAULT_HOME_BLOCKS = {
    'categories': {
        'eyebrow': 'Що шукаєте?',
        'heading': 'Оберіть категорію',
        'subheading': '',
        'perk_1': '',
        'perk_2': '',
        'perk_3': '',
        'cta_text': '',
        'cta_url': '',
    },
    'sale_products': {
        'eyebrow': 'Акція',
        'heading': 'Акційні товари',
        'subheading': '',
        'perk_1': '',
        'perk_2': '',
        'perk_3': '',
        'cta_text': '',
        'cta_url': '',
    },
    'reviews': {
        'eyebrow': 'Відгуки',
        'heading': 'Що кажуть клієнти',
        'subheading': '',
        'perk_1': '',
        'perk_2': '',
        'perk_3': '',
        'cta_text': '',
        'cta_url': '',
    },
    'cta': {
        'eyebrow': 'Доставка по всій Україні',
        'heading': 'Готові зробити замовлення?',
        'subheading': '',
        'perk_1': 'Доставка Новою Поштою та Укрпоштою',
        'perk_2': 'Перевірені бренди для ваших улюбленців',
        'perk_3': 'Магазин у Києві',
        'cta_text': 'Перейти в каталог',
        'cta_url': '/catalog/',
    },
}

REVIEW_SAMPLES = [
    {
        'text': (
            'Замовляла корм для кота вперше — привезли наступного дня. '
            'Ціни кращі, ніж у звичайних магазинах. Швидка доставка та чудовий асортимент!'
        ),
        'author': 'Оксана М., Київ',
    },
    {
        'text': (
            'Купила набір іграшок для мого улюбленця. Якість відмінна, пес грає весь день. '
            'Моя такса в захваті від кожної нової покупки!'
        ),
        'author': 'Марина Д., Бориспіль',
    },
    {
        'text': (
            'Знайшов потрібний корм для птахів. Оплата ПриватБанком — зручно. '
            'Доставили вчасно. Рекомендую всім власникам тварин!'
        ),
        'author': 'Андрій К., Вишневе',
    },
]


def populate_homeblock_texts(apps, schema_editor):
    HomeBlock = apps.get_model('core', 'HomeBlock')
    for block in HomeBlock.objects.all():
        defaults = DEFAULT_HOME_BLOCKS.get(block.key, {})
        changed = False
        use_defaults = getattr(block, 'text_mode', 'default') == 'default'
        for field in TEXT_FIELD_KEYS:
            current = getattr(block, field, '') or ''
            if not current and use_defaults:
                value = defaults.get(field, '')
                if value:
                    setattr(block, field, value)
                    changed = True
        for index, review in enumerate(REVIEW_SAMPLES, start=1):
            text_field = f'custom_review_{index}_text'
            author_field = f'custom_review_{index}_author'
            if not getattr(block, text_field, ''):
                setattr(block, text_field, review['text'])
                changed = True
            if not getattr(block, author_field, ''):
                setattr(block, author_field, review['author'])
                changed = True
        if changed:
            block.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_homeblock_custom_review_1_author_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_homeblock_texts, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='homeblock',
            name='text_mode',
        ),
    ]
