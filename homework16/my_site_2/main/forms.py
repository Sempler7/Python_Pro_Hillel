from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Ім’я',
            'email': 'Електронна пошта',
            'message': 'Повідомлення',
        }
