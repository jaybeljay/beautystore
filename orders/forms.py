from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from django.forms import ModelForm, TextInput, Textarea

from .models import Order


class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user_first_name', 'user_last_name', 'user_phone', 'user_address', 'comments']

        widgets = {
            'user_first_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'user_last_name': TextInput(attrs={'class': 'form-control'}),
            'user_phone': PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control', 'required': True}),
            'user_address': TextInput(attrs={'class': 'form-control', 'required': True}),
            'comments': Textarea(attrs={'class': 'form-control'}),
        }
