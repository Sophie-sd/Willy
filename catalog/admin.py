from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, TabularInline

from .forms import ProductAdminForm
from .models import AnimalCategory, Product, Subcategory


class SubcategoryInline(TabularInline):
    model = Subcategory
    extra = 0
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AnimalCategory)
class AnimalCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview',)
    search_fields = ('name', 'slug')
    inlines = [SubcategoryInline]
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'image', 'image_preview', 'order', 'is_active')}),
    )

    @admin.display(description='Превʼю')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px">',
                obj.image.url,
            )
        return '—'


@admin.register(Subcategory)
class SubcategoryAdmin(ModelAdmin):
    list_display = ('name', 'category', 'slug', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug', 'category__name')
    autocomplete_fields = ('category',)


@admin.action(description='Зняти з продажу')
def mark_unavailable(modeladmin, request, queryset):
    queryset.update(is_available=False)


@admin.action(description='Додати в акцію')
def mark_on_sale(modeladmin, request, queryset):
    queryset.update(is_on_sale=True)


@admin.action(description='Прибрати з акції')
def mark_off_sale(modeladmin, request, queryset):
    queryset.update(is_on_sale=False)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'name', 'category', 'subcategory', 'price',
        'is_on_sale', 'is_available', 'is_featured', 'image_preview',
    )
    list_filter = ('category', 'subcategory', 'is_on_sale', 'is_available', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_on_sale', 'is_available', 'is_featured')
    autocomplete_fields = ('category', 'subcategory')
    readonly_fields = ('image_preview', 'created_at')
    date_hierarchy = 'created_at'
    actions = [mark_unavailable, mark_on_sale, mark_off_sale]
    fieldsets = (
        ('Основне', {
            'fields': (
                'name', 'slug', 'category', 'subcategory',
                'description', 'image', 'image_preview',
            ),
        }),
        ('Ціни та акція', {
            'fields': ('price', 'old_price', 'is_on_sale', 'sale_starts_at', 'sale_ends_at'),
        }),
        ('Наявність', {
            'fields': ('is_available', 'is_featured', 'created_at'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'description':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    @admin.display(description='Превʼю')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px">',
                obj.image.url,
            )
        return '—'
