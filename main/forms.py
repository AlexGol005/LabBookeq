from django import forms

from .models import AttestationJ

MODEL = AttestationJ


class AttestationJForm(forms.ModelForm):
    """форма для внесения нового журнала"""
    name = forms.CharField(initial='Журнал...', label='Наименование журнала', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Журнал аттестации...'}))
    ndocument = forms.CharField(label='Методы испытаний', max_length=100,
                                widget=forms.Textarea(attrs={'class': 'form-control',
                                                             'placeholder': 'ГОСТ...'}))
    for_url = forms.CharField(label='URL адрес журнала (латиницей)', max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'kinematicviscosity'}))
    CM = forms.CharField(label='Испытуемые объекты', max_length=100,
                         widget=forms.Textarea(attrs={'class': 'form-control',
                                                      'placeholder': 'ХСН-ПА-1 (ГСО 9867-2011);'}))
    extra_info = forms.CharField(label='Дополнительная информация к заголовку журнала', max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    formuls = forms.CharField(label='Формулы для расчётов', max_length=100, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': ''}))
    str_html = forms.CharField(label='HTML код для страницы журнала', max_length=10000, required=False,
                               help_text='Заполните табличку на сайте https://iksweb.ru/tools/generator-table-html/ ,'
                               ' скопируйте все из поля "HTML КОД ТАБЛИЦЫ" и вставьте сюда. '
                               'Используйте раздел "Добавить текст".'
                               ' Заголовки в таблице пишите просто текстом, а поля пишите в форме: '
                               ' {{ note.name}} , где '
                               'вместо "name" подставляйте название поля на латинице, '
                               'такое как дата = date, партия - lot и так далее',
                               widget=forms.Textarea(attrs={'class': 'form-control',
                                                            'placeholder': '{{ note.name}}'}))
    img = forms.ImageField(label='Загрузите  картинку для заглавной страницы электронного журнала', required=False,
                           widget=forms.FileInput)

    class Meta:
        model = MODEL
        fields = ['name', 'ndocument', 'for_url', 'CM', 'extra_info',
                  'str_html',
                  'img']
