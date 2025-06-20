from django import forms
from .models import Order
from users.forms import PhoneMixin
from .validators import validate_phone

class OrderCreateForm(forms.ModelForm):
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        required=True,
        validators=[validate_phone],  # Добавляем наш валидатор
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (___) ___-__-__',
            'data-mask': '+7 (000) 000-00-00'
        }),
        help_text="На этот номер мы позвоним для подтверждения заказа"
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request and self.request.user.is_authenticated:
            user = self.request.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            
            if hasattr(user, 'phone') and user.phone:
                self.fields['phone'].initial = user.phone
            elif hasattr(user, 'profile') and hasattr(user.profile, 'phone'):
                self.fields['phone'].initial = user.profile.phone

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            order.user = self.request.user
        if commit:
            order.save()
        return order