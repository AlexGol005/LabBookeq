import datetime
from datetime import date
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

input_formats = (
    '%Y-%m-%d',
    '%m/%d/%Y',
    '%m/%d/%y',
    '%d.%m.%Y',
)

now = date.today()

class SearchDateForm(forms.Form):
    """форма для поиска записей по датам"""
    datestart = forms.DateField(label='От', initial=datetime.date.today,
                                widget=forms.DateInput(
                                    attrs={'class': 'form-control', 'placeholder': ''}))
    datefinish = forms.DateField(label='До', initial=datetime.date.today,
                                 widget=forms.DateInput(attrs={'placeholder': datetime.date.today}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row(Column('datestart', css_class='form-group col-md-9 mb-1 ml-4')),
                Row(Column('datefinish', css_class='form-group col-md-9 mb-1 ml-4')),
                Row(Submit('submit', 'Найти', css_class='btn  btn-primary col-md-9 mb-3 mt-4 ml-4')))

class YearForm(forms.Form):
    """форма для поиска записей по году"""
    date = forms.DateField(label='Год в формате ГГГГ', initial=now.year,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': '2022'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'сформировать', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))


class CreateYearForm(forms.Form):
    """форма для поиска записей по году"""
    date = forms.DateField(label='Год в формате ГГГГ', initial=now.year,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': '2022'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'сформировать', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))


class LookYearForm(forms.Form):
    """форма для поиска записей по году"""
    date = forms.DateField(label='Год в формате ГГГГ', initial=now.year,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': '2022'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'посмотреть', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))


class AddYearForm(forms.Form):
    """форма для поиска и добавления по году"""
    date = forms.DateField(label='Год в формате ГГГГ', initial=now.year,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': '2022'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'добавить', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))

class DelYearForm(forms.Form):
    """форма для поиска и удаления по году"""
    date = forms.DateField(label='Год в формате ГГГГ', initial=now.year,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': '2022'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'удалить', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))

class GetYearForm(forms.Form):
    """форма для поиска записей по году"""
    date = forms.DateField(label='Год в формате ГГГГ', initial=now.year,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': '2022'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'выгрузить', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))

class SimpleSearchForm(forms.Form):
    """форма для поиска"""
    qwery = forms.CharField(label='Поисковый запрос', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('qwery', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'найти', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))


class DubleSearchForm(forms.Form):
    """форма для поиска"""
    qwery = forms.CharField(label='Внутренний номер', 
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    qwery1 = forms.CharField(label='Год',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('qwery', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Column('qwery1', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'найти', css_class='btn  btn-primary col-md-6 mb-3 mt-4 ml-2 mr-2')))
