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
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-slate-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'Ismingizni kiriting'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-slate-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'Yoshingiz',
                'min': 8,
                'max': 100
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-slate-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
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
        if age and (age < 8 or age > 100):
            raise forms.ValidationError('Yosh 8 dan 100 gacha bo\'lishi kerak.')
        return age

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 9:
            raise forms.ValidationError('To\'g\'ri telefon raqamini kiriting.')
        return phone
