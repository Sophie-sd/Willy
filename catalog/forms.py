from django import forms

from catalog.models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        starts = cleaned.get('sale_starts_at')
        ends = cleaned.get('sale_ends_at')
        if starts and ends and ends <= starts:
            self.add_error('sale_ends_at', 'Кінець акції має бути після початку.')
        return cleaned
