from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class SearchKinematicaForm(forms.Form):
    "форма для поиска по полям ЖАЗ кинематики, партия"
    "при копировании поменять поля на нужные"
    name = forms.CharField(label='Название', initial='РЭВ-100',
                           help_text='введите название в форме: РЭВ-100',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'РЭВ-100'}))
    lot = forms.CharField(label='Партия', initial='10', required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0 ml-2 mr-2'),
                Column('lot', css_class='form-group col-md-1 mb-0 ml-2 mr-2'),
                Submit('submit', 'Найти', css_class='btn  btn-info col-md-2 mb-3 mt-4 ml-2 mr-2'),
                css_class='form-row'
            ))



