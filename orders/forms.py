from django import forms
from .models import Order
from accounts.models import UserAddress


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_note']


class NewUserAddress(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['full_name', 'phone_number', 'email', 'address_line_1', 'address_line_2', 'pincode', 'city', 'state', 'country']