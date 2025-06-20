from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User
import re

class PhoneMixin:
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return phone
            
        # Удаляем все нецифровые символы кроме +
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Приводим российские номера к формату +79164980603
        if cleaned.startswith('8') and len(cleaned) == 11:
            return '+7' + cleaned[1:]
        elif cleaned.startswith('7') and len(cleaned) == 11:
            return '+' + cleaned
        elif len(cleaned) == 10 and cleaned.startswith('9'):
            return '+7' + cleaned
            
        return cleaned  # Для международных номеров оставляем как есть

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegistrationForm(PhoneMixin, UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (___) ___-__-__',
            'data-mask': '+7 (000) 000-00-00'
        }),
        help_text="Введите номер в любом формате"
    )
    agree_to_policy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Я согласен с политикой конфиденциальности'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2', 'agree_to_policy')

class ProfileForm(PhoneMixin, UserChangeForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (___) ___-__-__',
            'data-mask': '+7 (000) 000-00-00'
        })
    )

    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email', 'phone')