from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact

class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Как Вас зовут', required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Ваш емаил для ответа', required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', required=True,  max_length=1000,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))



    class Meta:
        model = Contact
        fields = ['name',  'email', 'message']