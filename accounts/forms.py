from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField()

    class Meta:
        model = Account
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'is_admin', 'is_staff', 'is_active', 'is_superadmin')
