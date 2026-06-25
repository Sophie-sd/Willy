from django.db import models
from django.urls import reverse


class AnimalCategory(models.Model):
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    image = models.ImageField('Зображення', upload_to='categories/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Категорія тварин'
        verbose_name_plural = 'Категорії тварин'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class Subcategory(models.Model):
    category = models.ForeignKey(
        AnimalCategory,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категорія',
    )
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('Slug')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'
        ordering = ['order', 'name']
        unique_together = [['category', 'slug']]

    def __str__(self):
        return f'{self.category.name} — {self.name}'

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={
            'category_slug': self.category.slug,
            'subcategory_slug': self.slug,
        })


class Product(models.Model):
    name = models.CharField('Назва', max_length=255)
    slug = models.SlugField('Slug', unique=True)
    category = models.ForeignKey(
        AnimalCategory,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категорія',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Підкатегорія',
    )
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        'Стара ціна', max_digits=10, decimal_places=2, null=True, blank=True,
    )
    is_on_sale = models.BooleanField('Акція', default=False)
    is_available = models.BooleanField('В наявності', default=True)
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Зображення', upload_to='products/', blank=True)
    is_featured = models.BooleanField('Рекомендований', default=False)
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0

    @property
    def subcategory_label(self):
        return f'{self.subcategory.name} для {self.category.name.lower()}'
