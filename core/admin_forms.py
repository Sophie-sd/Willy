from django import forms

from core.content_services import DEFAULT_HOME_BLOCKS, TEXT_FIELD_KEYS
from core.models import ContentPage, HomeBlock
from core.page_content import (
    CONTACTS_PAGE,
    DELIVERY_PAGE,
    FAQ_PAGE,
    PROMOTIONS_PAGE,
    REVIEWS,
)

CONTENT_PAGE_DEFAULTS = {
    'promotions': PROMOTIONS_PAGE,
    'delivery': DELIVERY_PAGE,
    'faq': FAQ_PAGE,
    'contacts': CONTACTS_PAGE,
}

CONTENT_PAGE_TEXT_FIELDS = ('title', 'eyebrow', 'lead', 'empty_text', 'note')

CUSTOM_REVIEW_FIELD_NAMES = (
    'custom_review_1_text', 'custom_review_1_author',
    'custom_review_2_text', 'custom_review_2_author',
    'custom_review_3_text', 'custom_review_3_author',
)


def _apply_field_defaults(form, defaults, field_names, instance=None):
    if form.is_bound:
        return
    for name in field_names:
        if name not in form.fields:
            continue
        current = ''
        if instance is not None:
            current = getattr(instance, name, '') or ''
        if not current:
            default_val = defaults.get(name, '')
            if default_val:
                form.initial[name] = default_val


def _custom_review_defaults():
    defaults = {}
    for index, review in enumerate(REVIEWS[:3], start=1):
        defaults[f'custom_review_{index}_text'] = review['text']
        defaults[f'custom_review_{index}_author'] = review['author']
    return defaults


class HomeBlockAdminForm(forms.ModelForm):
    class Meta:
        model = HomeBlock
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if not instance or not instance.pk:
            return

        block_defaults = DEFAULT_HOME_BLOCKS.get(instance.key, {})
        _apply_field_defaults(self, block_defaults, TEXT_FIELD_KEYS, instance)
        _apply_field_defaults(
            self,
            _custom_review_defaults(),
            CUSTOM_REVIEW_FIELD_NAMES,
            instance,
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        block_defaults = DEFAULT_HOME_BLOCKS.get(instance.key, {})
        for field in TEXT_FIELD_KEYS:
            if not getattr(instance, field, ''):
                setattr(instance, field, block_defaults.get(field, ''))
        review_defaults = _custom_review_defaults()
        for field in CUSTOM_REVIEW_FIELD_NAMES:
            if not getattr(instance, field, ''):
                setattr(instance, field, review_defaults.get(field, ''))
        if commit:
            instance.save()
        return instance


class ContentPageAdminForm(forms.ModelForm):
    class Meta:
        model = ContentPage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if not instance or not instance.slug:
            return
        page_defaults = CONTENT_PAGE_DEFAULTS.get(instance.slug, {})
        if not page_defaults:
            return
        defaults = {
            'title': page_defaults.get('title', ''),
            'eyebrow': page_defaults.get('eyebrow', ''),
            'lead': page_defaults.get('lead', ''),
            'empty_text': page_defaults.get('empty_text', ''),
            'note': page_defaults.get('note', ''),
        }
        _apply_field_defaults(self, defaults, CONTENT_PAGE_TEXT_FIELDS, instance)

    def save(self, commit=True):
        instance = super().save(commit=False)
        page_defaults = CONTENT_PAGE_DEFAULTS.get(instance.slug, {})
        if page_defaults:
            fallbacks = {
                'title': page_defaults.get('title', ''),
                'eyebrow': page_defaults.get('eyebrow', ''),
                'lead': page_defaults.get('lead', ''),
                'empty_text': page_defaults.get('empty_text', ''),
                'note': page_defaults.get('note', ''),
            }
            for field, fallback in fallbacks.items():
                if not getattr(instance, field, '') and fallback:
                    setattr(instance, field, fallback)
        if commit:
            instance.save()
        return instance
