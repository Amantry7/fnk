from django import forms

from .models import ConsultRequest


class ConsultRequestForm(forms.ModelForm):
    # Honeypot — скрытое поле для отсева ботов
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ConsultRequest
        fields = ['name', 'phone', 'email', 'company', 'plan', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'autocomplete': 'name',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+996 (___) __-__-__',
                'autocomplete': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'E-mail (необязательно)',
                'autocomplete': 'email',
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Компания (необязательно)',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Кратко опишите вашу задачу',
                'rows': 4,
            }),
        }

    def clean_website(self):
        # Если бот заполнил honeypot — отклоняем
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Спам обнаружен.')
        return ''
