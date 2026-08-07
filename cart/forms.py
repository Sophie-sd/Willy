from django import forms

from orders.models import Order
from orders.nova_poshta import is_configured


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        label='Імʼя та прізвище',
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'checkout-field__input', 'autocomplete': 'name'}),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'checkout-field__input',
            'autocomplete': 'tel',
            'inputmode': 'tel',
        }),
    )
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'checkout-field__input', 'autocomplete': 'email'}),
    )
    delivery_method = forms.ChoiceField(
        label='Спосіб доставки',
        choices=Order.DELIVERY_CHOICES,
        initial=Order.DELIVERY_NOVA,
        widget=forms.Select(attrs={
            'class': 'checkout-field__input',
            'id': 'id_delivery_method',
        }),
    )
    delivery_city = forms.CharField(
        label='Місто',
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'checkout-field__input',
            'id': 'id_delivery_city',
            'autocomplete': 'off',
            'autocapitalize': 'words',
            'spellcheck': 'false',
            'placeholder': 'Почніть вводити місто…',
        }),
    )
    delivery_address = forms.CharField(
        label='Відділення',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'checkout-field__input',
            'id': 'id_delivery_address',
            'autocomplete': 'off',
            'spellcheck': 'false',
            'placeholder': 'Оберіть відділення…',
        }),
    )
    house_number = forms.CharField(
        label='Будинок / квартира',
        max_length=64,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'checkout-field__input',
            'id': 'id_house_number',
            'autocomplete': 'off',
            'placeholder': 'напр. 12, кв. 5',
        }),
    )
    city_ref = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_city_ref'}),
    )
    settlement_ref = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_settlement_ref'}),
    )
    comment = forms.CharField(
        label='Коментар',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'checkout-field__input checkout-field__textarea',
            'rows': 3,
        }),
    )

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('delivery_method')
        city = (cleaned.get('delivery_city') or '').strip()
        address = (cleaned.get('delivery_address') or '').strip()
        house = (cleaned.get('house_number') or '').strip()
        city_ref = (cleaned.get('city_ref') or '').strip()
        settlement_ref = (cleaned.get('settlement_ref') or '').strip()

        if is_configured():
            if not city_ref or not settlement_ref:
                self.add_error('delivery_city', 'Оберіть місто зі списку підказок.')
            if method == Order.DELIVERY_NOVA and not address:
                self.add_error('delivery_address', 'Оберіть відділення зі списку.')
            if method == Order.DELIVERY_NOVA_ADDRESS:
                if not address:
                    self.add_error('delivery_address', 'Оберіть вулицю зі списку.')
                if not house:
                    self.add_error('house_number', 'Вкажіть номер будинку.')

        if method == Order.DELIVERY_NOVA_ADDRESS and address and house:
            cleaned['delivery_address'] = f'{address}, {house}'

        cleaned['delivery_city'] = city
        return cleaned
