from django.contrib import admin

from .models import AnimalCategory, Product, Subcategory


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AnimalCategory)
class AnimalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubcategoryInline]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'order', 'is_active')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'subcategory', 'price',
        'is_on_sale', 'is_available', 'is_featured',
    )
    list_filter = ('category', 'subcategory', 'is_on_sale', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_on_sale', 'is_available', 'is_featured')
