from django import forms
from main.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ( 'address', 'postal_code','city', 'country','payment_method')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].label = 'Please write your address: '
        self.fields['postal_code'].label = 'Postal code:'
        self.fields['city'].label = 'City:'
        self.fields['country'].label = 'Please choose your country:'
        self.fields['payment_method'].label = 'Please choose payment method:'
