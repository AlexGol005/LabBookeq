from django import forms
from .models import *


class CommentCreationForm(forms.ModelForm):
    """форма для  комментариев"""
    """стандартная"""
    text = forms.CharField(label='Текст комментария', max_length=10000, required=True,
                           widget=forms.Textarea(attrs={
                               'class': 'form-control'}))
    author = forms.CharField(label='Автор', max_length=10000, required=True,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'}))
    class Meta:
        model = Comments
        fields = ['text', 'author']
