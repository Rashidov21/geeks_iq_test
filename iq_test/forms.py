"""
Forms for Geeks Andijan IQ Test.
"""

from django import forms
from .models import UserResult


class StudentInfoForm(forms.ModelForm):
    """Form for collecting student info before test."""

    class Meta:
        model = UserResult
        fields = ['name', 'age', 'gender', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border-2 border-white/20 text-white placeholder-gray-500 focus:border-geeks-green focus:ring-1 focus:ring-geeks-green outline-none transition',
                'placeholder': 'Ismingizni kiriting'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border-2 border-white/20 text-white placeholder-gray-500 focus:border-geeks-green focus:ring-1 focus:ring-geeks-green outline-none transition',
                'placeholder': 'Yoshingiz',
                'min': 8,
                'max': 100
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border-2 border-white/20 text-white placeholder-gray-500 focus:border-geeks-green focus:ring-1 focus:ring-geeks-green outline-none transition',
                'placeholder': '+998 90 123 45 67'
            }),
        }
        labels = {
            'name': 'Ism',
            'age': 'Yosh',
            'gender': 'Jinsi',
            'phone': 'Telefon raqam',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.RadioSelect(attrs={'class': 'flex gap-4'})

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Ism kamida 2 ta belgidan iborat bo\'lishi kerak.')
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            raise forms.ValidationError('Yoshni kiriting.')
        if age < 8 or age > 100:
            raise forms.ValidationError('Yosh 8 dan 100 gacha bo\'lishi kerak.')
        return age

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 9:
            raise forms.ValidationError('To\'g\'ri telefon raqamini kiriting.')
        if digits.startswith('998') and len(digits) >= 12:
            return '+' + digits[:12]
        if len(digits) == 9:
            return '+998' + digits
        return '+998' + digits[-9:] if len(digits) > 9 else phone
