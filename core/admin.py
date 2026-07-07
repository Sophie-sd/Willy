from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from .models import ContentPage, FaqItem, HeroSlide, Review, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Контакти', {
            'fields': ('name', 'phone', 'phone_intl', 'phone_href', 'email', 'address', 'hours'),
        }),
        ('Карта Google', {
            'fields': ('map_embed_url', 'google_maps_url', 'map_lat', 'map_lng', 'google_place_id'),
            'description': (
                'Вставте src з iframe Google Maps у поле «Код карти». '
                'Рекомендований розмір карти: 600×450 px. '
                'Для імпорту відгуків запустіть: python3 manage.py sync_google_reviews'
            ),
        }),
    )

    def has_add_permission(self, request) -> bool:
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[obj.pk]),
        )


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ('title', 'image_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'cta_text')
    ordering = ('order', 'pk')
    readonly_fields = ('image_preview',)
    fieldsets = (
        ('Тексти', {
            'fields': ('title', 'subtitle', 'cta_text', 'cta_url'),
            'description': (
                'Заголовок — до 80 символів. Підзаголовок — до 200 символів. '
                'Текст кнопки — до 48 символів.'
            ),
        }),
        ('Зображення', {
            'fields': ('image', 'image_preview', 'object_position'),
            'description': 'Рекомендовано: 1920×1080 px, JPG або WebP, до 3 МБ.',
        }),
        ('Відображення', {
            'fields': ('order', 'is_active'),
        }),
    )

    @admin.display(description='Превʼю')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px;object-fit:cover">',
                obj.image.url,
            )
        return '—'


@admin.register(FaqItem)
class FaqItemAdmin(ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    ordering = ('order', 'pk')


@admin.action(description='Опублікувати')
def publish_reviews(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='Відхилити')
def reject_reviews(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('author', 'short_text', 'rating', 'source', 'show_on_homepage', 'is_published', 'created_at')
    list_filter = ('source', 'is_published', 'show_on_homepage', 'rating', 'created_at')
    search_fields = ('author', 'text')
    actions = [publish_reviews, reject_reviews]
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('author', 'text', 'rating', 'source', 'google_review_id'),
            'description': 'Текст — без обмеження. Автор — до 128 символів.',
        }),
        ('Відображення', {
            'fields': ('show_on_homepage', 'is_published', 'created_at'),
        }),
    )

    @admin.display(description='Текст')
    def short_text(self, obj):
        text = obj.text[:80] + '…' if len(obj.text) > 80 else obj.text
        return format_html('<span title="{}">{}</span>', obj.text, text)


@admin.register(ContentPage)
class ContentPageAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'header_image_preview')
    search_fields = ('title', 'slug', 'lead')
    readonly_fields = ('header_image_preview',)
    fieldsets = (
        (None, {
            'fields': ('slug', 'title', 'eyebrow', 'lead', 'body'),
            'description': (
                'Заголовок — до 128 символів. Eyebrow — до 128 символів. '
                'Lead — короткий вступний текст.'
            ),
        }),
        ('Зображення', {
            'fields': ('header_image', 'header_image_preview'),
            'description': 'Рекомендовано: 1440×480 px, JPG або WebP, до 1.5 МБ.',
        }),
        ('JSON-дані', {
            'fields': ('extra_data',),
            'description': 'sections, cards, note, empty_text, map_embed_url тощо.',
        }),
    )

    def changelist_view(self, request, extra_context=None):
        slug = request.GET.get('slug')
        if slug:
            try:
                page = ContentPage.objects.get(slug=slug)
                return HttpResponseRedirect(
                    reverse('admin:core_contentpage_change', args=[page.pk]),
                )
            except ContentPage.DoesNotExist:
                pass
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description='Превʼю')
    def header_image_preview(self, obj):
        if obj.header_image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px;object-fit:cover">',
                obj.header_image.url,
            )
        return '—'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
