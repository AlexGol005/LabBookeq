from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class SearchForm(forms.Form):
    """форма для поиска по записям"""

    name = forms.CharField(label='Поисковый запрос', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-9 mb-0'),
                Submit('submit', 'Найти', css_class='btn  btn-info col-md-2 mb-3 mt-4 ml-4'),
                css_class='form-row'
            ))