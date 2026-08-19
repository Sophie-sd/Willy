from django.db import migrations


DELIVERY_SECTION_ITEMS = [
    (
        'Нова Пошта',
        'Доставка у відділення, поштомат або курʼєром до дверей. '
        'Термін — зазвичай 1–3 робочих дні.',
    ),
    (
        'Вартість',
        'Розраховується за тарифами обраної служби доставки '
        'під час оформлення замовлення.',
    ),
    (
        'Відстеження',
        'Після відправки надішлемо номер ТТН — за ним можна відстежити '
        'посилку на сайті перевізника.',
    ),
]

FAQ_DELIVERY_ANSWER = (
    'Доставляємо Новою Поштою: у відділення, поштомат або курʼєром за адресою. '
    'Спосіб обираєте під час оформлення замовлення.'
)


def sync_delivery_section_items(apps, schema_editor):
    DeliverySection = apps.get_model('core', 'DeliverySection')
    DeliveryItem = apps.get_model('core', 'DeliveryItem')

    section = (
        DeliverySection.objects.filter(step='01').first()
        or DeliverySection.objects.filter(title__icontains='Доставка').first()
    )
    if not section:
        return

    section.items.all().delete()
    for order, (label, text) in enumerate(DELIVERY_SECTION_ITEMS, start=1):
        DeliveryItem.objects.create(
            section=section,
            label=label,
            text=text,
            order=order,
        )


def sync_faq_delivery_answer(apps, schema_editor):
    FaqItem = apps.get_model('core', 'FaqItem')

    updated = FaqItem.objects.filter(
        question__icontains='способи доставки',
    ).update(answer=FAQ_DELIVERY_ANSWER)
    if updated:
        return

    FaqItem.objects.filter(answer__icontains='Укрпошт').update(answer=FAQ_DELIVERY_ANSWER)


def sync_delivery_content(apps, schema_editor):
    sync_delivery_section_items(apps, schema_editor)
    sync_faq_delivery_answer(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_sitesettings_fop_fields'),
    ]

    operations = [
        migrations.RunPython(sync_delivery_content, migrations.RunPython.noop),
    ]
