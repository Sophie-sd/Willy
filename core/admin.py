from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from .models import ContentPage, FaqItem, Review, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Контакти', {
            'fields': ('name', 'phone', 'phone_intl', 'phone_href', 'email', 'address', 'hours'),
        }),
        ('Карта', {
            'fields': ('map_lat', 'map_lng'),
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
    list_display = ('author', 'short_text', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('author', 'text')
    actions = [publish_reviews, reject_reviews]
    readonly_fields = ('created_at',)

    @admin.display(description='Текст')
    def short_text(self, obj):
        text = obj.text[:80] + '…' if len(obj.text) > 80 else obj.text
        return format_html('<span title="{}">{}</span>', obj.text, text)


@admin.register(ContentPage)
class ContentPageAdmin(ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug', 'lead')
    fieldsets = (
        (None, {'fields': ('slug', 'title', 'eyebrow', 'lead', 'body')}),
        ('JSON-дані', {
            'fields': ('extra_data',),
            'description': 'sections, cards, note, empty_text, map_embed_url тощо.',
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
