import random

from django.db import models
from django.utils import timezone

from catalog.models import Product


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PAID = 'paid'
    STATUS_SHIPPED = 'shipped'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Нове'),
        (STATUS_PAID, 'Оплачено'),
        (STATUS_SHIPPED, 'Відправлено'),
        (STATUS_DONE, 'Виконано'),
        (STATUS_CANCELLED, 'Скасовано'),
    ]

    DELIVERY_NOVA = 'nova_poshta'
    DELIVERY_UKR = 'ukrposhta'
    DELIVERY_CHOICES = [
        (DELIVERY_NOVA, 'Нова Пошта'),
        (DELIVERY_UKR, 'Укрпошта'),
    ]

    number = models.CharField('Номер', max_length=32, unique=True, editable=False)
    customer_name = models.CharField('Імʼя', max_length=128)
    phone = models.CharField('Телефон', max_length=32)
    email = models.EmailField('Email', blank=True)
    delivery_method = models.CharField('Доставка', max_length=32, choices=DELIVERY_CHOICES)
    delivery_city = models.CharField('Місто', max_length=128)
    delivery_address = models.CharField('Адреса / відділення', max_length=255)
    comment = models.TextField('Коментар', blank=True)
    total = models.DecimalField('Сума', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', max_length=16, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.number} — {self.customer_name}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self._generate_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_number():
        date_part = timezone.now().strftime('%Y%m%d')
        suffix = random.randint(1000, 9999)
        return f'W-{date_part}-{suffix}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Замовлення',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар',
    )
    product_name = models.CharField('Назва товару', max_length=255)
    quantity = models.PositiveIntegerField('Кількість', default=1)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'

    @property
    def subtotal(self):
        return self.price * self.quantity
