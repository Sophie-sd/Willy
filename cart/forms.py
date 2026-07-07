from django import forms

from orders.models import Order


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
        widget=forms.Select(attrs={'class': 'checkout-field__input'}),
    )
    delivery_city = forms.CharField(
        label='Місто',
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'checkout-field__input', 'autocomplete': 'address-level2'}),
    )
    delivery_address = forms.CharField(
        label='Відділення / адреса',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'checkout-field__input', 'autocomplete': 'street-address'}),
    )
    comment = forms.CharField(
        label='Коментар',
        required=False,
        widget=forms.Textarea(attrs={'class': 'checkout-field__input checkout-field__textarea', 'rows': 3}),
    )
