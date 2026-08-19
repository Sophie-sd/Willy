from django import forms

from core.content_services import DEFAULT_HOME_BLOCKS, FOP_DEFAULTS, FOP_FIELD_NAMES, TEXT_FIELD_KEYS
from core.models import ContentPage, HomeBlock, SiteSettings
from core.page_content import (
    CONTACTS_PAGE,
    DELIVERY_PAGE,
    FAQ_PAGE,
    OFFER_PAGE,
    PRIVACY_PAGE,
    PROMOTIONS_PAGE,
    REVIEWS,
)

CONTENT_PAGE_DEFAULTS = {
    'promotions': PROMOTIONS_PAGE,
    'delivery': DELIVERY_PAGE,
    'faq': FAQ_PAGE,
    'contacts': CONTACTS_PAGE,
    'offer': OFFER_PAGE,
    'privacy': PRIVACY_PAGE,
}

CONTENT_PAGE_TEXT_FIELDS = ('title', 'eyebrow', 'lead', 'body', 'empty_text', 'note')

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
    fop_full_name = forms.CharField(
        label='Повне імʼя ФОП',
        max_length=128,
        required=False,
    )
    fop_trade_name = forms.CharField(
        label='Найменування ФОП',
        max_length=128,
        required=False,
    )
    fop_rnokpp = forms.CharField(
        label='РНОКПП',
        max_length=16,
        required=False,
    )
    fop_unzr = forms.CharField(
        label='УНЗР',
        max_length=32,
        required=False,
    )

    class Meta:
        model = ContentPage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if not instance or not instance.slug:
            return
        page_defaults = CONTENT_PAGE_DEFAULTS.get(instance.slug, {})
        if page_defaults:
            defaults = {
                'title': page_defaults.get('title', ''),
                'eyebrow': page_defaults.get('eyebrow', ''),
                'lead': page_defaults.get('lead', ''),
                'body': page_defaults.get('body', ''),
                'empty_text': page_defaults.get('empty_text', ''),
                'note': page_defaults.get('note', ''),
            }
            _apply_field_defaults(self, defaults, CONTENT_PAGE_TEXT_FIELDS, instance)

        if instance.slug != 'offer':
            for name in FOP_FIELD_NAMES:
                self.fields.pop(name, None)
            return

        settings_obj = SiteSettings.objects.filter(pk=1).first()
        fop_defaults = FOP_DEFAULTS.copy()
        if settings_obj:
            for name in FOP_FIELD_NAMES:
                fop_defaults[name] = getattr(settings_obj, name, '') or fop_defaults[name]
        _apply_field_defaults(self, fop_defaults, FOP_FIELD_NAMES)

    def save(self, commit=True):
        instance = super().save(commit=False)
        page_defaults = CONTENT_PAGE_DEFAULTS.get(instance.slug, {})
        if page_defaults:
            fallbacks = {
                'title': page_defaults.get('title', ''),
                'eyebrow': page_defaults.get('eyebrow', ''),
                'lead': page_defaults.get('lead', ''),
                'body': page_defaults.get('body', ''),
                'empty_text': page_defaults.get('empty_text', ''),
                'note': page_defaults.get('note', ''),
            }
            for field, fallback in fallbacks.items():
                if not getattr(instance, field, '') and fallback:
                    setattr(instance, field, fallback)
        if commit:
            instance.save()

        if instance.slug == 'offer':
            settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
            for name in FOP_FIELD_NAMES:
                value = self.cleaned_data.get(name, '')
                if not value:
                    value = FOP_DEFAULTS.get(name, '')
                setattr(settings_obj, name, value)
            settings_obj.save()

        return instance
