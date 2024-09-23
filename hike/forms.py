from django import forms
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


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


class SearchForm(forms.Form):
    """форма для поиска по названию маршрута"""
    title = forms.CharField(label='Поиск по названию', required=False,
                           help_text='слово для поиска',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-4 mb-0'),
                Row(Submit('submit', 'Найти', css_class='btn  btn-warning col-md-9 mb-3 mt-4 ml-4'))))
